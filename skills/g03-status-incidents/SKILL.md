---
name: g03-status-incidents
description: Registra, actualiza y cierra los incidentes del reporte semanal del equipo a partir de evidencia real (bugs en Jira, CI fallido, hotfixes, exposiciones de seguridad). Usar cuando el PM pide anotar un incidente o completar la parte de incidentes del reporte.
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - mantenimiento
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
# Incident log for the status sheet

An **incident** is something that already happened and disrupted or could have disrupted the work or the product: a bug in a deployed build, a leaked secret, CI blocking merges, a developer blocked by hardware or licenses, an environment down. Planned work that is late is a schedule matter (`status-schedule`); something that might happen is a risk (`status-risks`).

## Procedure

1. **Read the incidents table** in our tab first, so you update existing rows (close them, add a resolution) rather than duplicating them.
2. **Find candidates** since the last report (read-only):
   - Jira: issues of type `Error`, tickets whose title starts with `[FE-FIX-n]`/`[BE-FIX-n]`, tickets created and resolved within days that describe a fix.
   - Git (`git log origin/develop`): commits like "fix", "corrijo errores de merge", "agrego paréntesis que se perdió en el merge", revert commits, repeated "formato/imports" commits right after a failed CI run.
   - CI (`gh run list -R Planify-Lab-IV/<repo>`): failed runs on feature branches or `develop`, and how long until the next green run.
   - Security/hygiene: secrets or private addresses committed, tokens in config files.
   - People and tooling: only what the PM reports (hardware, licenses, absences) or what the sheet already records.
   - Merge-blocked PRs and PRs with no review for days, when they actually blocked someone.
