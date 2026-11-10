---
name: g06-linear-delivery-ops
description: Reconcilia entregas, ciclos, estimaciones y bloqueos usando Linear como fuente de estado. Usar para preparar seguimiento de proyecto con evidencia y aprobación humana.
license: MIT
metadata:
  author: NutrIA
  version: 0.1.0
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
  - mantenimiento
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
  source_path: skills/linear-delivery-ops/SKILL.md
  source_name: linear-delivery-ops
  source_sha256: 37c01a639514c6f5c5fd15e6dea86a62660120716a9881ebdc09275cf728ed52
  source_description: 'Trigger: Linear status, cycle, estimate, hours, blocker, weekly report. Operate NutrIA delivery tracking safely.'
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. Original source: [`skills/linear-delivery-ops/SKILL.md`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/skills/linear-delivery-ops/SKILL.md). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Activation Contract
Use for project-management and reporting tasks in Linear.

# Hard Rules
- Linear is the work-status source of truth.
- Estimate is complexity/capacity, not actual hours.
- Use a linked time tracker for actual hours.
- Read first. Do not reassign, reprioritize, close or change scope without human approval.

# Execution Steps
1. Query project, cycle, issues and statuses.
2. Reconcile linked PR/test evidence before reporting completion.
3. Report committed/completed, estimates, time-in-status, logged hours, blockers and owner.
4. Propose changes; wait for approval before mutations.

# Output Contract
Produce a compact decision-ready status report with source links.


## Ejemplo de uso

**Pedido:** Revisar el avance del ciclo actual y sus bloqueos sin cambiar estados.

**Resultado:** Un resumen de entregas, desvíos y acciones que necesitan decisión del PM.
