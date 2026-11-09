---
name: g02-multica-guide
description: Guía para conectarse a Multica y usar su CLI en el proyecto Zest, con instalación, login, comandos de todos los días y convenciones de tickets. Usar cuando alguien del equipo o un agente necesita leer, crear o mover tickets de Zest.
metadata:
  tipo: skill
  area:
  - gestion
  - documentacion
  fase:
  - planificacion
  - mantenimiento
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - multica
  grupo: '02'
  autor:
    nombre: Luz Laura
    github: luzlaura
  responsables:
  - luzlaura
  madurez: usado-en-proyecto
  relacionados:
  - g02-zest-ticket-format
---
# Multica — project tracking

Zest's tickets live in [Multica](https://multica.ai), not GitHub Issues. This file explains what Multica is, how to connect to it, and the conventions this project uses for tickets.

## What is Multica

Multica is a project/issue tracker with both a web UI and a CLI (`multica`). The CLI is how an AI agent (or a human from the terminal) reads and creates tickets without leaving the repo.

- Workspace: **Zest** (slug `zest`, id `64e615d4-aa77-44b1-819e-cf3983db5331`)
- Board: **Zest** project (id `a4cea3ee-7bd0-4cd4-af8c-fd133b41eba5`)
- Web: https://multica.ai/zest/projects/a4cea3ee-7bd0-4cd4-af8c-fd133b41eba5

## Connecting the CLI

1. Install it (Homebrew tap):
   ```
   brew install multica-ai/tap/multica
   ```
2. Authenticate and pick up your workspaces automatically:
   ```
   multica login
   ```
   This opens a browser for OAuth. On an SSH-only box without browser access, `multica setup cloud` walks through the same flow with a token instead (`multica login --token`).
3. Point the CLI at this project's workspace by default:
   ```
   multica workspace switch zest
   ```
   Check it worked with `multica auth status`.

Once connected, no need to pass `--workspace-id` on every command — it defaults to whatever `workspace switch` set (or `MULTICA_WORKSPACE_ID` if you export it).

Ask an existing member (owner: igassiebayle) to invite you to the `zest` workspace if `multica login` doesn't show it — the CLI only discovers workspaces you already have access to.

## Everyday commands

```
# See what's on the board
multica issue list --project a4cea3ee-7bd0-4cd4-af8c-fd133b41eba5

# Filter by status or label
multica issue list --project a4cea3ee-7bd0-4cd4-af8c-fd133b41eba5 --status in_review
multica issue list --project a4cea3ee-7bd0-4cd4-af8c-fd133b41eba5 --assignee <name>

# Read one ticket
multica issue get ZEST-12

# Create a ticket
multica issue create --project a4cea3ee-7bd0-4cd4-af8c-fd133b41eba5 \
  --title "Short imperative title" \
  --description "..." \
  --status backlog

# Move it along
multica issue status ZEST-90 in_progress
multica issue assign ZEST-90 --assignee <name>
```

Add `--output json` to any read command if you need to script against it.

## Conventions used in this project

- **Identifiers**: `ZEST-<n>`, assigned automatically on create — don't invent your own numbering.
- **Statuses**: `backlog` → `in_progress` → `in_review` → `done`. A ticket sits in `in_review` until someone reviews the PR/work it corresponds to, not just when the code is written.
- **Labels**: `frontend`, `backend`, `infra` (see `multica label list`). Apply the ones that match; a ticket spanning both frontend and backend gets both labels rather than being split.
- **Description format**: existing tickets use a short one-line summary, then `**Tareas**` (bullet checklist of concrete steps) and `**Criterios de aceptación**` (bullet checklist of what "done" means) sections written in Spanish, matching the rest of the team's docs. Follow that shape for new tickets — see `multica issue get ZEST-77` for a real example.
- **Sub-issues / parents**: bigger tickets (like the CD/infra work) are filed as sub-issues under a parent epic via `--parent <id>`. Check whether a new ticket belongs under an existing parent before creating it standalone.

## What NOT to do

- Don't create a ticket without checking `multica issue list` first for an existing/duplicate one (`issue create` will warn on an active duplicate — don't `--allow-duplicate` past that warning without a reason).
- Don't put secrets or credentials in a ticket description — same rule as the repo itself (see `AGENTS.md`).
- Don't skip straight to `done` — leave it in `in_review` so someone else actually looks at the change.

## Ejemplo de uso
**Pedido:** ¿Cómo veo los tickets de Zest que están en revisión desde la terminal?
**Resultado:** Indica cómo conectar la CLI si hace falta y da el comando `multica issue list` con el proyecto de Zest y `--status in_review`.
