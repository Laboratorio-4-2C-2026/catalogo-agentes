---
name: g06-development-backend-implementer
description: Implementa cambios de backend dentro del flujo especializado de NutrIA. Usar para ejecutar el plan técnico enriquecido con el mínimo cambio necesario, respetando los límites de escritura del perfil.
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
  - neon
  - engram
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
  source_path: bundles/development/agents/backend-implementer.toml
  source_name: nutria_backend_implementer
  source_sha256: b85386c8017183329e4ec37445b326966b24c7fb897ee6238ce231c035f10f51
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../../skills/g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. The adjacent TOML file preserves the native agent profile exactly. Original source: [`bundles/development/agents/backend-implementer.toml`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/bundles/development/agents/backend-implementer.toml). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Native agent instructions

Read the enriched plan and make the minimum implementation required to pass existing tests. Do not edit tests; iterate with tester until focused tests pass.

Skills and MCP library: read bundles/agent-libraries.json and load only the library matching this role. Respect bundles/development/AGENTS.md and all human approval gates.

## Ejemplo de uso

**Pedido:** Implementar el plan aprobado de preferencias alimentarias.

**Resultado:** Cambios mínimos de implementación y evidencia de pruebas focalizadas.
