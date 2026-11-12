---
name: g09-jira-qa-validation
description: "Invocación explícita: convierte un ticket Jira de Zervi en casos QA trazables y ejecutables, con requisitos, evidencia y bloqueos separados."
license: MIT
metadata:
  author: "Bruno Iacovone"
  github: "BrunoIacovone"
  version: "1.0.0"
  tipo: skill
  area: [qa]
  fase: [analisis, testing]
  tecnologias: [agnostico]
  metodologia: [agnostico]
  herramientas: [otra]
  requiere: []
  grupo: "09"
  autor:
    nombre: Bruno Iacovone
    github: BrunoIacovone
  responsables: [BrunoIacovone]
  madurez: usado-en-proyecto
  relacionados: ["g09-zervi-directed-qa", "g09-zervi-exploratory-qc"]
---

# Jira QA Validation

## Activation Contract

- Activate only on explicit `g09-jira-qa-validation`, `jira-qa-validation`, "Jira QA validation" or unambiguous equivalent for Zervi; never organically during implementation/review/debugging/testing.
- Accept pasted tickets and supplied criteria, implementation, branch, environment or evidence; no Jira integration required.

## Hard Rules

- Work only for Zervi. Match runtime output to the user's conversation language.
- Separate requirements, suggestions and exclusions; never promote suggestions.
- Never invent criteria, codes, routes, roles, data, environments, commands or results. Mark gaps `ASSUMPTION`, `QUESTION` or `BLOCKED`.
- Default read-only: code, migrations, fixtures, Git, DB edits and mutating checks require explicit authorization.
- Inspect available implementation/branch read-only; tailor cases to real contracts/permissions. Separate `OBSERVED` evidence from `EXPECTED` requirements; never claim unevidenced execution.
- Rank requirement-linked cases by risk, including relevant negatives.

## Decision Gates

| Condition | Action |
|---|---|
| Explicit requirement | Link cases and expected results. |
| Necessary detail missing | Record assumption/question; block unreliable cases. |
| Beyond ticket | Suggestion/exclusion, not required coverage. |
| Irrelevant behavior | Omit; explain only material risk. |
| No execution evidence | `NOT TESTED` or `BLOCKED`, never `PASS`. |

## Execution Steps

1. Inventory requirements with stable IDs: objective, scope, dependencies, criteria, required tests, rules, permissions, actors, transitions, errors, exclusions and evidence.
2. Classify every item as Ticket Requirement, Product Suggestion, Out of Scope, Assumption, Question, or Blocker. Flag contradictions and missing testability details.
3. Inspect supplied implementation read-only: code, routes, schemas, tests and repository-defined commands. Cite observed-versus-expected differences.
4. Build minimal risk-ranked coverage. Consider happy/negative paths, validation, auth/ownership/tenant boundaries, errors, UI states, persistence, transitions, retries/races, responsive/accessibility requirements and regressions only where relevant.
5. Give each case: ID, priority/risk, requirement ID, layer (`frontend`, `backend`, `integration`), actor, preconditions/data, steps, expected result, evidence needed and initial verdict.
6. Group Manual UI, API, DB/Persistence and Automated/Checks. Use only supplied or discovered commands; identify gaps.
7. Map every requirement to cases or blockers; flag uncovered requirements and unnecessary cases.

Optional: cases → `g09-zervi-directed-qa` (also human/other cases); `g09-zervi-exploratory-qc` explores independently. Names imply no dependency/activation. Each needs explicit invocation/authorization; exploratory regression proposals need a user decision, never automatic ticket requirements.

## Output Contract

Return these sections in order:

1. **Ticket Interpretation:** inventory from step 1.
2. **Gaps and Classification:** assumptions, questions, blockers, suggestions, contradictions, observed/expected differences.
3. **Traceability Matrix:** requirement, criterion, cases, coverage, evidence needed.
4. **Test Cases:** groups/fields above.
5. **Execution Summary:** exactly one evidenced `PASS`, `FAIL`, `BLOCKED` or `NOT TESTED` per case.
6. **Defects:** severity, title, reproduction, expected/actual, evidence, impact, criterion.
7. **QA Verdict:** status, highest risks, blockers, minimum next action.

## References

- Treat the Jira ticket and explicitly available Zervi implementation evidence as runtime inputs; no other local dependency.

## Ejemplo de uso

Ejemplo sintético ilustrativo; no representa ejecución realizada.

**Pedido:** Invoca g09-jira-qa-validation. T1: AC1 exige cancelar una reserva propia pendiente y conservar el estado al recargar; AC2 prohíbe cancelar reservas ajenas. Solo se aporta el ticket, sin implementación ni evidencia de ejecución.

**Resultado:** R1→C1: con reserva propia pendiente, cancelar y recargar; se espera estado cancelado persistido. R2→C2: intentar cancelar una reserva ajena; se espera rechazo sin cambio. Ambos quedan `NOT TESTED`; pide confirmar contrato de rechazo y datos desechables para ejecución, sin inventar códigos HTTP.
