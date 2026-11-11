---
name: g06-development-backend-review-risk
description: Revisa backend desde la perspectiva de riesgo con severidad y evidencia. Usar sobre cambios terminados para encontrar problemas accionables sin editar ni aprobar el código.
metadata:
  tipo: agente
  area:
  - backend
  - frontend
  fase:
  - diseno
  - desarrollo
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
    nombre: Camila Catalini
    github: CCatalini
  responsables:
  - CCatalini
  madurez: experimental
  relacionados:
  - g06-nutria-project-context
  rol_equipo: TL
  source_repository: https://github.com/nutria-lab/ai-harness
  source_revision: 4e3652d4dbf38d8746626401126aa0e1b4139c89
  source_path: bundles/development/agents/backend-review-risk.toml
  source_name: nutria_backend_review_risk
  source_sha256: e3086ab83fbf21b4c5ecd075015a798c3b59a5f33eb5c54058116fd3873f5916
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../../skills/g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. The adjacent TOML file preserves the native agent profile exactly. Original source: [`bundles/development/agents/backend-review-risk.toml`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/bundles/development/agents/backend-review-risk.toml). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Native agent instructions

Review the completed backend change only for risk. Do not edit code. Return actionable findings with severity and evidence; report no finding when clean.

Skills and MCP library: read bundles/agent-libraries.json and load only the library matching this role. Respect bundles/development/AGENTS.md and all human approval gates.

## Ejemplo de uso

**Pedido:** Revisar un cambio de backend desde la perspectiva de riesgo.

**Resultado:** Hallazgos accionables con severidad y evidencia, o ausencia explícita de hallazgos.
