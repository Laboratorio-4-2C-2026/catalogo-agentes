---
name: g06-documentation-evidence
description: Prepara documentación y reportes que distinguen trabajo planeado, implementado y verificado. Usar cuando un informe de avance necesita evidencia trazable.
license: MIT
metadata:
  author: NutrIA
  version: 0.1.0
  tipo: skill
  area:
  - documentacion
  - gestion
  fase:
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
  source_path: skills/documentation-evidence/SKILL.md
  source_name: documentation-evidence
  source_sha256: a295c7aa6576d930ebe70c179d37f57fb4b230204116253bd2542e587441262a
  source_description: 'Trigger: documentation, final report, evidence, architecture report, test report. Keep NutrIA claims auditable.'
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. Original source: [`skills/documentation-evidence/SKILL.md`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/skills/documentation-evidence/SKILL.md). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Activation Contract
Use for project artifacts and final reports.

# Hard Rules
- Distinguish planned, implemented and verified work.
- Link claims to Linear, PR, test, ADR or artifact evidence.
- Never invent test, deployment, user-research or time-tracking results.

# Execution Steps
1. Gather current primary evidence.
2. Create concise audience-appropriate documentation.
3. Flag missing evidence as a gap.
4. Update Engram only for durable conventions/findings.

# Output Contract
Return a traceable report section with references and open gaps.


## Ejemplo de uso

**Pedido:** Preparar el reporte semanal con enlaces a tickets, PR y resultados de pruebas.

**Resultado:** Un reporte auditable que identifica evidencia disponible y brechas pendientes.
