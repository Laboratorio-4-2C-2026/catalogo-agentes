#!/usr/bin/env python3
"""extraer_hechos.py — hechos observables de una feature ya mergeada.

Lee el diff de un merge (o un rango) en el repo del producto y lista, sin
interpretar, lo que cambió y le importa a quien opera, desarrolla o decide:
migraciones SQL, workflows de n8n, variables de entorno y secretos (sólo
nombres), dependencias, infraestructura y carpetas de código tocadas.

Cada hecho lleva un id (H1, H2…), su origen (archivo) y las audiencias a las
que le sirve (devops / devs / direccion) según la matriz de la skill.

Uso:
  python3 extraer_hechos.py --repo ~/Projects/vaiven/vaiven-app --merge fdd1cb0 --ticket SCRUM-135 --salida hechos.json
  python3 extraer_hechos.py --repo <repo> --rango origin/main~3..origin/main --ticket SCRUM-99 --salida hechos.json

Sólo lee git. No imprime valores de secretos: de un secreto se guarda el nombre.
"""
import argparse
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

INFRA = re.compile(r"(docker-compose|Caddyfile|vercel\.json|\.github/workflows/|supabase/config\.toml|(^|/)scripts/.*\.(sh|py)$|cargar-en-n8n)")
DESTRUCTIVO = re.compile(r"\b(DROP\s+(TABLE|COLUMN|POLICY|TRIGGER|FUNCTION|ROLE|SCHEMA|EXTENSION)|TRUNCATE|DELETE\s+FROM|ALTER\s+TABLE\s+\S+\s+DROP)\b", re.I)
OBJETO_SQL = re.compile(r"\b(CREATE\s+(?:OR\s+REPLACE\s+)?(?:TABLE|POLICY|ROLE|TRIGGER|FUNCTION|EXTENSION|INDEX|VIEW|TYPE|SCHEMA)(?:\s+IF\s+NOT\s+EXISTS)?\s+(?:\"[^\"]+\"|[\w.]+)|GRANT\s+[\w, ]+\s+ON\s+[\w.]+\s+TO\s+\w+|ALTER\s+TABLE\s+[\w.]+\s+\w+(?:\s+\w+)?)", re.I)
VAULT = re.compile(r"vault\.(?:decrypted_secrets|secrets)[^;]*?name\s*=\s*'([^']+)'", re.I | re.S)
ENV_CODIGO = re.compile(r"(?:import\.meta\.env|process\.env)\.([A-Z][A-Z0-9_]+)|\$env\.([A-Z][A-Z0-9_]+)|\$vars\.([A-Za-z_][A-Za-z0-9_]*)|secrets\.([A-Za-z0-9_]+)|Deno\.env\.get\(['\"]([A-Z0-9_]+)['\"]\)")
ENV_ARCHIVO = re.compile(r"^\+\s*(?:export\s+)?([A-Z][A-Z0-9_]{2,})\s*=")
ADR = re.compile(r"\bADR[- ]?(\d{4})\b")
HOST = re.compile(r"https?://([A-Za-z0-9.\-{}$ ]+?)(?:[/:\"'\s]|$)")


def git(repo, *args):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, timeout=120)
    return r.stdout.decode("utf-8", "replace")


