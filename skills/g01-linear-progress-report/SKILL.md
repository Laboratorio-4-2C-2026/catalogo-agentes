---
name: g01-linear-progress-report
description: "Calcula el avance de Cinematch por categoría (módulo) en story points, hechos/total y %, leyendo Linear en vivo. Usala cuando piden el avance o \"% de avance por categoría\", cuánto lleva un módulo en puntos o por qué un módulo que vence hoy no está al 100%."
author: Francisco
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - revision
  tecnologias:
  - agnostico
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
  - g01-cinematch-pm-weekly
---
# Linear progress report by category (story points)

Computes how far along each category is, measured in story points, using live data from Linear.

Notes you write follow [AGENTS.md](../../../AGENTS.md), so their content is in Spanish. This skill is in English.

**Read [Medición del avance](../../../Cronograma/Medicion%20del%20avance.md) first.** The story-point % this skill produces is one more way to measure progress. It is not the EVM figure and it is not the Tablero's manual % per module. When you report it, call it "avance en story points según Linear" so nobody mixes it up with the others.

## Definitions

- **Category**: a child label of the label group `Categoría` in Linear. Get the list with `list_issue_labels` (`includeGroups: true`) and keep the labels whose parent is `Categoría`. They match the module names in the Tablero.
- **Tickets counted**: only `[T]` task tickets. Exclude `[US ...]` user stories (their points duplicate their children), `[HAB-...]` enablers, and anything in `Duplicate` or `Canceled`.
- **Points**: `estimate.value`. A `[T]` ticket with no estimate is listed apart and left out of the math.
- **Done**: status type `completed`. In Progress, In Review, Todo and Backlog all count as not done.
- **Progress %** = done points / total points × 100, rounded to 1 decimal.

## Steps

1. **Always fetch fresh data.** Statuses change daily, so never reuse numbers from earlier in a conversation or from a note. Call `list_issues` with `fields: ["title","estimate","status","labels","dueDate"]` and `limit: 250`, and keep paginating with `cursor` while `hasNextPage` is true.
2. Filter to `[T]` tickets, then assign each one to every `Categoría` label it carries.
3. Tally in a script (python in bash), never by hand, because hand tallies have produced wrong totals before:
   - per category: done pts, total pts, %, ticket count, latest `dueDate`
   - overall: sum of done / sum of total
4. Sanity checks to run before answering:
   - Total `[T]` tickets = categorized + uncategorized. Report both numbers.
   - List every `[T]` ticket with **no** category label.
   - List every category label with **0 tickets**, and show it as "sin tickets", not 0%. `Capacitación` is the known case: in the Tablero it is 100% done by date, but no ticket carries its label.
   - Linear labels win over any older note or markdown. If they disagree, use Linear and point out the difference.
5. For each category whose latest due date is today or already past and whose % is under 100, name the tickets that are not done and give each one's status.

## Output

Show a compact table in the user's language (Spanish):

| Categoría | Hecho / Total (pts) | % | Tickets | Fecha límite |
|---|---|---|---|---|

Below the table, add one line with the overall total and short notes on uncategorized tickets, empty categories and overdue categories. Write a note only if asked. If you do, it goes in `Seguimiento PM/` with the date in its file name (`AAAA-MM-DD <tema>.md`) and dates in absolute form, following [AGENTS.md](../../../AGENTS.md).

## Don'ts

- Don't modify Linear (labels, dates, status) unless the person explicitly asks.
- Don't present this % as the project's avance without the caveat from [Medición del avance](../../../Cronograma/Medicion%20del%20avance.md).

## Ejemplo de uso

**Pedido:** ¿Qué % de avance tiene cada categoría?

**Resultado:** Devuelve una tabla por categoría con puntos hechos, totales y % (como "avance en story points según Linear"), y lista aparte los tickets [T] sin estimación.
