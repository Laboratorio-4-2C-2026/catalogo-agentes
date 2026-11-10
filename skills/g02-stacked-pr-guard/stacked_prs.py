#!/usr/bin/env python3
"""Detecta PRs apiladas con problemas. Solo lee GitHub con la CLI `gh`."""
import argparse
import json
import subprocess
import sys

FIELDS = "number,title,baseRefName,headRefName,author,mergedAt"


def fetch_prs(repo, state):
    out = subprocess.run(
        ["gh", "pr", "list", "-R", repo, "--state", state, "--limit", "300", "--json", FIELDS],
        check=True, capture_output=True, text=True,
    ).stdout
    return json.loads(out)


def analyze(open_prs, merged_prs, trunk):
    """Devuelve una lista de (tipo, pr, detalle) para las PRs que no apuntan a trunk."""
    open_by_head = {p["headRefName"]: p for p in open_prs}
    merged_by_head = {}
    for p in sorted(merged_prs, key=lambda x: x["mergedAt"] or ""):
        merged_by_head[p["headRefName"]] = p

    alerts = []
    for pr in open_prs:
        base = pr["baseRefName"]
        if base in (trunk, "main"):
            continue
        if base in open_by_head:
            alerts.append(("CADENA", pr, f"depende de la PR {open_by_head[base]['number']}"))
        elif base in merged_by_head:
            m = merged_by_head[base]
            alerts.append(("RAMA MUERTA", pr,
                           f"su base `{base}` ya se mergeó en la PR {m['number']} (hacia `{m['baseRefName']}`)"))
        else:
            alerts.append(("BASE SIN PR", pr, f"su base `{base}` no tiene PR"))
    return alerts


def dependents(open_prs, branch):
    return [p for p in open_prs if p["baseRefName"] == branch]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("repo")
    ap.add_argument("--trunk", default="dev")
    ap.add_argument("--branch", help="rama puntual que se quiere mergear o borrar")
    args = ap.parse_args()

    open_prs = fetch_prs(args.repo, "open")
    if args.branch:
        deps = dependents(open_prs, args.branch)
        if not deps:
            print(f"Ninguna PR abierta usa `{args.branch}` como base.")
            return 0
        print(f"Atención: estas PRs abiertas usan `{args.branch}` como base:")
        for p in deps:
            print(f"- PR {p['number']} ({p['author']['login']}): {p['title']}")
        return 1

    alerts = analyze(open_prs, fetch_prs(args.repo, "merged"), args.trunk)
    if not alerts:
        print(f"Todas las PRs abiertas apuntan a `{args.trunk}`. Sin apiladas.")
        return 0
    for kind, pr, detail in alerts:
        print(f"[{kind}] PR {pr['number']} ({pr['author']['login']}, {pr['headRefName']}): {detail}")
    return 1 if any(a[0] != "CADENA" for a in alerts) else 0


if __name__ == "__main__":
    sys.exit(main())
