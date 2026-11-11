---
name: g01-cinematch-steering-prep
description: "Prepara un Steering de Cinematch de punta a punta, salvo las slides de presupuesto y EVM: la nota fuente slide por slide con cada cifra trazada a su origen, el cruce para que ninguna slide contradiga a otra, las reglas que dejó el feedback anterior, las preguntas abiertas con responsable y el checklist de entrega con un único dueño. Usala al empezar, armar o revisar el deck de un Steering o una demo, o para saber si está consistente y qué hay que subir; los números de EVM salen de g01-cinematch-steering-evm y el feedback posterior va por g01-steering-feedback-triage."
author: Tomás
metadata:
  tipo: skill
  area:
  - gestion
  - documentacion
  fase:
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - linear
  - github
  - google-drive
  grupo: "01"
  autor:
    nombre: Tomás Roldán Borjas
    github: TomRolB
  responsables:
  - TomRolB
  madurez: experimental
  relacionados:
  - g01-cinematch-steering-evm
  - g01-cinematch-demo-recording
  - g01-steering-feedback-triage
  - g01-cinematch-baseline-change
  - g13-preparador-de-steering
  - g11-auditar-steering
---
# Cinematch Steering prep

A Steering is read as a whole: every slide has to agree with the others, with the Tablero and with the previous Steering, and every correction already received has to be applied. This skill builds the deck from a source note where every figure names its origin, checks it against everything said in earlier feedback, and closes with a checklist that has one owner.

Notes you write are in Spanish. This skill is in English.

## 0. Never write to a source

This skill reads Linear, GitHub, Drive and the vault, and writes only notes in the vault. When the deck and a source disagree, the mismatch is listed for whoever owns the source (the PM for the Tablero and the workbook, the PO for Linear), never fixed here. Uploads to the campus are done by the checklist's owner.

## 1. Start from the calendar and everything said before

1. `python ../g01-cinematch-pm-weekly/scripts/pm.py calendar` gives the Steering date and the period it cuts at. A Steering falls on the Thursday that closes its period, so work merged that day counts, and the deck says so.
2. Read every earlier Steering folder in `Demos/`: the source note, the presented PDF, and every feedback note (the meeting, the one addressed to all teams, the written one from the campus). Feedback accumulates: a correction from the first Steering still applies to the last.
3. Read the `# Para el Steering N (dd/mm)` sections of the files in `TODO/`. That is deck work the team already committed to.
4. Create `Demos/<Nombre (dd-mm)>/` and, inside it, the source note `Steering N (md).md`.

## 2. The source note

One note holds the whole deck, in the format the professors have already seen:

- **Frontmatter** with `description` and `author`.
- **A header block**: the draft date, the convention that italics are build notes and not slide text, the marker `[A CONFIRMAR: Qn]` for data no source gives, and the build rules for this deck (section 3).
- **One section per slide**: a title that states the conclusion rather than the topic, the content as tables, build notes in italics, and the speaker notes as a quote.
- **An annex that never reaches the deck**: a table mapping each feedback point to the slide that answers it, where every number comes from, and the open questions (section 6).

## 3. Rules every deck follows

They come from the feedback received at earlier Steerings, and every deck applies them:

- **Legible when projected.** Nothing under 18 pt. Tables and images before paragraphs. What does not fit goes to the annex or behind a link.
- **One taxonomy of modules** across scope, progress, schedule and milestones: the same rows, with the same names, in every slide and in the Tablero's Actividades clave.
- **Scope changes, activity progress and milestones achieved are three separate slides.** The scope slide is the only one that tells the story of the scope.
- **Every progress figure has its planned figure beside it.** A percentage alone reads as being behind.
- **The unexpected goes first**: a challenge or a change, with its impact on scope, schedule and cost, the decision record, the trade-off and how the plan recovers.
- **The gantt follows the standard**: baseline and actual on the same bar, milestones as diamonds, the critical path highlighted, a line for today.
- **Risks are events**, named by the bad thing that may happen, each with id, probability, impact, score (expected monetary value when quantified), owner by role, mitigation and contingency. The highest exposures go on the slide and the full register behind a link that can be opened during the questions. A risk that already happened is an issue and goes elsewhere.
- **The snapshot and the projection**: the EVM slides show where the project ends, not only where it is.
- **Product requirements the professors made mandatory are checked in the running product** before the Steering, with the browser console open.

