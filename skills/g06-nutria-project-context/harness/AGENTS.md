# NutrIA Agent Harness

This repository distributes the NutrIA operating model for Codex and Claude.

## Project knowledge

Read `.ai/index.md` first and then only the module relevant to the task. For client-side work, load `google-modern-web-guidance` before writing code.

## Product constraints

- NutrIA is a web MVP for personalized meal planning, recipes, shopping and adherence.
- It does not provide medical diagnosis, treatment, or clinical nutrition recommendations.
- Human roles retain approval authority: PM (delivery/scope), PO (priority/product), TL (architecture/release), QA (quality evidence).
- Stitch is the design source. Do not introduce a Figma workflow.

## Agent roster

Load the relevant TOML profile from the bundle before work:

- Management: `bundles/management/agents/*.toml`, including its own four generic 4R reviewer profiles for any-scope TL PR review.
- Development: `bundles/development/agents/*.toml`, including its own backend/frontend 4R reviewer profiles and `frontend-checker-lite`. Management includes full `frontend-checker`; use the project `review` skill for aggregate review routing.

The bundle workflow and library mappings are authoritative; do not use the retired `agents/` roster.

## Persistent memory and structure

Follow [`docs/engram-protocol.md`](docs/engram-protocol.md) exactly. For structural codebase questions, follow [`docs/codegraph-guidance.md`](docs/codegraph-guidance.md) and load `codegraph-guidance` before broad search.

## MCP safety

- Linear: read first; no priority, status, assignee or scope change without human approval.
- Neon: development branches only; no production connection, secrets or PII.
- Stitch: generated artifacts are proposals until the PO approves.
- Engram: follow `docs/engram-protocol.md`; save curated discoveries and close every session with a summary.
- CodeGraph: use `codegraph_explore` before broad filesystem exploration; never use administrative lifecycle commands during normal work.
