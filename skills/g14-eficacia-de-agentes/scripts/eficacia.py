#!/usr/bin/env python3
"""eficacia.py — ¿qué agentes y skills de un proyecto corrieron, cuándo y con qué efecto observable?

No depende de un formato propio: descubre las piezas en cualquier repo git
(SKILL.md en .claude/skills, .agents, .cursor, .codex, .opencode, catalogo/…;
agentes con frontmatter; workflows de GitHub Actions) y busca, para cada una,
las huellas que dejó:

  * evidencia: archivos versionados en carpetas de salidas/evidencia/reportes
    que nombran a la pieza o a sus scripts, con su historia de commits;
  * ejecuciones automáticas: `gh run list` de los workflows (opcional, --online);
  * deriva: rutas que la skill cita y ya no existen; espejos que divergieron;
  * frescura: si la pieza cambió después de su última evidencia.

Clasifica cada una; no juzga si el resultado fue bueno (eso es de una persona).
Las «señales de hallazgo» son conteos textuales sobre la última evidencia.

Uso:
  python3 eficacia.py --raiz ~/Projects/vaiven [--online] [--salida informe.md] [--json datos.json]
"""
import argparse
import hashlib
import json
import re
import subprocess
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

DIRS_EVIDENCIA = {"salidas", "salida", "evidencia", "evidence", "outputs", "reportes", "reports", "resultados", "runs", "logs-de-corrida"}
SIG_HALLAZGO = re.compile(r"(🔴|✗|❌|\bALTA\b|bloqueante|hallazgo|violaci[oó]n|\bFAIL\b|desv[ií]o|discrepancia)", re.I)
SIG_LIMPIO = re.compile(r"(🟢|✓|✅|sin hallazgos|0 violaciones|\bOK\b|limpi[ao])", re.I)
SIG_CERO = re.compile(r"(0 hallazgos|sin hallazgos|hallazgos?:\s*0|0 violaciones)", re.I)
RUTA_CITADA = re.compile(r"`([A-Za-z0-9_./-]+\.(?:py|sh|mjs|js|ts|md|json|ya?ml|toml|sql)|[A-Za-z0-9_.-]+/[A-Za-z0-9_./-]*/)`")
VENCIDA_DIAS = 0  # la pieza cambió después de su última evidencia


def git(repo, *args):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, timeout=120)
    return r.returncode, r.stdout.decode("utf-8", "replace")


def leer(p, tope=400_000):
    try:
        return p.read_text("utf-8", "replace") if p.stat().st_size <= tope else ""
    except OSError:
        return ""


def frontmatter(texto):
    m = re.match(r"---\n(.*?)\n---", texto, re.S)
    out = {}
    if m:
        for l in m.group(1).splitlines():
            k = re.match(r"^([a-zA-Z_]+):\s*(.*)$", l)
            if k and not l.startswith(" "):
                out[k.group(1)] = k.group(2).strip().strip("'\"")
    return out


def fecha_commit(repo, rel):
    _, o = git(repo, "log", "-1", "--format=%cs", "--", rel)
    return date.fromisoformat(o.strip()) if o.strip() else None


def n_commits(repo, rel):
    _, o = git(repo, "rev-list", "--count", "HEAD", "--", rel)
    return int(o.strip() or 0)


def cron_activo(t):
    return any(re.match(r"\s*(schedule:|-\s*cron:)", l) for l in t.splitlines())


