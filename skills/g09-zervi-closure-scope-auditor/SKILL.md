---
name: g09-zervi-closure-scope-auditor
description: "Invocación explícita: audita la trazabilidad del alcance de cierre de Zervi y separa entrega, aceptación y evidencia pendiente."
license: MIT
metadata:
  author: "Bruno Iacovone"
  github: "BrunoIacovone"
  version: "1.0.0"
  status: "experimental; not execution-validated"
  tipo: skill
  area: [gestion, qa]
  fase: [analisis, revision]
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

Activate only on explicit named invocation for the rotating PM's closure scope review (`g09-zervi-closure-scope-auditor` or original name `zervi-closure-scope-auditor`). Authoring this skill is not activation.

## Hard Rules

- Accept pasted baseline, changes, criteria and delivery/acceptance records; no integration required. Zervi is a marketplace connecting clients with service providers; assess only supplied commitments.
- Return a draft in chat in the user's language. File writes and publication need explicit authorization; do not operate the app or external services.
- Cite source IDs, version/environment and cutoff when supplied. Separate facts, reported claims and proposals; a link alone is not verified evidence. Preserve conflicts and mark consequential gaps without inventing data.
- Done/green is not acceptance. Humans approve the baseline, delivery acceptance and closure; keep their decisions separate from this assessment.

## Decision Gates

| Input | Result |
|---|---|
| No approved baseline | Provisional inventory; no scope-compliance verdict. |
| Done without supporting evidence | Reported-delivered; acceptance-unverified. |
| Conflicting versions or approvals | Show competing sources; request human resolution. |

## Execution Steps

1. Inventory supplied baseline, approved changes, acceptance criteria, delivery and acceptance evidence; mark unknowns.
2. Map each commitment and criterion to delivery evidence and separate acceptance evidence, including approving authority when supplied.
3. Identify omissions, additions, deviations and evidence gaps without treating unsupported items as failures.
4. Draft bounded findings and decision requests; complete useful partial output while withholding unsupported conclusions.

## Output Contract

Return a draft with:
1. Boundary: approved baseline/source, delivery version, environment and cutoff; state whether a scope verdict is supportable.
2. Matrix: `commitment/criterion | baseline/change source | delivery evidence/status | acceptance evidence/authority/status | gap`.
3. Deviations and next human decisions, each tied to the affected criterion and needed evidence. Use provisional inventory if baseline approval is missing; do not calculate compliance from ticket counts.

## Ejemplo de uso

Ejemplo sintético ilustrativo; no representa ejecución realizada.

**Pedido:** Invoca g09-zervi-closure-scope-auditor. B1 aprobada exige publicar servicios y cancelar reservas propias; D1 documenta publicación, D2 cancelación y A1 registra aceptación del PO solo de publicación.

**Resultado:** C1 queda entregado y aceptado según D1/A1; C2 entregado según D2 pero pendiente de aceptación. Solicita al PO decidir C2, sin convertir la aceptación parcial en cierre del proyecto.
