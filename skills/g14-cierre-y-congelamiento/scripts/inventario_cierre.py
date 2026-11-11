#!/usr/bin/env python3
"""inventario_cierre.py — checklist de cierre/traspaso a partir de lo que los repos realmente usan.

Dos modos:

  generar  Descubre servicios, accesos, secretos referenciados y crons activos
           en los repos y arma el checklist (Markdown + JSON con las
           verificaciones). Si se pasa --higiene con el JSON de
           g14-auditor-de-higiene-pre-entrega, suma los hallazgos de higiene;
           si no, deja un ítem previo "correr el auditor de higiene".

  verificar  Lee el checklist (los ítems marcados [x]) y comprueba lo que se
           puede comprobar sin credenciales: crons apagados, archivos
           sensibles ya ignorados, repos archivados (con --online, vía `gh`
           de sólo lectura). Lo que no se puede comprobar queda como
           «confirmación humana», nunca como «verificado».

Uso:
  python3 inventario_cierre.py generar --raiz ~/Projects/vaiven [--higiene higiene.json] --salida cierre.md
  python3 inventario_cierre.py verificar cierre.md [--online]

Nunca lee valores de variables de entorno: sólo sus nombres.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", "__pycache__", ".venv"}
HOSTS = re.compile(r"https?://((?:[a-z0-9-]+\.)+(?:atlassian\.net|supabase\.co|vercel\.app|figma\.com|canva\.com|run\.app))", re.I)
SECRETS_REF = re.compile(r"\$\{\{\s*(secrets|vars)\.([A-Za-z0-9_]+)\s*\}\}")
ENV_NAME = re.compile(r"^\s*(?:export\s+)?([A-Z][A-Z0-9_]{2,})\s*=")
REMOTE = re.compile(r"github\.com[:/]([^/]+)/([^/.\s]+)")
SERVICIO = {  # sufijo de host -> (nombre, acción por defecto, cómo se comprueba)
    "atlassian.net": ("Jira / Atlassian", "transferir", "Que el nuevo dueño figure como admin del sitio y el anterior pueda salir."),
    "supabase.co": ("Supabase (proyecto)", "transferir", "Panel → Settings → el nuevo dueño en la organización; dump de la base exportado y guardado."),
    "vercel.app": ("Vercel (despliegue)", "transferir", "El proyecto figura en el equipo del nuevo dueño o fue eliminado; el dominio ya no responde si se apagó."),
    "figma.com": ("Figma", "transferir", "Los archivos están en un equipo del nuevo dueño."),
    "canva.com": ("Canva", "transferir", "Los diseños fueron transferidos o exportados a PDF."),
    "run.app": ("Google Cloud Run", "apagar", "El servicio no figura en la consola o devolvió 404."),
}


def git(repo, *args):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, timeout=60)
    return r.returncode, r.stdout.decode("utf-8", "replace")


def sha(*partes):
    return hashlib.sha1("|".join(map(str, partes)).encode()).hexdigest()[:8]


def leer(path, tope=300_000):
    try:
        if Path(path).stat().st_size > tope:
            return ""
        return Path(path).read_text("utf-8", "replace")
    except OSError:
        return ""


def cron_activo(texto):
    return any(re.match(r"\s*(schedule:|-\s*cron:|cron:)", l) for l in texto.splitlines())


def descubrir(repo):
    repo = Path(repo)
    _, tracked = git(repo, "ls-files", "-z")
    tracked = [p for p in tracked.split("\0") if p]
    d = {"nombre": repo.name, "ruta": str(repo), "github": None, "servicios": {}, "crons": [],
         "secretos": {}, "env": {}, "mcp": [], "marcas": []}
    _, rem = git(repo, "remote", "get-url", "origin")
    m = REMOTE.search(rem)
    if m:
        d["github"] = f"{m.group(1)}/{m.group(2)}"
    for rel in tracked:
        p = repo / rel
        name = Path(rel).name
        if rel.startswith(".github/workflows/") and rel.endswith((".yml", ".yaml")):
            t = leer(p)
            if cron_activo(t):
                d["crons"].append(rel)
            for tipo, nombre in SECRETS_REF.findall(t):
                d["secretos"].setdefault(nombre, {"tipo": tipo, "en": []})["en"].append(rel)
        elif name.startswith(".env") and name.endswith((".example", ".sample")):
            for l in leer(p).splitlines():
                mm = ENV_NAME.match(l)
                if mm:
                    d["env"].setdefault(mm.group(1), []).append(rel)
        elif name == ".mcp.json":
            try:
                d["mcp"] += list(json.loads(leer(p)).get("mcpServers", {}).keys())
            except ValueError:
                pass
        if name == "vercel.json":
            d["marcas"].append(("Vercel", rel))
        elif rel.endswith("supabase/config.toml"):
            d["marcas"].append(("Supabase (stack local)", rel))
        elif name.lower().startswith(("docker-compose", "caddyfile")):
            d["marcas"].append(("VM / contenedores (compose o Caddy)", rel))
        elif "n8n" in rel.split("/")[:2] and rel.endswith(".json"):
            if not any(a == "n8n (workflows)" for a, _ in d["marcas"]):
                d["marcas"].append(("n8n (workflows)", rel))
        if rel.endswith((".md", ".json", ".toml", ".yml", ".yaml", ".env.example", ".html")):
            for h in HOSTS.findall(leer(p, 150_000)):
                h = h.lower()
                d["servicios"].setdefault(h, set()).add(rel)
    return d


def items_de(d, higiene):
    it = []
    def add(tipo, accion, objeto, origen, verif, check):
        it.append({"id": sha(d["nombre"], tipo, objeto, origen), "repo": d["nombre"], "tipo": tipo,
                   "accion": accion, "objeto": objeto, "origen": origen, "dueno": "<dueño>",
                   "verificacion": verif, "check": check})
    if d["github"]:
        add("repo", "transferir/archivar", f"Repo GitHub {d['github']}", "git remote origin",
            "Con `gh repo view --json isArchived,owner`: archivado, o dueño = el destinatario.",
            {"tipo": "gh-archivado", "repo": d["github"]})
    for cr in d["crons"]:
        add("cron", "apagar", f"Workflow programado `{cr}`", cr,
            "El archivo ya no tiene `schedule:`/`cron:` activo (o el workflow está deshabilitado).",
            {"tipo": "cron-off", "ruta": d["ruta"], "archivo": cr})
    for nombre, info in sorted(d["secretos"].items()):
        add("secreto", "rotar y retirar", f"{info['tipo']}.{nombre} (GitHub Actions)", ", ".join(sorted(set(info["en"]))),
            "Revocado en el proveedor y borrado de la configuración del repo; confirmación humana.", {"tipo": "manual"})
    if d["env"]:
        nombres = sorted(d["env"])
        add("env", "entregar o revocar", f"{len(nombres)} variables de entorno: " + ", ".join(nombres[:12]) + ("…" if len(nombres) > 12 else ""),
            ", ".join(sorted({x for v in d["env"].values() for x in v})),
            "Cada valor real se entrega por canal privado al nuevo dueño o se revoca; confirmación humana.", {"tipo": "manual"})
    for mcp in sorted(set(d["mcp"])):
        add("mcp", "documentar", f"Servidor MCP `{mcp}` (.mcp.json)", ".mcp.json",
            "El destinatario sabe qué credencial usa y la reemplaza por la propia.", {"tipo": "manual"})
    for marca, rel in d["marcas"]:
        add("infra", "documentar/apagar", marca, rel,
            "Se entrega el runbook de este componente (ver g14-runbook-por-audiencia) o se lo apaga; confirmación humana.", {"tipo": "manual"})
    for host, archivos in sorted(d["servicios"].items()):
        for suf, (nombre, accion, verif) in SERVICIO.items():
            if host.endswith(suf):
                add("servicio", accion, f"{nombre}: {host}", ", ".join(sorted(archivos)[:2]), verif, {"tipo": "manual"})
                break
    if higiene:
        repo_h = next((r for r in higiene["repos"] if r["nombre"] == d["nombre"]), None)
        for h in (repo_h or {"hallazgos": []})["hallazgos"]:
            if h["severidad"] in ("ALTA", "MEDIA"):
                chk = {"tipo": "ignorado", "ruta": d["ruta"], "archivo": h["archivo"]} if h["tipo"] == "sensible-sin-ignorar" else {"tipo": "manual"}
                add("higiene", "resolver", f"[{h['severidad']}] {h['tipo']} — {h['archivo']}" + (f":{h['linea']}" if h["linea"] else ""),
                    "auditor de higiene", h["accion"], chk)
    return it


def generar(a):
    raiz = Path(a.raiz)
    repos = sorted(p for p in raiz.iterdir() if (p / ".git").exists())
    higiene = json.loads(Path(a.higiene).read_text("utf-8")) if a.higiene else None
    items = []
    if not higiene:
        items.append({"id": "previo-higiene", "repo": "(todos)", "tipo": "previo", "accion": "correr",
                      "objeto": "Auditoría de higiene (g14-auditor-de-higiene-pre-entrega)", "origen": "—", "dueno": "<dueño>",
                      "verificacion": "Sin esta corrida el checklist no sabe qué secretos hay que rotar. Pasar su JSON con --higiene.",
                      "check": {"tipo": "manual"}})
    for r in repos:
        items += items_de(descubrir(r), higiene)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    L = ["# Checklist de cierre y congelamiento", "",
         f"Generado: {fecha} · Repos: {', '.join(r.name for r in repos)} · Higiene: {'incluida' if higiene else 'NO incluida'}", "",
         "Marcá `[x]` cuando esté hecho y corré `inventario_cierre.py verificar <este archivo>`.", "",
         "| Hecho | ID | Repo | Acción | Objeto | Origen | Dueño | Cómo se comprueba |", "|---|---|---|---|---|---|---|---|"]
    esc = lambda s: s.replace("|", "\\|")
    for i in items:
        L.append(f"| [ ] | {i['id']} | {i['repo']} | {i['accion']} | {esc(i['objeto'])} | {esc(i['origen'])} | {i['dueno']} | {esc(i['verificacion'])} |")
    por_tipo = {}
    for i in items:
        por_tipo[i["tipo"]] = por_tipo.get(i["tipo"], 0) + 1
    L += ["", "Resumen: " + ", ".join(f"{k}={v}" for k, v in sorted(por_tipo.items())) + f" · total={len(items)}"]
    out = Path(a.salida)
    out.write_text("\n".join(L) + "\n", "utf-8")
    out.with_suffix(".json").write_text(json.dumps({"generado": fecha, "items": items}, indent=2, ensure_ascii=False), "utf-8")
    print("\n".join(L[:6]) + f"\n… {len(items)} ítems → {out} (+ {out.with_suffix('.json').name})")


def verificar(a):
    md = Path(a.checklist)
    spec = {i["id"]: i for i in json.loads(md.with_suffix(".json").read_text("utf-8"))["items"]}
    marcados, total = {}, 0
    for l in md.read_text("utf-8").splitlines():
        m = re.match(r"\|\s*\[(.)\]\s*\|\s*([^|\s]+)\s*\|", l)
        if m and m.group(2) in spec:
            total += 1
            marcados[m.group(2)] = m.group(1).lower() == "x"
    res = {"ok": [], "falla": [], "humano": [], "pendiente": []}
    for iid, hecho in marcados.items():
        i, c = spec[iid], spec[iid]["check"]
        if not hecho:
            res["pendiente"].append(i)
            continue
        ok, nota = None, ""
        if c["tipo"] == "cron-off":
            p = Path(c["ruta"]) / c["archivo"]
            ok = (not p.exists()) or (not cron_activo(leer(p)))
            nota = "workflow sin cron activo" if ok else "el workflow todavía tiene `schedule:`/`cron:`"
        elif c["tipo"] == "ignorado":
            p = Path(c["ruta"]) / c["archivo"]
            ign, _ = git(c["ruta"], "check-ignore", "-q", c["archivo"])
            ok = (not p.exists()) or ign == 0
            nota = "ya ignorado o inexistente" if ok else "sigue sin ignorar"
        elif c["tipo"] == "gh-archivado" and a.online:
            r = subprocess.run(["gh", "repo", "view", c["repo"], "--json", "isArchived", "-q", ".isArchived"], capture_output=True, text=True)
            ok = r.stdout.strip() == "true" if r.returncode == 0 else None
            nota = ("archivado" if ok else "NO está archivado") if ok is not None else f"no se pudo consultar ({r.stderr.strip()[:60]})"
        if ok is True:
            res["ok"].append((i, nota))
        elif ok is False:
            res["falla"].append((i, nota))
        else:
            res["humano"].append(i)
    print(f"Checklist: {md.name} · {total} ítems · {sum(marcados.values())} marcados")
    print(f"  verificados automáticamente: {len(res['ok'])}")
    print(f"  MARCADOS PERO NO CUMPLEN:    {len(res['falla'])}")
    print(f"  confirmación humana (sin verificación automática): {len(res['humano'])}")
    print(f"  pendientes: {len(res['pendiente'])}")
    for i, n in res["falla"]:
        print(f"  ✗ {i['id']} {i['objeto']} — {n}")
    for i, n in res["ok"]:
        print(f"  ✓ {i['id']} {i['objeto']} — {n}")
    sys.exit(1 if res["falla"] else 0)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="modo", required=True)
    g = sub.add_parser("generar")
    g.add_argument("--raiz", required=True)
    g.add_argument("--higiene", help="JSON de g14-auditor-de-higiene-pre-entrega (opcional)")
    g.add_argument("--salida", required=True)
    v = sub.add_parser("verificar")
    v.add_argument("checklist")
    v.add_argument("--online", action="store_true", help="permite consultas de sólo lectura con `gh`")
    a = ap.parse_args()
    generar(a) if a.modo == "generar" else verificar(a)


if __name__ == "__main__":
    main()
