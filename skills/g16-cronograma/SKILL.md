---
name: g16-cronograma
description: 'Propone las filas actualizadas del cronograma que el equipo le muestra a la cátedra de Laboratorio IV a partir de Jira, GitHub y los reportes de los agentes (semanales, incidentes y post-deploy), y marca lo que no cierra en la planilla actual. Usar cuando el PM pide actualizar el cronograma o el estado semanal.'
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
  tecnologias:
  - agnostico
  herramientas:
  - claude-code
  requiere:
  - github
  - jira
  grupo: "16"
  autor:
    nombre: Valentino Gianuzzo
    github: ValentinoGianuzzo
  responsables:
  - ValentinoGianuzzo
  madurez: experimental
  relacionados:
  - g16-steering-prep
  - g16-eureka-progreso-semanal
  - g04-cronograma
  - g03-status-schedule
---

# Cronograma

The team keeps a spreadsheet that it shows to the professors to report
progress. It has three sections: **Cronograma**, **Estado semanal** (the same
rows on the report date) and **Incidentes**. Each row is a block of work, not a
ticket, with these columns:

| Actividades clave | Estado tarea | Avance [%] | F. Fin L. Base | F. Fin Estimado | F. Fin Real | Desvío [+/- días] | Comentarios |

Above the table: **Avance Global [%]** and **Fecha de Fin Prevista**.

The spreadsheet is not in the repo. This skill proposes the rows; the PM pastes
them. Talk to the user in Spanish (rioplatense).

## The rules that matter

1. **The spreadsheet is the source of truth for real dates.** Jira dates were
   often stale, and a PR merge date is when the review ended, not when the work
   was delivered. Use Jira and GitHub only to know *whether* something exists
   and is done. Never fill `F. Fin Real` or `Desvío` from them: propose a date
   only as "a confirmar", saying where it comes from, and ask the PM.
2. **The baseline never moves.** `F. Fin L. Base` is what was planned. If a row
   is late, `F. Fin Estimado` moves; the baseline does not. Moving it erases the
   deviation the professors are supposed to see. If the PM moved one, say so.
3. **Rows are blocks.** Group tickets the way the sheet already does ("Flujo de
   compartir patente", "Configuración Mercado Pago (Pagos - Wallet - Checkout)").
   A Jira epic is usually a good block. Do not add a row per ticket, and do not
   add small fixes as their own row: they go in an existing block.
4. **Nothing done without evidence.** A block is `Finaliz.` only if its tickets
   are done in Jira and the work is merged (or the PM confirms it was delivered
   another way). A ticket marked done in Jira with no PR is "a confirmar".

## Step 1 — Get the current sheet

Ask the PM for the current table: a screenshot or the pasted rows. Without it
you cannot tell what changed. Read it carefully and note, for later, every
inconsistency you see in it (step 4).

## Step 2 — Gather the evidence

- **Jira** (project `EP`): if an Atlassian/Jira tool is available in this
  session, list the tickets and epics with status, assignee and parent. Group
  tickets by epic. If no Jira tool is available, ask the PM for the status of
  the open blocks instead of guessing.
- **GitHub**: `gh pr list --state all --limit 100 --json number,title,state,author,createdAt,mergedAt,url`
  against this repository. PR titles and branch names usually carry the ticket
  (`EP-44`, `feat/ep-44-…`). An open PR in review means the block is close to
  done, not done.
- **Weekly reports** (`reporte-semanal` label) for what moved each week.
- **Incidents** (`incidente` label, from Eureka Incidentes, and `post-deploy`):
  one row each for the Incidentes section, with date, what happened, impact and
  whether it is closed.

## Step 3 — Propose the rows

For every row of the current sheet, and for every block that is missing:

- **Estado tarea**: `Finaliz.`, `En curso` or `Pend.`, as the sheet uses them.
  A PR in review is `En curso`.
- **Avance [%]**: 100 only when finished, 0 when pending. In between, use what
  the assignee reports; if you only have the PR state, ~90 for "PR open, in
  review" and ask the assignee otherwise.
- **Dates**: keep the existing baseline. For a new block, the baseline is the
  date it was planned for when it was planned (ask the PM if unsure).
  `F. Fin Real` and `Desvío` come from the PM (rule 1).
- **Desvío** = baseline − real, in days. Negative means late. Check the
  arithmetic of every row that has both dates.
- **Comentarios**: only when a deviation needs an explanation, as the sheet
  already does ("el deploy fue terminado en tiempo y forma, pero…").

Remember the team's capacity: each developer works about six hours a week. An
estimated date that assumes more than that for an open block is a risk worth
pointing out.

## Step 4 — Check the sheet

List every problem found, by row:

- Baselines that moved (rule 2).
- `Finaliz.` rows without real date or deviation.
- Wrong deviation arithmetic.
- Status and progress that contradict each other (`Pend.` with progress above
  0, `Finaliz.` below 100).
- Open rows whose estimated date already passed.
- Dates without year or in a different format, and typos in the activity names.

## Step 5 — Hand it over

Give the PM, in this order:

1. The table of rows to paste, in the sheet's column order, with "a confirmar"
   in every cell that needs their input.
2. The list of problems from step 4.
3. **Avance Global**: the simple average of the Avance column, with the formula
   `=PROMEDIO.SI(<actividades>;"<>";<avance>)` (`AVERAGEIF` and `,` in an
   English Excel) so empty rows do not count, and the value it gives with the
   proposed rows.
4. The list of "a confirmar", grouped by who has to answer (the PM, each
   assignee).

Do not edit Jira or the spreadsheet, and do not commit, push or publish
anything: the PM reviews and updates the sheet.

## Ejemplo de uso

**Pedido:** «Actualizá el cronograma para mostrárselo a los profesores.» (con una captura de la planilla actual)

**Resultado:** Junta el estado de Jira y los PRs, propone las filas nuevas o corregidas, incluida la sección de incidentes, y lista las inconsistencias que encontró en la planilla. Si no hay una herramienta de Jira, pregunta el estado en vez de adivinar.
