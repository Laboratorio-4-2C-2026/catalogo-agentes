---
name: g06-google-modern-web-guidance
description: Consulta documentación web actual antes de modificar HTML, CSS o JavaScript del navegador. Usar para fundamentar decisiones de implementación y compatibilidad frontend.
license: MIT
metadata:
  author: NutrIA
  version: 0.1.0
  tipo: skill
  area:
  - frontend
  fase:
  - desarrollo
  tecnologias:
  - react
  - typescript
  metodologia:
  - scrum
  herramientas:
  - codex
  - claude-code
  - otra
  requiere: []
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
  source_path: skills/google-modern-web-guidance/SKILL.md
  source_name: google-modern-web-guidance
  source_sha256: a495bcd61660b2dc16d76d3bae434dc0a808fb2b276c37719306de1cd46948fe
  source_description: 'Trigger: frontend, React, TypeScript, CSS, HTML, accessibility, responsive UI, web performance. Fetch current Google Modern Web Guidance before client-side work.'
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. Original source: [`skills/google-modern-web-guidance/SKILL.md`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/skills/google-modern-web-guidance/SKILL.md). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Activation Contract
Run this skill first for every HTML, CSS, React or browser JavaScript change.

# Hard Rules
- Do not implement client-side behavior from memory when current platform guidance is available.
- Search before writing code; retrieve the most relevant result before implementation.
- Use Google Modern Web Guidance through `npx`; it is not an MCP.
- Follow the documented fallback guidance for features that are not Baseline Widely Available.

# Execution Steps
1. Run `npx -y modern-web-guidance@latest search "<action-oriented task>" --skill-version 2026_05_16-c5e78707`.
2. Retrieve the selected guidance: `npx -y modern-web-guidance@latest retrieve "<guide-id>"`.
3. Apply it to the React/Vite implementation and test the relevant responsive/accessibility/performance behavior.
4. Cite the guide ID in the PR or Linear evidence when it materially changed the implementation.

# Output Contract
Return searched guide IDs, the applied decision, browser/fallback impact and validation evidence.


## Ejemplo de uso

**Pedido:** Consultar la guía actual antes de implementar un diálogo accesible de edición.

**Resultado:** Referencias vigentes y restricciones de compatibilidad para la implementación.
