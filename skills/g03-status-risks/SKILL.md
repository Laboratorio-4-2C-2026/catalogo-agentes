---
name: g03-status-risks
description: Detecta y escribe los riesgos de la semana en la planilla de estado del equipo, con su color, a partir de evidencia real (tickets vencidos, PRs abiertos, integraciones pendientes). Usar cuando el PM pide revisar o anotar los riesgos del reporte semanal.
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
# Weekly risks for the status sheet

A **risk** is something that has not hurt the schedule yet but can: it is about the future. If it already caused a delay it belongs in the schedule skill (`status-schedule`); if it is an event that already happened and was handled or is being handled, it belongs in `status-incidents`. When one fact is both (an incident that also threatens the next milestone), record the incident there and the *remaining exposure* here, without repeating the text.

## Procedure

1. **Read the current state** of our tab (previous weeks' colours, Motivo and Acción text) so the new line continues the history instead of repeating it.
2. **Collect evidence for the week** (never from memory):
   - **Jira**: started tickets (`En curso`/`En revisión`) that are overdue, how long they have been in review, and dependencies between epics. Ignore backlog tickets (see the backlog rule below): their due dates, assignees and counts are not risk evidence.
   - **Code** (read-only): what is merged in `develop` versus what each ticket needs. The strongest recurring risk on this project is **integration debt**: screens that are built but still wired to `Fake*Repository` instead of a real HTTP repository (look at the `*_providers.dart` files under `lib/features/*/presentation/controllers/` in `planify-mobile`), and `[INT-n]` tickets that are `En curso` while their BE and FE are merged.
   - **PRs** (`gh pr list`): open for more than a few days with no review, long chains of branches that keep needing merge fixes.
   - **People and scope**: work concentrated in one or two developers, several started tickets stuck on the same person, upcoming milestones (builds, deployments) that depend on unfinished work.
   - **Team / environment**: only what the PM reports or the sheet already records (hardware, licenses, availability).
3. **Rank and cut.** Keep at most **3 risks** per week, ordered by (probability × how close the date is). Each risk is one sentence with the number or fact that proves it ("5 tareas INT abiertas", "11 tickets vencen el 07/10"), not an opinion.
4. **Pick the colour** for `Riesgos` in the week's column with the sheet's criteria: Verde = no relevant risk; Amarillo = at least one risk with evidence that can cause a delay; Rojo = a risk that is already materialising and affecting dates. Say why in your reply.
5. **Write** the week's lines:
   - `Motivo`: `Sem-NN: <risk 1>. <risk 2>.` — facts only.
   - `Acción tomada`: `Sem-NN: <what was done>` for things that already happened, and `Sem-NN (propuesta): <what to do>` for suggestions. Every risk gets an action or an explicit "sin acción definida".
6. **Close the loop on old risks.** If a risk from a past week is gone (the ticket was integrated, the PR merged), add a short `Sem-NN: <riesgo> resuelto` line to the Acción cell so the history shows it.

## Output to the PM

Reply in Spanish with: the proposed colour and why, the 1–3 risks with their evidence, the lines to be written (cell → text), and one question if something needs the PM's decision (for example, a scope cut). Write directly (standing authorisation) and report what you wrote.

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
- Incidents table: `Descripción`, `Estado` (`Abierto`/`Cerrado`), `Criticidad` (`Alta`/`Media`/`Baja`), `F. Alta`, `F. Límite`, `F. Cierre`, `Vencido` (formula), `Resolución`.
- Dates are `dd/mm/yy`. The current week is the Monday on or before today; before the week ends, fill the current week's column, not the next one.

**Reading the sheet** (works without login while it is shared by link): `https://docs.google.com/spreadsheets/d/<id>/gviz/tq?tqx=out:csv&gid=<tab gid>&headers=0&range=A1:Z140`. Row numbers in this export can be shifted by hidden rows, so confirm the real cell in the UI before writing.

**Writing the sheet.** Use whatever the agent has: a Sheets connector/API, or a browser with the PM's session. In a browser (Sheets is a canvas, plain typing is dropped): click the Name box, type the address, Enter; press `F2` to enter edit mode, `ctrl+a` to replace or `ctrl+End` to append, `alt+Return` for a new line inside a cell (wait a second before and after it, otherwise the line break can land in the wrong place), `Tab`/`Return` to commit. Dropdown cells (Estado, Criticidad, status colour) accept the exact option text. If the agent cannot write, produce a paste-ready table per cell and say so.

**Where the evidence is**
- Jira: project `PLANIFY` on `planify2026.atlassian.net`. Epics are the schedule rows; epic children carry the real status and due dates; a due date in the past with status not `Finalizada` is a delay. Ticket prefixes: `[BE-n]`, `[FE-n]`, `[INT-n]`, `[INFRA-n]`.
- Git: PRs and commits carry the ticket key; `develop` is the integration branch. Jira status can lag the code (a ticket "En revisión" that is already merged), so cross-check.
- CI: `gh run list -R Planify-Lab-IV/<repo>`; failures that block a merge are quality signals.

## Ejemplo de uso

**Pedido:** "Anotá los riesgos de la semana."

**Resultado:** La fila de Riesgos de la planilla con cada riesgo, su evidencia y el color de la semana, separando hechos de propuestas.
