---
name: g09-zervi-final-project-report
description: "Invocación explícita: redacta el informe final de Zervi con evidencia delimitada, indicadores y decisiones de cierre pendientes de revisión humana."
license: MIT
metadata:
  author: "Bruno Iacovone"
  github: "BrunoIacovone"
  version: "1.0.0"
  status: "experimental; not execution-validated"
  tipo: skill
  area: [gestion, documentacion]
  fase: [revision]
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

Activate only on explicit named invocation to draft the rotating PM's final project report (`g09-zervi-final-project-report` or original name `zervi-final-project-report`).

## Hard Rules

- Accept pasted scope, residuals, handover, lessons and KPI records; no integration required. Zervi is a service marketplace; report only the supplied scope and results.
- Return a draft in chat in the user's language. Writes and publication need explicit authorization; do not operate the app or external services.
- Cite source IDs, version/environment and cutoff. Preserve inherited IDs, conflicts and limitations; multiple reports repeating one source are not independent corroboration.
- Do not invent costs, dates, owners or results. Targets are not actuals; synthetic measures are not adoption. Done/green is not acceptance, and a report does not authorize closure: humans decide.

## Decision Gates

| Evidence | Wording |
|---|---|
| Closure decision absent | Draft for closure review, not project closed. |
| KPI target only | Actual unknown; achievement not assessed. |
| Upstream claim unsupported/conflicting | Attribute and qualify; do not reapprove it. |

## Execution Steps

1. Inventory versioned scope, residual, handover and lessons artifacts plus chronology and KPI sources; mark absent inputs.
2. Establish report boundary and source IDs stable within supplied records, without persistent-memory claims.
3. Synthesize commitments/results, deviations, quality/acceptance, residuals, handover and lessons with source-level limitations.
4. Separate delivery conclusions from closure decision status and future benefits review.
5. Complete a useful partial report; identify evidence and human decisions needed for stronger conclusions.

## Output Contract

Return a draft with:
1. Executive conclusion and report boundary: scope/baseline source, version, environment, cutoff.
2. Commitments: `criterion | baseline/change | delivery evidence | acceptance evidence/status | deviation`.
3. Quality and KPIs: `measure | population/window | target/source | actual/source | limits`; include numerator/denominator for rates and label synthetic samples. Calculate variance only with comparable supplied baseline and actuals.
4. Residual IDs/disposition, recipient handover evidence and lessons/actions, distinguishing candidates from validated learning.
5. Documented closure decision/authority/conditions or pending human review; proposed next actions.
6. Compact evidence list: `ID | source/version/locator | basis | limitations/conflicts`.

## Ejemplo de uso

Ejemplo sintético ilustrativo; no representa ejecución realizada.

**Pedido:** Invoca g09-zervi-final-project-report. S1 vincula publicación entregada con aceptación A1 del PO; R1 mantiene QA-4 abierto; H1 registra recepción y responsabilidad documental del PM entrante. K1 registra 9 cancelaciones persistidas de 10 intentos sintéticos del 9/11, sin KPI oficial ni decisión de cierre.

**Resultado:** Informa 90% en esa muestra, no adopción real ni KPI oficial; vincula publicación aceptada S1→A1, residual QA-4 y transferencia documental H1. Propone revisar QA-4 antes de decidir cierre.
