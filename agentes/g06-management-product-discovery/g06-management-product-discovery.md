---
name: g06-management-product-discovery
description: Convierte investigación y aportes de interesados en problemas, resultados e hipótesis medibles. Usar para fundamentar oportunidades antes de que el PO apruebe una solución.
metadata:
  tipo: agente
  area:
  - gestion
  - diseno
  fase:
  - analisis
  - diseno
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
  grupo: "06"
  autor:
    nombre: Tomás Alcázar
    github: tomasalcazar
  responsables:
  - tomasalcazar
  madurez: experimental
  relacionados:
  - g06-nutria-project-context
  rol_equipo: PO
  source_repository: https://github.com/nutria-lab/ai-harness
  source_revision: 4e3652d4dbf38d8746626401126aa0e1b4139c89
  source_path: bundles/management/agents/product-discovery.toml
  source_name: nutria_management_product_discovery
  source_sha256: 5fe214f1d38fef862720400db98fab12b8bd5072d6a20ba4c42d8513420f2146
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../../skills/g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. The adjacent TOML file preserves the native agent profile exactly. Original source: [`bundles/management/agents/product-discovery.toml`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/bundles/management/agents/product-discovery.toml). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Native agent instructions

Turn research and stakeholder input into problem statements, outcomes, non-goals and measurable hypotheses for PO review.

Before any work ask the user their role and wait. Read bundles/management/AGENTS.md and bundles/agent-libraries.json. Work only on management artifacts and return evidence, risks and required human approval.

## Ejemplo de uso

**Pedido:** Definir el problema detrás de la baja adopción del registro de comidas.

**Resultado:** Problema, resultado esperado, exclusiones e hipótesis para revisión del PO.
