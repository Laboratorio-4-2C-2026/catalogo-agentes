---
name: g06-engram-memory-protocol
description: Conserva decisiones, descubrimientos y resúmenes de sesión en Engram con claves estables. Usar para mantener continuidad operativa entre sesiones del equipo.
license: MIT
metadata:
  author: NutrIA
  version: 0.1.0
  tipo: skill
  area:
  - gestion
  - documentacion
  fase:
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
  source_path: skills/engram-memory-protocol/SKILL.md
  source_name: engram-memory-protocol
  source_sha256: af7e65ce0908bcbd0181a3373b19230189da0ff4dfa25f00e9a5aad61d0c4a35
  source_description: 'Trigger: memory, decision, bug fix, discovery, session summary, Engram. Preserve NutrIA continuity with curated project memory.'
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. Original source: [`skills/engram-memory-protocol/SKILL.md`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/skills/engram-memory-protocol/SKILL.md). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Activation Contract
Use at session start, after important work and before session end.

# Hard Rules
- Call `mem_context` at session start for ongoing work; search before relying on a past decision.
- Save decisions, bugs, discoveries, conventions and confirmed preferences immediately with `mem_save`.
- Use stable `topic_key` values for evolving topics; do not overwrite unrelated memories.
- Save a session summary before declaring work done.
- Never store secrets, tokens, connection strings or sensitive user data.

# Execution Steps
1. Feed the user prompt through `mem_save_prompt` when available.
2. Retrieve recent context and full observations as needed.
3. Save curated structured observations with What, Why, Where and Learned.
4. Resolve returned conflicts explicitly; do not silently ignore them.

# Output Contract
Leave searchable, minimal memory and a session handoff.


## Ejemplo de uso

**Pedido:** Guardar la decisión aprobada sobre el reporte semanal y cerrar la sesión.

**Resultado:** Una observación estructurada y un resumen de sesión sin información sensible.
