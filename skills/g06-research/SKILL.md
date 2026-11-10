---
name: g06-research
description: Investiga problemas actuales de experiencia de usuario con fuentes y evidencia verificable. Usar para fundamentar oportunidades de producto antes de priorizar soluciones.
metadata:
  tipo: skill
  area:
  - diseno
  - gestion
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
  source_path: skills/research/SKILL.md
  source_name: research
  source_sha256: bf824e72dd93941c8d591e4af13bb7e3a09380cd6ed7dd8c1f61a295648fa023
  source_description: Run fast, source-grounded UX research on the highest-signal problems users are experiencing with a user-specified digital product. Use when the user asks to research user pain, UX friction, onboarding issues, docs/help problems, developer experience friction, support pain, product workflow issues, or current user complaints for a named product.
---

## Catalog integration

This catalog entry belongs to the NutrIA harness. Read the [shared context and dependency guide](../g06-nutria-project-context/README.md) before use. The catalog prefix identifies this submission; source runtime names and project-relative references remain unchanged. Original source: [`skills/research/SKILL.md`](https://github.com/nutria-lab/ai-harness/blob/4e3652d4dbf38d8746626401126aa0e1b4139c89/skills/research/SKILL.md). Team ownership is the role-based assignment for this submission; upstream provenance is preserved separately.

# Research

Run a fresh UX research scan for the product the user specifies.

Focus on current, evidence-backed user problems. Prioritize logged-in product experience, self-serve flows, onboarding, docs/help, developer experience, support friction, and product workflows.

## Critical Overrides

- Refer to the Plugin router [$index](../index/SKILL.md) before proceeding.
- Follow [$critical-overrides](../../references/critical-overrides.md).

## User Context

Before starting, load [$user-context](../user-context/SKILL.md) and run its preflight script when local shell access is available.

Use saved product URLs, Figma files, screenshots, reference images, codebase paths, Storybook, tokens, design systems, brand assets, component refs, browser preferences, and share targets as grounding material when relevant.

Do not inspect every saved reference. Inspect only what the current task needs.

## Contract

- Restate the product, audience, time horizon, and research scope before scanning.
- Use public sources by default. Use internal sources when the connectors are available and the user request allows it.
- Cite sources wherever available.
- Separate observed evidence from inference.
- Do not overclaim from anecdotes.
- Do not return a dump of complaints. Tell a clear product story.
- Say clearly when source access is missing or weak.

## Workflow

1. Restate the research scope.

2. Search public sources:

- Reddit
- X/Twitter
- Hacker News
- Stack Overflow
- GitHub issues/discussions
- forums, blogs, reviews, YouTube comments, and developer communities where relevant

3. Search internal sources when available:

- Slack
- Gong
- Notion
- Google Drive/docs
- Linear/Jira/GitHub
- support or CRM notes if available

4. Cluster evidence into the highest-signal UX problems.

5. Separate:

- product UI/workflow friction
- docs/help friction
- onboarding friction
- account, billing, permissions, or setup friction
- developer/API/SDK friction
- reliability/performance issues
- feature requests

6. Rank problems by severity, frequency, confidence, and product leverage.

7. Tell a clear product story.

## Output

Default to an in-chat research brief unless the user asks for another format.

Include:

- Executive read: the core story in 5-7 sentences.
- Ranked UX problems: for each problem, include the problem, user goal, surface, what breaks, evidence, severity, frequency signal, confidence, and recommended product move.
- Source map: what was searched, what each source contributed, and where signal was weak.
- Opportunity map: group recommendations into fix this week, fix this quarter, and needs deeper research.

## Rules

- Use citations wherever available.
- Do not overclaim from anecdotes.
- Separate loud complaints from frequent problems.
- Separate UX friction from missing features.
- Separate reliability/performance issues from UX workflow issues.
- Mark internal-only evidence separately from public evidence.
- Keep the brief sharp, specific, and easy to consume.


## Ejemplo de uso

**Pedido:** Investigar fricciones de onboarding en un producto digital indicado por el usuario.

**Resultado:** Problemas priorizados, fuentes y límites de la evidencia reunida.
