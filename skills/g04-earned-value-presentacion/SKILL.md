---
name: g04-earned-value-presentacion
description: Concilia el Earned Value de PitStop (PV, EV, AC, SPI, CPI) con la historia real de Linear y el plan local, y prepara los números para presentarlos. Usar al actualizar project-plan/earned-value.yaml, reportar la performance del proyecto o armar la lámina de Earned Value.
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - revision
  - planificacion
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - linear
  grupo: "04"
  autor:
    nombre: Tomás Serra
    github: TomasSerra
  colaboradores:
  - nombre: Manuel Lostaló
    github: ManuLosta
  responsables:
  - TomasSerra
  madurez: usado-en-proyecto
  relacionados:
  - g15-evm-calculator
---

# PitStop — Refresh Earned Value

`project-plan/earned-value.yaml` is the weekly source for the Earned Value chart.
It must describe the project's observed history and its approved remaining plan, not a
perfect curve and not a flat copy of team capacity.

## Sources and authority

Read these before changing anything:

- `project-plan/earned-value.yaml` — current weekly record and prior actuals.
- `project-plan/features.yaml` — approved scope, feature estimates, planned dates, and
  `ticket_refs`.
- `project-plan/team.yaml` — team, weekly cadence, capacity, and Linear coordinates.
- `project-plan/risks.yaml` — incidents or risks that explain a material variance.

Then query Linear through the configured MCP for all PIT issues, including:

```
team=PIT
limit=250
includeArchived=true
fields=["id", "title", "estimate", "status", "statusType", "createdAt",
        "startedAt", "completedAt", "canceledAt", "dueDate", "project",
        "assignee", "updatedAt"]
```

Linear is authoritative for issue state, estimate, and completion timestamp. The local
plan is authoritative for scope, feature grouping, and the approved schedule. Do not
write to Linear for this task unless the user explicitly asks for a Linear change.

## Weekly convention

The team works Thursday to Thursday. A planned feature belongs to the row whose
`week_start` equals its `starts` date. Its `ends` date is the due Thursday for that
row.

For completed work, put a ticket in the week in which it was completed. When a ticket
is completed on a shared Thursday boundary, assign it to the earlier week if that is
its `dueDate`; otherwise assign it to the new week. State this convention in the final
summary when it affects a total.

## Historical lock

Treat completed reporting periods as closed. An ordinary refresh may edit only the
current week and, when late evidence arrives, the immediately previous week. Never
rewrite an older row automatically, even when Linear history would produce a different
result today.

If an older discrepancy is found, report it separately with the affected week and the
evidence. Change it only after the user explicitly authorizes a historical correction
or a formal rebaseline. This preserves the project's reporting history instead of
making past performance move every time tickets are cleaned up in Linear.

## Calculate each measure

### PV — Planned Value

PV is planned work, not available capacity. For each future week, sum the estimates of
features whose `starts` date is that week. A week with 7 SP or 0 SP is valid if that is
what the approved plan schedules; do not silently fill it to 18.

For closed historical weeks, preserve the recorded baseline. Rebuild PV only for the
current or immediately previous week, unless the user explicitly asks for a historical
correction or rebaseline.

### EV — Earned Value

EV is the estimate of work that is actually Done. Sum only non-canceled Linear issues
with `statusType=completed`, using their Linear estimate. Map them through
`ticket_refs`; a feature split into several tickets earns each ticket's completed
estimate once.

Do not earn value for Backlog, In Progress, or In Review work. Do not give partial EV
just because a ticket is almost done. Include a completed orphan issue only after
confirming it belongs to the PitStop scope; otherwise report it as an unmapped issue
instead of silently changing the data.

### AC — Actual Cost

Linear timestamps and status changes do not measure hours. Use actual-cost evidence in
this order:

1. Approved time logs or a weekly team report.
2. A documented incident, handoff, rework, or explicit user-provided effort.
3. The existing AC value, if there is no new evidence.

Never invent AC from ticket estimates, dates, or a desire to improve CPI. If a proxy is
explicitly requested, label it as an estimate and keep it plausible: a small overrun
or underrun must be supported by the execution record, not tuned to make the chart
look ideal.

Future rows always have `ac: 0` and `ev: 0`.

## Reconciliation procedure

1. Build a ticket-to-feature map from `ticket_refs`.
2. Compare Linear estimates and dates with the plan. Use Linear completion dates for
   EV; flag material estimate or date mismatches before treating them as a rebaseline.
3. Calculate PV, EV, and evidence-backed AC only for the current and immediately
   previous week. Preserve every older row verbatim and report, rather than apply, any
   discrepancy found there.
4. Update only `project-plan/earned-value.yaml`. Keep the YAML sorted by `week_start`
   and do not add comments: the app rewrites this file.
5. Run `npm run check:earned-value`.
6. Report the changed weeks, the source of each non-zero EV/AC, unresolved orphan
   issues, and the current cumulative SPI/CPI. Explain meaningful variances plainly.

## Guardrails

- A non-perfect curve is normal. Do not force SPI or CPI to 1.00.
- Do not count a ticket twice because it appears in both a feature and a Linear project.
- Do not turn a capacity gap into PV. It is a planning signal, not a calculation error.
- Do not alter product scope, ticket status, estimates, or dates merely to improve the
  metric.
- Do not modify a week older than the previous one without explicit user approval.
- If the result exposes an empty planned week, report it. Move work only when the user
  requests a schedule change.

## Final response

Keep the report concise. Include the updated file, validation result, and any decision
the PM needs to make. Distinguish facts retrieved from Linear from AC values that were
kept because no actual-cost source exists.


## Para la presentación

Cuando el resultado se va a presentar, sumar a la respuesta final:

1. **Tabla acumulada** hasta la última semana cerrada: PV, EV y AC acumulados, SPI (EV / PV) y CPI (EV / AC). Las semanas futuras no entran en el acumulado de EV ni de AC.
2. **Un mensaje por lámina:** una frase que diga si el proyecto va adelantado o atrasado y si gasta más o menos de lo planificado.
3. **Causa de cada desvío importante**, con el riesgo o incidente de `project-plan/risks.yaml` que lo explica.
4. **Advertencias:** qué valores de AC no tienen respaldo real. No redondear ni elegir el período para que la curva se vea mejor.

El gráfico sale de la pestaña Earned Value de la app, no se redibuja a mano.

## Ejemplo de uso
**Pedido:** Actualizá el Earned Value y dame los números para la presentación del viernes.

**Resultado:** Actualiza la semana actual con evidencia de Linear, valida el archivo y entrega la tabla acumulada, el SPI y el CPI, las causas de los desvíos y los valores de AC que no tienen respaldo.