class Proyecto:
    def __init__(self, repos):
        self.repos = [Path(r).resolve() for r in repos]
        self.tracked = {}
        for r in self.repos:
            _, o = git(r, "ls-files", "-z")
            self.tracked[r] = [p for p in o.split("\0") if p]
        self.piezas = {}          # clave -> dict
        self.evidencia = []       # (repo, rel, texto_lower)
        self.automatizaciones = []  # (repo, rel, texto_lower, tiene_cron)

    # descubrimiento ---------------------------------------------------
    def descubrir(self):
        for r in self.repos:
            for rel in self.tracked[r]:
                n = Path(rel).name
                partes = Path(rel).parts
                if n == "SKILL.md":
                    t = leer(r / rel)
                    fm = frontmatter(t)
                    nombre = fm.get("name") or Path(rel).parent.name
                    self._pieza(nombre, "skill", r, rel, t)
                elif ("agentes" in partes[:-1] or ".claude/agents" in rel) and n.endswith(".md") and n.lower() != "readme.md":
                    t = leer(r / rel)
                    fm = frontmatter(t)
                    if fm.get("name") and fm.get("tipo", "agente") == "agente":
                        self._pieza(fm["name"], "agente", r, rel, t)
                elif rel.startswith(".github/workflows/") and rel.endswith((".yml", ".yaml")):
                    t = leer(r / rel)
                    self.automatizaciones.append((r, rel, t.lower(), cron_activo(t)))
                    self._pieza(f"{r.name}:{Path(rel).stem}", "workflow", r, rel, t)
                elif n.startswith(("pre-commit", "pre-push")) and "hook" in rel.lower():
                    self.automatizaciones.append((r, rel, leer(r / rel).lower(), False))
                if set(p.lower() for p in partes[:-1]) & DIRS_EVIDENCIA and rel.endswith((".txt", ".md", ".json", ".log", ".csv")):
                    self.evidencia.append((r, rel, (leer(r / rel) + " " + rel).lower()))

    def _pieza(self, nombre, tipo, repo, rel, texto):
        k = (tipo, nombre)
        p = self.piezas.setdefault(k, {"nombre": nombre, "tipo": tipo, "archivos": [], "hashes": set(), "textos": []})
        p["archivos"].append((repo, rel))
        p["hashes"].add(hashlib.sha1(re.sub(r"\s+", " ", texto).encode()).hexdigest())
        p["textos"].append(texto)

    # análisis ---------------------------------------------------------
    def _claves(self, p, tipo, nombre):
        claves = {nombre.split(":")[-1].lower()} if tipo == "workflow" else {nombre.lower()}
        scripts = set()
        for repo, rel in p["archivos"]:
            carpeta = (repo / rel).parent
            if (carpeta / "scripts").is_dir():
                scripts |= {f.name.lower() for f in (carpeta / "scripts").iterdir() if f.is_file()}
        for t in p["textos"]:
            scripts |= {m.lower().split("/")[-1] for m in RUTA_CITADA.findall(t) if re.search(r"\.(py|sh|mjs)$", m)}
        claves |= {x for x in scripts if len(x) >= 8}
        return {c for c in claves if len(c) >= 6}

    def _compartidas(self):
        """Evidencias que nombran a muchas piezas por contenido (resúmenes globales): no son de ninguna en particular."""
        cuenta = defaultdict(int)
        for (tipo, nombre), p in self.piezas.items():
            claves = self._claves(p, tipo, nombre)
            for repo, rel, txt in self.evidencia:
                if any(c in txt for c in claves):
                    cuenta[rel] += 1
        return {rel for rel, n in cuenta.items() if n > 4}

    def fichas(self):
        out = []
        compartidas = self._compartidas()
        for (tipo, nombre), p in sorted(self.piezas.items()):
            claves = self._claves(p, tipo, nombre)
            mias = {rel for _, rel in p["archivos"]}

            # evidencia
            ev = []
            for repo, rel, txt in self.evidencia:
                if rel in mias:
                    continue
                en_ruta = any(c in rel.lower() for c in claves)
                if (en_ruta or rel not in compartidas) and any(c in txt for c in claves):
                    ev.append((repo, rel))
            fechas = [(fecha_commit(r, rel), r, rel) for r, rel in ev]
            fechas = [f for f in fechas if f[0]]
            ultima = max(fechas, key=lambda x: x[0]) if fechas else None
            corridas = sum(n_commits(r, rel) for r, rel in ev)
            hallazgos = limpio = 0
            if ultima:
                lineas = leer(ultima[1] / ultima[2]).splitlines()
                hallazgos = sum(1 for l in lineas if SIG_HALLAZGO.search(l) and not SIG_CERO.search(l))
                limpio = sum(1 for l in lineas if SIG_LIMPIO.search(l))

            # disparo
            disparo = "humano"
            automat = []
            for repo, rel, txt, cron in self.automatizaciones:
                if rel in mias:
                    continue
                if any(c in txt for c in claves):
                    automat.append((repo, rel, cron))
            if tipo == "workflow":
                disparo = "cron" if self._cron(p) else "evento"
            elif any("pre-commit" in rel or "pre-push" in rel for _, rel, _ in automat):
                disparo = "hook"
            elif any(c for _, _, c in automat):
                disparo = "cron"
            elif automat:
                disparo = "evento"

            # cambios de la pieza
            cambios = [fecha_commit(r, rel) for r, rel in p["archivos"]]
            cambios = [c for c in cambios if c]
            ult_cambio = max(cambios) if cambios else None

            # deriva
            rotas = set()
            if tipo != "workflow":
                for (repo, rel), t in zip(p["archivos"], p["textos"]):
                    base = (repo / rel).parent
                    for cita in RUTA_CITADA.findall(t):
                        if any(x in cita for x in ("<", "*", "~", "http")) or cita.startswith("/"):
                            continue
                        c = cita.rstrip("/")
                        if not any((b / c).exists() for b in (base, repo, repo.parent)):
                            rotas.add(cita)
            out.append({"nombre": nombre, "tipo": tipo, "repos": sorted({r.name for r, _ in p["archivos"]}),
                        "archivos": [f"{r.name}/{rel}" for r, rel in p["archivos"]],
                        "espejos": len(p["archivos"]), "divergen": len(p["hashes"]) > 1,
                        "disparo": disparo, "evidencias": len(ev), "commits_de_evidencia": corridas,
                        "ultima_evidencia": ultima[0].isoformat() if ultima else None,
                        "archivo_ultima_evidencia": f"{ultima[1].name}/{ultima[2]}" if ultima else None,
                        "ultimo_cambio": ult_cambio.isoformat() if ult_cambio else None,
                        "senal_hallazgos": hallazgos, "senal_limpio": limpio,
                        "rutas_rotas": sorted(rotas)[:8], "n_rutas_rotas": len(rotas),
                        "_repo_objs": sorted({r for r, _ in p["archivos"]}, key=str), "_rel": [rel for _, rel in p["archivos"]]})
        return out

    @staticmethod
    def _cron(p):
        return any(cron_activo(t) for t in p["textos"])


