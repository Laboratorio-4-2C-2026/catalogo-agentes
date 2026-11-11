---
name: g01-cinematch-issue-draft
description: "Redacta el cuerpo de un issue de Cinematch para Linear de modo que un desarrollador lo tome en frío y lo termine sin preguntar nada: formato de dos partes que separa el contexto de gestión (Ficha) del texto que llega a Linear (Descripción), qué nunca va en la descripción, criterios de aceptación verificables y cuándo dividir. Usala para escribir, reescribir o revisar si un issue está listo para crearse; planificar y secuenciar issues es de g01-cinematch-issue-management."
author: Tomás
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - analisis
  - planificacion
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - linear
  grupo: "01"
  autor:
    nombre: Tomás Roldán Borjas
    github: TomRolB
  responsables:
  - TomRolB
  madurez: usado-en-proyecto
  relacionados:
  - g01-cinematch-issue-management
  - g15-po-ticket-author
  - g11-redactar-ticket
---
# Cinematch issue draft

An issue has one reader: the person who picks it up. Roles rotate monthly, so it has to read cold: an issue cannot assume it is finished by whoever started it.

Everything below follows from that. Issue bodies are in Spanish. This skill is in English.

## 1. The draft format

Drafts live in `Issues/<Sprint>/drafts/`, one file per issue, with an `INDEX.md` listing them. Each file has two parts and the split is the point.

**`## Ficha`** is for us. A table of the fields needed to create it (title, estimate, parent, blocked by, blocks, labels, proposed week) plus prose explaining why the issue exists, what is still undecided, what it supersedes, and anything the creator has to do first. None of this reaches Linear.

**`## Descripción`** is a fenced markdown block containing exactly what gets pasted into Linear. If something in it would only make sense to someone doing planning, it is in the wrong half.

Anything unresolved goes in the Ficha as a named open question, not as a vague sentence in the body. Drafts that are blocked on a decision say so at the top: `> DECISIÓN ABIERTA. No crear este issue todavía.`

## 2. What the description contains

In this order:

1. **`## Objetivo`**, one or two sentences. What the issue achieves, not how.
2. **State of the code**, when the developer needs it. Call it `## Estado actual`, `## Contexto técnico`, or something equally concrete. This is where you say what already exists so they do not rebuild it, or what is currently broken so they know what they are fixing. **Say what already works**, and that it must not be rewritten: it changes the estimate.
3. **`## Alcance`**, numbered. Each item is a thing to do, with the exact values decided. Not "a large enough set" but "two hundred, ordered by popularity". If a number is missing, the developer invents one and it is not the one you meant.
4. **`## No incluye`**, explicit. Boundaries with neighbouring issues, and anything deliberately deferred. When a table or endpoint does not exist yet, say so **and say what to do about it**: `no la consultes ni la mockees`. Otherwise the feature gets built against mocked data.
5. **`## Criterios de aceptación`**, in given/when/then.
6. **`## Dependencias`**, naming what blocks it and what it blocks, and what the developer receives from each.

## 3. What never goes in the description

The body is not where planning lives. Keep all of this in the Ficha:

- Sprints, weeks, points, capacity, budget, earned value.
- Why we decided something, what the alternatives were, what it supersedes.
- Tickets that do not exist yet. A reference to a future issue is noise to someone trying to finish this one.
- Other tickets' due dates.
- Who else is working on what, and role scheduling.
- Vague pointers. "It is in the team's research" tells a developer something exists without telling them where. Either link it, attach it, or leave a marked placeholder in the house style: `[PENDIENTE — AGREGAR LINK A ...]`.

Note that Linear turns every ticket mention into a live cross-reference, so anything named becomes a link the developer will click. That makes the discipline matter more, not less.

## 4. Acceptance criteria that can be checked

**Every criterion must be verifiable with what exists when the issue is picked up.** An issue that blocks the pipeline cannot have a criterion that requires the pipeline. State how verification happens instead: bring the stack up by hand, and deliver the smoke check as a runnable script that another issue wires in.

Also:

- **Verify against the real thing, not a mock.** Write it into the criterion: `verificable contra el backend corriendo, no contra un test con mock`.
- **Cover the edges that have a defined contract**: empty input, a null column, a user with no data, the provider down.
- **Criteria can assert structure, not just behaviour.** `los componentes que ya existían no fueron modificados` is how an extensibility requirement gets checked rather than assumed.
- **Do not write criteria that need a browser or a human eye** when a command answers them.

## 5. Split the work, not the file

Management can create accounts, click panels, generate tokens, load secrets and configure DNS: none of that is programming. Developers do anything that lands in the repository, because management has no write access there. A body that is half panel work and half code forces the developer to filter for their part, so the description must carry only the developer's half.

But **the management half is not a second issue, and not a separate note either.** Linear is developer-only, so it would have nowhere to live, and inventing a standalone document makes a precondition look like independent work when it only exists to unblock that one issue.

It goes in the **Ficha of the same draft**, outside the fenced block. That is precisely what that half of the format is for: everything a manager needs and a developer never sees. One draft, two audiences, one file.

Then two things connect it:

- **The description opens with an "Antes de empezar" section** naming what must already be done, and telling the developer to say so if it is not. That is how the dependency reaches them without a Linear relation pointing at something Linear does not hold.
- **The pendiente itself, with its date and owner, goes to `TODO/`.** Only that. The detail stays in the Ficha, so there is one place to maintain it.

## 6. Getting material to the developer

When an issue depends on a document we hold:

- **Attach it to the issue. Never link this vault: developers do not have access to it.** A link nobody can open is worse than nothing. The same goes for any other source only management can reach.
- **Do not link a file in the application repository that does not exist yet.** Management cannot commit it. If the document belongs in the repo, make copying and adapting it the first item of the issue's scope, with its own acceptance criterion.
- That also solves the stale-attachment problem: the attachment is the seed, and the adapted copy in the repository is what the team uses afterwards.

## 7. Before creating it in Linear

- Every dependency is loaded as a real `blocked by` or `blocks` relation, not described in prose.
- The estimate covers developer work only. Management issues go unestimated.
- The parent is real. Do not hang new issues off a parent marked Duplicate without saying so.
- Placeholders are resolved, attachments attached.
- Read the description once as if you had never seen this project. Anything you can only understand because you were in the planning conversation comes out.

## Ejemplo de uso

**Pedido:** Redactá el issue para el endpoint que alimenta el mazo de swipes.

**Resultado:** Escribe un draft con la Ficha (estimación, padre, bloqueos, semana propuesta y preguntas abiertas) y la Descripción lista para pegar en Linear: Objetivo, Estado actual, Alcance numerado con valores concretos, No incluye, criterios de aceptación en given/when/then y Dependencias.
