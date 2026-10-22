---
name: g03-planify-jira-ticket
description: Escribe, mejora o crea tickets de Jira del proyecto Planify con un paso a paso anclado al código real de los repos mobile (Flutter) y backend (Express + Prisma). Usar cuando se pide redactar, revisar o detallar un ticket, aunque solo se dé el número.
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
  - analisis
  tecnologias:
  - flutter
  - express
  - prisma
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - jira
  grupo: '03'
  autor:
    nombre: Julieta Iglesias
    github: JuliIglesias
  responsables:
  - JuliIglesias
  madurez: usado-en-proyecto
  relacionados: []
---
# Writing Jira tickets for Planify

This skill captures the way tickets are written on the Planify project. The audience for these tickets is junior developers who start the feature **from scratch**, reading nothing but the ticket. That is why the level of detail matters: not so generic that it is unclear what to do, and not so resolved that nothing is left to think about.

The skill works whether the caller is Claude Code (invocable as `/jira-tickets`) or any other agent reading this file as context — the instructions below assume no particular tool, only the ability to read files and code and to talk to Jira (via API, via MCP, or however that agent has it wired up).

**Language of the output:** tickets are written in Spanish, because the entire PLANIFY project in Jira is in Spanish. The fixed section headers, the ticket prefixes, and the Prisma model and field names quoted throughout this document are literals — reproduce them exactly as written, do not translate them.

## Before writing a single word: read the actual state of things

Never write a textbook step-by-step. Every step must be anchored to what exists in the code **today**, not to generic best practice. Before drafting:

1. **Locate the repositories.** `planify-mobile` and `planify-backend` (org `Planify-Lab-IV`). If they are not available locally, ask whoever is using you to clone them or point at where they are — do not treat their absence as licence to write something generic.
2. **`planify-mobile` and `planify-backend` are read-only for this work.** Never edit, commit, or push to them — not even to "try something out". To inspect another branch without touching the working tree, use read-only commands (`git log`, `git show <branch>:<path>`, `git ls-tree`) instead of `git checkout`. This rule is hard, not a style preference — it applies regardless of which agent is running this skill.
3. **Read the real structure related to the ticket**: the folder tree of the closest already-built feature (on mobile, `lib/features/auth/` has the data/domain/presentation pattern in place; on backend, `src/routes` → `src/controllers` → `src/services` → `src/repositories`), the dependencies already declared in `pubspec.yaml` / `package.json` (sometimes a package is already added but nobody uses it yet — that is valuable information for the ticket), each repository's `README.md` (branch convention, how to bring up the local environment), and the commit and branch history of both repositories to see which tickets are already merged and under what branch or commit name.
4. **If the ticket depends on others, read those tickets in Jira** to know whether they are merged, and say so explicitly in the ticket (see "Depende de" below) — do not assume that because Jira says "Finalizada"/"Done" the work is already in `develop`; cross-check it against the git history where possible. It has already happened on this project that a ticket sat in "En revisión" in Jira while it was in fact already merged.
5. **If a well-written sibling ticket exists** (same epic, same style), use it as the quality and tone benchmark — do not rewrite it unless asked.

## When the capability does not exist in the code yet: two ways to start

The previous section assumes there is something similar already built to anchor the ticket against. When there is **not** — a genuinely new end-to-end feature, with no code and no sibling ticket to look at — this skill must still produce a complete ticket (title, prefix, and the full fixed structure below), but it needs more information from the person using it before it can be written to the same level of detail as the rest of the project's tickets. There are two paths, and which one applies depends on what information already exists:

### A. Starting from a free-form description of the capability

If the person describes in their own words what they want built (with no reference ticket and no reference code), do not rush into writing the ticket from that description alone — first ask whatever questions you need in order to anchor the step-by-step to real decisions rather than generic ones:

- **Prefix and scope**: is this FE, BE, or INT? If the person does not know, help them decide using the same logic as the "What each prefix implies" section below — sometimes a single description is really 2-3 separate tickets (BE + FE + INT), and that needs to be said explicitly instead of blending them into one.
- **Epic and dependencies**: which Jira epic does it belong to? Search Jira for existing epics on a similar theme before assuming a new one is needed. If it depends on another ticket (existing or yet to be created), state it under "Depende de".
- **Conventions to reuse**: even when there is no code for *this* particular feature, there is almost always a sibling feature already built with a similar structural pattern (same kind of screen, same kind of CRUD endpoint, etc.) — find it the same way as in point 3 of "Before writing a single word", and use it as a template for *where* the new files go, even if the content differs.
- **Design (if FE)**: is there a Figma link already prepared for this screen, or does the ticket need to state explicitly that no design exists yet and record that as a dependency or blocker?
- **Domain-specific acceptance criteria**: if the capability touches money, dates, or state shared across users, ask which edge cases matter to the team instead of inventing them.