def mostrar(repo, rev, ruta):
    return git(repo, "show", f"{rev}:{ruta}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--merge", help="commit de merge de un PR (usa <merge>^1..<merge>)")
    g.add_argument("--rango", help="rango git A..B")
    ap.add_argument("--ticket", required=True)
    ap.add_argument("--salida", required=True)
    a = ap.parse_args()
    repo = Path(a.repo)

    if a.merge:
        base, destino = f"{a.merge}^1", a.merge
    else:
        base, destino = a.rango.split("..", 1)
    destino_sha = git(repo, "rev-parse", destino).strip()
    base_sha = git(repo, "rev-parse", base).strip()

    cambios = []
    for l in git(repo, "diff", "--name-status", "-M", base_sha, destino_sha).splitlines():
        partes = l.split("\t")
        cambios.append((partes[0][0], partes[-1]))
    commits = [{"sha": l.split(" ", 1)[0], "asunto": l.split(" ", 1)[1] if " " in l else ""}
               for l in git(repo, "log", "--no-merges", "--format=%h %s", f"{base_sha}..{destino_sha}").splitlines()]
    diff_total = git(repo, "diff", "-U0", base_sha, destino_sha)

    hechos = []
    def add(tipo, titulo, origen, audiencias, detalle, irreversible=False):
        hechos.append({"id": f"H{len(hechos) + 1}", "tipo": tipo, "titulo": titulo, "origen": origen,
                       "audiencias": audiencias, "irreversible": irreversible, "detalle": detalle})

    # migraciones
    for est, ruta in cambios:
        if ruta.startswith("supabase/migrations/") and ruta.endswith(".sql") and est in "AM":
            sql = mostrar(repo, destino_sha, ruta)
            sin_comentarios = "\n".join(re.sub(r"--.*$", "", l) for l in sql.splitlines())
            objetos = [re.sub(r"\s+", " ", o).strip() for o in OBJETO_SQL.findall(sin_comentarios)]
            destructivo = sorted({re.sub(r"\s+", " ", m.group(0)).upper() for m in DESTRUCTIVO.finditer(sin_comentarios)})
            vault = sorted(set(VAULT.findall(sin_comentarios)))
            aud = ["devops", "devs"] + (["direccion"] if destructivo or vault or re.search(r"CREATE\s+ROLE", sin_comentarios, re.I) else [])
            add("migracion", f"Migración {Path(ruta).name}", ruta, aud,
                {"estado": {"A": "nueva", "M": "modificada"}[est], "objetos": objetos[:12], "destructivo": destructivo, "secretos_vault": vault},
                irreversible=bool(destructivo))
            for nombre in vault:
                add("secreto", f"Secreto de Vault `{nombre}`", ruta, ["devops", "devs", "direccion"],
                    {"nombre": nombre, "donde": "Supabase Vault", "valor": "no se registra"})

    # workflows de n8n
    for est, ruta in cambios:
        if ruta.startswith("n8n/") and ruta.endswith(".json") and est in "AM":
            texto = mostrar(repo, destino_sha, ruta)
            try:
                wf = json.loads(texto)
            except ValueError:
                continue
            nodos = wf.get("nodes", [])
            webhooks = [{"path": n.get("parameters", {}).get("path"), "metodo": n.get("parameters", {}).get("httpMethod", "GET"),
                         "autenticacion": n.get("parameters", {}).get("authentication", "ninguna")}
                        for n in nodos if n.get("type", "").endswith(".webhook")]
            creds = sorted({f"{tipo}: {c.get('name')}" for n in nodos for tipo, c in (n.get("credentials") or {}).items()})
            hosts = sorted({h.strip() for n in nodos for h in HOST.findall(json.dumps(n.get("parameters", {}))) if "." in h and "{" not in h})
            previo = None
            if est == "M":
                try:
                    previo = {n["name"] for n in json.loads(mostrar(repo, base_sha, ruta)).get("nodes", [])}
                except (ValueError, KeyError):
                    previo = None
            nombres = {n.get("name") for n in nodos}
            add("workflow-n8n", f"Workflow n8n `{wf.get('name', Path(ruta).stem)}`", ruta, ["devops", "devs", "direccion"],
                {"estado": {"A": "nuevo", "M": "modificado"}[est], "nodos": len(nodos), "webhooks": webhooks, "credenciales": creds,
                 "hosts_externos": hosts[:6],
                 "nodos_agregados": sorted(nombres - previo)[:10] if previo is not None else None,
                 "nodos_quitados": sorted(previo - nombres)[:10] if previo is not None else None,
                 "inactivo_en_el_archivo": not wf.get("active", False)})
            for c in creds:
                previo_h = next((h for h in hechos if h["tipo"] == "credencial-n8n" and h["detalle"]["nombre"] == c), None)
                if previo_h:  # la misma credencial en varios workflows es un solo hecho
                    previo_h["detalle"].setdefault("tambien_en", []).append(ruta)
                    continue
                add("credencial-n8n", f"Credencial de n8n `{c}`", ruta, ["devops", "direccion"],
                    {"nombre": c, "donde": "n8n (panel de credenciales)", "valor": "no se registra"})

    # variables de entorno / secretos de CI, vistos en líneas agregadas
    nombres_env = {}
    archivo_actual = None
    for l in diff_total.splitlines():
        if l.startswith("+++ b/"):
            archivo_actual = l[6:]
        elif l.startswith("+") and not l.startswith("+++") and archivo_actual:
            if archivo_actual.endswith((".env.example", ".env.sample")):
                m = ENV_ARCHIVO.match(l)
                if m:
                    nombres_env.setdefault(m.group(1), set()).add(archivo_actual)
            elif not archivo_actual.endswith((".sql", ".lock", ".yaml")) and "pnpm-lock" not in archivo_actual:
                for m in ENV_CODIGO.finditer(l):
                    nombre = next(g for g in m.groups() if g)
                    nombres_env.setdefault(nombre, set()).add(archivo_actual)
    for nombre, archivos in sorted(nombres_env.items()):
        if nombre in ("NODE_ENV", "MODE", "DEV", "PROD", "BASE_URL", "GITHUB_TOKEN"):
            continue
        add("variable", f"Variable `{nombre}`", sorted(archivos)[0], ["devops", "devs"],
            {"nombre": nombre, "vista_en": sorted(archivos)[:4], "valor": "no se registra"})

    # dependencias
    if any(r == "package.json" for _, r in cambios):
        def deps(rev):
            try:
                j = json.loads(mostrar(repo, rev, "package.json"))
            except ValueError:
                return {}
            return {**j.get("dependencies", {}), **j.get("devDependencies", {})}
        antes, ahora = deps(base_sha), deps(destino_sha)
        nuevas = {k: v for k, v in ahora.items() if k not in antes}
        subidas = {k: f"{antes[k]} → {v}" for k, v in ahora.items() if k in antes and antes[k] != v}
        if nuevas or subidas:
            add("dependencias", "Dependencias cambiadas", "package.json", ["devs"], {"nuevas": nuevas, "actualizadas": subidas})

    # infraestructura
    for est, ruta in cambios:
        if INFRA.search(ruta) and est in "AMD":
            add("infraestructura", f"Infraestructura: `{ruta}` ({ {'A': 'nuevo', 'M': 'modificado', 'D': 'borrado'}[est] })", ruta,
                ["devops"], {"estado": est})

    # código de la app (sólo carpetas)
    carpetas = {}
    for est, ruta in cambios:
        if ruta.startswith("src/"):
            c = "/".join(ruta.split("/")[:3])
            carpetas[c] = carpetas.get(c, 0) + 1
    if carpetas:
        add("codigo-app", "Código de la app tocado", "src/", ["devs"], {"carpetas": dict(sorted(carpetas.items()))})

    adrs = sorted({m for c in commits for m in ADR.findall(c["asunto"])} | set(ADR.findall(diff_total)))
    salida = {"ticket": a.ticket, "generado": datetime.now().strftime("%Y-%m-%d %H:%M"), "repo": repo.name,
              "base": base_sha[:10], "destino": destino_sha[:10], "destino_completo": destino_sha,
              "commits": commits, "adrs_citados": adrs, "archivos_cambiados": len(cambios), "hechos": hechos}
    Path(a.salida).parent.mkdir(parents=True, exist_ok=True)
    Path(a.salida).write_text(json.dumps(salida, indent=2, ensure_ascii=False), "utf-8")
    print(f"{a.ticket}: {len(cambios)} archivos, {len(commits)} commits, {len(hechos)} hechos "
          f"({', '.join(sorted({h['tipo'] for h in hechos}))}) → {a.salida}")


if __name__ == "__main__":
    main()
