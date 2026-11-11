---
name: g06-get-context
description: Aclara el producto, el problema y el resultado esperado antes de diseñar una interfaz. Usar cuando faltan datos del brief para un trabajo de Product Design.
metadata:
  tipo: skill
  area:
  - gestion
  - diseno
  fase:
  - analisis
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
  source_path: skills/get-context/SKILL.md
  source_name: get-context
  source_sha256: 19a38a3ac4443cb477a01c2303e77c891c304234a195dd2da248e3e736b22679
  source_description: Mandatory design-brief gate for clarifying the product and outcome. Use before ideation, image-to-code builds, redesigns, or product UI work to clarify missing product information and play back the brief before proceeding.
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. Original source: [`skills/get-context/SKILL.md`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/skills/get-context/SKILL.md). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Get Context


Run this skill at the start of Product Design requests that ask to design, build, prototype, clone, redesign, extend, or generate product UI directions.

Use question mode to clarify the following:

- what product, site, feature, workflow, component, or screen is being designed, redesigned, or extended
- what the feature, change, app, or website should help the user do

Do not re-ask answered questions. When both are clear, play back the brief and defaults in one pithy note, name the next workflow, and continue in the same turn. Playback is not a request for approval. The user can course-correct style, scope, or interactivity at any point.

Hard boundary: do not implement UI, scaffold a prototype, start a server, or create files while the design target or intended user outcome is still missing.

## Critical Overrides

- Refer to the Plugin router [$index](../index/SKILL.md) before proceeding.
- Follow [$critical-overrides](../../references/critical-overrides.md).

## User Context

Before starting, load [$user-context](../user-context/SKILL.md) and run its preflight script when local shell access is available.

Use saved product URLs, Figma files, screenshots, reference images, codebase paths, Storybook, tokens, design systems, brand assets, component refs, browser preferences, and share targets as grounding material when relevant.

Do not inspect every saved reference. Inspect only what the current task needs.

## Handoff To The Next Workflow

1. When the next workflow is already clear, read that skill before sending the brief playback. Do not only name a skill you have not read.

2. Before executing `$ideate`, `$url-to-code`, or `$image-to-code`, play back the minimum brief and any defaults in one pithy user-visible note.

3. If the target and intended user outcome are clear, continue to the next workflow in the same turn. Do not wait for explicit confirmation. If the user provides feedback, incorporate it and course-correct.

4. Before starting an involved app, prototype, clone, redesign, or build, send one short expectation-setting note and continue. Example:

```text
This kind of build usually takes about 10-15 minutes, and ambitious ones can take longer. Good moment to grab coffee or tend to something else; I’ll keep moving and bring the prototype back when it is ready.
```

Do not send this note for tiny static changes, quick audits, simple research, setup-only, or share-only requests.

Done means the design target and intended user outcome are clear, defaults have been played back, and any already-determined next skill has been read.


## Ejemplo de uso

**Pedido:** Definir el objetivo y los usuarios de una pantalla para editar preferencias alimentarias.

**Resultado:** Un brief confirmado con el objetivo del producto y las decisiones pendientes.
