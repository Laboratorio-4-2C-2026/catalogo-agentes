#!/usr/bin/env python3
"""cron-check.py — Cron de respaldo para vaivendev.

Mitigación obligatoria por el hallazgo E3 del spike:
GitHub Actions no dispara eventos pull_request cuando un PR tiene conflicto de merge.
Este script busca PRs abiertos en vaiven-app donde se haya solicitado review a vaivendev
y que aún no tengan la review correspondiente publicada para el último SHA.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run_cmd(cmd, check=True):
    res = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if check and res.returncode != 0:
        raise RuntimeError(f"Error ejecutando '{cmd}': {res.stderr.strip()}")
    return res.stdout.strip(), res.stderr.strip(), res.returncode


def main():
    repo = os.environ.get("TARGET_REPO", "vaiven-austral/vaiven-app")
    bot_login = os.environ.get("BOT_LOGIN", "vaivendev").lower()

    print(f"[*] Buscando PRs abiertos en {repo} con review solicitada a '{bot_login}'...")

    cmd = (
        f"gh pr list --repo {repo} --state open "
        f"--json number,headRefOid,reviewRequests,title,headRefName"
    )
    stdout, stderr, code = run_cmd(cmd, check=False)
    if code != 0:
        print(f"[!] Error al listar PRs: {stderr}")
        sys.exit(1)

    prs = json.loads(stdout)
    pending_prs = []

    for pr in prs:
        num = pr["number"]
        sha = pr["headRefOid"]
        requests = [r.get("login", "").lower() for r in pr.get("reviewRequests", [])]

        if bot_login in requests:
            # Comprobar si ya se publicó review para este SHA
            # Solo reviews de la cuenta del bot: el marcador en otro comentario no cuenta.
            cmd_reviews = f"gh api repos/{repo}/pulls/{num}/reviews --jq '.[] | select(.user.login==\"{bot_login}\") | .body'"
            rev_out, _, rev_code = run_cmd(cmd_reviews, check=False)
            marker = f"<!-- code-reviewer-de-prs:sha:{sha} -->"

            if rev_code == 0 and marker in rev_out:
                print(f"[-] PR #{num} ya tiene review para {sha[:7]}. Omitiendo.")
            else:
                print(f"[+] PR #{num} ({pr['title']}) necesita review.")
                pending_prs.append((num, sha))

    if not pending_prs:
        print("[✓] No hay PRs pendientes de review.")
        sys.exit(0)

    print(f"\n[*] Ejecutando review para {len(pending_prs)} PR(s) pendiente(s)...")
    for pr_num, pr_sha in pending_prs:
        print(f"\n--- Procesando PR #{pr_num} (SHA: {pr_sha[:7]}) ---")
        run_review = f"python3 {ROOT}/scripts/generar-review.py --pr {pr_num} --sha {pr_sha} --repo {repo}"
        out, err, ret = run_cmd(run_review, check=False)
        print(out)
        if ret != 0:
            print(f"[!] Error procesando PR #{pr_num}: {err}")

    print("\n[✓] Cron de respaldo finalizado.")


if __name__ == "__main__":
    main()
