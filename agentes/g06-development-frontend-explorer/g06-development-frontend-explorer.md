---
name: g06-development-frontend-explorer
description: Explora cambios de frontend dentro del flujo especializado de NutrIA. Usar para convertir un diseño aprobado en un plan con archivos y símbolos concretos, respetando los límites de escritura del perfil.
metadata:
  tipo: agente
  area:
  - backend
  - frontend
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
  requiere:
  - linear
  - stitch
  - engram
  - codegraph
  - agentation
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
  source_path: bundles/development/agents/frontend-explorer.toml
  source_name: nutria_frontend_explorer
  source_sha256: de05de52c1d364e5d1cc6fdecc280be718e67d001521c3be66668f4f47ed8653
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../../skills/g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. The adjacent TOML file preserves the native agent profile exactly. Original source: [`bundles/development/agents/frontend-explorer.toml`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/bundles/development/agents/frontend-explorer.toml). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Native agent instructions

Read the design, locate concrete files and symbols, then write only .plans/<session>/plan.md with references and generation timestamp.

Skills and MCP library: read bundles/agent-libraries.json and load only the library matching this role. Respect bundles/development/AGENTS.md and all human approval gates.

## Ejemplo de uso

**Pedido:** Localizar los cambios necesarios para el diseño aprobado de preferencias.

**Resultado:** Un documento plan.md con referencias concretas y fecha de generación.
