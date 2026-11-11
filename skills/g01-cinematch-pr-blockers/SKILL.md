---
name: g01-cinematch-pr-blockers
description: "Encuentra qué está trabado entre los pull requests abiertos del repo de Cinematch y main, y quién tiene que actuar hoy: reviews pendientes, cambios pedidos sin respuesta, aprobados sin mergear, PRs apilados sobre la rama de otro PR, conflictos, checks fallidos y estados de Linear que contradicen al PR. Usala para el seguimiento diario con los devs, cuando nada se mergea o para decidir si escalar un incidente; es de solo lectura y nunca comenta, aprueba ni mergea."
author: Tomás
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - revision
  tecnologias:
  - python
  - git
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  - linear
  grupo: "01"
  autor:
    nombre: Tomás Roldán Borjas
    github: TomRolB
  responsables:
  - TomRolB
  madurez: experimental
  relacionados:
  - g01-cinematch-pm-weekly
  - g01-cinematch-kpi-watch
  - g02-stacked-pr-guard
  - g10-blocker-detector
---
# Cinematch PR blockers

Earned value only counts when a baseline issue is merged and Done ([evm.md](../g01-cinematch-pm-weekly/references/evm.md)). Work sitting in review costs actual cost every period and earns nothing, and the weekly control ([g01-cinematch-pm-weekly](../g01-cinematch-pm-weekly/SKILL.md)) only sees it after the period has closed. This skill looks at the open pull requests today, while a nudge can still move them, the way [g01-cinematch-kpi-watch](../g01-cinematch-kpi-watch/SKILL.md) looks at today's KPIs.

Notes you write are in Spanish. This skill is in English.

## 0. Never write to a source

This skill reads the app repository and Linear, and writes to neither. It never comments on a pull request, requests a review, approves, merges, retargets or closes one, and never changes a Linear issue. The management team does not commit to the app repository. The follow-up reaches each person from the PM, outside the repository. Linear mismatches are listed for the PO, who owns the tracker.

## 1. Run it

```
python ../g01-cinematch-pm-weekly/scripts/pm.py blockers
```

The script is shared with `g01-cinematch-pm-weekly`, which also sets it up: run its `doctor` once. `gh` needs read access to the app repository ([project.json](../g01-cinematch-pm-weekly/project.json)). Linear comes through the Linear MCP (section 3).

**When.** Once a day, in the afternoon, so the morning's pushes and reviews are in. Run it daily from the moment a PR goes over a limit until it merges, and on the day before an issue's due date.

## 2. What it reports

Open pull requests that are not drafts are grouped by who has to act, oldest wait first. `OVER` marks a wait past its limit.

| Group | State | Measured from | Limit | Who acts |
|---|---|---|---|---|
| Waiting on a merge | Approved | The latest approval | 24 h | A developer or a repository admin |
| Waiting on the author | Changes requested, no commit since | The latest change request | 48 h | The author |
| Waiting on a reviewer | No decision yet | The later of opening and the last commit | 48 h | The requested reviewer |
| Waiting on a reviewer | Changes requested, commits pushed after it | The last commit | 48 h | The reviewer who asked for changes |

48 h is the review threshold of the blocker detector in the cátedra's list of agents. An approved PR gets a single day because a merge is all it needs, and only the merge earns value.

**Before merging** lists what breaks a merge even when the review is done:

- **A PR stacked on another PR's branch.** Its base is not `main`. Merged first, its code lands on the other branch instead of `main`, and Linear can still mark its issue Done. The script gives the safe order: merge the base PR, retarget this one to `main`, then merge it. When the base branch has no open PR, the PR must be retargeted before anything else.
- **Merge conflicts** with the base branch: the author resolves them.
- **Failing checks** on the last commit: the author fixes them before anyone reviews again.

**Drafts** are listed and never followed up: the author has not asked for review yet.

## 3. Cross-check with Linear

Through the Linear MCP, read the issues the script names plus every issue In Progress or In Review, and compare:

| Linear says | The PR says | Reading |
|---|---|---|
| In Review | Waiting on the author | The status overstates progress: the work is back with the developer |
| Todo or In Progress | Approved | Status stale; the work is a merge away |
| Done | Still open, or merged into a branch other than `main` | Not delivered: no earned value |
| In Progress, due date within two days or past | No PR at all | Ask how the work is going; work not yet in a PR cannot be reviewed in time |
| Any state but Done, due date past | Anything | Late. The due date is the week's Thursday |

Every mismatch goes on the list for the PO, never into Linear.

## 4. Turn it into the follow-up

Write one short message per person who has to act, for the PM to send through the team's usual channel: the PR, what it needs, and how long it has waited. Order them by what earns value soonest:

1. **Approved PRs**: a merge takes minutes and delivers the work right away.
2. **Requested changes without an answer**: they hold the issue until the author replies.
3. **Reviews and re-reviews**: they hold the author.

Stacked PRs go in the message to whoever merges, with the order spelled out. In notes, name people by role, never by GitHub user, so the note still reads right for someone who joins later.

## 5. Record it

- **Nothing over its limit**: no note.
- **Something over its limit**: add an `## Actualización del dd-mm` section to the current week's control in `Seguimiento PM/`, with what moved since the last check and the follow-up sent. Do not restate the whole queue.
- **A PR still over its limit at the next check**: propose an incident in the Tablero's Incidentes block, Criticidad Media (the team is handling it), with a F. Límite. If the limit arrives and the same PRs are still stuck, propose Alta, which means escalating to the professors ([tablero.md](../g01-cinematch-pm-weekly/references/tablero.md)). The PM decides both.
- **The weekly control** reads the same evidence for Cronograma (issues past their due date, a period closing without earned value) and Incidentes (the open incident).

What never goes to Riesgos: a stacked PR or a merge order is a procedure to follow, not a project risk, and a PR already late is a deviation that Cronograma shows, not a risk.

## 6. Things that look wrong and are not

- **A PR still approved after the author pushed again.** The script follows GitHub's own decision: the approval stands unless the repository dismisses stale approvals, and then the PR waits on a reviewer.
- **A long wait on a reviewer after the author replied with comments only.** The script cannot see replies in comments, only commits. Open the PR before following up with the reviewer.
- **The last commit is older than the push.** The time comes from the commit itself: a rebase updates it, but pushing an old commit does not.
- **An approved PR with unresolved threads.** GitHub lets it merge and the script does not count threads; the reviewer decides whether they block.
- **The listing fails with a GraphQL node limit.** Each PR costs about 10,000 nodes. Keep `--limit` under 48; the default is 30.

## Ejemplo de uso

**Pedido:** ¿Qué PRs están trabados hoy y a quién le tengo que escribir?

**Resultado:** Lista los PRs abiertos agrupados por quién tiene que actuar, marca los que pasaron su límite, da el orden seguro de merge de los PRs apilados, lista para el PO los estados de Linear que contradicen al PR y redacta un mensaje corto por persona, ordenado por lo que gana valor antes.
