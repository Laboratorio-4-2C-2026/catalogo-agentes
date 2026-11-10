#!/usr/bin/env python3
"""Estima horas trabajadas por persona y por período a partir de la actividad de git.

Es un piso reproducible, no un parte de horas: no ve reuniones, diseño ni
investigación que no dejan commits. Solo lee el historial: no modifica nada.

    python3 horas_git.py --repo ../zest --desde 2026-08-06 --hasta 2026-11-12 \
        --inicio-periodos 2026-08-06 --alias alias.yml --tarifa 10

Cada día con actividad de una persona vale:
    acotar((último commit - primer commit) + margen, piso, techo)
"""
import argparse
import csv
import subprocess
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path


def leer_alias(ruta):
    """alias.yml: `Nombre visible: [email o nombre de git, ...]`. Sin PyYAML para no sumar dependencias."""
    alias, actual = {}, None
    if not ruta:
        return alias
    for linea in Path(ruta).read_text(encoding="utf-8").splitlines():
        if not linea.strip() or linea.lstrip().startswith("#"):
            continue
        if not linea.startswith((" ", "-", "\t")) and linea.rstrip().endswith(":"):
            actual = linea.rstrip()[:-1].strip()
        elif actual:
            alias[linea.strip().lstrip("-").strip().strip("'\"").lower()] = actual
    return alias


def es_superficial(repo):
    out = subprocess.run(["git", "-C", repo, "rev-parse", "--is-shallow-repository"], capture_output=True, text=True)
    return out.stdout.strip() == "true"


def commits(repo, desde, hasta):
    fmt = "%H%x1f%an%x1f%ae%x1f%aI"
    out = subprocess.run(
        ["git", "-C", repo, "log", "--all", "--no-merges", f"--since={desde}", f"--until={hasta} 23:59", f"--format={fmt}"],
        capture_output=True, text=True, check=True,
    ).stdout
    vistos = set()
    for linea in out.splitlines():
        sha, nombre, email, cuando = linea.split("\x1f")
        if sha in vistos:
            continue
        vistos.add(sha)
        yield nombre, email, datetime.fromisoformat(cuando)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", action="append", required=True, help="Repo a leer (se puede repetir)")
    ap.add_argument("--desde", required=True)
    ap.add_argument("--hasta", required=True)
    ap.add_argument("--inicio-periodos", required=True, help="Primer día del período 1 (los períodos son semanales)")
    ap.add_argument("--alias", help="YAML simple que agrupa emails o nombres de git por persona")
    ap.add_argument("--excluir", default="", help="Personas a excluir, separadas por coma (por ejemplo, gestión ya presupuestada como LOE)")
    ap.add_argument("--margen", type=float, default=1.0)
    ap.add_argument("--piso", type=float, default=1.5)
    ap.add_argument("--techo", type=float, default=9.0)
    ap.add_argument("--tarifa", type=float, help="USD por hora, para valorizar el AC")
    ap.add_argument("--csv", help="Guardar el detalle por persona y día")
    a = ap.parse_args()

    for repo in a.repo:
        if es_superficial(repo):
            print(f"AVISO: {repo} es un clon superficial: subestima el esfuerzo. Corré `git fetch --unshallow` antes.", file=sys.stderr)

    alias = leer_alias(a.alias)
    excluir = {x.strip().lower() for x in a.excluir.split(",") if x.strip()}
    inicio = date.fromisoformat(a.inicio_periodos)

    dias = defaultdict(list)  # (persona, fecha) -> [hora, ...]
    for repo in a.repo:
        for nombre, email, cuando in commits(repo, a.desde, a.hasta):
            persona = alias.get(email.lower()) or alias.get(nombre.lower()) or nombre
            if persona.lower() in excluir:
                continue
            local = cuando.astimezone()
            dias[(persona, local.date())].append(local)

    detalle, por_periodo, un_commit = [], defaultdict(float), defaultdict(int)
    for (persona, dia), horas in sorted(dias.items()):
        span = (max(horas) - min(horas)).total_seconds() / 3600
        estimado = min(max(span + a.margen, a.piso), a.techo)
        periodo = (dia - inicio).days // 7 + 1
        detalle.append((persona, dia.isoformat(), periodo, len(horas), round(estimado, 2)))
        por_periodo[(persona, periodo)] += estimado
        if len(horas) == 1:
            un_commit[persona] += 1

    personas = sorted({p for p, _ in por_periodo})
    periodos = sorted({n for _, n in por_periodo})
    num = lambda x: f"{x:g}".replace(".", ",")
    print(f"Horas estimadas desde git ({a.desde} → {a.hasta}). Margen {num(a.margen)} h, piso {num(a.piso)} h, techo {num(a.techo)} h.\n")
    print("| Persona | " + " | ".join(f"P{n} ({(inicio + timedelta(weeks=n - 1)).strftime('%d/%m')})" for n in periodos) + " | Total |")
    print("|---|" + "---|" * (len(periodos) + 1))
    total_general = 0.0
    for p in personas:
        fila = [por_periodo.get((p, n), 0.0) for n in periodos]
        total_general += sum(fila)
        print(f"| {p} | " + " | ".join(f"{h:.1f}".replace(".", ",") for h in fila) + f" | **{sum(fila):.1f}**".replace(".", ",") + " |")
    print(f"\nTotal: {total_general:.1f} h".replace(".", ","))
    if a.tarifa:
        print(f"AC estimado: USD {total_general * a.tarifa:,.0f}".replace(",", "."))
    for p, n in sorted(un_commit.items()):
        print(f"- {p}: {n} día(s) con un solo commit, contados al piso de {num(a.piso)} h.")

    if a.csv:
        with open(a.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["persona", "fecha", "periodo", "commits", "horas_estimadas"])
            w.writerows(detalle)


if __name__ == "__main__":
    main()
