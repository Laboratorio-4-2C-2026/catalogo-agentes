---
name: g06-meal-plan-ai-safety
description: Define contratos, validaciones y evaluaciones para generación segura de planes alimentarios. Usar al modificar prompts o respuestas estructuradas sin introducir recomendaciones clínicas.
license: MIT
metadata:
  author: NutrIA
  version: 0.1.0
  tipo: skill
  area:
  - backend
  - ia
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
  requiere: []
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
  source_path: skills/meal-plan-ai-safety/SKILL.md
  source_name: meal-plan-ai-safety
  source_sha256: 1e69c4df85b5826defa235433f167464b27a35b153beadfd457ec3d29ebfb3ff
  source_description: 'Trigger: OpenAI meal plan, prompt, structured output, food restrictions, AI evaluation. Build NutrIA AI safely.'
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. Original source: [`skills/meal-plan-ai-safety/SKILL.md`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/skills/meal-plan-ai-safety/SKILL.md). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Activation Contract
Use for meal plan or recipe generation features.

# Hard Rules
- Require explicit preferences, restrictions and objective inputs.
- Enforce a structured response schema and server-side validation.
- Do not make health diagnoses or clinical recommendations.
- Invalid, unsafe or incomplete output fails recoverably; do not invent a substitute.

# Execution Steps
1. Define input/output contract and version prompt/schema.
2. Add deterministic evaluation fixtures for restrictions and malformed outputs.
3. Validate generated output before persistence/display.
4. Attach evaluation evidence to Linear and save durable learnings to Engram.

# Output Contract
Return contracts, safety cases, evaluation result and limitations.


## Ejemplo de uso

**Pedido:** Definir validaciones para un plan generado que contiene un ingrediente restringido.

**Resultado:** Contrato de entrada y salida, casos de evaluación y fallos recuperables explícitos.
