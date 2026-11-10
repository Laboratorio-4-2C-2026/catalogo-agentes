---
name: g06-product-backlog
description: Convierte necesidades de producto en historias con criterios de aceptación verificables. Usar para refinar backlog por valor de usuario y mantener la prioridad bajo aprobación del PO.
license: MIT
metadata:
  author: NutrIA
  version: 0.1.0
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
  - analisis
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
    nombre: Tomás Alcázar
    github: tomasalcazar
  responsables:
  - tomasalcazar
  madurez: experimental
  relacionados:
  - g06-nutria-project-context
  rol_equipo: PO
  source_repository: https://github.com/nutria-lab/ai-harness
  source_revision: 4e3652d4dbf38d8746626401126aa0e1b4139c89
  source_path: skills/product-backlog/SKILL.md
  source_name: product-backlog
  source_sha256: a5c29cef2b879329f5da8269b641cf8052e8d56e87e518f758872d6301565217
  source_description: 'Trigger: user story, acceptance criteria, backlog refinement, epic, priority. Create testable NutrIA product work.'
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. Original source: [`skills/product-backlog/SKILL.md`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/skills/product-backlog/SKILL.md). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Activation Contract
Use to turn product requests into Linear issues.

# Hard Rules
- Each issue has a user outcome, non-goals, acceptance criteria and UX states.
- Keep clinical advice outside the product scope.
- Do not split work by frontend/backend alone; split by user value and verifiable increment.

# Execution Steps
1. Map request to NutrIA epic.
2. Write a concise story and measurable acceptance criteria.
3. Add failure, empty, loading and restricted-input cases.
4. Identify dependencies and QA evidence.

# Output Contract
Return a ready-to-review Linear issue draft, not an unapproved issue mutation.


## Ejemplo de uso

**Pedido:** Refinar una historia para modificar una comida del plan semanal.

**Resultado:** Historia con resultado esperado, límites, estados de error y criterios verificables.
