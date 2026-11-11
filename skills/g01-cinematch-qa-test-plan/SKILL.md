---
name: g01-cinematch-qa-test-plan
description: "Arma el plan de pruebas de QA para cada ticket de Cinematch en revisión (o para un ticket o PR puntual), decidiendo qué probar a partir de sus criterios de aceptación y del diff real, con los flujos paso a paso y lo que ya cubren los tests del PR. Usala cuando preguntan qué probar, casos o flujos de prueba antes de un merge o una demo; es de solo lectura sobre Linear y GitHub."
author: Francisco
metadata:
  tipo: skill
  area:
  - qa
  fase:
  - testing
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - linear
  - github
  grupo: "01"
  autor:
    nombre: Francisco Zizzi
    github: FranciscoZizzi
  responsables:
  - FranciscoZizzi
  madurez: probado
  relacionados:
  - g01-cinematch-issue-draft
  - g01-cinematch-pm-weekly
---
# Cinematch QA test plan

A ticket is ready to merge when its acceptance criteria are proven against the running app, not when the diff looks right. This skill turns each ticket in review into the concrete flows that prove it, and says which ones the PR's own tests already prove so QA spends its time on the rest.

Plans are in Spanish, following the vault's [AGENTS.md](../../../AGENTS.md). A flow that becomes an automated test is named in English, following the app repository's `AGENTS.md`.

Read-only: it comments on no PR, moves no issue and commits nothing to the app repository. A gap is reported with who should close it: the author for missing tests, the PO for a criterion that cannot be checked.

## 1. Pick the tickets

A named ticket or PR is the whole set. Otherwise the set is:

- every `CIN` issue in Linear with status In Review (`list_issues`, `team: CIN`, `state: In Review`, paginating while `hasNextPage`);
- every open PR from `python3 ../g01-cinematch-pm-weekly/scripts/pm.py blockers`, which also catches a ticket marked Done whose PR is still open: it counts as in review.

A ticket In Review whose PR already merged (`pm.py prs`) stays in the set, tested on `main` instead of the branch, and its stale status goes to the PO.

Order them by what the next milestone needs first: `Critical Path` label, then earliest due date. `pm.py calendar` gives the milestone.

## 2. Read each ticket and its PR

For each ticket, all of it:

- **The issue**: `get_issue` and `list_comments`. Its description follows [cinematch-issue-draft](../g01-cinematch-issue-draft/SKILL.md): `Objetivo`, `Alcance`, `No incluye`, `Criterios de aceptación` (given/when/then) and `Dependencias`. A user story (`[US ...]`) is tested through its `[T]` children.
- **The PR**: `gh pr view <n> -R Lab-2-Cinematch/lab2-cinematch-app --json title,body,files,baseRefName,reviews,statusCheckRollup` and `gh pr diff <n> -R Lab-2-Cinematch/lab2-cinematch-app`.
- **The code it touches**, enough to name the real screen, route, endpoint, error message and feature flag in each flow. The local checkout of the app repository is read-only context; it may be behind the PR, so the diff wins.
- **Its tests**: the `*.spec.ts` and `test/*.e2e-spec.ts` files in the diff, read case by case.

Done when you can name, for each acceptance criterion, the code that implements it.

## 3. Decide what to test

Build the coverage matrix: every acceptance criterion is one row, and gets at least one flow. Then add the rows the criteria miss:

- **Diff outside the criteria**: behaviour the PR adds or changes that no criterion asks for. Test it, and flag it as scope the ticket did not describe.
- **`No incluye` boundaries**: the ticket must not do them, and the neighbouring issue that will must still be possible.
- **Regressions**: features that share a changed file, endpoint or component with this PR. The diff's file list says which.
- **Edge cases**, each one only where it applies to this ticket: empty state, provider or LLM down, another user's data, a second session or a second group member at the same time, an expired session, quota or rate limit reached, the mobile viewport (the frontend is mobile-first, 390-410 px), and no new console errors or warnings (open since the [Steering 1 feedback](../../../Demos/Primera%20(17-09)/Feedback.md)).

For each row, mark it **Automatizado** when a test in the PR proves it against the behaviour, not only against a mock of it, and **Manual** otherwise. A criterion that says `verificable contra el backend corriendo` is Manual even when a mocked test exists.

Done when every criterion, every out-of-criteria change and every regression area has a row.

## 4. Write the flows

Each Manual row gets a flow a person can run cold:

- **Precondiciones**: environment (local with `npm run seed` in `apps/backend`, or the deployed one), the accounts it needs and how many, the data it starts from, the PR branch (`gh pr checkout <n>`), and any flag to turn on.
- **Pasos**, numbered, each one action on a named screen or a request to a named endpoint (`curl` against `http://localhost:3000` for backend-only tickets, with how to get the session).
- **Resultado esperado** after the step that checks it, observable on screen, in the response or in the database. "Funciona" is not a result.

Backend tickets get API flows; frontend tickets get UI flows on a 390 px viewport; a ticket that connects both gets one end-to-end flow plus the API flow for its error cases.

## 5. Report

In chat, one section per ticket, in the order of step 1:

1. **Encabezado**: ticket, title, PR, author, review state, CI, due date, and what it blocks.
2. **Matriz de cobertura**: criterion or area → flow → Automatizado / Manual, with the test name when automated.
3. **Flujos**: the Manual flows from step 4.
4. **Huecos**: criteria that cannot be checked as written, changes no criterion covers, missing tests, and who closes each.

End with one line per ticket: what QA has to run before it merges. Save the plan to the vault only when asked, as `Code Review/<yyyy-mm-dd> Plan de pruebas <CIN-NN>.md`, with `description` and `author` in its frontmatter.

## Ejemplo de uso

**Pedido:** ¿Qué tiene que probar QA de lo que está en review?

**Resultado:** Devuelve en español, por cada ticket en revisión, los flujos de prueba paso a paso derivados de sus criterios de aceptación, marcando cuáles ya cubren los tests del PR y a quién corresponde cada hueco.
