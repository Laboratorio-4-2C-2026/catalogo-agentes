---
name: g06-architecture-adr
description: Documenta decisiones de arquitectura y contratos mediante ADR con alternativas y consecuencias. Usar para cambios técnicos que requieren aprobación del TL.
license: MIT
metadata:
  author: NutrIA
  version: 0.1.0
  tipo: skill
  area:
  - backend
  fase:
  - diseno
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - codex
  - claude-code
  - otra
  requiere:
  - engram
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
  source_path: skills/architecture-adr/SKILL.md
  source_name: architecture-adr
  source_sha256: f5f76433f0536330492ede2779389648f16127b44baad032a8fe89e5288ee788
  source_description: 'Trigger: architecture decision, API contract, ADR, integration boundary. Record reversible and consequential technical choices.'
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. Original source: [`skills/architecture-adr/SKILL.md`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/skills/architecture-adr/SKILL.md). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Activation Contract
Use for technical decisions with lasting impact.

# Hard Rules
- Record decisions that affect contracts, data model, security, reliability or delivery cost.
- Prefer smallest reversible design compatible with the current MVP.
- Do not use production data through tools.

# Execution Steps
1. State context, constraints and alternatives.
2. Evaluate consequences for React/Vite, NestJS, Prisma, Neon and OpenAI integration.
3. Choose with human TL approval.
4. Save ADR and an Engram observation using a stable topic key.

# Output Contract
Return context, decision, alternatives, consequences and migration/rollback notes.


## Ejemplo de uso

**Pedido:** Documentar la decisión de separar la generación del plan semanal de su persistencia.

**Resultado:** Un ADR con contexto, alternativas, consecuencias y aprobación técnica pendiente.
