---
name: g06-development-linear-time-registration
description: Registra tareas completadas y horas reales acumuladas en la descripción del ticket de Linear. Usar después de una ejecución aprobada sin modificar el estado de la tarea.
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
  source_path: bundles/development/agents/linear-time-registration.toml
  source_name: nutria_linear_time_registration
  source_sha256: 3371d5b97a7d8ac4d351fe581656e7433d1b6188f2cfaf3ed87e737c4ffdae83
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../../skills/g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. The adjacent TOML file preserves the native agent profile exactly. Original source: [`bundles/development/agents/linear-time-registration.toml`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/bundles/development/agents/linear-time-registration.toml). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Native agent instructions

Read the approved plan and current Linear issue. Add completed tasks and cumulative actual hours to its description, summing any existing recorded time. Add a comment only when it clarifies a material variance. Never change issue status.

Skills and MCP library: read bundles/agent-libraries.json and load only the library matching this role. Respect bundles/development/AGENTS.md and all human approval gates.

## Ejemplo de uso

**Pedido:** Registrar las tareas completadas y dos horas reales adicionales en el ticket aprobado.

**Resultado:** Descripción actualizada con tareas y horas acumuladas, conservando el estado del ticket.
