#!/usr/bin/env python3
"""Reporte semanal de branches de proyecto-zest/zest en la planilla "Zest — Limpieza de branches".

Uso:
    python3 branch_report.py --repo ~/zest-agentes/zest --dry-run   # muestra el reporte, no escribe
    python3 branch_report.py --repo ~/zest-agentes/zest             # actualiza la planilla

Qué hace:
  1. git fetch --prune (trae todas las branches remotas y descarta las que ya se borraron).
  2. Clasifica cada branch remota (menos main):
       Mergeada   -> todos sus commits están en main, o su PR figura como mergeado (squash merge)
       Abandonada -> tiene commits fuera de main y 14 días o más sin actividad
       Activa     -> tuvo actividad en los últimos 14 días
  3. Reescribe la pestaña "Branches" y agrega una fila en "Historial".

Nunca borra branches. El estado de los PRs se toma de `gh` si está instalado y logueado; si no, solo git.
Credenciales: ~/.config/zest/google-sa.json (o GOOGLE_SA_KEY).
"""
import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
from zoneinfo import ZoneInfo

SHEET_ID = "1auaI7xH8hF4QNlxotKb28uYayFI7ColpcZATPMm7OTo"
REPO_SLUG = "proyecto-zest/zest"
DIAS_ABANDONADA = 14
TZ = ZoneInfo("America/Argentina/Buenos_Aires")
ORDEN = {"Mergeada": 0, "Abandonada": 1, "Activa": 2}


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, check=True).stdout.strip()


def default_branch(repo):
    try:
        ref = git(repo, "symbolic-ref", "--short", "refs/remotes/origin/HEAD")
        return ref.split("/", 1)[1]
    except subprocess.CalledProcessError:
        return "main"


def pr_states():
    """headRefName -> PR más reciente {number, state}. Vacío si gh no está disponible."""
    if not shutil.which("gh"):
        return {}
    try:
        out = subprocess.run(
            ["gh", "pr", "list", "--repo", REPO_SLUG, "--state", "all", "--limit", "500",
             "--json", "number,headRefName,state,updatedAt"],
            capture_output=True, text=True, check=True, timeout=60).stdout
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return {}
    prs = {}
    for p in sorted(json.loads(out), key=lambda p: p["updatedAt"]):
        prs[p["headRefName"]] = {"number": p["number"], "state": p["state"]}
    return prs


def collect(repo, hoy):
    git(repo, "fetch", "--prune", "origin", "+refs/heads/*:refs/remotes/origin/*")
    main = default_branch(repo)
    prs = pr_states()
    fmt = "%(refname:short)|%(committerdate:iso-strict)|%(authorname)"
    rows = []
    for line in git(repo, "for-each-ref", f"--format={fmt}", "refs/remotes/origin").splitlines():
        ref, fecha, autor = line.split("|", 2)
        name = ref.split("/", 1)[1] if "/" in ref else ref
        if name in ("HEAD", main) or ref == "origin":
            continue
        last = dt.datetime.fromisoformat(fecha).astimezone(TZ).date()
        dias = (hoy - last).days
        fuera = int(git(repo, "rev-list", "--count", f"origin/{main}..{ref}"))
        pr = prs.get(name)
        pr_txt = f"#{pr['number']}" if pr else ""
        pr_state = {"MERGED": "Mergeado", "OPEN": "Abierto", "CLOSED": "Cerrado sin merge"}.get(
            pr["state"], pr["state"]) if pr else ("Sin PR" if prs else "(sin datos de PRs)")

        if fuera == 0 or (pr and pr["state"] == "MERGED"):
            estado, rec = "Mergeada", f"Borrar: ya está en {main}"
        elif dias >= DIAS_ABANDONADA:
            estado = "Abandonada"
            if pr and pr["state"] == "OPEN":
                rec = f"PR {pr_txt} abierto sin actividad: revisar con {autor}"
            elif pr and pr["state"] == "CLOSED":
                rec = f"PR cerrado sin merge: confirmar con {autor} y borrar"
            else:
                rec = f"Preguntar a {autor} si sigue; si no, borrar"
        else:
            estado = "Activa"
            rec = f"Seguir: PR {pr_txt} abierto" if pr and pr["state"] == "OPEN" else "Seguir"

        rows.append([name, estado, rec, last.strftime("%d/%m/%y"), dias, autor, fuera, pr_txt, pr_state,
                     hoy.strftime("%d/%m/%y")])
    rows.sort(key=lambda r: (ORDEN[r[1]], -r[4], r[0]))
    return rows


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True, help="Ruta al clon local de proyecto-zest/zest")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    repo = os.path.expanduser(args.repo)
    hoy = dt.datetime.now(TZ).date()

    rows = collect(repo, hoy)
    cuenta = {k: sum(1 for r in rows if r[1] == k) for k in ORDEN}
    resumen = {"total": len(rows), **cuenta}

    if args.dry_run:
        print(json.dumps({"resumen": resumen, "branches": rows}, ensure_ascii=False, indent=2))
        return 0

    import gspread
    key = os.environ.get("GOOGLE_SA_KEY") or os.path.expanduser("~/.config/zest/google-sa.json")
    sh = gspread.service_account(filename=key).open_by_key(SHEET_ID)
    ws, hist = sh.worksheet("Branches"), sh.worksheet("Historial")

    anteriores = {v for v in ws.col_values(1)[1:] if v}
    borradas = len(anteriores - {r[0] for r in rows}) if anteriores else ""

    ws.batch_clear(["A2:J"])
    if rows:
        ws.update(values=rows, range_name=f"A2:J{len(rows) + 1}", value_input_option="RAW")
    hist.append_row([hoy.strftime("%d/%m/%y"), len(rows), cuenta["Mergeada"], cuenta["Abandonada"],
                     cuenta["Activa"], borradas], value_input_option="USER_ENTERED")

    print(json.dumps({"resumen": resumen, "borradas_desde_la_semana_anterior": borradas,
                      "planilla": f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
