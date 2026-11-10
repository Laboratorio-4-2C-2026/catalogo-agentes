---
name: g06-gentle-ai-engram
description: Combina la gobernanza de agentes NutrIA con memoria persistente de Gentle AI y Engram. Usar para coordinar continuidad de trabajo sin sobrescribir configuraciones existentes.
license: MIT
metadata:
  author: NutrIA
  version: 0.1.0
  tipo: skill
  area:
  - gestion
  - documentacion
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
  source_path: skills/gentle-ai-engram/SKILL.md
  source_name: gentle-ai-engram
  source_sha256: 2aab8be1996c2aeea7f149b3bb14d0395273c51096117ef9590cb99a2df1a235
  source_description: 'Trigger: Gentle AI, Engram setup, orchestrator memory, session continuity. Combine NutrIA agent governance with persistent memory.'
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. Original source: [`skills/gentle-ai-engram/SKILL.md`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/skills/gentle-ai-engram/SKILL.md). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Activation Contract
Use when running NutrIA agents with Gentle AI and Engram.

# Hard Rules
- Gentle AI manages orchestration behavior; this harness provides NutrIA-specific roles and skills.
- Do not overwrite an existing Gentle AI or Engram configuration.
- Call `mem_context` at session start and `mem_session_summary` before ending a session.
- Use `mem_save_prompt` when the real prompt is available; save only curated, non-sensitive observations.

# Execution Steps
1. Detect existing Gentle AI / Engram setup.
2. Load `team-orchestrator` and the role profile matching the task.
3. Apply Linear, Neon and Stitch safety gates.
4. Persist approved decisions, bugs, discoveries and conventions in Engram.

# Output Contract
Return the selected role, approval owner, current evidence and memory handoff.


## Ejemplo de uso

**Pedido:** Retomar el trabajo del equipo utilizando su configuración existente de Engram.

**Resultado:** Contexto recuperado, rol operativo identificado y memoria de cierre de la sesión.
