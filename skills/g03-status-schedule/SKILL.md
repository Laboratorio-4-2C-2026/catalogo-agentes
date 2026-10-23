---
name: g03-status-schedule
description: Actualiza el cronograma de la planilla de estado semanal del equipo (estado, avance, fechas y comentarios por épica) a partir de evidencia real de Jira, git y PRs. Usar cuando el PM pide actualizar avances, fechas o atrasos de la semana.
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  - codex
  requiere:
  - jira
  - github
  - google-sheets
  grupo: '03'
  autor:
    nombre: Julieta Iglesias
    github: JuliIglesias
  responsables:
  - JuliIglesias
  madurez: usado-en-proyecto
  relacionados: []
---
# Schedule update for the status sheet

Each row of "Actividades Clave" is one **Jira epic**. This skill recomputes its progress and dates from Jira and the repos and writes them back, without moving the baseline. The cells it fills are `Estado`, `Avance [%]`, `F. Fin L. Base` (only when empty), `F. Fin Estimado`, `F. Fin Real` (only when the epic is complete) and `Comentarios`; `F. Fin L. Base` is filled once from Jira (only when empty) and `Desvío` is calculated by the sheet.

## Rules for the numbers

- **Avance [%]** = `epic children with status Finalizada ÷ total children of the epic`, rounded to a whole percent. Count *every* child ticket (stories, tasks, bugs), including `[INT-n]` integration tickets; do not count the epic itself. Verified against the sheet: Módulo de Gastos = 14 of 20 = 70%. Do not mix in subjective progress.
- **Cross-check Jira against git before counting.** A ticket marked `Finalizada` whose PR is not merged in `develop`, or a ticket "En revisión" that is already merged, is a discrepancy: use the real state and say so in `Comentarios`.
- **Estado**: `Finaliz.` only when all children are `Finalizada` (100%); `En curso` when any child is started or the epic's sprint is running; empty if not started.
- **F. Fin L. Base**: fill it for **every epic row**, including future ones, with the epic's due date in Jira (the original plan). Only fill it when the cell is empty; **never overwrite a base that is already filled**, even if it differs from Jira — flag the mismatch instead.
- **F. Fin Estimado**: fill it for **every epic row too**, never leave it empty when a base exists. Estimate at the team's real pace, not at the plan: take the slip of the epics that already closed or are forecast (`F. Fin Real` or `F. Fin Estimado` minus `F. Fin L. Base`, ignoring outliers caused by a typo or a deliberate re-plan) and add the typical slip to the base of the open and future epics. With the data of 02/10 the typical slip is 7 days (Disponibilidad, Asistencia and Gastos), so estimate = base + 7 days. Re-compute it every week as more epics close, and for an epic already in progress use the remaining non-backlog work and open PRs instead of the generic slip. If the epic already has an estimate, only change it with evidence and say so in `Comentarios`. **Hard ceiling: no estimated date can be later than 12/11/26, the day of the final presentation.** If the pace-based estimate falls after it, write 12/11/26 and report it as an epic with no slack left (it will show up as a risk once it is `En curso` or `En revisión`; backlog epics are not cited in the sheet). Always tell the PM in the reply which method you used.
- **F. Fin Real**: the date the last child ticket was merged/resolved. Only when the epic is 100%.
- **Desvío [+/-días]** is a **formula of the sheet: never write it** (do not overwrite or retype the cell). It is computed from the dates you fill: `F. Fin L. Base − F. Fin Real` (or `− F. Fin Estimado` while the epic is open); negative = late, positive = early. Use it only to read the result (e.g. Set Up de Infraestructura base 21/08, real 16/09 → −26) and to report delays.
- **Comentarios = alerts only, not a log.** Do **not** narrate which PRs were merged or which tickets are still pending: progress lives in `Avance [%]` and the weekly Motivo/Acción, and a daily log turns the cell into an unreadable wall of text. Add a short `dd/mm: ...` line only for something that should jump out to the reader, for example:
  - a PR left without review for many days, or approved but blocked (merge conflicts, failing CI, requested changes not applied yet);
  - Jira contradicting the code (`Finalizada` with no PR or not merged, `En revisión` with no PR/branch, `En revisión` already merged);
  - a ticket added to the epic outside the original plan, or a merge with no ticket;
  - an estimate that slipped or is due today, and why (also move-the-estimate notes required by `F. Fin Estimado`);
  - a risk from the Riesgos row that hits this epic.
  Keep 1–3 lines per epic; if nothing surprising happened, add nothing. Facts, ticket keys, numbers; no adjectives. When an epic closes, it is fine to condense its comment to one line on what delayed it.
