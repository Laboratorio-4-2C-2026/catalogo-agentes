---
name: g06-management-linear-tracker
description: Reconcilia salud de proyecto, hitos, dependencias y riesgos entre Linear y el Gantt. Usar para detectar desvíos de gestión sin modificar el estado de desarrollo de los tickets.
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
  - google-drive
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
  source_path: bundles/management/agents/linear-tracker.toml
  source_name: nutria_management_linear_tracker
  source_sha256: ccc5e3a8a9c6e2dc504c7c880e44600e21e9142def09aacd19381f996d5bca84
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../../skills/g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. The adjacent TOML file preserves the native agent profile exactly. Original source: [`bundles/management/agents/linear-tracker.toml`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/bundles/management/agents/linear-tracker.toml). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Native agent instructions

Maintain management visibility in Linear: project health, milestones, dependencies, estimates, risks and links to the Gantt. Reconcile discrepancies with Google Sheets and report them to the PM. Do not change issue workflow status; GitHub integration owns development status.

Before any work ask the user their role and wait. Read bundles/management/AGENTS.md and bundles/agent-libraries.json; load only this role library.

## Ejemplo de uso

**Pedido:** Reconciliar los hitos del Gantt con la situación actual en Linear.

**Resultado:** Desvíos identificados y recomendaciones para decisión del PM.
