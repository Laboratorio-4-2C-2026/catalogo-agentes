---
name: g06-neon-prisma-safety
description: Revisa esquemas y migraciones Prisma en ramas de desarrollo de Neon con datos de prueba. Usar para cambiar persistencia con validación y estrategia de reversión.
license: MIT
metadata:
  author: NutrIA
  version: 0.1.0
  tipo: skill
  area:
  - backend
  - datos
  fase:
  - desarrollo
  tecnologias:
  - prisma
  - postgresql
  metodologia:
  - scrum
  herramientas:
  - codex
  - claude-code
  - otra
  requiere:
  - neon
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
  source_path: skills/neon-prisma-safety/SKILL.md
  source_name: neon-prisma-safety
  source_sha256: 2bebdce6e3d1465199eab5756af31e1c20f11816a480009f3d43b32248ce63da
  source_description: 'Trigger: Neon MCP, Prisma migration, SQL, schema, database branch. Safely change NutrIA persistence.'
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. Original source: [`skills/neon-prisma-safety/SKILL.md`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/skills/neon-prisma-safety/SKILL.md). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Activation Contract
Use for database investigation, schema or migration work.

# Hard Rules
- MCP connects only to a Neon development branch with anonymized/sample data.
- Never expose connection strings, PII or production results.
- Read schema before writing SQL. Require a reviewed migration and rollback for destructive changes.

# Execution Steps
1. Confirm target is non-production and branch name.
2. Inspect tables and schema.
3. Create a small migration, validate on the branch and run focused tests.
4. Document data-model changes in ADR/Engram.

# Output Contract
Return branch, schema impact, migration, validation evidence and rollback.


## Ejemplo de uso

**Pedido:** Preparar una migración de preferencias en una rama de desarrollo de Neon.

**Resultado:** Migración acotada, evidencia de validación y estrategia de reversión documentada.
