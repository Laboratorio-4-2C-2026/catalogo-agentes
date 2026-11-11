#!/usr/bin/env python3
"""auditar_higiene.py — higiene de repositorios previa a una entrega.

Recorre uno o varios repos git y reporta, sin imprimir nunca un valor secreto
(sólo tipo, ubicación y una huella sha256 corta):

  1. Archivos sensibles por nombre (.env*, claves, cuentas de servicio) y su
     estado: versionado / ignorado / sin versionar y sin ignorar.
  2. Secretos dentro de los archivos versionados.
  3. Secretos en el historial (líneas agregadas en cualquier rama).
  4. Cobertura mínima del .gitignore, remotes con credenciales embebidas,
     artefactos de build versionados, archivos pesados, emails en datos de
     prueba, README/LICENSE.

Uso:
  python3 auditar_higiene.py --raiz ~/Projects/vaiven            # busca repos en el primer nivel
  python3 auditar_higiene.py --repos a b c --json salida.json    # repos explícitos + salida para otras skills
  python3 auditar_higiene.py --raiz . --check                    # exit 1 si hay hallazgos ALTA

Sólo lee. No modifica ningún repo ni llama a la red.
"""
import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", "__pycache__", ".venv", "venv", ".turbo"}
EJEMPLOS = (".example", ".sample", ".template", ".dist")
NOMBRE_SENSIBLE = [
    re.compile(r"^\.env(\..+)?$", re.I),
    re.compile(r".*\.(pem|key|p12|pfx|jks|keystore)$", re.I),
    re.compile(r"^id_(rsa|dsa|ecdsa|ed25519)$", re.I),
    re.compile(r".*_SA_JSON$", re.I),
    re.compile(r".*(credentials?|service[-_]?account|secrets?)(\.(json|ya?ml|txt|env))?$", re.I),
]
SALTAR_CONTENIDO = {"package-lock.json", "pnpm-lock.yaml", "yarn.lock", "poetry.lock"}
MAX_BYTES = 1_000_000

# (tipo, regex, severidad). Los "fuertes" también se buscan en el historial.
FUERTES = [
    ("clave-privada", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----"), "ALTA"),
    ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "ALTA"),
    ("github-token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{50,})\b"), "ALTA"),
    ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}"), "ALTA"),
    ("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"), "ALTA"),
    ("atlassian-token", re.compile(r"\bATATT[A-Za-z0-9_=-]{30,}"), "ALTA"),
    ("llm-api-key", re.compile(r"\bsk-(?:or-v1-|ant-)?[A-Za-z0-9_-]{32,}"), "ALTA"),
    ("supabase-secret", re.compile(r"\bsb_secret_[A-Za-z0-9_-]{20,}"), "ALTA"),
]
JWT = re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.(eyJ[A-Za-z0-9_-]{10,})\.[A-Za-z0-9_-]{10,}")
ASIGNACION = re.compile(
    r"""(?i)\b(password|passwd|secret|token|api[_-]?key)\b["']?\s*[:=]\s*["']?([A-Za-z0-9/+_.\-]{16,})["']?""")
PLACEHOLDER = re.compile(r"(?i)(<|>|xxx|your|example|changeme|placeholder|dummy|process\.env|import\.meta|\$\{|\$\(|secrets\.|\.\.\.)")
REMOTE_CRED = re.compile(r"https?://[^/\s:@]+:[^/\s@]+@")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})")
EMAIL_OK = re.compile(r"(?i)(example\.|test|localhost|noreply|no-reply|users\.noreply\.github)")


def git(repo, *args, timeout=60):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, timeout=timeout)
    return r.returncode, r.stdout.decode("utf-8", "replace")


def huella(valor):
    return f"len={len(valor)} sha256:{hashlib.sha256(valor.encode()).hexdigest()[:8]}"


