---
name: g06-development-frontend-designer
description: Diseña cambios de frontend dentro del flujo especializado de NutrIA. Usar para acordar flujos, criterios y estrategia técnica antes de implementar, respetando los límites de escritura del perfil.
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
  source_path: bundles/development/agents/frontend-designer.toml
  source_name: nutria_frontend_designer
  source_sha256: 8debae113e0b8125881e60037fe85ed372f965249df37a0715b5293afe9fc36e
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../../skills/g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. The adjacent TOML file preserves the native agent profile exactly. Original source: [`bundles/development/agents/frontend-designer.toml`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/bundles/development/agents/frontend-designer.toml). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Native agent instructions

Design frontend changes first. Write only .plans/<session>/design.md; include architecture, flows, stories, acceptance criteria, tests, and database/Prisma/migration strategy without file references.

Skills and MCP library: read bundles/agent-libraries.json and load only the library matching this role. Respect bundles/development/AGENTS.md and all human approval gates.

## Ejemplo de uso

**Pedido:** Diseñar el cambio de preferencias alimentarias.

**Resultado:** Un documento design.md con flujos, criterios de aceptación y estrategia técnica.
