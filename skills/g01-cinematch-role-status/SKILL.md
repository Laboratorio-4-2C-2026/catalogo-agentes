---
name: g01-cinematch-role-status
description: "Arma un reporte de estado de Cinematch pensado para un rol (PM, PO, Tech Lead, QA, dev o la cátedra), a partir de las notas de PM del vault, Linear y los PRs de GitHub. Usala cuando alguien pregunta cómo viene el proyecto o qué debería mirar o hacer hoy desde su rol; es de solo lectura."
author: Francisco
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - revision
  tecnologias:
  - python
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - linear
  - github
  grupo: "01"
  autor:
    nombre: Francisco Zizzi
    github: FranciscoZizzi
  responsables:
  - FranciscoZizzi
  madurez: probado
  relacionados:
  - g01-cinematch-pm-weekly
  - g01-cinematch-issue-management
---
# Cinematch status by role

One snapshot of the project, cut for the person reading it. Every role sees the same facts; what changes is which facts lead and which actions are theirs. The failure this skill prevents is a status repeated from the last note: the notes are history, Linear and GitHub are the present, and the report says which is which.

Notes and reports follow [AGENTS.md](../../../AGENTS.md): the report is in Spanish, with absolute dates. This skill is in English.

Read-only: it writes to no source, comments on nothing, moves no issue. A mismatch is reported with who should fix it ([Fuentes de Contexto](../../../Fuentes%20de%20Contexto.md) says who owns what).

## 1. Pin the role

Take the role from the request. Without one, ask for it (offering the roles in section 4) before reading anything, since the role decides what to dig into. Map aliases (product owner → PO, desarrollador / dev → Dev, profes / docentes / stakeholder → Cátedra). An unknown role gets the closest lens, named as such in the report.

## 2. Gather, all fresh

Run these in parallel. `pm.py` is `python3 ../g01-cinematch-pm-weekly/scripts/pm.py` from this skill's folder (`python` on Windows); if it fails, run its `doctor` and follow that skill's setup.

- **Where we are**: `pm.py calendar`. Say which numbering you quote (Tablero Sem-NN, TODO Semana N, gantt W, EVM P).
- **PM notes**: the newest control in `Seguimiento PM/` (by the date in the file name) including its `Actualización` sections, plus any newer note there; `TODO/TODO <Role>.md` (PM, PO, QA, Tech Lead) at its current `# Semana N` section and `# Sin semana`; `TODO/TODO General.md` open items. Dev and Cátedra have no TODO file: read the PM and Tech Lead ones.
- **Linear** (MCP, team `CIN`): `list_issues` with `fields: ["title","status","assignee","estimate","labels","dueDate","updatedAt"]`, `limit: 250`, paginating while `hasNextPage`. If the MCP only offers `authenticate`, ask the person to run `/mcp` and stop; a report without Linear is not this report.
- **GitHub**: `pm.py prs --since <date of the newest control note>` and `pm.py blockers`.

Done when every source above is read and you hold the time each was read.

## 3. Reconcile

The note is the claim, the live source is the check. For every fact the newest note states about an issue or a PR, compare it with Linear and `prs`; when they disagree the live source wins and the report says the note is stale. Then the cross-checks every role needs:

- **Done in Linear without a merged PR**: not delivered.
- **Open in Linear with a merged PR**: delivered, status stale (the PO fixes it).
- **Due date passed and not Done**: late.
- **Merged PR without an issue key**: work outside the plan.
- **Stacked PRs and merge order**: take them from `blockers`, never infer them.

Done when every claim in the newest note is confirmed, superseded or marked unverifiable.

## 4. Apply the lens

Each role leads with its own block and gets only the actions it owns.

| Role | Leads with | Its actions |
|---|---|---|
| PM | Schedule against the next milestone, late issues, open incidents, KPI days, what the Tablero will need. | Escalations, the weekly control (point to cinematch-pm-weekly), chasing owners. |
| PO | Linear statuses that contradict GitHub, issues missing for the upcoming weeks, scope per module, unassigned or unestimated issues. | Fix statuses, create or reorder issues (point to cinematch-issue-management). |
| Tech Lead | PRs stuck in review, merge conflicts, stacked PRs and their merge order, failing CI, technical decisions pending in the notes. | Reviews to do, merges in order, decisions to close. |
| QA | Merged work without tests, end-to-end coverage of the critical path, failing checks, bugs opened. | What to test before the milestone, CI gaps. |
| Dev | Their assigned issues (ask for their name if not given) and their PRs' state, what blocks them, what is due this Thursday. | Answer reviews, rebase, push. |
| Cátedra | Progress against the milestone, what is delivered vs. planned, risks, without internal tooling detail. | None: this is an outward summary. Quote numbers only as the notes and [Medición del avance](../../../Cronograma/Medicion%20del%20avance.md) define them. |

## 5. Report

In chat, in Spanish, short enough to read in two minutes:

1. **Encabezado**: role, date and time read, calendar line.
2. **En 3 líneas**: the three facts that matter most for this role.
3. **Lo que te toca**: the role's actions, each with its issue or PR and the date it is due.
4. **Estado**: the role's lead block, then anything else that changes its picture.
5. **Notas desactualizadas**: each note claim the live sources superseded, with the link to the note.
6. **Fuentes**: what was read and when.

Each fact carries its evidence (`CIN-NN`, `#NN`, or the note link). Write the report to `Seguimiento PM/` only when asked, as `<yyyy-mm-dd> Estado para <rol>.md` with the vault's frontmatter (`description`, `author`).

## Ejemplo de uso

**Pedido:** Soy el Tech Lead, ¿cómo venimos?

**Resultado:** Lee las notas del vault, Linear y los PRs abiertos y devuelve en español un estado del proyecto ordenado para el Tech Lead, con las acciones que le tocan y las diferencias entre fuentes con su responsable, sin modificar nada.
