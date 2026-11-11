# MCP safety baseline

## Linear

Connect via OAuth. Grant read-only access first. Agents may draft issues/reports, but only an authorized human may approve issue mutation. Link PRs through the GitHub integration so status is backed by code review and CI evidence.

## Neon

Use only a development branch with anonymized or sample data. Never use the MCP to access production, retrieve connection strings, expose PII, or make unreviewed destructive schema changes.

## Stitch

Use the Google Stitch MCP endpoint. Stitch replaces Figma in this workflow. Generated screens are design proposals; reference their linked Linear issue and get PO approval before implementation.

## Engram / Gentle AI

The installer provisions the Gentleman Programming Engram binary locally and exposes `engram mcp --tools=agent` through an absolute command path. The repository's `.engram/config.json` fixes the project name. Agents must proactively save curated decisions, bugs and discoveries; never save secrets, credentials, PII or raw transcripts.

## Agentation

The full management `frontend-checker` uses the auto-provisioned local Agentation MCP through `npx --yes agentation-mcp server`. It has no remote endpoint. Visual annotations remain human-approved review input; the MCP must not be treated as authorization to change scope, merge, deploy or bypass PO/TL approval.
