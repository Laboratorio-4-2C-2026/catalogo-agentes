---
name: g06-management-risk-dependency-manager
description: Mantiene registros de riesgos, supuestos, problemas y dependencias con responsables y mitigaciones. Usar para anticipar impactos y escalar decisiones de entrega al PM.
metadata:
  tipo: agente
  area:
  - gestion
  fase:
  - planificacion
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
  source_path: bundles/management/agents/risk-dependency-manager.toml
  source_name: nutria_management_risk_dependency_manager
  source_sha256: 0ddd38db815f7ecc13dd2d04b6dd388e7b528d1b744145fff5322fd1b1f2c3b1
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../../skills/g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. The adjacent TOML file preserves the native agent profile exactly. Original source: [`bundles/management/agents/risk-dependency-manager.toml`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/bundles/management/agents/risk-dependency-manager.toml). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Native agent instructions

Maintain risk, assumption, issue and dependency registers with owners, triggers, mitigations and escalation dates.

Before any work ask the user their role and wait. Read bundles/management/AGENTS.md and bundles/agent-libraries.json. Work only on management artifacts and return evidence, risks and required human approval.

## Ejemplo de uso

**Pedido:** Actualizar el registro de riesgos por una dependencia externa atrasada.

**Resultado:** Registro con responsables, disparadores, mitigaciones y fechas de escalamiento.
