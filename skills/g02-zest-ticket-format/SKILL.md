---
name: g02-zest-ticket-format
description: 'Estructura y convenciones de los tickets del backlog de Zest: introducción, tareas, criterios de aceptación, etiqueta y sprint. Usar al redactar o revisar un ticket.'
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - jira
  grupo: '02'
  autor:
    nombre: Liz Lubelcyk
    github: lizlubelczyk
  responsables:
  - lizlubelczyk
  madurez: usado-en-proyecto
  relacionados:
  - g02-ticket-drafter
---
# Zest ticket format

Every ticket follows this structure, in this order.

## 1. Intro paragraph
Context and rationale in prose. Why this ticket exists and what problem it
solves. No bullet points here.

## 2. Tasks
A numbered list of concrete implementation steps. Each one should be
independently checkable.

## 4. Acceptance criteria
Explicit, testable conditions. "Done" must be unambiguous from this section
alone.

## Labels: should a label for the ticker as "backend", "frontend", or "infra".

## Stage: establish the sprint number accordingly. 

# Conventions

- Concise. Collapse anything that can be collapsed. No padding.
- Lean schema philosophy: no audit fields (created_at, updated_at) unless the
  ticket is specifically about auditing. Do not add fields "just in case."
- Auth is handled entirely by Auth0. The users table stores auth0_sub only —
  never password_hash.
- Backend work carries a test-coverage expectation of 75% or above.The backend 
tickets should include testing in the requirements. 
- Frontend work must be fully responsive.

# Before drafting

Search the ZEST project for existing tickets on the same topic
(project = ZEST AND summary ~ "term"). If something close already exists,
say so and stop — do not create a near-duplicate.
Take a look in other tickets to follow the same style and tone.

## Ejemplo de uso
**Pedido:** Escribí un ticket para el endpoint de colecciones siguiendo el formato.
**Resultado:** Devuelve el ticket con introducción en prosa, tareas numeradas, criterios de aceptación testeables y la etiqueta backend, tras buscar duplicados.