You do not need to ask everything at once — prioritise what changes the structure of the ticket (prefix, epic, dependencies) over fine detail, and only move on to the step-by-step once you have those.

### B. Starting from an existing Jira ticket as a reference, plus targeted questions

If instead the person gives you an existing Jira ticket (from this epic or another) to use as a model — for example "que quede como el PLANIFY-33" but for a different capability — read it first (the full description, not just the title) and use it as the benchmark for structure and tone, exactly as the "Before writing a single word" section already prescribes for sibling tickets. The difference here is that the reference ticket describes a *different* capability from the one you have to write, so:

1. Extract the pattern from the reference ticket (how it divides the step-by-step, what level of detail it uses, how it assembles the acceptance criteria) but do not literally copy steps that do not apply to the new capability.
2. Ask the same questions as in section A that the reference ticket does not answer on its own — typically the prefix, the target epic, and the dependencies differ even when the shape is similar.
3. If the new capability is in practice a close variation of the one in the reference ticket (same data model, same flow with one specific change), say so explicitly in the new ticket's Objetivo — it helps the reader understand why it resembles another ticket so closely without being a duplicate.

### In both cases

- The final title follows the same format as the rest of the skill: `[PREFIJO-N] Título` — but since the issue does not exist in Jira yet, the ticket number is assigned by Jira on creation, not by you. Draft the summary without a number (`[FE] Selector de disponibilidad semanal`) and let the real key (`PLANIFY-XX`) be filled in once the user confirms creation.
- Show the complete draft in chat (or in a temporary working file, never inside `planify-mobile` / `planify-backend`) and ask for explicit confirmation before creating the issue in Jira — the same rule that already applies to writing into an existing ticket (see "About Jira itself" below).
- If after the first round of questions you still cannot anchor a given step to a real decision (for example, there is no agreement yet on which library to use), do not invent one — mark it in the ticket as a pending decision rather than a decision of yours disguised as settled.

## What each ticket prefix implies (FE / INT / BE)

The bracketed prefix in the summary is not cosmetic — it determines what kind of work this is and therefore what it makes sense to ask for in the ticket:

- **`[FE-N]`**: in the overwhelming majority of cases, this means building the frontend for that capability — a screen or a component — following the project's Figma design (look for the link in `docs/design-system.md` in the mobile repository, or the Figma file corresponding to that screen if a specific one exists) **with genuine implementation freedom** in everything Figma does not explicitly dictate: the widget's internal structure, file and class names, how state is organised, and so on. The ticket must not read as "copy this pixel by pixel with no room for decisions" — the goal is that it looks and behaves like the design, leaving the how to whoever builds it. If there is no specific design for a given detail, say so in the ticket (do not claim "follow Figma" when nothing is documented for that case) and let it be resolved with the rest of the design system already in use on the project.
- **`[INT-N]`**: this is the integration of what the corresponding FE and BE tickets have already built — connecting the real frontend to the real backend, replacing the fakes used to make progress in parallel. In this team's practice, whoever did the FE ticket usually ends up doing the integration too (because they already know the fake that has to be replaced and how the contract was shaped on the client side) — it is worth stating that in the ticket so it is not assumed that anyone can pick it up at random.
- **`[BE-N]`**: this is pure backend — there is no frontend involved yet to test it manually or visually. Tickets of this kind are tested with Postman (or an equivalent tool: curl, Thunder Client, Insomnia, whatever the repository already has installed — check whether collections already exist before assuming a tool) against the real endpoint, in addition to automated tests (the backend already has `supertest` as a dependency, which exists precisely for this). Do not write the acceptance criteria of a BE ticket as though someone were going to "see" the result on a screen — there is no screen yet.

## Consistency across tickets (model, field, and literal names)

When a BE ticket invents or assumes the name of a model, field, or state literal that also appears (or should appear) in another ticket, those names have to match — and when they do not, **fix them rather than leaving a note explaining the discrepancy.**

