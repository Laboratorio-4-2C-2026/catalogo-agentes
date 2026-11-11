---
name: g01-cinematch-pm-weekly
description: "Control semanal del PM de Cinematch: exporta de Drive el Tablero de estado, el EVM y el gantt con rclone, lista lo que falta o no cierra en la semana del Tablero, cruza Linear con lo mergeado en GitHub, actualiza el valor ganado y propone cada semáforo con su evidencia para que el PM lo cargue a mano. Usala cuando el PM pregunta qué cargar esta semana, cómo viene el proyecto, si Linear coincide con lo mergeado o cómo va el reporte de KPIs; es de solo lectura sobre todas las fuentes."
author: Tomás
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
  - revision
  tecnologias:
  - python
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - google-drive
  - linear
  - github
  grupo: "01"
  autor:
    nombre: Tomás Roldán Borjas
    github: TomRolB
  responsables:
  - TomRolB
  madurez: usado-en-proyecto
  relacionados:
  - g01-cinematch-kpi-watch
  - g01-cinematch-steering-evm
  - g01-cinematch-pr-blockers
  - g01-cinematch-baseline-change
  - g01-checkpoint-reconciler
  - g10-weekly-sheet-checker
  - g02-status-report-format
---
# Cinematch PM weekly control

The Tablero is the project's weekly status report. This skill keeps it current and grounded: every value it proposes comes with the evidence behind it, taken from the source that rules over it, so colors, percentages and dates reflect the week that just closed.

Notes you write are in Spanish. This skill is in English.

## 0. Never write to a source

This skill reads Drive, Linear, GitHub and the KPI platform, and writes to none of them.

- **Drive** is exported with a read-only rclone remote. The PM types the values into the Tablero by hand: proposing them is the job, entering them is not.
- **Linear** mismatches are reported, never fixed. Changing issues is the PO's job, and silently "correcting" the tracker hides exactly what the report should show.
- **The app repository** is read with `gh`, never written: the management team does not commit code.
- **Exports never go into this vault.** The Tablero holds every team's tab, and the vault syncs itself to GitHub. Export into a scratch folder outside it (in Claude Code, the session scratchpad). Do not quote other teams' tabs anywhere.

## 1. What the PM owns

The PM's responsibilities, as given in class:

- **The Tablero, every week** (class of 20-08: "completar una planilla de avance todas las semanas"), tab of our team only.
- **Earned value**, in the team's EVM workbook (class of 27-08), and its slides at each Steering.
- **That every role does its job** (class of 13-08), plus the mandatory weekly internal session.
- **ADRs and change control**: a challenge is a scope change with its impact on scope, schedule and cost, as the team's ADR for the KPI challenge did.
- **The pendientes** in `TODO/TODO PM.md` and the unowned ones in `TODO/TODO General.md`.

## 2. Setup, once per person

Run `python <this skill's folder>/scripts/pm.py doctor` (`python3` on macOS and Linux). It checks openpyxl, timezone data, rclone with a Google Drive remote, and `gh`. For anything marked MISSING, follow [references/setup.md](references/setup.md). rclone's configuration is interactive, so the person runs it in their own terminal; walk them through the prompts.

Linear comes through the Linear MCP inside Claude Code, which the script cannot check. If the MCP only offers `authenticate`, ask the person to run `/mcp`. Do not fall back to anything else.

## 3. The weekly run

All commands are `python <this skill's folder>/scripts/pm.py <command>`. Every one accepts `--help`, and the date-dependent ones take `--as-of YYYY-MM-DD`.

1. **`calendar`** says where we are in each of the four numberings, which never agree: the Tablero's Monday columns, the TODO files' Thursday weeks, the gantt weeks and the EVM periods. Use the numbering of whichever document you are talking about, and say which one.
2. **`fetch <scratch folder>`** exports the Tablero, both EVM workbooks and the gantt.
3. **`tablero <scratch folder>`** shows the last four weeks and lists every gap. Each column is headed by its report Monday and is filled once the development week closes. The gaps it finds: unloaded areas, a General that breaks the rule, yellows without Motivo or Acción, dates already past, deviations that do not match their dates, incidents past their limit, fields never filled, and any cell of a template formula (Desvío, Vencido) replaced by a typed value or another formula.
4. **Gather the evidence** for this week (section 4): Linear through the MCP, `prs --since <last report date>`, `kpis`, `evm`, and `gantt --ids` for the earned value.
5. **Propose** what to type, as one table per Tablero block, each value with its tab and cell and its evidence; the workbooks are large, and a value without its cell leaves the PM searching. `evm` prints the input cell of every period still missing and checks the cut cell. Section 5 says how to choose the colors; [references/tablero.md](references/tablero.md) explains every field.
6. **After the PM types it in, `fetch` into a new folder and run `diff <earlier folder> <new folder>`**: it lists every cell that changed, formulas included, in our Tablero tab and the team workbooks. Then run `tablero` and `evm` on the new folder and confirm the gaps are gone. The export is the only proof that the Sheet says what was agreed.
7. **Record what came out of it.** The week's control goes into `Seguimiento PM/` as `<yyyy-mm-dd> Control semanal Sem-NN.md`. A new pendiente goes into `TODO/TODO PM.md` under the current `# Semana N (dd/mm)` section, and a decision into `Decisiones Técnicas.md`. A baseline change found or approved this week is recorded with [g01-cinematch-baseline-change](../g01-cinematch-baseline-change/SKILL.md).

## 4. Evidence and cross-checks