3. **Filter.** Register an incident only if it cost time, blocked someone, or exposed something. A CI failure fixed in the next commit with no impact is noise: group repeated ones into a single row ("fallas intermitentes del CI") instead of one row per run. Do not register more than the PM can read in a minute.
4. **Fill each row** with real data only:
   - `Descripción`: what happened and its effect, one or two sentences, no blame.
   - `Estado`: `Abierto` or `Cerrado`. **`Cerrado` only with proof**: (a) for a code problem, the Jira ticket is `Finalizada` **and** the fix is merged in `develop` (check both); (b) when there is no ticket, a mitigation that is already done and **can be confirmed in the code** (the commit/PR is in `develop`, the file no longer has the problem, CI is green again). For non-code incidents (hardware, licenses, access) only what the PM confirms. Anything else stays `Abierto` — a fix in an open PR, a ticket "En revisión" or "En curso", or a promise to fix is **not** closed. Type the exact word `Abierto`: the sheet's `Vencido` formula only reads that value.
   - `F. Alta`: the day the incident was **detected**, or since when it exists if it was found late (first commit, ticket, CI run or report that shows it). Say which one you used.
   - `F. Límite`: the latest acceptable date to resolve it. **Default rule: the Thursday of the week after the one in which the incident was detected** (weeks run Monday to Sunday, the same weeks as the sheet's columns), so the fix lands in the next ticket week and never inside the same week. Examples: detected Fri 02/10 or Mon 28/09 → Thu 08/10; detected Thu 17/09 → Thu 24/09; detected Sat 26/09 → Thu 01/10. It is required for every incident, because `Vencido` depends on it. Use another date only if the PM gives one or a hard milestone forces an earlier one, and say why. Never leave it blank on an `Abierto` incident, and do not move it later to avoid a `SI` in `Vencido` — if it is going to be missed, say so in `Resolución`/`Motivo` and let the PM decide.
   - `F. Cierre`: the **real day it was resolved**, never a planned one. Use the merge date of the fix (or the Jira resolution date; say which if they differ). Empty while the incident is `Abierto`.
   - `Vencido`: a sheet formula, never written (see the layout notes).
   - `Resolución`: what was done, with the ticket key (`PLANIFY-145: ...`). If there is a preventive follow-up that is only a suggestion, prefix it with `Acción:` and keep it separate from what was actually done.
5. **Set the `Incidentes` colour** for the week's column: Verde = nothing open and nothing new that cost time; Amarillo = something open or something new that may cause delays; Rojo = an open incident already causing delays. Add the `Sem-NN:` line to Motivo / Acción for Amarillo and Rojo.
6. **Never delete** an old incident row. Closed rows stay as history.

## Output to the PM

Reply in Spanish with a table: incident, criticidad (and why), dates, estado, evidence (ticket / commit / run), then the cell edits to be written. Ask the PM only about what you cannot know (real deadline, who was blocked).

## The status sheet (shared by the three `status-*` skills)

The weekly status board is a Google Sheet ("Tablero Estado Proyecto", id `1tA2CFxUesISCr39-MmhhdxwmitZKZBhTdOjfpSGjCec`, shared as editable by link). Every team has its own tab; ours is **`Equipo 03`** (Planify). If the PM names a different sheet or tab, use theirs.

**Hard rules**
1. **Only write to our own team tab.** The other `Equipo NN` tabs are read-only examples of how other teams fill the board. `RESUMEN` is formula-driven: never edit it.
2. **`planify-mobile` and `planify-backend` are read-only.** Never edit, commit, branch, push, merge or open PRs there. Inspect with `git log`, `git show <ref>:<path>`, `git ls-tree`, `gh pr list`, `gh run list`. No `git checkout`.
3. **Facts first, then judgement, and label which is which.** Every line written to the sheet must trace to Jira, git history, PRs, CI runs, or something the PM told you. If it is your proposal rather than something that happened, write it as "(propuesta)". Never invent dates, owners or causes. If a field has no real value (e.g. a due date nobody set), leave it empty.
4. **Do not move a status colour the team already reported without saying so.** If the evidence suggests a different colour, either change it and state that in your reply, or leave it and recommend the change. Never do it silently.
5. **Append, never overwrite** the history in the Motivo / Acción / Comentarios cells: each week adds a line prefixed `Sem-NN:` under the existing ones.
6. **The weekly status matrix takes only the colour.** Each cell of `General / Alcance / Cronograma / Incidentes / Calidad / Riesgos` gets exactly `Verde`, `Amarillo` or `Rojo` — no text, no notes, no dates. The explanation goes in `Motivo` / `Acción tomada` (columns V and W). `General` is calculated: never write it.
7. **Standing authorisation: write directly, report afterwards.** The PM has authorised these skills to write to our tab without asking first. After writing, re-read the cells to confirm they saved and report what changed (cell → old → new) plus anything you decided on judgement (a colour, an estimated date, a criticidad). Stop and ask only if the change would touch another team's tab, a baseline date, or a cell you cannot identify with certainty.

**Backlog is out of scope for risks and delays.** Tickets in Jira status `This week` or `Tareas por hacer` (category "Por hacer") are backlog, even when they carry a sprint and a due date. They are **not** evidence of risk, overload, unassigned work or delay: do not count them as overdue, as load per developer, or as "no responsible", and do not cite them in Motivo/Acción/Comentarios. Only started work counts: `En curso`, `En revisión`, and what is already merged. The one exception is the `Avance [%]` calculation, where backlog children stay in the denominator (progress = Finalizada ÷ all children). If a backlog ticket becomes `En curso`, it starts counting from that day.

**Sheet layout (Equipo 03)**
- Weekly status matrix: rows `General / Alcance / Cronograma / Incidentes / Calidad / Riesgos`, one column per week (`Sem-01` = 10/08, one column per Monday; `Sem-08` = 28/09, column I). Values: `Verde` / `Amarillo` / `Rojo`.
  - Verde: no problems. Amarillo: warnings or problems that may lead to delays. Rojo: critical situations already causing delays.
  - `General` is computed in `RESUMEN` (Rojo if any domain is Rojo or 3+ are Amarillo; Amarillo if any is Amarillo).
- `Motivo (si Amarillo o Rojo)` (column V) and `Acción tomada (si Amarillo o Rojo)` (column W), one cell per area row, history as `Sem-NN: ...` lines.
- Schedule table ("Actividades Clave"): one row per Jira epic, columns `Estado` (`Finaliz.` / `En curso` / empty), `Avance [%]`, `F. Fin L. Base`, `F. Fin Estimado`, `F. Fin Real`, `Desvío [+/-días]`, `Comentarios`.
- Incidents table: `Descripción`, `Estado` (`Abierto`/`Cerrado`), `Criticidad` (`Alta`/`Media`/`Baja`), `F. Alta`, `F. Límite`, `F. Cierre`, `Vencido` (formula, read-only), `Resolución`.
- Dates are `dd/mm/yy`. The current week is the Monday on or before today; before the week ends, fill the current week's column, not the next one.

**Reading the sheet** (works without login while it is shared by link): `https://docs.google.com/spreadsheets/d/<id>/gviz/tq?tqx=out:csv&gid=<tab gid>&headers=0&range=A1:Z140`. Row numbers in this export can be shifted by hidden rows, so confirm the real cell in the UI before writing.

**Writing the sheet.** Use whatever the agent has: a Sheets connector/API, or a browser with the PM's session. In a browser (Sheets is a canvas, plain typing is dropped): click the Name box, type the address, Enter; press `F2` to enter edit mode, `ctrl+a` to replace or `ctrl+End` to append, `alt+Return` for a new line inside a cell (wait a second before and after it, otherwise the line break can land in the wrong place), `Tab`/`Return` to commit. Dropdown cells (Estado, Criticidad, status colour) accept the exact option text. If the agent cannot write, produce a paste-ready table per cell and say so.

**Where the evidence is**
- Jira: project `PLANIFY` on `planify2026.atlassian.net`. Epics are the schedule rows; epic children carry the real status and due dates; a due date in the past with status not `Finalizada` is a delay. Ticket prefixes: `[BE-n]`, `[FE-n]`, `[INT-n]`, `[INFRA-n]`.
- Git: PRs and commits carry the ticket key; `develop` is the integration branch. Jira status can lag the code (a ticket "En revisión" that is already merged), so cross-check.
- CI: `gh run list -R Planify-Lab-IV/<repo>`; failures that block a merge are quality signals.

## Ejemplo de uso

**Pedido:** "Anotá el incidente del deploy que falló ayer."

**Resultado:** Una fila nueva en la tabla de Incidentes con fecha, descripción, impacto, evidencia y estado, y el color de Incidentes de la semana actualizado.