def runs_gh(ficha):
    """Estadísticas de ejecución de un workflow vía `gh run list` (sólo lectura)."""
    repo = ficha["_repo_objs"][0]
    _, rem = git(repo, "remote", "get-url", "origin")
    m = re.search(r"github\.com[:/]([^/]+)/([^/.\s]+)", rem)
    if not m:
        return None
    r = subprocess.run(["gh", "run", "list", "-R", f"{m.group(1)}/{m.group(2)}", "--workflow", Path(ficha["_rel"][0]).name,
                        "--limit", "50", "--json", "conclusion,createdAt,status,event"], capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        return None
    try:
        runs = json.loads(r.stdout)
    except ValueError:
        return None
    hechos = [x for x in runs if x["conclusion"] in ("success", "failure", "timed_out", "startup_failure")]  # los "skipped"/"cancelled" no cuentan
    return {"n": len(runs), "ok": sum(x["conclusion"] == "success" for x in hechos), "hechos": len(hechos),
            "ultima": runs[0]["createdAt"][:10] if runs else None,
            "ultima_conclusion": hechos[0]["conclusion"] if hechos else None,
            "eventos": sorted({x["event"] for x in runs})}


def clasificar(f, hoy):
    if f["tipo"] == "workflow":
        g = f.get("gh")
        if g is None:
            return "sin-datos-de-ejecucion"
        if g["n"] == 0:
            return "nunca-corrio"
        if g["ultima_conclusion"] not in ("success", None):
            return "fallando"
        return "corriendo"
    if f["evidencias"] == 0 and not f.get("gh_auto"):
        return "sin-corridas"
    if f["ultima_evidencia"] and f["ultimo_cambio"] and f["ultimo_cambio"] > f["ultima_evidencia"]:
        return "evidencia-vencida"
    if f["senal_hallazgos"] > 0:
        return "corrio-con-hallazgos"
    return "corrio-sin-hallazgos"


def informe(fichas, fecha):
    cuenta = defaultdict(int)
    for f in fichas:
        cuenta[f["estado"]] += 1
    L = [f"# Eficacia de agentes y skills — {fecha}", "",
         f"Piezas descubiertas: **{len(fichas)}** ({sum(f['tipo']=='skill' for f in fichas)} skills, "
         f"{sum(f['tipo']=='agente' for f in fichas)} agentes, {sum(f['tipo']=='workflow' for f in fichas)} workflows).", "",
         "| Estado | Piezas |", "|---|---|"]
    L += [f"| {k} | {v} |" for k, v in sorted(cuenta.items(), key=lambda x: -x[1])]
    L += ["", "Las *señales de hallazgo* son conteos de líneas en la última evidencia (🔴, ✗, ALTA, bloqueante, hallazgo…); "
          "indican que la corrida encontró algo, no que lo encontrado fuera correcto.", ""]
    for tipo, titulo in (("skill", "Skills"), ("agente", "Agentes"), ("workflow", "Workflows (GitHub Actions)")):
        sub = [f for f in fichas if f["tipo"] == tipo]
        if not sub:
            continue
        L += [f"## {titulo}", ""]
        if tipo == "workflow":
            L += ["| Workflow | Disparo | Ejecuciones (ok/total) | Última | Estado |", "|---|---|---|---|---|"]
            for f in sub:
                g = f.get("gh")
                L.append(f"| {f['nombre']} | {f['disparo']} | " + (f"{g['ok']}/{g['hechos']}" if g else "—") +
                         f" | {g['ultima'] if g else '—'} | {f['estado']} |")
        else:
            L += ["| Pieza | Repos | Disparo | Evid. | Commits evid. | Última evid. | Últ. cambio | Señal hall./limpio | Deriva | Estado |",
                  "|---|---|---|---|---|---|---|---|---|---|"]
            for f in sorted(sub, key=lambda x: (x["estado"], x["nombre"])):
                deriva = []
                if f["n_rutas_rotas"]:
                    deriva.append(f"{f['n_rutas_rotas']} ruta(s) rota(s)")
                if f["divergen"]:
                    deriva.append("espejos divergen")
                L.append(f"| {f['nombre']} | {','.join(f['repos'])} | {f['disparo']} | {f['evidencias']} | {f['commits_de_evidencia']} | "
                         f"{f['ultima_evidencia'] or '—'} | {f['ultimo_cambio'] or '—'} | {f['senal_hallazgos']}/{f['senal_limpio']} | "
                         f"{'; '.join(deriva) or '—'} | {f['estado']} |")
        L.append("")
    rotas = [f for f in fichas if f["n_rutas_rotas"]]
    if rotas:
        L += ["## Rutas citadas que no existen", ""]
        for f in rotas:
            L.append(f"- **{f['nombre']}**: " + ", ".join(f"`{r}`" for r in f["rutas_rotas"]))
        L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raiz")
    ap.add_argument("--repos", nargs="*", default=[])
    ap.add_argument("--excluir", nargs="*", default=[], help="nombres de repos a dejar afuera (p. ej. un catálogo ajeno)")
    ap.add_argument("--online", action="store_true", help="consulta `gh run list` (sólo lectura)")
    ap.add_argument("--salida")
    ap.add_argument("--json")
    a = ap.parse_args()
    repos = [Path(r) for r in a.repos]
    if a.raiz:
        repos += sorted(p for p in Path(a.raiz).iterdir() if (p / ".git").exists())
    repos = [r for r in repos if r.name not in a.excluir]
    if not repos:
        ap.error("indicá --raiz o --repos")
    pr = Proyecto(repos)
    pr.descubrir()
    fichas = pr.fichas()
    for f in fichas:
        if a.online and f["tipo"] == "workflow":
            f["gh"] = runs_gh(f)
    for f in fichas:
        f["estado"] = clasificar(f, date.today())
    texto = informe(fichas, datetime.now().strftime("%Y-%m-%d"))
    print(texto)
    if a.salida:
        Path(a.salida).write_text(texto, "utf-8")
    if a.json:
        limpio = [{k: v for k, v in f.items() if not k.startswith("_")} for f in fichas]
        Path(a.json).write_text(json.dumps(limpio, indent=2, ensure_ascii=False, default=str), "utf-8")


if __name__ == "__main__":
    main()
