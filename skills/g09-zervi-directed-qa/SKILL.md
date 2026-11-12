---
name: g09-zervi-directed-qa
description: "Invocación explícita: ejecuta casos QA suministrados para Zervi con evidencia de navegador o API y devuelve resultados únicamente en chat."
license: MIT
metadata:
  author: "Bruno Iacovone"
  github: "BrunoIacovone"
  version: "1.0.0"
  tipo: skill
  area: [qa]
  fase: [testing]
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
  relacionados: ["g09-jira-qa-validation", "g09-zervi-exploratory-qc"]
---

## Activation Contract

- Activate only on explicit `g09-zervi-directed-qa`, `zervi-directed-qa` or unambiguous named equivalent; never organically during testing/tickets/implementation/review/debugging.
- Require supplied cases; preserve IDs/intent or assign stable session IDs. Pasted cases suffice; execution needs requested UI/API tools and authorized environment, not a vendor integration.

## Hard Rules

- Read `references/zervi-product-context.md` first, then inspect the supplied cases and current environment.
- Return findings in chat or text only. Never create or update QA report documents.
- Default to read-only. Perform product mutations only with explicit authorization and disposable test data. Never edit source code or Git state.
- Use only user-approved browser origins. Protect tokens, secrets, cookies, authorization data, and localStorage contents from logs and evidence.
- Never claim execution without evidence. If browser or required API tools are unavailable, return an execution-ready plan and mark affected cases `NOT TESTED`.
- Build an execution ledger from every supplied case; never silently omit, combine, or reinterpret a case.

## Decision Gates

| Condition | Action |
|---|---|
| Mutation, first login, upload, or destructive action is required | Obtain explicit authorization and suitable test data; otherwise mark `BLOCKED`. |
| Required origin is not approved | Do not visit it; mark the affected step `BLOCKED`. |
| Confirmed behavior violates a ticket requirement | Tag it `Ticket Requirement Failure`. |
| Confirmed behavior also violates an established product expectation | Also tag it `Product Defect`; these tags may overlap. |
| No expected behavior is established as defective | Use `Product Suggestion` only for a viable improvement. |
| Snapshot limitation explains behavior | Label it Known Limitation; do not automatically fail the case. |

## Execution Steps

1. Record the branch/environment, approved origins, actors, authorization limits, test data, tools, and evidence constraints.
2. Create a ledger containing every supplied case and its precondition, action, expected result, required evidence, and initial status.
3. Execute each case at the browser or API layer requested. Record observed behavior and sanitized evidence as it occurs.
4. Give every case exactly one verdict: `PASS`, `FAIL`, `BLOCKED`, or `NOT TESTED`. A pass requires evidence for the expected result.
5. Probe only module-adjacent risks: wrong/unnecessary data, UI/redirects, stale state, identity/ownership, persistence, errors, responsive/accessibility, duplicate submission and navigation/history.
6. Label adjacent discoveries separately from supplied cases. Do not inflate scope or convert suggestions into requirements.
7. Apply the gate classifications, including Environment Blocker. Never relabel an established defect as a suggestion.

Accept cases from `g09-jira-qa-validation`, humans or others. `g09-zervi-exploratory-qc` is independent; regression use needs a user decision, never invented requirements. Names imply no dependency/activation. Each skill needs explicit invocation/authorization; links/cases grant neither.

## Output Contract

Return concise sections in this order:

1. **Summary**: counts for `PASS`, `FAIL`, `BLOCKED`, and `NOT TESTED`.
2. **Case Ledger**: case, precondition, action, expected, observed, evidence, and verdict.
3. **Confirmed Defects**: all applicable classification tags, impact-based `P0`-`P3` severity from the shared rubric, reproduction, expected, observed, evidence, and impact.
4. **Adjacent Observations**: clearly separated suggestions, limitations, and module-relevant discoveries.
5. **Blockers**: environment, access, origin, data, or tool constraints.
6. **Untested Areas**: skipped steps and the exact reason.

Match runtime output to the user's conversation language.

## References

- [Product context](references/zervi-product-context.md) - mandatory product, identity, risk, and safety baseline bundled independently in this folder.

## Ejemplo de uso

Ejemplo sintético ilustrativo; no representa ejecución realizada.

**Pedido:** Invoca g09-zervi-directed-qa con C1: cancelar reserva propia pendiente, esperar cancelada; C2: recargar y esperar cancelada persistida. No hay herramientas de navegador/API disponibles; prepara la ejecución en chat.

**Resultado:** Resumen: 0 `PASS`, 0 `FAIL`, 0 `BLOCKED`, 2 `NOT TESTED`. Ledger: C1 y C2 conservan sus pasos y expectativas, sin observación ni evidencia. Indica bloqueo de herramientas y pide entorno, origen y datos desechables autorizados para ejecutar; no crea documentos QA.