Each source is checked against the others, because each one drifts in its own way.

**Linear against GitHub** (`prs` groups pull requests by issue key):
- **Done without a merged PR**: not delivered. A stacked PR can close when its base merges, and Linear then marks the issue Done with the code off `main`.
- **Todo or In Progress with a merged PR**: delivered, status stale.
- **Due date passed and not Done**: late. The due date is the week's Thursday.
- **Merged PRs without an issue key**: work outside the plan. It costs actual cost and earns no value.

What is still open in review, while a nudge can still move it, is the job of [g01-cinematch-pr-blockers](../g01-cinematch-pr-blockers/SKILL.md) (`blockers`), which also gives the merge order of stacked PRs before anyone merges them.

**The Tablero's activities against Linear.** Each "Actividad clave" is a module. Its Avance is the share of its baseline points already closed, not a guess. Each module is a Linear label with the same name as the Tablero row, all in one label group. Two traps:
- **Not every issue carries its module label.** An issue created after the gantt can lack the label and still belong to a module. Count by the gantt's points and epic, using the label only to find the issues.
- **Scope with no issue yet still counts as pending.** A gantt task not yet created in Linear keeps the module below 100%.

An activity whose baseline issues all closed is Finaliz., and its F. Fin Real is the last merge (from `prs`), not the day someone moved the card. **A F. Fin L. Base never moves without a baseline change**: if it differs from the gantt or from an earlier export, flag it.

**Earned value.** Follow [references/evm.md](references/evm.md). In short: the EV of a period is the gantt points of the baseline issues closed in it (`gantt --ids`), the AC is 18 HH, and both go into the team workbook.

**KPIs.** `kpis` gives the grade per reception day. A day with nothing received is lost for good: it is an incident. A catalog smaller than what the ADR promised caps the grade below 10, and that is a risk until fixed. The `data` branch lags the platform; the live state is on the platform's "Mi equipo" page, which only someone with the team key can open. Today's delivery, while it can still be saved, is the job of [g01-cinematch-kpi-watch](../g01-cinematch-kpi-watch/SKILL.md), which reads each run's artifact for same-day proof.

**Steerings.** The budget, EVM and S-curve slides are built with [g01-cinematch-steering-evm](../g01-cinematch-steering-evm/SKILL.md), from the same workbook this control keeps up to date.

**Calendar.** `calendar` lists the next milestones. A challenge or a Steering within two weeks belongs in Riesgos.

## 5. Choosing the colors

The Tablero's own criteria, from the sheet: Verde, no inconvenientes; Amarillo, situations that can lead to deviations; Rojo, critical situations already causing deviations. General is not chosen: it follows from the five areas by the rule on the RESUMEN tab (Rojo with one red or three yellows, Amarillo with one yellow).

What each area looks at:

| Area | Signals |
|---|---|
| Alcance | Baseline changes, challenges, scope cut or added, work merged outside the plan |
| Cronograma | SPI of the closed period, activities past their baseline date, Linear issues past their due date |
| Incidentes | Open incidents and their criticidad, KPI days lost, blocked developers |
| Calidad | CI success rate, bugs opened, review rework, production availability from the KPIs |
| Riesgos | Risks that moved or materialized, upcoming challenges |

Two things that look like signals and are not:
- **A gantt task with no Linear issue before its week.** Issues are created close to the Thursday they are due, so a missing issue is late only once that Thursday passes.
- **A F. Fin Estimado in the past.** It is the forecast, meant to move: propose the new date. The Desvío stays empty until the activity finishes (the template only computes it from the F. Fin Real, see [references/tablero.md](references/tablero.md)).

Two rules for the proposal:
- **Criticidad follows its definition**: Alta means escalating to the professors, Media means the team is handling it.
- **A green needs the same evidence as a yellow.** An area that has not changed in many weeks is checked against what actually happened in them.

Every yellow or red needs its Motivo and Acción tomada, written as cause and concrete action, in Spanish. Propose them; the PM decides the final wording.

## 6. When something does not fit

- **The script stops with "Label ... not found"**: the cátedra changed the sheet. Read the export, adapt the parser in `scripts/pm_weekly/spreadsheets/`, and say what changed.
- **rclone fails on authentication**: its shared Google client is being retired during 2026. The fix is an own OAuth client, in [references/setup.md](references/setup.md#own-client-id).
- **A number disagrees with a Steering slide**: the slide is history; recompute from the sources and say which base each number uses.

Project constants (file and sheet names, repositories, the KPI workflow, calendar anchors) live in [project.json](project.json). Change them there, never in the code. The Drive folder id and the KPI project id come from environment variables instead ([references/setup.md](references/setup.md#environment-variables)). The script in `scripts/` also serves [g01-cinematch-kpi-watch](../g01-cinematch-kpi-watch/SKILL.md) (`kpi-watch`), [g01-cinematch-steering-evm](../g01-cinematch-steering-evm/SKILL.md) (`steering`) and [g01-cinematch-pr-blockers](../g01-cinematch-pr-blockers/SKILL.md) (`blockers`), so a change to it can affect them.

## Ejemplo de uso

**Pedido:** Soy el PM, ¿qué tengo que cargar en el Tablero esta semana?

**Resultado:** Exporta el Tablero, los workbooks de EVM y el gantt a una carpeta temporal, lista los huecos de la semana y propone, bloque por bloque, cada valor con su pestaña, su celda y su evidencia (Linear, PRs mergeados, KPIs, valor ganado), sin escribir nada en el Sheet.
