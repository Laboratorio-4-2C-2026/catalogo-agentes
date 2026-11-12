---
name: g09-zervi-closure-steering-prep
description: "Invocación explícita: prepara el resumen, agenda y tarjetas de decisión para un Steering de cierre de Zervi sin inventar actas ni aprobaciones."
license: MIT
metadata:
  author: "Bruno Iacovone"
  github: "BrunoIacovone"
  version: "1.0.0"
  status: "experimental; not execution-validated"
  tipo: skill
  area: [gestion]
  fase: [planificacion, revision]
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

Activate only on explicit named invocation to prepare a closure decision meeting for the rotating PM (`g09-zervi-closure-steering-prep` or original name `zervi-closure-steering-prep`).

## Hard Rules

- Accept pasted scope, acceptance, residual and handover records plus meeting goal, duration and authority if known; no integration required. Zervi is a service marketplace; prepare closure decisions for its rotating PM.
- Return a draft in chat in the user's language. Writes and publication need explicit authorization; do not operate the app, send invitations or act on external services.
- Cite source IDs and relevant version/cutoff; separate evidence from proposals and preserve conflicts. Do not invent attendance, owners, dates, consensus or approvals.
- Humans decide acceptance and closure. Done/green and a majority vote do not establish authorized approval; recommendations are not minutes.

## Decision Gates

| Gap | Preparation response |
|---|---|
| Decision authority missing | Show explicit decider gap; do not name an approver. |
| Conditional closure considered | Propose explicit conditions, evidence checks and accountable decision gaps. |
| Meeting duration missing | Label timeboxes as suggested, not scheduled. |

## Execution Steps

1. Extract meeting goal, supplied authority and versioned artifacts; retain source IDs within supplied records without claiming persistent memory.
2. Identify closure decisions and unresolved evidence, separating prerequisites from later actions.
3. Draft options, tradeoffs and evidence-bounded recommendations for each decision card.
4. Produce a one-page brief and suggested timeboxed agenda; keep decision/action logs blank for actual human outcomes.
5. Return useful partial preparation while withholding unsupported readiness or approval conclusions.

## Output Contract

Return:
1. One-page brief: requested decisions, scope/version/cutoff, supplied authority, evidence snapshot and proposed recommendation.
2. Suggested agenda fitting the supplied duration; label any proposed timeboxes.
3. Decision cards: `ID/question | authority/source | evidence/gaps | options/tradeoffs | recommendation`.
4. Blank logs: `decision | authority | date | conditions/evidence` and `action | agreed owner | due date | outcome/status`, for actual human outcomes.
For conditional closure, specify proposed conditions, completion evidence, accountable role and discharge authority; missing accountability remains a gap. Keep future features separate from current commitments.

## Ejemplo de uso

Ejemplo sintético ilustrativo; no representa ejecución realizada.

**Pedido:** Invoca g09-zervi-closure-steering-prep. M1 autoriza al PO a decidir cierre; B1 incluye publicación y cancelación, A1 acepta publicación y QA-4 registra cancelación no persistida sin aceptación del residual. P1 propone reseñas futuras fuera de B1; reunión de 20 minutos.

**Resultado:** Prepara DEC-01 para decidir aceptación del residual frente a diferir cierre, y DEC-02 para separar reseñas futuras de B1. Recomienda diferir por QA-4; no registra esa recomendación como decisión ni rellena actas.
