---
name: g06-nutria-project-context
description: Aplica el alcance del MVP NutrIA y sus límites de producto a una solicitud concreta. Usar para contrastar funcionalidades con criterios de aceptación y exclusiones.
license: MIT
metadata:
  author: NutrIA
  version: 0.1.0
  tipo: skill
  area:
  - gestion
  fase:
  - analisis
  - planificacion
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
  relacionados: []
  rol_equipo: PM
  source_repository: https://github.com/nutria-lab/ai-harness
  source_revision: 4e3652d4dbf38d8746626401126aa0e1b4139c89
  source_path: skills/nutria-project-context/SKILL.md
  source_name: nutria-project-context
  source_sha256: 601d7a84cc2b7b9ea27f31a85454f15fad4c7ffd989ed1818f0e79f37757508c
  source_description: 'Trigger: NutrIA feature, scope, product decision. Apply the MVP scope, domain boundaries and delivery constraints.'
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. Original source: [`skills/nutria-project-context/SKILL.md`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/skills/nutria-project-context/SKILL.md). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Activation Contract
Load for any NutrIA work.

# Hard Rules
- Product scope: profile/preferences, weekly plans, recipes, shopping list and adherence.
- Do not make medical, diagnostic or treatment claims.
- The user decides; AI proposes and explains.
- Treat the charter as product context, not runtime truth; confirm current Linear issues.

# Execution Steps
1. Read the relevant Linear issue and acceptance criteria.
2. Identify affected epic and non-goals.
3. State assumptions before implementation.
4. Attach evidence to the issue after validation.

# Output Contract
Return scope, assumptions, acceptance evidence and outstanding decisions.


## Ejemplo de uso

**Pedido:** Evaluar si una propuesta de seguimiento alimentario pertenece al MVP NutrIA.

**Resultado:** Alcance, supuestos, exclusiones y evidencia necesaria para la decisión del PO.
