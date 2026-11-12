---
name: g09-zervi-residual-risks-consolidator
description: "Invocación explícita: consolida riesgos, incidencias y pendientes residuales de Zervi sin confundir propuestas con aceptación o transferencia."
license: MIT
metadata:
  author: "Bruno Iacovone"
  github: "BrunoIacovone"
  version: "1.0.0"
  status: "experimental; not execution-validated"
  tipo: skill
  area: [gestion]
  fase: [revision, mantenimiento]
  tecnologias: [agnostico]
  metodologia: [agnostico]
  herramientas: [otra]
  requiere: []
  grupo: "09"
  autor:
    nombre: Bruno Iacovone
    github: BrunoIacovone
  responsables: [BrunoIacovone]
  madurez: experimental
  relacionados: []
---

## Activation Contract

Activate only on explicit named invocation to consolidate closure residuals for the rotating PM (`g09-zervi-residual-risks-consolidator` or original name `zervi-residual-risks-consolidator`).

## Hard Rules

- Accept pasted risk, issue, QA and deferred-work records; no integration required. Zervi is a service marketplace; consolidate only the supplied closure scope.
- Return a draft in chat in the user's language. Writes and publication need explicit authorization; do not operate the app or external services.
- Cite source IDs, relevant version/environment and cutoff; distinguish observed issues from uncertain future risks and proposed treatment. Preserve conflicting assessments.
- Preserve IDs, severity and rating scales. Do not invent scores, owners, dates or acceptance. Treatment approval, residual acceptance and transfer acknowledgment are separate human decisions; Done is not approval.

## Decision Gates

| Condition | Action |
|---|---|
| Existing defect/event | Classify as issue; link a separate future risk only if justified. |
| True duplicate | Merge with aliases and provenance; retain conflicting assessments. |
| Recipient proposed, no acknowledgment | Transfer pending, never transferred. |

## Execution Steps

1. Inventory supplied risk, issue, QA, deferred-work and decision records; mark source boundaries and unknowns.
2. Classify and deduplicate by underlying event, scope and evidence, not similar titles.
3. Express risks as cause/event/effect; preserve QA severity and supplied impact/rating. Separate risk owner from action owner.
4. Propose treatments and recipients explicitly as proposals; record acknowledgment, acceptance authority/status and review date only when supplied.
5. Return a useful partial register and decision gaps; withhold unsupported acceptance or closure conclusions.

## Output Contract

Return a draft boundary and register, split into linked tables if needed:
- Exposure: `ID | risk/issue/deferred work/decision gap | description | source/aliases | supplied impact/severity`.
- Treatment: `ID | proposed/approved action and source | risk owner | action owner | supplied review date`.
- Disposition: `ID | acceptance authority/status/evidence | recipient | acknowledgment/status`.
Add duplicate rationale, retained disagreements and next human decisions. Use cause → uncertain event → effect for risks; an already observed defect remains an issue. Keep unknown assignments unassigned and proposals explicit.

## Ejemplo de uso

Ejemplo sintético ilustrativo; no representa ejecución realizada.

**Pedido:** Invoca g09-zervi-residual-risks-consolidator. QA-4 y D-8 describen la misma reserva cancelada que reaparece pendiente al recargar en la misma demo, con severidad P2 suministrada. H1 no explica cómo conciliarla; no hay aceptación ni destinatario confirmado.

**Resultado:** Consolida QA-4 con alias D-8 y severidad P2; vincula R-01: falta de guía→PM podría duplicar la reserva→demo inconsistente. Propone guía de conciliación y decisión del PO; aceptación y transferencia siguen pendientes.
