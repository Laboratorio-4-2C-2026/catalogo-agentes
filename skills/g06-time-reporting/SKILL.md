---
name: g06-time-reporting
description: Analiza horas reales y capacidad con registros vinculados a tickets, sin inferir esfuerzo desde commits. Usar para calibrar planificación y explicar desvíos de entrega.
license: MIT
metadata:
  author: NutrIA
  version: 0.1.0
  tipo: skill
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
  source_path: skills/time-reporting/SKILL.md
  source_name: time-reporting
  source_sha256: 98262ea79786028dff8a2a453742534def3b2a31a4ee9ec2d2a3a2d8f30abae4
  source_description: 'Trigger: hours, effort, capacity, time tracking, Harvest, weekly allocation. Report team time ethically.'
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. Original source: [`skills/time-reporting/SKILL.md`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/skills/time-reporting/SKILL.md). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Activation Contract
Use when analyzing actual hours or capacity.

# Hard Rules
- Actual hours come from the configured tracker linked to Linear issues.
- Do not derive working hours from commits, chat activity or agent output.
- Never rank people or infer performance from time entries.
- Group reports by workstream and project first; show individual detail only to authorized PM/TL.

# Execution Steps
1. Verify time entries map to a Linear issue and date range.
2. Compare actual hours with estimates as calibration, not a productivity score.
3. Highlight missing, duplicate or unlinked entries.
4. Recommend capacity or scope changes.

# Output Contract
Return totals, variance, data-quality caveats and decisions needed.


## Ejemplo de uso

**Pedido:** Comparar las horas registradas del ciclo con sus estimaciones originales.

**Resultado:** Un reporte por proyecto y línea de trabajo con desvíos y calidad de datos explícitos.
