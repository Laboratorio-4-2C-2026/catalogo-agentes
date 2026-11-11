---
name: g01-gantt-from-linear
description: "Genera un Gantt semanal en Excel (.xlsx) con los tickets [T] actuales de Linear, una semana por tarea, coloreado por categoría y con los tickets sin fecha marcados \"Sin fecha\". Usala cuando piden un Gantt, cronograma o timeline de los tickets de Linear tal como están hoy; no sirve para el Gantt de línea base ni el del Steering."
author: Francisco
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
  tecnologias:
  - python
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - linear
  grupo: "01"
  autor:
    nombre: Francisco Zizzi
    github: FranciscoZizzi
  responsables:
  - FranciscoZizzi
  madurez: usado-en-proyecto
  relacionados:
  - g01-cinematch-steering-draft
---
# Gantt from Linear (Excel)

Builds a weekly Gantt `.xlsx` from the tickets currently in Linear. It's a snapshot of how the dates are loaded in Linear right now.

Notes you write follow [AGENTS.md](../../../AGENTS.md), so their content is in Spanish. This skill is in English.

**This is not the baseline.** The current week-by-week plan and its changelog live elsewhere: see [Cronograma](../../../Cronograma/Cronograma.md) and [Fuentes de Contexto](../../../Fuentes%20de%20Contexto.md). For the steering-deck gantt use `cinematch-steering-draft`. If someone wants this chart to compare against the baseline, tell them it isn't the plan and point them to those sources.

## Defaults (overridable in chat)

- **Tickets**: only `[T]` task tickets. Skip `[US ...]` stories and anything in `Duplicate`/`Canceled`.
- **Category**: the ticket's child label under the `Categoría` group. A ticket without one goes to "Sin categoría".
- **Duration**: every task is **1 week**. `dueDate` marks the end of the bar and the start is dueDate − 6 days.
- **Undated tickets** stay in the chart. Their Start and End read "Sin fecha" in red italics, and their ticket ID goes in a grey cell in a final **"Sin fecha"** column.
- **Week columns**: one per week, from the earliest to the latest dueDate in 7-day steps, aligned to the weekday the due dates fall on (Thursdays in Cinematch). Header format is `mm/dd`. A dueDate that falls between columns shades the week that contains it.

## Steps

1. Fetch fresh data with `list_issues`, `fields: ["title","estimate","status","labels","dueDate"]` and `limit: 250`, paginating while `hasNextPage` is true.
2. Build the task list as `(ticket, category, title without "[T] ", status, dueDate|None)`.
3. Generate the file with openpyxl in a script. Don't write cells by hand.
4. Layout of the "Gantt" sheet:
   - A1 holds the title "Cinematch — Gantt de Tickets (1 semana por tarea)", merged A1:F1, Arial 14 bold.
   - A2 holds a one-line italic note that explains the 1-week assumption and the "Sin fecha" marking, and says the chart is a snapshot of Linear on <AAAA-MM-DD>.
   - Row 4 holds the headers: `Ticket | Categoría | Título | Estado | Inicio | Fin / Fecha límite | <weeks…> | Sin fecha`, white bold on `404040`.
   - Sort rows by category order, then by dueDate, with undated tickets last.
   - Each bar is the week cell holding the ticket ID, filled with the category color, in 8pt bold centered text.
   - Give every row thin `BFBFBF` borders. Freeze panes at the first week column, one row below the header.
   - Column widths: A=10, B=20, C=55 (wrap), D=12, E=12, F=14, weeks=7, Sin fecha=10.
   - Below the data, leave two empty rows and add a legend with one color swatch per category and a grey swatch labeled "Sin fecha límite asignada en Linear".
5. Category palette, in this order and reused cyclically: `FFD966, 9DC3E6, A9D18E, F4B183, B4A7D6, F8CBAD, BDD7EE, C6E0B4, FFE699, D9D2E9`. No-date fill: `D9D9D9`.
6. Save as `Cinematch_Gantt_<AAAA-MM-DD>.xlsx` in the session's outputs folder. Don't commit it to this vault: per [AGENTS.md](../../../AGENTS.md), shared files live in Drive.
7. Before delivering, verify with a script:
   - task rows = `[T]` tickets fetched
   - filled week cells + "Sin fecha" cells = rows (each ticket appears exactly once)
   - the undated tickets listed = the tickets with `dueDate == null`

   Report the counts in one line.

## Don'ts

- Don't change dates or anything else in Linear. A ticket without a date shows up as "Sin fecha".
- Don't invent dates for undated tickets.

## Ejemplo de uso

**Pedido:** Armame un Gantt con los tickets de Linear.

**Resultado:** Devuelve un archivo Cinematch_Gantt_<fecha>.xlsx con una barra semanal por ticket [T] terminando en su dueDate, coloreada por categoría, y una columna "Sin fecha" para los tickets sin fecha.
