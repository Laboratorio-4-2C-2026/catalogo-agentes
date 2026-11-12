---
name: g09-zervi-lessons-learned-facilitator
description: "Invocación explícita: prepara lecciones de cierre de Zervi basadas en evidencia y acciones de adopción, sin inventar causas, consenso ni resultados."
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

Activate only on explicit named invocation to prepare or facilitate closure learning for the rotating PM (`g09-zervi-lessons-learned-facilitator` or original name `zervi-lessons-learned-facilitator`); never assume a workshop occurred.

## Hard Rules

- Accept pasted timelines, retrospective notes, participant input and prior actions; no integration required. Zervi is a service marketplace; support learning across PM rotations.
- Return a draft in chat in the user's language. Writes and publication need explicit authorization; do not operate the app or external services.
- Cite source IDs and relevant scope/cutoff. Separate observations, testimony, causal hypotheses and proposals; preserve dissent and do not count repeated reports as independent support.
- Be blame-free. Do not invent causes, consensus, owners, dates or outcomes. Humans validate lessons and agree adoption; a Done action does not prove improvement.

## Decision Gates

| Evidence | Response |
|---|---|
| No participant input | Workshop plan and candidate questions, not validated lessons or consensus. |
| Plausible cause, no supporting evidence | Causal hypothesis plus alternative explanations. |
| Historic action marked Done, no outcome evidence | Outcome unverified; keep learning follow-up open. |

## Execution Steps

1. Inventory timeline, retrospectives, incidents, positive outcomes, participant testimony and previous actions with limitations.
2. Prepare a suggested facilitation agenda around observations before interpretations.
3. Separate observations, causal hypotheses and candidate lessons; record validation evidence and dissent where supplied.
4. Preserve supplied adoption agreements; label new owners proposed/unassigned. Specify observable success checks and historic outcome gaps.
5. Return useful partial learning material without conclusions requiring absent participation or evidence.

## Output Contract

Return:
1. Purpose, supplied scope/cutoff and a suggested agenda: observations, explanations, lessons, actions.
2. Learning table: `ID/source | observation | causal hypothesis/alternative | practice to repeat/change | validation basis/dissent | candidate/validated/contested`.
3. Actions: `lesson | practice | confirmed/proposed/unassigned owner | supplied date | observable success check | outcome evidence/status`.
4. Only the questions needed for validation. Without participant input, offer a workshop plan and candidate themes, not validated learning. A reported implementation without outcome evidence remains outcome-unverified.

## Ejemplo de uso

Ejemplo sintético ilustrativo; no representa ejecución realizada.

**Pedido:** Invoca g09-zervi-lessons-learned-facilitator. W1: participantes encontraron la aceptación A1 usando el checklist; W2: faltó acceso a la demo. V1 registra validación de los participantes sobre localizar A1; AD1 acuerda pilotar el checklist en la próxima rotación, sin resultado aún.

**Resultado:** Documenta L1 validada solo para localizar aceptación, conserva el límite de acceso de L2 y AD1 acordada con comprobación en la siguiente rotación; no declara adopción exitosa sin resultado posterior.
