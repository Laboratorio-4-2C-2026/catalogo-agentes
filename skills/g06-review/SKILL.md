---
name: g06-review
description: Coordina revisión de cambios mediante lentes de riesgo, resiliencia, legibilidad y confiabilidad. Usar para consolidar hallazgos accionables de un PR sin aprobarlo ni fusionarlo.
license: Apache-2.0
metadata:
  author: nutria-ai
  version: '1.0'
  tipo: skill
  area:
  - qa
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
  - github
  - linear
  - engram
  - codegraph
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
  source_path: skills/review/SKILL.md
  source_name: review
  source_sha256: 97ef664763fce4df5a12295b12b3fca34643859be2c077697b086ad7a7bf0bd2
  source_description: 'Trigger: /review, code review, PR review, diff review. Run focused review lenses and report actionable findings.'
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. Original source: [`skills/review/SKILL.md`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/skills/review/SKILL.md). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

## Activation Contract

Use this skill for `/review` or an explicit request to review a completed change. Review only the diff and directly relevant context. Do not create an aggregate reviewer agent.

## Hard Rules

- For management/TL PR gates, use exactly the four generic management profiles in `bundles/management/agents`: `review-risk`, `review-resilience`, `review-readability`, and `review-reliability`. Each applies to any PR scope and loads `management_review`.
- For developer workflow review, select backend or frontend reviewer variants from `bundles/development/agents` based on changed scope; for mixed scope, run both applicable variants.
- Run the four lenses: risk, resilience, readability, and reliability.
- Treat an unavailable required lens as a **BLOCKER** and report it; do not silently substitute another lens.
- The parent orchestrator must pass the already-resolved role and selected task in every subagent handoff. Review subagents are non-interactive and must not repeat the primary role/task gate.
- Resolve the shared bundle root before declaring `management_review` unavailable: check the workspace `bundles/` path and then the configured shared bundle location.
- Report actionable findings only. Deduplicate overlapping findings and preserve lens attribution. No praise, essays, speculative nitpicks, merge/deploy actions, or approval claims.

## Execution Steps

1. Determine whether `/review` is being run for the management/TL PR gate or the developer workflow.
2. Determine changed scope and inspect the diff plus directly relevant context only.
3. Run all four lenses from the correct bundle: generic management profiles for any management/TL PR scope, or development backend/frontend variants for developer workflow scope.
4. Normalize each finding as `SEVERITY | file:line | lens | evidence | required fix`.
5. Return a concise `READY` or `NOT READY` recommendation. `NOT READY` applies to any unresolved finding or unavailable lens.

## Output Contract

Return only actionable findings, blockers, and the recommendation. Use stable severities: `BLOCKER`, `CRITICAL`, `WARNING`, or `SUGGESTION`. State `No findings` for a clean lens and preserve the lens name on deduplicated findings.

## References

- `bundles/management/AGENTS.md` — management/TL PR gate review workflow.
- `bundles/development/AGENTS.md` — developer workflow review and backend/frontend variants.
- `bundles/agent-libraries.json` — development `review` and management `management_review` libraries.


## Ejemplo de uso

**Pedido:** Revisar un PR terminado con las cuatro lentes de revisión de gestión.

**Resultado:** Hallazgos consolidados por severidad, evidencia y recomendación de preparación.
