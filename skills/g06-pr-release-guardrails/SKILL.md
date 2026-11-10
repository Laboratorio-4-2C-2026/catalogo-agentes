---
name: g06-pr-release-guardrails
description: Evalúa evidencia de pruebas, CI, migraciones y reversión antes de un merge o release. Usar para producir una recomendación sin aprobar ni desplegar automáticamente.
license: MIT
metadata:
  author: NutrIA
  version: 0.1.0
  tipo: skill
  area:
  - qa
  - devops
  fase:
  - revision
  - despliegue
  tecnologias:
  - git
  metodologia:
  - scrum
  herramientas:
  - codex
  - claude-code
  - otra
  requiere:
  - github
  - linear
  - engram
  grupo: "06"
  autor:
    nombre: Felipe Fernandez Cronenbold
    github: sonpipe0
  responsables:
  - sonpipe0
  madurez: experimental
  relacionados:
  - g06-nutria-project-context
  rol_equipo: PM
  source_repository: https://github.com/nutria-lab/ai-harness
  source_revision: 4e3652d4dbf38d8746626401126aa0e1b4139c89
  source_path: skills/pr-release-guardrails/SKILL.md
  source_name: pr-release-guardrails
  source_sha256: 7005ec2db0f8e146f30658ef7ac05eb6493266db04241012880d6b63e86307f8
  source_description: 'Trigger: PR review, CI, release, deploy, rollback. Assess NutrIA changes before human approval.'
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. Original source: [`skills/pr-release-guardrails/SKILL.md`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/skills/pr-release-guardrails/SKILL.md). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Activation Contract
Use before merge or release.

# Hard Rules
- No automatic merge, deploy or approval.
- Check linked Linear issue, tests, migration safety, secrets, performance and accessibility impact.
- A missing test is an explicit risk, not a passing check.

# Execution Steps
1. Reconcile diff to acceptance criteria and architecture decision.
2. Inspect CI/test evidence and migration/rollback plan.
3. Return only actionable findings by severity.
4. Link findings to Linear and preserve release learnings in Engram.

# Output Contract
Return ready/not-ready recommendation, evidence and owner for each blocker.


## Ejemplo de uso

**Pedido:** Revisar la evidencia de un PR de lista de compras antes de recomendar su release.

**Resultado:** Hallazgos accionables y riesgos pendientes con aprobación humana requerida.
