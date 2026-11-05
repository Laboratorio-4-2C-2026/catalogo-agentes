---
name: g02-acceptance-criteria-to-tests
description: Método en dos fases para derivar casos de prueba solo desde los criterios de aceptación de un ticket, antes de leer el código. Usar al escribir tests independientes de la implementación.
metadata:
  tipo: skill
  area:
  - qa
  fase:
  - testing
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: '02'
  autor:
    nombre: Liz Lubelcyk
    github: lizlubelczyk
  responsables:
  - lizlubelczyk
  madurez: usado-en-proyecto
  relacionados:
  - g02-e2e-test-writer
---
# Deriving test cases from acceptance criteria

Work in two phases. Do not merge them.

## Phase 1 — Derive (no source code)

Read only the ticket: description, acceptance criteria, and the numbered
tasks. Do not open the diff, any source file, or any existing spec.

Produce a numbered list. For each case:
- the input or starting state
- the expected outcome, stated concretely
- the acceptance criterion it traces to

Cover the happy path, each stated edge case, and each stated error
condition. Do not invent cases with no traceable criterion.

If a criterion is too vague to test — a number left unspecified, an
undefined behaviour past a boundary — list it under "Underspecified" and
say what's missing. Do not resolve the ambiguity by reading the code.

Write this list to `derived-cases.md` in the zest-support working directory
before opening any source file. Once written, do not edit it. If Phase 2
reveals a case you got wrong, note the correction in your final report —
do not rewrite the derivation.

## Phase 2 — Implement

Now read the source, but only for mechanics: names, signatures, routes,
selectors, how existing tests are set up.

Re-read derived-cases.md before writing each spec. The expected values there
are authoritative, even where the implementation disagrees.

Write one test per Phase 1 case, keeping the expected values exactly as
written in Phase 1.

## Rules that override convenience

- Never change an expected value to make a test pass.
- A failing test is a finding. Report it; do not fix it.
- Never add cases that don't trace to a criterion.
- Report pass/fail per acceptance criterion, not per test file.

## Ejemplo de uso
**Pedido:** Derivá los casos de prueba del ticket ZEST-87.
**Resultado:** Genera derived-cases.md con los casos trazados a cada criterio y los criterios ambiguos, sin abrir el código, y recién después implementa los tests.