def jwt_info(payload_b64):
    """(rol, vencido) del payload de un JWT; vencido es None si no trae exp."""
    try:
        pad = "=" * (-len(payload_b64) % 4)
        d = json.loads(base64.urlsafe_b64decode(payload_b64 + pad))
        exp = d.get("exp")
        return d.get("role"), (None if exp is None else exp < datetime.now().timestamp())
    except Exception:
        return None, None


def descubrir_repos(raiz):
    return sorted(p for p in Path(raiz).iterdir() if (p / ".git").exists())


class Repo:
    def __init__(self, ruta):
        self.ruta = Path(ruta).resolve()
        self.nombre = self.ruta.name
        self.hallazgos = []
        self.rastreados = set()

    def add(self, sev, tipo, archivo, detalle, accion, linea=None, huella_=None):
        hid = hashlib.sha1(f"{self.nombre}|{tipo}|{archivo}|{linea}|{huella_}".encode()).hexdigest()[:10]
        self.hallazgos.append({"id": hid, "repo": self.nombre, "severidad": sev, "tipo": tipo,
                               "archivo": archivo, "linea": linea, "detalle": detalle,
                               "huella": huella_, "accion": accion})

    # 1 ---------------------------------------------------------------
    def archivos_sensibles(self):
        for dirpath, dirnames, filenames in os.walk(self.ruta):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for f in filenames:
                if f.endswith(EJEMPLOS):
                    continue
                if not any(p.match(f) for p in NOMBRE_SENSIBLE):
                    continue
                rel = os.path.relpath(os.path.join(dirpath, f), self.ruta)
                if rel in self.rastreados:
                    self.add("ALTA", "sensible-versionado", rel,
                             "Archivo sensible por nombre está versionado.",
                             "git rm --cached, agregarlo al .gitignore y rotar lo que contenga.")
                    continue
                ign, _ = git(self.ruta, "check-ignore", "-q", rel)
                if ign == 0:
                    self.add("OK", "sensible-ignorado", rel, "Sensible por nombre, ignorado por git.", "Ninguna.")
                else:
                    self.add("ALTA", "sensible-sin-ignorar", rel,
                             "Sensible por nombre, sin versionar y sin ignorar: un `git add .` lo sube.",
                             "Agregar el patrón al .gitignore (o moverlo fuera del repo).")

    # 2 ---------------------------------------------------------------
    def secretos_versionados(self):
        for rel in sorted(self.rastreados):
            if Path(rel).name in SALTAR_CONTENIDO:
                continue
            p = self.ruta / rel
            try:
                if p.stat().st_size > MAX_BYTES or not p.is_file():
                    continue
                data = p.read_bytes()
            except OSError:
                continue
            if b"\0" in data[:8192]:
                continue
            for n, linea in enumerate(data.decode("utf-8", "replace").splitlines(), 1):
                if len(linea) > 2000:
                    continue
                self._linea(rel, n, linea)

    def _linea(self, rel, n, linea):
        for tipo, rx, sev in FUERTES:
            m = rx.search(linea)
            if m:
                self.add(sev, f"secreto:{tipo}", rel, f"Posible {tipo} versionado.",
                         "Rotar en el proveedor, sacarlo del repo y del historial.", n, huella(m.group(0)))
        m = JWT.search(linea)
        if m:
            rol, vencido = jwt_info(m.group(1))
            if rol == "service_role":
                self.add("ALTA", "secreto:jwt-service-role", rel, "JWT con rol service_role versionado.",
                         "Rotar la clave del proyecto y sacarla del repo.", n, huella(m.group(0)))
            else:
                self.add("BAJA", "jwt-otro", rel, f"JWT versionado con rol `{rol}`"
                         + {True: ", ya vencido", False: ", NO vencido", None: ", sin exp"}[vencido]
                         + " (la anon key es pública por diseño; confirmalo).",
                         "Confirmar que no da acceso privilegiado." if vencido is not True else "Sin urgencia: ya venció.", n, huella(m.group(0)))
            return
        m = ASIGNACION.search(linea)
        if (m and not PLACEHOLDER.search(linea) and re.search(r"\d", m.group(2))
                and not linea[m.end():m.end() + 1] == "(" and not m.group(2).startswith(("env.", "process."))):
            self.add("MEDIA", "asignacion-sospechosa", rel,
                     f"Asignación a `{m.group(1)}` con valor literal.", "Revisar a mano: ¿es un secreto real?",
                     n, huella(m.group(2)))

    # 3 ---------------------------------------------------------------
    def historial(self):
        fuertes = "|".join(rx.pattern for _, rx, _ in FUERTES)
        rc, out = git(self.ruta, "log", "--all", "-G", fuertes, "--format=@@%h %as", "-p", "--unified=0",
                      "--no-color", timeout=180)
        if rc != 0:
            return
        commit, archivo, vistos = "?", "?", set()
        for linea in out.splitlines():
            if linea.startswith("@@"):
                commit = linea[2:]
            elif linea.startswith("+++ b/"):
                archivo = linea[6:]
            elif linea.startswith("+") and not linea.startswith("+++"):
                for tipo, rx, sev in FUERTES:
                    m = rx.search(linea)
                    if m and not PLACEHOLDER.search(m.group(0)):
                        h = huella(m.group(0))
                        if (h, archivo) in vistos:
                            continue
                        vistos.add((h, archivo))
                        vigente = archivo in self.rastreados
                        self.add("ALTA", f"historial:{tipo}", archivo,
                                 f"{tipo} agregado en commit {commit}" + ("" if vigente else " (ya no está en HEAD, pero sigue en el historial)"),
                                 "Rotar en el proveedor; reescribir historial sólo si el repo lo justifica.",
                                 None, h)

    # 4 ---------------------------------------------------------------
    def estructurales(self):
        muestras = [".env", ".env.local"]
        if (self.ruta / "package.json").exists():
            muestras.append("node_modules/x")
        for m in muestras:
            rc, _ = git(self.ruta, "check-ignore", "-q", "--no-index", m)
            if rc != 0:
                self.add("MEDIA", "gitignore-incompleto", ".gitignore", f"`{m}` no queda cubierto por el .gitignore.",
                         f"Agregar un patrón que cubra `{m}`.")
        _, remotes = git(self.ruta, "remote", "-v")
        if REMOTE_CRED.search(remotes):
            self.add("ALTA", "remote-con-credenciales", ".git/config", "Un remote tiene usuario:token embebido en la URL.",
                     "git remote set-url sin credenciales y rotar el token.")
        for rel in self.rastreados:
            partes = Path(rel).parts
            if "node_modules" in partes[:-1] or partes[0] in ("dist", "build"):
                self.add("MEDIA", "artefacto-versionado", rel, "Artefacto de build o dependencias versionado.",
                         "git rm -r --cached y agregar al .gitignore.")
                break
        for rel in self.rastreados:
            try:
                if (self.ruta / rel).stat().st_size > 5_000_000:
                    self.add("BAJA", "archivo-pesado", rel, ">5 MB versionado.", "Evaluar si corresponde (LFS o fuera del repo).")
            except OSError:
                pass
        for rel in sorted(self.rastreados):
            if re.search(r"(?i)(seed|datos|fixtures?|golden)", rel) and rel.endswith((".sql", ".json", ".csv", ".md")):
                try:
                    txt = (self.ruta / rel).read_text("utf-8", "replace")[:MAX_BYTES]
                except OSError:
                    continue
                reales = {m.group(0).lower() for m in EMAIL.finditer(txt) if not EMAIL_OK.search(m.group(1))}
                if reales:
                    self.add("BAJA", "emails-en-datos-de-prueba", rel,
                             f"{len(reales)} email(s) con dominio no reservado en datos de prueba.",
                             "Confirmar que son ficticios, no de personas reales.", huella_=f"n={len(reales)}")
        nombres = {Path(r).name.lower() for r in self.rastreados if "/" not in r}
        if not any(n.startswith("readme") for n in nombres):
            self.add("BAJA", "sin-readme", "README", "El repo no tiene README en la raíz.", "Agregarlo antes de entregar.")
        if not any(n.startswith("license") or n.startswith("licence") for n in nombres):
            self.add("BAJA", "sin-licencia", "LICENSE", "El repo no declara licencia.", "Decidir licencia o dejarlo explícito en el README.")

    def correr(self, con_historial):
        rc, out = git(self.ruta, "ls-files", "-z")
        self.rastreados = {p for p in out.split("\0") if p}
        self.archivos_sensibles()
        self.secretos_versionados()
        if con_historial:
            self.historial()
        self.estructurales()
        return self


