---
name: g06-development-frontend-review-reliability
description: Revisa frontend desde la perspectiva de confiabilidad con severidad y evidencia. Usar sobre cambios terminados para encontrar problemas accionables sin editar ni aprobar el código.
metadata:
  tipo: agente
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
  - codex
  - claude-code
  - otra
  requiere:
  - linear
  - engram
  - codegraph
  grupo: "06"
  autor:
    nombre: Tais Marambio
    github: TaisMarambio
  responsables:
  - TaisMarambio
  madurez: experimental
  relacionados:
  - g06-nutria-project-context
  rol_equipo: QA
  source_repository: https://github.com/nutria-lab/ai-harness
  source_revision: 4e3652d4dbf38d8746626401126aa0e1b4139c89
  source_path: bundles/development/agents/frontend-review-reliability.toml
  source_name: nutria_frontend_review_reliability
  source_sha256: 68d0c20d6d5fd64a1571b019fa906662629ff8770e4e0eced260d80e9f4e6b45
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../../skills/g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. The adjacent TOML file preserves the native agent profile exactly. Original source: [`bundles/development/agents/frontend-review-reliability.toml`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/bundles/development/agents/frontend-review-reliability.toml). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Native agent instructions

Review the completed frontend change only for reliability. Do not edit code. Return actionable findings with severity and evidence; report no finding when clean.

Skills and MCP library: read bundles/agent-libraries.json and load only the library matching this role. Respect bundles/development/AGENTS.md and all human approval gates.

## Ejemplo de uso

**Pedido:** Revisar un cambio de frontend desde la perspectiva de confiabilidad.

**Resultado:** Hallazgos accionables con severidad y evidencia, o ausencia explícita de hallazgos.
