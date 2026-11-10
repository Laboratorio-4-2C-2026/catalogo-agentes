---
name: g06-share
description: Publica un prototipo ejecutable mediante la herramienta de despliegue elegida por el usuario. Usar cuando un prototipo validado debe compartirse para revisión.
metadata:
  tipo: skill
  area:
  - frontend
  - devops
  fase:
  - despliegue
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - codex
  - claude-code
  - otra
  requiere: []
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
  source_path: skills/share/SKILL.md
  source_name: share
  source_sha256: 5976cfbc9d865230db085af37f0c25a2d8beed3ff58e0e2edb9d0a4f7ca987b5
  source_description: Share a runnable prototype using the user's preferred deployment tool.
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. Original source: [`skills/share/SKILL.md`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/skills/share/SKILL.md). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Share

Deploy the user's runnable prototype so they can share it with others.

## Critical Overrides

- Refer to the Plugin router [$index](../index/SKILL.md) before proceeding.
- Follow [$critical-overrides](../../references/critical-overrides.md).

## User Context

Before starting, load [$user-context](../user-context/SKILL.md) and run its preflight script when local shell access is available.

Use saved product URLs, Figma files, screenshots, reference images, codebase paths, Storybook, tokens, design systems, brand assets, component refs, browser preferences, and share targets as grounding material when relevant.

Do not inspect every saved reference. Inspect only what the current task needs.

## Workflow

1. Confirm the prototype directory and the user's preferred deployment target.
2. If the user invokes Product Design with @Sites, @Vercel, or another deployment tool, treat that as the selected hosting target.
3. If the user did not choose a target, ask one question:

> Where should I deploy this: @Sites, @Vercel, or another target?

4. Use the selected deployment tool when it is available.
5. If the selected tool is not available, say that clearly and ask whether to use another target.
6. Run the deployment when possible. Do not give setup instructions if you can complete the deployment directly.
7. Return the shareable URL.
8. State any misses or manual follow-up the user still needs to do.

## Rules

- Do not deploy before the user chooses or confirms the target.
- Do not claim the prototype is shared until you have a working URL.
- If the selected tool is not available, say that clearly and ask whether to use another target.


## Ejemplo de uso

**Pedido:** Compartir el prototipo de recetas con la herramienta de despliegue autorizada.

**Resultado:** Una URL utilizable y la evidencia de verificación del prototipo publicado.
