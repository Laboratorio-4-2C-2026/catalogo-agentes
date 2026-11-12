---
name: g16-tests-review
description: 'Checklist para encontrar el comportamiento nuevo o cambiado que ningún test ejercita en un PR de Eureka (lib/, app/api/, contratos y Supabase): dónde viven los tests, qué cuenta como faltante y cómo proponer el caso concreto. Es el checklist que carga g16-eureka-revisor-tests.'
metadata:
  tipo: skill
  area:
  - qa
  fase:
  - revision
  - testing
  tecnologias:
  - typescript
  - foundry
  - supabase
  herramientas:
  - claude-code
  requiere: []
  grupo: "16"
  autor:
    nombre: Valentino Gianuzzo
    github: ValentinoGianuzzo
  responsables:
  - ValentinoGianuzzo
  madurez: experimental
  relacionados:
  - g16-eureka-revisor-tests
  - g08-qa-engineer
---

# Eureka tests review

The Definition of Done asks for "Tests pasando", and Eureka DoD checks that the
PR shows evidence of it. Passing says nothing about what is not tested: a PR can
add a new failure path, a new route or a new contract function and keep every
existing test green. This review finds the behavior the PR adds or changes that
no test exercises, and proposes the cases that are missing.

It does not judge whether the tests pass (that is DoD) and does not look for
bugs in the code (the other reviewers do). If the diff only touches tests,
docs, styles or configuration, say so in a single comment and stop.

## Where the tests live

| Code | Tests |
|---|---|
| `lib/` | `test/lib/` (Vitest, mocked Supabase) |
| `app/api/` | `test/app/` (Vitest) |
| `visual_pages/` | `test/visual_pages/` |
| SQL functions and RLS in `supabase/` | `test/integration/` (Vitest against a real Supabase, see `vitest.integration.config.ts`) |
| `contracts/src/` | `contracts/test/` (Foundry), `*Pentest.t.sol` and `*Invariant.t.sol` for adversarial cases |
| User flows | `cypress/e2e/` |

Before saying a test is missing, search for it: a case may be covered by an
existing test outside the diff. Read the test files for the module the PR
changes, not only the ones in the diff.

## Priority order

1. Money and authorship paths: credits, reservations, payments, minting,
   registration, sharing and access keys
2. Failure paths of anything new: errors, reverts, rejected inputs, timeouts
3. Authorization: who can call a route or a contract function, and that
   anyone else is rejected
4. New branches in existing logic
5. Happy paths of new code

Stop expanding scope once the first items are covered: a short list of the
cases that matter beats an exhaustive one.

## What counts as missing

- A new route, function or contract method with no test at all.
- A new `if`, `catch`, `require` or `revert` whose branch no test reaches.
- A guard that lives in SQL (a `where status = …`, a policy, a constraint)
  tested only with mocked Supabase. A mock does not prove a SQL guard: the
  case belongs in `test/integration/`.
- A contract change tested only on the happy path. Failure paths are required
  by the PR template ("cubren los caminos de falla").
- A bug fix with no test that fails before the fix.

Not missing: trivial getters, type-only changes, renames, copy changes, and
code already exercised by an existing test you found.

## How to report

- One comment per missing case, anchored to the line of the untested behavior.
- Open each with a severity tag: `[Crítico]`, `[Alto]`, `[Medio]`, `[Bajo]`.
  - `[Crítico]`: an untested path that can move credits, mint, register or
    expose access keys.
  - `[Alto]`: an untested failure or authorization path.
  - `[Medio]`: an untested branch in other logic, or a SQL guard tested only
    with mocks.
  - `[Bajo]`: an untested happy path of low-risk code.
- Propose the test concretely: the file where it goes, a test name, and one
  line each for setup, action and expected result.
- If you are not sure the case is uncovered (it may be tested indirectly),
  say so.
- Do not comment on formatting, naming or style of the tests.

## Ejemplo de uso

**Pedido:** «Con la skill de tests, decime qué casos le faltan a este PR que agrega una función al contrato.»

**Resultado:** Busca los tests existentes en `test/`, `contracts/test/` y `cypress/e2e/`, y por cada comportamiento sin cubrir propone el test: archivo, nombre, setup, acción y resultado esperado.
