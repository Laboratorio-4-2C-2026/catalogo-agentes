#!/usr/bin/env python3
"""Sincroniza tickets de Multica con PRs mergeadas a dev.

  audit <repo>           lista tickets atrasados; con --apply los pasa a done.
  event                  procesa una PR mergeada, con PR_BASE, PR_HEAD y PR_TITLE.
                         Simula salvo que se pase --apply.
"""
import argparse
import json
import os
import re
import subprocess
import sys

TICKET = re.compile(r"\bZEST-(\d+)\b", re.IGNORECASE)
TRUNK = "dev"


def extract_ticket(head, title):
    """Devuelve (ticket, motivo). Mira la rama y el título, nunca la descripción."""
    ids = {int(n) for n in TICKET.findall(f"{head} {title}")}
    if not ids:
        return None, "la PR no tiene ID de ticket en la rama ni en el título"
    if len(ids) > 1:
        return None, "hay más de un ID: " + ", ".join(f"ZEST-{n}" for n in sorted(ids))
    return f"ZEST-{ids.pop()}", ""


def decide(base, status, labels):
    """Devuelve (mover, motivo)."""
    if base != TRUNK:
        return False, f"la PR se mergeó en `{base}`, no en `{TRUNK}`"
    if status != "in_review":
        return False, f"el ticket está en `{status}`, no en `in_review`"
    if "infra" in labels:
        return False, "tiene etiqueta infra: necesita evidencia"
    return True, "PR mergeada a dev"


def run_json(cmd):
    return json.loads(subprocess.run(cmd, check=True, capture_output=True, text=True).stdout)


def get_issue(ticket):
    data = run_json(["multica", "issue", "get", ticket, "--output", "json"])
    return data["status"], [l["name"] for l in data.get("labels") or []]


def in_review_tickets():
    data = run_json(["multica", "issue", "list", "--status", "in_review",
                     "--limit", "100", "--output", "json"])
    issues = data if isinstance(data, list) else data.get("issues", [])
    return {i["identifier"] for i in issues}


def move_to_done(ticket):
    subprocess.run(["multica", "issue", "status", ticket, "done", "--no-start"], check=True)


def audit(repo, apply_changes=False):
    prs = run_json(["gh", "pr", "list", "-R", repo, "--state", "merged", "--base", TRUNK,
                    "--limit", "300", "--json", "number,title,headRefName"])
    pending = moved = 0
    in_review = in_review_tickets()
    for pr in prs:
        ticket, _ = extract_ticket(pr["headRefName"], pr["title"])
        if not ticket or ticket not in in_review:
            continue
        try:
            status, labels = get_issue(ticket)
        except subprocess.CalledProcessError:
            print(f"? {ticket}: no se pudo leer (PR {pr['number']})")
            continue
        should_move, reason = decide(TRUNK, status, labels)
        if should_move:
            pending += 1
            print(f"PENDIENTE {ticket}: PR {pr['number']} ya está en dev — {pr['title'][:70]}")
            if apply_changes:
                move_to_done(ticket)
                moved += 1
                print(f"MOVIDO {ticket} a done")
        elif status == "in_review":
            print(f"OMITIDO {ticket}: {reason} (PR {pr['number']})")
    print(f"Tickets pendientes: {pending}. Movidos a done: {moved}.")


def event(apply_changes):
    base, head, title = (os.environ[k] for k in ("PR_BASE", "PR_HEAD", "PR_TITLE"))
    ticket, reason = extract_ticket(head, title)
    if not ticket:
        print(f"Sin cambios: {reason}.")
        return
    if base != TRUNK:
        print(f"Sin cambios en {ticket}: la PR se mergeó en `{base}`.")
        return
    status, labels = get_issue(ticket)
    should_move, reason = decide(base, status, labels)
    if not should_move:
        print(f"Sin cambios en {ticket}: {reason}.")
    elif apply_changes:
        move_to_done(ticket)
        print(f"{ticket} pasó a done.")
    else:
        print(f"Simulación: {ticket} pasaría a done.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="mode", required=True)
    audit_parser = sub.add_parser("audit")
    audit_parser.add_argument("repo")
    audit_parser.add_argument("--apply", action="store_true")
    sub.add_parser("event").add_argument("--apply", action="store_true")
    args = ap.parse_args()
    if args.mode == "audit":
        audit(args.repo, args.apply)
    else:
        event(args.apply)


if __name__ == "__main__":
    sys.exit(main())
