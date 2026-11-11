---
name: g06-stitch-ui-workflow
description: Genera y revisa propuestas de interfaz NutrIA usando Stitch como fuente de diseño. Usar para definir estados visuales y preparar el traspaso al desarrollo con aprobación del PO.
license: MIT
metadata:
  author: NutrIA
  version: 0.1.0
  tipo: skill
  area:
  - diseno
  - frontend
  fase:
  - diseno
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
  - stitch
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
  source_path: skills/stitch-ui-workflow/SKILL.md
  source_name: stitch-ui-workflow
  source_sha256: 38444d8ea5634fcde1ecc8b325a751f8548551ae5ecb376205318953bee5be21
  source_description: 'Trigger: Stitch UI, screen generation, design refinement, responsive UI. Use Stitch rather than Figma for NutrIA design work.'
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. Original source: [`skills/stitch-ui-workflow/SKILL.md`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/skills/stitch-ui-workflow/SKILL.md). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Activation Contract
Use for NutrIA visual design and front-end handoff.

# Hard Rules
- Stitch is the design source; do not request Figma workflows.
- Preserve Terra: forest green, warm cream, amber accents, Literata headings and Nunito Sans body text.
- Design mobile and desktop states, including loading, empty and error states.
- A generated UI is a proposal until PO approves it.

# Execution Steps
1. Read Linear acceptance criteria.
2. Generate/refine a Stitch artifact with a specific user flow.
3. Review accessibility, hierarchy and responsive behavior.
4. Link output to the Linear issue.

# Output Contract
Return the Stitch artifact, rationale and implementation-ready states.


## Ejemplo de uso

**Pedido:** Proponer en Stitch los estados vacíos y de error de la lista de compras.

**Resultado:** Una propuesta visual con estados relevantes y aprobación del PO pendiente.
