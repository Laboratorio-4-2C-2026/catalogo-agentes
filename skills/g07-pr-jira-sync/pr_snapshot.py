#!/usr/bin/env python3
"""Snapshot de los PRs de un repo de GitHub, listo para cruzar con Jira.

Usa el CLI `gh` (ya autenticado) en modo solo lectura. Imprime un JSON con:
  - prs: PRs abiertos + mergeados/cerrados en los últimos N días, cada uno con
    las keys de Jira que menciona (título o branch) y sus señales propias
    (sin key, viejo, sin reviewer, draft).
  - by_key: índice key de Jira -> números de PR, para que el cruce con Jira
    sea un lookup y no un re-parseo.

Uso:
  python3 pr_snapshot.py --repo <org>/<repo> --project <KEY> [--days 14] [--stale-days 3]
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone

PR_FIELDS = ",".join([
    "number", "title", "headRefName", "baseRefName", "state", "isDraft",
    "author", "createdAt", "updatedAt", "mergedAt", "closedAt",
    "reviewDecision", "reviewRequests", "latestReviews", "url",
])


def gh_pr_list(repo, state, search=None, limit=200):
    cmd = ["gh", "pr", "list", "--repo", repo, "--state", state,
           "--limit", str(limit), "--json", PR_FIELDS]
    if search:
        cmd += ["--search", search]
    try:
        out = subprocess.run(cmd, check=True, capture_output=True, text=True).stdout
    except FileNotFoundError:
        sys.exit("error: no se encontró el CLI `gh`. Instalalo y corré `gh auth login`.")
    except subprocess.CalledProcessError as e:
        sys.exit(f"error: falló `{' '.join(cmd)}`:\n{e.stderr.strip()}")
    return json.loads(out)


def parse_ts(value):
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", required=True, help="owner/nombre del repo de GitHub")
    ap.add_argument("--project", required=True, help="project key de Jira (ej: STUDY)")
    ap.add_argument("--days", type=int, default=14, help="ventana para PRs mergeados/cerrados (default: 14)")
    ap.add_argument("--stale-days", type=int, default=3, help="días sin actividad para marcar un PR abierto como viejo (default: 3)")
    args = ap.parse_args()

    now = datetime.now(timezone.utc)
    since = (now - timedelta(days=args.days)).date().isoformat()
    key_re = re.compile(rf"\b{re.escape(args.project)}-\d+\b", re.IGNORECASE)

    raw = gh_pr_list(args.repo, "open")
    raw += gh_pr_list(args.repo, "closed", search=f"closed:>={since}")

    prs, by_key = [], {}
    for pr in raw:
        keys = sorted({k.upper() for k in key_re.findall(f"{pr['title']} {pr['headRefName']}")},
                      key=lambda k: int(k.split("-")[1]))
        state = "MERGED" if pr.get("mergedAt") else pr["state"]
        updated = parse_ts(pr["updatedAt"])
        age_days = (now - parse_ts(pr["createdAt"])).days
        idle_days = (now - updated).days if updated else None

        flags = []
        if not keys:
            flags.append("sin_key_jira")
        if state == "OPEN":
            if pr["isDraft"]:
                flags.append("draft")
            if idle_days is not None and idle_days >= args.stale_days:
                flags.append("viejo")
            if not pr["reviewRequests"] and not pr["latestReviews"]:
                flags.append("sin_reviewer")
            if pr["reviewDecision"] == "CHANGES_REQUESTED":
                flags.append("cambios_pedidos")

        entry = {
            "number": pr["number"],
            "title": pr["title"],
            "branch": pr["headRefName"],
            "base": pr["baseRefName"],
            "state": state,
            "author": (pr.get("author") or {}).get("login"),
            "review_decision": pr["reviewDecision"] or None,
            "reviewers": sorted({r.get("login") or r.get("name") or "?" for r in pr["reviewRequests"]}
                                | {(r.get("author") or {}).get("login", "?") for r in pr["latestReviews"]}),
            "created_at": pr["createdAt"],
            "merged_at": pr.get("mergedAt"),
            "age_days": age_days,
            "idle_days": idle_days,
            "jira_keys": keys,
            "flags": flags,
            "url": pr["url"],
        }
        prs.append(entry)
        for k in keys:
            by_key.setdefault(k, []).append(pr["number"])

    prs.sort(key=lambda p: p["number"], reverse=True)
    json.dump({
        "repo": args.repo,
        "generated_at": now.isoformat(timespec="seconds"),
        "window_days": args.days,
        "stale_days": args.stale_days,
        "counts": {
            "open": sum(p["state"] == "OPEN" for p in prs),
            "merged": sum(p["state"] == "MERGED" for p in prs),
            "closed_unmerged": sum(p["state"] == "CLOSED" for p in prs),
        },
        "prs": prs,
        "by_key": by_key,
    }, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
