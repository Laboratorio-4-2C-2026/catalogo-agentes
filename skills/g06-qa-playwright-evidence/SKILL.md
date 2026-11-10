---
name: g06-qa-playwright-evidence
description: Diseña y ejecuta escenarios de regresión basados en criterios de aceptación con Playwright. Usar para reunir resultados, trazas y brechas de cobertura antes de una entrega.
license: MIT
metadata:
  author: NutrIA
  version: 0.1.0
  tipo: skill
  area:
  - qa
  fase:
  - testing
  tecnologias:
  - playwright
  metodologia:
  - scrum
  herramientas:
  - codex
  - claude-code
  - otra
  requiere:
  - playwright
  grupo: "06"
  autor:
    nombre: Tais Marambio
    github: TaisMarambio
  responsables:
  - TaisMarambio
  madurez: experimental
  relacionados:
  - g06-nutria-project-context
  rol_equipo: QA
  source_repository: https://github.com/nutria-lab/ai-harness
  source_revision: 4e3652d4dbf38d8746626401126aa0e1b4139c89
  source_path: skills/qa-playwright-evidence/SKILL.md
  source_name: qa-playwright-evidence
  source_sha256: ed7ec94ec9b307a1240ce23327f3027d4cb8fcc73f98b7108a370c45b1f80132
  source_description: 'Trigger: QA, Playwright, E2E, regression, test plan. Produce reliable evidence for NutrIA releases.'
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. Original source: [`skills/qa-playwright-evidence/SKILL.md`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/skills/qa-playwright-evidence/SKILL.md). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Activation Contract
Use for feature validation and regressions.

# Hard Rules
- Derive tests from approved acceptance criteria.
- Prefer role/label/test-id locators and deterministic fixtures.
- Separate a product defect from a test or environment defect.
- Do not auto-close issues.

# Execution Steps
1. Create a human-readable scenario plan.
2. Generate focused tests for desktop and relevant mobile states.
3. Execute and retain failures/traces as evidence.
4. Report pass/fail, coverage gap and recommended Linear status.

# Output Contract
Return test evidence linked to the issue and explicit untested risks.


## Ejemplo de uso

**Pedido:** Validar la edición de una receta en escritorio y en un viewport móvil relevante.

**Resultado:** Escenarios ejecutados, resultados, trazas de fallos y brechas de cobertura.