- **Source of truth, in this order of priority:** (1) what is already merged in the real code (`schema.prisma`, `src/`); (2) what a well-written sibling ticket has already defined for the same model — normally the ticket that first creates or extends that model (e.g. PLANIFY-39 creates `Evento`/`Participante`, PLANIFY-138 extends `Participante` with `esOrganizador` and `usuarioId` — no other ticket should invent a parallel `Member` model for the same thing); (3) only if neither exists, choose a name yourself and apply it consistently.
- **Convention already established on this project** (derived from the well-written tickets, not invented): Prisma models and fields are in Spanish, mirroring the business domain (`Evento`, `Participante`, `Grupo`, `esOrganizador`, `estado`), while application classes (controllers/services/repositories) and HTTP routes may be in English (`EventService`, `EventController`, `/events/:id/...`). Do not mix layers: `Evento.estado`, never `Event.state`; `Participante.esOrganizador`, never `Member.isOrganizer`.
- If you find a discrepancy between two tickets (one you wrote yourself, or one that was already in Jira), do not leave it as a note along the lines of "coordinate with the other ticket once this is decided" — determine which of the two has the correct name according to the priority above and correct the one that is wrong, so both agree. If the incorrect ticket is already in Jira (yours or someone else's), correct it there too (with the usual confirmation before writing to Jira).
- Before signing off on a new ticket, review the tickets from the same epic or about the same model that have already gone through this skill, looking specifically for this kind of invented naming — it is an easy mistake to make (and an easy one to carry forward unnoticed) when a ticket describes a model that does not exist yet.

## Proposing an order across tickets in the same epic

When you are asked to work on several tickets from the same epic at once (or the user gives a list of numbers with no stated order), do not simply rewrite them in the order requested or in Jira's numeric order — first propose a suggested order and, where applicable, a possible merge of tickets, and wait for the user to confirm before investing time in the full step-by-step of each one (if things have to be reordered or merged afterwards, that work is thrown away).

Heuristics for building the order (learned while rewriting the availability management epic — PLANIFY-50/51/52/53/54/55/56/57/58):

- **Within a single vertical slice (a Story with its BE/FE/INT trio), the natural order is BE → FE → INT.** That story's FE can be built against a fake while the BE does not exist, and the INT always needs both to be real and merged — it can never come first.
- **Do not assume a dependency between two tickets in the same epic merely because they are numbered consecutively.** Look at the text: if one BE neither mentions nor consumes data from another BE in the same epic (e.g. "confirm the time slot" does not need to read the heatmap, it only receives the date the organiser already chose), they do not depend on each other even if they are conceptually related — state that explicitly under "Depende de" instead of assuming a chain that does not exist.
- **There is a real dependency between two FE tickets when one is built literally on top of the other's screen** (e.g. the time-slot selector is added onto the same heatmap screen) — there the order matters even though nothing connects them at the data-contract level.
- **INT tickets always come last, after everything they integrate**, and if two INT tickets in the same epic turn out in practice to be a single continuous testing session (same environment, same test data, one step following naturally from the other, and neither adding new logic or test coverage), propose merging them into one — explain the reasoning and the downsides (see the merge section below) and let the user decide.
- When merging two Jira tickets into one: keep the lower key as the surviving ticket (update its `summary` to reflect the combined scope, not just the description), and leave the other with a short description pointing at the survivor plus a `Duplicate` link (`createIssueLink`) — do not delete the ticket or change its status unless the user explicitly asks; a ticket's status affects sprint tracking, and that is the team's decision, not yours.

Present the proposed order (and the merge, if applicable) in a short message before writing anything — something like a list with arrows or a table — and wait for explicit confirmation before starting on the step-by-step of each ticket.

## Fixed structure

Always these headers, in this order, in Spanish:

```
# [<KEY>](https://planify2026.atlassian.net/browse/<KEY>) [PREFIJO-N] Título

## Objetivo
## Depende de
## Paso a paso
## Fuera de alcance
## Criterios de aceptación
```

- **Objetivo**: 2-4 sentences in plain language explaining which user or system problem this ticket solves — not a task list, but the "what for" of the whole ticket.
- **Depende de**: link every ticket it depends on as `[PLANIFY-N](https://planify2026.atlassian.net/browse/PLANIFY-N)`. State explicitly whether those dependencies are already merged into `develop` or not (verify it against the git history, do not assume).
- **Fuera de alcance**: what is deliberately left unresolved here and why (so the ticket does not balloon or overlap with another). A couple of bullets is enough; if there is a non-obvious reason for leaving something out, state it.
- **Criterios de aceptación**: see its own section below.

## The golden rule for each step of the "Paso a paso"

This is the most important part of the skill. Every step — not every few steps, **every one** — must explain in prose (not as a one-line imperative):

- **What** is concretely done.
- **What it is for**: which real problem it solves, not just "do X" but why X matters in this particular flow.
- **Exactly where it goes**: a real file or folder path in the repository (`lib/features/invitations/domain/...`, `src/routes/router.ts`), never "in the appropriate file" or "wherever it belongs". If there is a choice between two possible locations, explain why one and not the other (e.g. "this goes in `lib/core/` and not inside the feature, because it is an app-wide event, not specific to this screen").
- **Why it cannot be skipped**: what ends up broken, ambiguous, or silently wrong if someone skips this step.

A step can — and generally should — take a full paragraph, not a single sentence. A ticket has **no 10-step limit** — split into more steps where that helps clarity, instead of packing two ideas into one number.

Examples of "generic" steps to avoid (and how to fix them):

| Generic (avoid) | With the rule applied |
|---|---|
| "Inicializar app_links." | Explains what the package is, whether it is already declared as a dependency but unused, in which file or folder that initialisation belongs and why there, and what happens if each screen initialises it on its own instead of centralising it. |
| "Centralizar la escucha." | Explains centralising it *where* (which file or provider), *what for* (preventing the same event from triggering two reactions when two widgets listen separately), and which concrete bug appears if it is not centralised. |
| "Agregar tests." | This kind of step does not belong in the step-by-step at all — it goes under Criterios de aceptación (see below). |

### Code snippets: yes, but not solved

Including a code fragment as an example is fine and welcome — a manifest or config block, the minimal usage of a package taken from its documentation, the shape of an interface. They help the reader understand the shape of what they have to write. But the snippet must **never** be the complete solution to the step or the ticket — if the snippet solves the whole problem, the reader learns nothing and merely copies. State explicitly when a snippet is "for reference only" and not the final code.

## Criterios de aceptación: bullets, two groups

Never prose, always bullets, always split into:

- **Funcionalidad mínima esperada**: the observable behaviour the ticket must deliver without exception (happy paths and the obvious edges: invalid input, empty case, network error, etc.).
- **Qué tiene que traer la PR**: here go, as bullets — **never as numbered steps in the "Paso a paso"** — items such as:
  - New tests for the code created in this ticket (pre-existing tests are not enough).
  - For a frontend ticket: screenshots of the flow or screen that was built, because that is what demonstrates the visual base is genuinely done, beyond what the diff shows.
  - That the repository's relevant quality tooling runs without errors (analyze/lint + format + tests, depending on the repository).
  - That CI is green.
  - Reproducible evidence for an integration ticket (the exact commands used, logs or screenshots of each case tested) — whoever reviews the pull request generally does not have the same environment running.

If any of the repository's quality scripts (tests, lint, etc.) is still a stub that runs nothing real, say so explicitly instead of assuming that "run the tests" already means something.

## About Jira itself

- The site is `planify2026.atlassian.net`, project **PLANIFY**.
- To read an existing ticket: look it up by its key (e.g. `PLANIFY-34`) and request the description field — that shows you the current text and, where applicable, gives you the style benchmark. Use whichever Jira/Atlassian tooling your environment provides (MCP, REST API, CLI, whatever it is) — this skill does not depend on a particular integration.
- To write the result into Jira: update the ticket's description field with the generated markdown. **This modifies a shared team artefact** — do not do it without explicit confirmation from the person using you, for that specific ticket. Show the draft first (in chat or in a file) and get a green light before writing to Jira.
- If you produce a draft file before uploading to Jira, save it in a temporary working location, not inside `planify-mobile` or `planify-backend`.

## What this skill does NOT do

- It does not touch code in `planify-mobile` or `planify-backend` — not even to "just try something".
- It does not create branches, commits, or pull requests in those two repositories.
- It does not upload anything to Jira without explicit permission for that particular ticket.

## Ejemplo de uso

**Pedido:** "Mejorá el PLANIFY-40 con un paso a paso como el del 33."

**Resultado:** La descripción completa del ticket en español, con Objetivo, Depende de (indicando si cada dependencia ya está mergeada), un Paso a paso donde cada paso dice qué se hace, para qué, en qué archivo real va y por qué no se puede saltear, Fuera de alcance y Criterios de aceptación. Antes de escribir en Jira, muestra el borrador y pide confirmación.