def informe(repos, fecha):
    L = ["=" * 78, "AUDITORÍA DE HIGIENE PRE-ENTREGA".center(78), "=" * 78,
         f"Fecha: {fecha}", "Nota: ningún valor secreto se imprime; sólo tipo, ubicación y huella.", ""]
    L.append(f"{'Repo':<22}{'ALTA':>6}{'MEDIA':>7}{'BAJA':>6}{'OK':>5}")
    L.append("-" * 46)
    for r in repos:
        c = {s: sum(h["severidad"] == s for h in r.hallazgos) for s in ("ALTA", "MEDIA", "BAJA", "OK")}
        L.append(f"{r.nombre:<22}{c['ALTA']:>6}{c['MEDIA']:>7}{c['BAJA']:>6}{c['OK']:>5}")
    for r in repos:
        L += ["", f"## {r.nombre}  ({r.ruta})"]
        pendientes = [h for h in r.hallazgos if h["severidad"] != "OK"]
        if not pendientes:
            L.append("  Sin hallazgos.")
        for h in sorted(pendientes, key=lambda h: ("ALTA", "MEDIA", "BAJA").index(h["severidad"])):
            ub = h["archivo"] + (f":{h['linea']}" if h["linea"] else "")
            L.append(f"  [{h['severidad']}] {h['tipo']} — {ub}")
            L.append(f"        {h['detalle']}" + (f"  [{h['huella']}]" if h["huella"] else ""))
            L.append(f"        → {h['accion']}")
        ok = [h for h in r.hallazgos if h["severidad"] == "OK"]
        if ok:
            L.append(f"  Controlado: {len(ok)} archivo(s) sensible(s) por nombre y correctamente ignorados: "
                     + ", ".join(h["archivo"] for h in ok[:6]) + ("…" if len(ok) > 6 else ""))
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raiz", help="carpeta cuyos subdirectorios git se auditan")
    ap.add_argument("--repos", nargs="*", default=[], help="repos explícitos")
    ap.add_argument("--json", help="escribe los hallazgos en este JSON (insumo para g14-cierre-y-congelamiento)")
    ap.add_argument("--salida", help="escribe el informe de texto en este archivo")
    ap.add_argument("--sin-historial", action="store_true", help="omite la búsqueda en el historial (más rápido)")
    ap.add_argument("--check", action="store_true", help="exit 1 si hay hallazgos ALTA")
    a = ap.parse_args()
    rutas = [Path(r) for r in a.repos] + (descubrir_repos(a.raiz) if a.raiz else [])
    if not rutas:
        ap.error("indicá --raiz o --repos")
    repos = [Repo(r).correr(not a.sin_historial) for r in rutas]
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    txt = informe(repos, fecha)
    print(txt, end="")
    if a.salida:
        Path(a.salida).write_text(txt, "utf-8")
    if a.json:
        Path(a.json).write_text(json.dumps({"generado": fecha, "repos": [
            {"nombre": r.nombre, "ruta": str(r.ruta), "hallazgos": r.hallazgos} for r in repos]},
            indent=2, ensure_ascii=False), "utf-8")
    if a.check and any(h["severidad"] == "ALTA" for r in repos for h in r.hallazgos):
        sys.exit(1)


if __name__ == "__main__":
    main()
