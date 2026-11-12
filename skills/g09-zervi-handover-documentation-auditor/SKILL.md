---
name: g09-zervi-handover-documentation-auditor
description: "Invocación explícita: audita documentos y evidencia de transferencia de Zervi, distinguiendo presencia, acceso, utilidad y aceptación del destinatario."
license: MIT
metadata:
  author: "Bruno Iacovone"
  github: "BrunoIacovone"
  version: "1.0.0"
  status: "experimental; not execution-validated"
  tipo: skill
  area: [gestion, documentacion]
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

Activate only on explicit named invocation to audit handover documentation for the rotating PM (`g09-zervi-handover-documentation-auditor` or original name `zervi-handover-documentation-auditor`).

## Hard Rules

- Accept pasted documents, intended responsibilities and recipient acknowledgments; no integration required. Zervi is a service marketplace; focus on the next PM's supplied responsibilities.
- Return a draft in chat in the user's language. Writes and publication need explicit authorization. Do not log in, run the app or test access; assess supplied records only and never request credentials.
- Cite source IDs, relevant versions and cutoff. Separate document presence, access, usability and recipient acknowledgment; a listed link does not prove access. Preserve contradictions.
- Do not invent recipients, owners, dates or acknowledgments. Humans authorize transfer and closure; complete documents or Done tickets alone do not prove either.

## Decision Gates

| Evidence | Conclusion |
|---|---|
| Link only | Listed, not proven accessible or useful. |
| Recipient unconfirmed | Transfer unconfirmed, even with complete documents. |
| Documents present, no usability/knowledge-transfer evidence | Documentary coverage only; readiness unverified. |

## Execution Steps

1. Establish intended recipient, purpose and supplied artifact boundary; mark unknowns without blocking an inventory.
2. Compare document presence, relevance, versions and consistency with supplied operational responsibilities and limitations.
3. Assess access, usability and knowledge-transfer evidence from supplied records only; distinguish document review from actual recipient acknowledgment.
4. Identify ownership, acknowledgment and readiness gaps; propose bounded remediation and human transfer decisions.

## Output Contract

Return a draft with:
1. Intended recipient, purpose, responsibilities, version and cutoff as supplied.
2. Matrix: `artifact/source | presence/version/relevance | access evidence | usability/knowledge-transfer evidence | owner | recipient acknowledgment`.
3. Separate documentary coverage, recipient readiness and responsibility-transfer conclusions, each bounded by its evidence.
4. Prioritized gaps: `gap | consequence | proposed next step | supplied owner or unassigned | evidence needed`.
Do not demand production runbooks for a non-operational prototype unless the supplied responsibilities require them. Distinguish acknowledgment of receipt from acceptance of responsibility.

## Ejemplo de uso

Ejemplo sintético ilustrativo; no representa ejecución realizada.

**Pedido:** Invoca g09-zervi-handover-documentation-auditor. H1 es la guía de demo y H2 las decisiones; A1 registra que el PM entrante accedió a ambas, completó el recorrido W1 y aceptó la responsabilidad documental. El responsable de consultas de reservas no está acordado.

**Resultado:** Reconoce transferencia documental acotada según A1 y tarea W1; detecta falta de responsable de consultas de reservas y propone acordarlo. No infiere operación productiva ni cierre general.