- **Average status of tasks**: also report the distribution across the project's tickets (Finalizada / En revisión / En curso / This week / sin asignar) as a summary line for the PM; it is for the reply and the weekly report, not a cell, unless the PM asks for one.

## Procedure

1. **Read our tab** (current %, dates, comments, past weeks' colours) and the template of one or two other teams' tabs if the PM wants a comparison. Never edit other tabs.
2. **Pull Jira**: all epics and their children with status, assignee, due date, sprint, `updated`. Page through results — the project has ~150 issues and the tool may truncate; save to file and process with a script if needed.
3. **Pull git/PR/CI** (read-only): merged PRs per ticket key since the last report, open PRs and how long they have been open, and for integration epics whether the real repositories exist or the app still uses fakes.
4. **Compute** per epic: %, estado, whether it is overdue (due date in the past and not Finalizada), remaining tickets, next milestone. Build the diff (cell → old → new) for the cells you are allowed to fill.
5. **Cronograma colour** for the week: Verde = every open epic on or before its estimated date; Amarillo = any epic overdue vs base but with a credible estimate, or a milestone within 2 weeks that depends on unfinished work; Rojo = an estimate already blown with no new date, or a delivery that will not be met. Read the calculated `Desvío` to quantify it. Write the `Sem-NN:` line in Motivo (what is late, by how many days, why — with keys) and Acción (done vs `(propuesta)`).
6. **Flag, don't fix**, inconsistencies — including, for every epic, whether the sheet's `F. Fin L. Base` equals the epic's due date in Jira (and whether the epic has a base at all). A mismatch usually means a typo or a re-plan and it changes the calculated `Desvío`, so report both dates and let the PM decide; never edit the base yourself. Also: a % in the sheet that differs from the count, estimated dates already past, tickets with no assignee or due date, epics whose Jira status contradicts the code.

## Output to the PM

Reply in Spanish: a table per epic (% old → new, estado, estimado, and the sheet's calculated desvío as read-only information), the Cronograma colour with its reason, the Motivo/Acción lines, the Jira status distribution, and the list of discrepancies for the PM to decide. Write the cells directly (standing authorisation) and report what changed.

## The status sheet (shared by the three `status-*` skills)

The weekly status board is a Google Sheet ("Tablero Estado Proyecto", id `1tA2CFxUesISCr39-MmhhdxwmitZKZBhTdOjfpSGjCec`, shared as editable by link). Every team has its own tab; ours is **`Equipo 03`** (Planify). If the PM names a different sheet or tab, use theirs.

**Hard rules**
1. **Only write to our own team tab.** The other `Equipo NN` tabs are read-only examples of how other teams fill the board. `RESUMEN` is formula-driven: never edit it.
2. **`planify-mobile` and `planify-backend` are read-only.** Never edit, commit, branch, push, merge or open PRs there. Inspect with `git log`, `git show <ref>:<path>`, `git ls-tree`, `gh pr list`, `gh run list`. No `git checkout`.
3. **Facts first, then judgement, and label which is which.** Every line written to the sheet must trace to Jira, git history, PRs, CI runs, or something the PM told you. If it is your proposal rather than something that happened, write it as "(propuesta)". Never invent dates, owners or causes. If a field has no real value (e.g. a due date nobody set), leave it empty.
4. **Do not move a status colour the team already reported without saying so.** If the evidence suggests a different colour, either change it and state that in your reply, or leave it and recommend the change. Never do it silently.
5. **Append, never overwrite** the history in the Motivo / Acción / Comentarios cells: each week adds a line prefixed `Sem-NN:` under the existing ones. (In this skill, the cronograma `Comentarios` follow the alerts-only rule above: append only alerts, and condense a cell when the PM asks.)
6. **The weekly status matrix takes only the colour.** Each cell of `General / Alcance / Cronograma / Incidentes / Calidad / Riesgos` gets exactly `Verde`, `Amarillo` or `Rojo` — no text, no notes, no dates. The explanation goes in `Motivo` / `Acción tomada` (columns V and W). `General` is calculated: never write it.
7. **Standing authorisation: write directly, report afterwards.** The PM has authorised these skills to write to our tab without asking first. After writing, re-read the cells to confirm they saved and report what changed (cell → old → new) plus anything you decided on judgement (a colour, an estimated date, a criticidad). Stop and ask only if the change would touch another team's tab, a baseline date, or a cell you cannot identify with certainty.

**Backlog is out of scope for risks and delays.** Tickets in Jira status `This week` or `Tareas por hacer` (category "Por hacer") are backlog, even when they carry a sprint and a due date. They are **not** evidence of risk, overload, unassigned work or delay: do not count them as overdue, as load per developer, or as "no responsible", and do not cite them in Motivo/Acción/Comentarios. Only started work counts: `En curso`, `En revisión`, and what is already merged. The one exception is the `Avance [%]` calculation, where backlog children stay in the denominator (progress = Finalizada ÷ all children). If a backlog ticket becomes `En curso`, it starts counting from that day.

**Sheet layout (Equipo 03)**
- Weekly status matrix: rows `General / Alcance / Cronograma / Incidentes / Calidad / Riesgos`, one column per week (`Sem-01` = 10/08, one column per Monday; `Sem-08` = 28/09, column I). Values: `Verde` / `Amarillo` / `Rojo`.
  - Verde: no problems. Amarillo: warnings or problems that may lead to delays. Rojo: critical situations already causing delays.
  - `General` is computed in `RESUMEN` (Rojo if any domain is Rojo or 3+ are Amarillo; Amarillo if any is Amarillo).
- `Motivo (si Amarillo o Rojo)` (column V) and `Acción tomada (si Amarillo o Rojo)` (column W), one cell per area row, history as `Sem-NN: ...` lines.
- Schedule table ("Actividades Clave"): one row per Jira epic, columns `Estado` (`Finaliz.` / `En curso` / empty), `Avance [%]`, `F. Fin L. Base`, `F. Fin Estimado`, `F. Fin Real`, `Desvío [+/-días]` (formula, read-only), `Comentarios`.
- Incidents table: `Descripción`, `Estado` (`Abierto`/`Cerrado`), `Criticidad` (`Alta`/`Media`/`Baja`), `F. Alta`, `F. Límite`, `F. Cierre`, `Vencido` (formula), `Resolución`.
- Dates are `dd/mm/yy`. The current week is the Monday on or before today; before the week ends, fill the current week's column, not the next one.

**Reading the sheet** (works without login while it is shared by link): `https://docs.google.com/spreadsheets/d/<id>/gviz/tq?tqx=out:csv&gid=<tab gid>&headers=0&range=A1:Z140`. Row numbers in this export can be shifted by hidden rows, so confirm the real cell in the UI before writing.

**Writing the sheet.** Use whatever the agent has: a Sheets connector/API, or a browser with the PM's session. In a browser (Sheets is a canvas, plain typing is dropped): click the Name box, type the address, Enter; press `F2` to enter edit mode, `ctrl+a` to replace or `ctrl+End` to append, `alt+Return` for a new line inside a cell (wait a second before and after it, otherwise the line break can land in the wrong place), `Tab`/`Return` to commit. Dropdown cells (Estado, Criticidad, status colour) accept the exact option text. If the agent cannot write, produce a paste-ready table per cell and say so.

**Where the evidence is**
- Jira: project `PLANIFY` on `planify2026.atlassian.net`. Epics are the schedule rows; epic children carry the real status and due dates; a due date in the past with status not `Finalizada` is a delay. Ticket prefixes: `[BE-n]`, `[FE-n]`, `[INT-n]`, `[INFRA-n]`.
- Git: PRs and commits carry the ticket key; `develop` is the integration branch. Jira status can lag the code (a ticket "En revisión" that is already merged), so cross-check.
- CI: `gh run list -R Planify-Lab-IV/<repo>`; failures that block a merge are quality signals.

## Ejemplo de uso

**Pedido:** "Actualizá el cronograma de esta semana."

**Resultado:** La pestaña del equipo en la planilla con el avance de cada épica, las fechas estimadas o reales y comentarios solo donde hay algo para alertar, todo respaldado por tickets, commits y PRs.
