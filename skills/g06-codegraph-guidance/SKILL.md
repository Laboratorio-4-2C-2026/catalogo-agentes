---
name: g06-codegraph-guidance
description: Explora símbolos, dependencias y alcance de un cambio con CodeGraph antes de buscar archivos. Usar para investigar la estructura técnica del proyecto.
license: MIT
metadata:
  author: NutrIA
  version: 0.1.0
  tipo: skill
  area:
  - backend
  - frontend
  fase:
  - analisis
  - desarrollo
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - codex
  - claude-code
  - otra
  requiere:
  - codegraph
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
  source_path: skills/codegraph-guidance/SKILL.md
  source_name: codegraph-guidance
  source_sha256: e49aaaad678f88a3c173dc07cd1310479da5d16200bd6314a0885ff837f4ff92
  source_description: 'Trigger: architecture, codebase map, call flow, dependency, symbol, impact, affected files. Use CodeGraph before broad filesystem exploration.'
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. Original source: [`skills/codegraph-guidance/SKILL.md`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/skills/codegraph-guidance/SKILL.md). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Activation Contract
Use before answering or changing structural codebase questions.

# Hard Rules
- Resolve the project root, confirm it is a project, then check `.codegraph/`.
- Initialize once only when the index is missing in a real project.
- Prefer `codegraph_explore`; use `codegraph explore` only if MCP is unavailable.
- Do not use administrative/destructive lifecycle commands in ordinary work.

# Execution Steps
1. Run `git rev-parse --show-toplevel || pwd`.
2. Check `<root>/.codegraph/`; if absent, run `codegraph init <root>`.
3. Ask one focused explore question for symbols, path, callers/callees and blast radius.
4. Fall back to filesystem search only if CodeGraph fails; state the fallback.

# Output Contract
Return the indexed evidence, call path/blast radius, and affected files. Do not claim structural facts from intuition.


## Ejemplo de uso

**Pedido:** Identificar dependencias y puntos de cambio del módulo de adherencia.

**Resultado:** Evidencia indexada de símbolos, rutas de llamadas y archivos afectados.