When a triage adds a deck rule ([g01-steering-feedback-triage](../g01-steering-feedback-triage/SKILL.md), step 8), add it to this list too, so the next deck starts with it.

## 4. Where each slide comes from

| Slide | Source | What to watch |
|---|---|---|
| The unexpected | The decision record of the change (an ADR) | First after the cover, when there is one |
| Product | Production, and the video from [g01-cinematch-demo-recording](../g01-cinematch-demo-recording/SKILL.md) | What changed since the previous Steering, not the whole product again |
| Team | The current rotation | Management roles of this sprint, and the developers' lanes |
| General status | The Tablero's latest loaded week | The colors are the Tablero's. If the deck wants a different reading, the Tablero changes first or the slide says why |
| Scope: change control | The baseline changelog in `Cronograma/Cronograma.md` | One row per approved change with its Δ HH and baseline version. [g01-cinematch-baseline-change](../g01-cinematch-baseline-change/SKILL.md) produces the rows |
| Progress by module | Closed baseline points per module in Linear, counted with the same gantt points as the EVM | Planned beside actual; the total equals EV / BAC on the EVM slide |
| Schedule | The current gantt in Drive | Section 3's standard |
| Milestones | The milestone list presented at the previous Steering | The same list, with base, actual or estimated date, deviation and status. Every change to the list is explained |
| Budget, EVM, S-curve | [g01-cinematch-steering-evm](../g01-cinematch-steering-evm/SKILL.md) | Built from the workbook, never retyped |
| Risks and opportunities | The risk register | Section 3's structure; owners are roles that exist this sprint |
| Quality | GitHub (CI, pull requests, review rework) and the KPI platform | Every metric promised at an earlier Steering, with its number |
| Next steps | The plan for the next sprint | At the last Steering: what was delivered against the charter instead |

## 5. Cross-check before it is final

Every figure that appears twice must be the same figure:

- Total progress on the module slide = physical progress on the EVM slide = Avance Global in the Tablero.
- BAC on the scope slide = BAC on the budget slide.
- Colors on the status slide = the Tablero's latest week.
- Milestone dates = the gantt = Linear (due date for pending, merge date for achieved).
- The module rows are identical on the scope, progress, schedule and milestone slides.

List every mismatch with both values and both sources, and resolve it at the source.

## 6. Open questions

Every `[A CONFIRMAR]` gets a number (`Q1`, `Q2`...), the slide it affects, and who can answer it, by role, in the annex table. Resolve them before the dry run. A resolved one is crossed out with its answer next to it, never deleted.

## 7. Before and after presenting

Before:

- **A dry run on the real setup**, projected or shared at the size the room will see, to check legibility.
- **The live demo rehearsed** against production, with the console open.
- **The Tablero's week loaded** and the EVM workbook cut at the Steering's period.

After, run by **one owner named in the source note by role**. A verbal "everyone checks" is not an owner. Each item is ticked with its evidence (a link, or the campus confirmation):

- [ ] Deck PDF uploaded to the campus
- [ ] Demo video uploaded to the campus
- [ ] The PDF copied into the Steering's folder as `Steering N.pdf`, which the feedback triage needs
- [ ] The presentation added to every place that lists the project's presentations
- [ ] The feedback captured the same day, verbatim, with [g01-steering-feedback-triage](../g01-steering-feedback-triage/SKILL.md)

## Ejemplo de uso

**Pedido:** Empecemos el deck del próximo Steering.

**Resultado:** Crea la carpeta del Steering en `Demos/` con la nota fuente slide por slide (cada cifra con su origen y `[A CONFIRMAR: Qn]` donde ninguna fuente da el dato), aplica las reglas del feedback anterior, cruza las cifras que aparecen en más de una slide y cierra con el checklist de entrega con un único responsable.
