---
name: g16-docs-review
description: 'Checklist para encontrar las oraciones de la documentación viva de Eureka que un PR vuelve falsas: qué documentos están vivos y cuáles describen un momento fijo, cómo buscar referencias a lo que cambió y cómo reportar con la oración corregida y una severidad según quién sigue ese documento. Es el checklist que carga g16-eureka-revisor-docs.'
metadata:
  tipo: skill
  area:
  - documentacion
  - qa
  fase:
  - revision
  tecnologias:
  - agnostico
  herramientas:
  - claude-code
  requiere: []
  grupo: "16"
  autor:
    nombre: Esteban Antonijevic
    github: eantonijevic
  responsables:
  - eantonijevic
  madurez: experimental
  relacionados:
  - g16-eureka-revisor-docs
  - g04-sync-project-docs
  - g01-schema-doc-drift-auditor
---

# Eureka docs review

Eureka's docs are not decoration: people act on them. The threat model says
where each mitigation is enforced, the security pipeline says which agent looks
at what, `CONTRATOS-ACTUALIZABLES.md` and `contracts/DEPLOYMENTS.md` are
followed step by step during an upgrade, and `consistency.md` explains what to
do when a cron fails. The PR template asks for docs to be updated, but nothing
checks it.

**A stale doc is worse than a missing one**, because nobody double-checks a doc
that looks authoritative. Your job is to find the sentences this PR makes
false, not to judge the writing.

You do not review the code itself: other reviewers own correctness and
security. If the change cannot affect any doc, say so and stop.

## Which docs are living

| Doc | Describes | Usually goes stale when the PR touches |
|---|---|---|
| `docs/AGENTES.md` | Every agent and skill, when it wakes and what it checks | `.github/workflows/eureka-*.yml`, `.github/skills/`, `.claude/skills/` |
| `docs/SECURITY-PIPELINE.md` | The review layers, their scope and cost | `.github/workflows/`, `.github/instructions/`, `.github/skills/` |
| `docs/THREAT-MODEL.md` | STRIDE threats and **where each mitigation is enforced today** | New entry points (`app/api/**`), auth, keys, contracts, reviewer scope |
| `docs/CONTRATOS-ACTUALIZABLES.md` | How the UUPS upgrade works and is done | `contracts/src/`, `contracts/script/`, the registry upgrade skill |
| `contracts/DEPLOYMENTS.md` | Current addresses, blocks and implementations | `contracts/registry-deployed-commit`, `contracts/marketplace-deployed-commit`, deploy scripts |
| `docs/REGISTRO-DE-PATENTES.md` | The registration flow step by step | `app/api/mint/**`, `lib/mint/**`, `lib/server/patent/**`, `supabase/schema.sql` |
| `docs/consistency.md` | Guarantees and runbook for minting and purchases | `consistency-cron.yml`, `lib/server/consistency/**`, purchase and mint routes |
| `docs/COMPARTIR-POR-EMAIL.md` | Sharing a record by email | sharing routes and libraries |
| `docs/testing-backlog.md` | What each test covers and what is blocked | `test/**`, `contracts/test/**` |
| `README.md` | Setup, scripts and environment variables | `package.json` scripts, new env vars |

**Not living, never flag:** `docs/AUDITORIA.md` and `docs/steering/**`
describe a fixed moment (they say which commit or month). A research doc like
`docs/CRIPTOGRAFIA-POSCUANTICA.md` only goes stale if the PR changes the
algorithms it says are in use.

The table is a starting point, not the whole map. For each changed file, Grep
`docs/`, `README.md` and `contracts/DEPLOYMENTS.md` for:

- its path and its file name;
- the route it serves (`/api/mint/reserve`), for files under `app/api/`;
- every function, SQL function, table, column, status, event, env var,
  workflow name or agent name the diff adds, removes or renames.

Then read each passage you found and decide whether it is still true.

## What counts as a finding

- **A sentence that is now false.** A route that no longer exists, a status
  that was renamed, a step in a procedure that changed order, an agent whose
  `paths` changed, an address that is no longer current.
- **A mitigation that moved.** The threat model says a check is enforced in a
  place the PR removes or moves it from.
- **A new thing a living doc lists exhaustively and now misses.** A new agent
  not in the AGENTES.md table, a new entry point that changes the threat model's
  attack surface, a new env var the README setup needs.

Not a finding: a doc that could say more, wording, typos, a doc that never
mentioned the thing, or a doc the PR already updated correctly. If the PR
updates a doc, check the update instead of the old text.

## How to report

- Anchor each comment to the changed line **in the code** that makes the doc
  wrong (the doc line is usually not in the diff). Quote the doc sentence and
  give the doc's path and section.
- One comment per finding, at most five per PR: keep the ones people will act
  on. If there are more, say so in the last one.
- Open each with a severity tag:
  - `[Alto]` — a security doc (`THREAT-MODEL.md`, `SECURITY-PIPELINE.md`) or a
    procedure people follow (`CONTRATOS-ACTUALIZABLES.md`, `DEPLOYMENTS.md`,
    the runbook in `consistency.md`) now says something false.
  - `[Medio]` — any other living doc now says something false.
  - `[Bajo]` — a list a doc keeps exhaustive now misses the new thing.
- Propose the corrected sentence, ready to paste.
- If you are not sure the doc is wrong, say what you would need to check.
- If nothing is stale, say so in a single comment.

## Ejemplo de uso

**Pedido:** «Con la skill de docs, decime qué documentos deja desactualizados este PR que mueve la ruta `/api/mint/release`.»

**Resultado:** Busca la ruta y el archivo en `docs/`, el README y `contracts/DEPLOYMENTS.md`, cita cada oración que quedó falsa con su documento y sección, le pone `[Alto]`, `[Medio]` o `[Bajo]` y propone la oración corregida. No marca la auditoría ni los steerings.
