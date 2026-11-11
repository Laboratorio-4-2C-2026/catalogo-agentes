---
name: g01-cinematch-steering-draft
description: "Arma el primer borrador del próximo Steering de Cinematch a partir de las notas del vault, el feedback de Steerings anteriores, Linear, el repositorio y Drive, y después entrevista al equipo en tandas cortas para completar lo que ninguna fuente responde. También genera la imagen del Gantt con hitos; orquesta g01-cinematch-steering-prep y g01-cinematch-steering-evm."
author: Francisco
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
  - revision
  tecnologias:
  - python
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
    nombre: Francisco Zizzi
    github: FranciscoZizzi
  responsables:
  - FranciscoZizzi
  madurez: usado-en-proyecto
  relacionados:
  - g01-cinematch-steering-prep
  - g01-cinematch-steering-evm
  - g01-cinematch-baseline-change
  - g01-steering-feedback-triage
---
# Cinematch Steering draft

A Steering deck is mostly derivable. Linear, the repository, the gantt, the workbook and the notes already hold almost every number, and the feedback notes hold every rule. What they don't hold is a handful of decisions and facts only the team knows: who held which role, what will merge before the cut, which of two contradicting notes is final. The way to get a good deck fast is to **draft everything that can be derived first, mark the rest, and only then ask**, a few questions at a time, each one tied to the slide it changes. A team member can react to a draft in minutes; an empty template with twenty questions costs an afternoon.

This skill is the workflow. The content rules live elsewhere and are not repeated here:

- [cinematch-steering-prep](../g01-cinematch-steering-prep/SKILL.md): the source note's format, the mandatory deck rules from earlier feedback, where each slide comes from, the cross-checks and the delivery checklist.
- [cinematch-steering-evm](../g01-cinematch-steering-evm/SKILL.md): the budget, earned value and S-curve slides, built with `pm.py steering`.
- [cinematch-baseline-change](../g01-cinematch-baseline-change/SKILL.md): when the Steering approves a scope change.

Notes you write follow [AGENTS.md](../../../AGENTS.md), so their content is in Spanish. This skill is in English.

## 0. Read-only on every source

Linear, GitHub, Drive and the Tablero are read, never written. The skill writes only the Steering's folder in `Demos/`. When a source is wrong, the fix goes to the annex for its owner. The project instructions also say that some notes are proposals, not decisions: a note titled "(propuesta)" or a line that says "propuesto" is not a fact until someone confirms it.

## 1. Check access before anything else

Say in one short message what you can and cannot reach, so the person knows what the draft will be missing:

- the vault (`Demos/`, `KPIs/`, `Issues/`, `Cronograma/`, `TODO/`, `Decisiones Técnicas.md`);
- Linear through the MCP (read only);
- Drive: the gantt, the EVM workbook, the Tablero, and any decision record (ADR) the team keeps there;
- the app repository (local `git log` works even when the GitHub API does not);
- the project's docs and memory.

**Past chat sessions cannot be read.** What survives a session is what someone saved: the transcripts in the Steering folders (`Transcript*.md`, `Transcripcion*.md`) and the project docs. Read those to learn how the previous gantt, budget and EVM were built, and say plainly that the chats themselves are out of reach.

## 2. Gather, and trust the right source for each thing

Do everything in [steering-prep §1](../g01-cinematch-steering-prep/SKILL.md#1-start-from-the-calendar-and-everything-said-before): calendar, every earlier Steering folder with all its feedback notes, the `Para el Steering N` TODOs. Then also:

- **What happened that was not in the plan**: challenges, the professors' messages (for example `KPIs/Consulta Whatsapp.md`), the ADRs. The deck opens with this.
- **The real state at the cut.** Linear lags the repository: an issue can sit In Review for days after its PR merged. Check merge dates in `git log` (or `pm.py prs`) and treat merged work as done, saying so.
- **The latest version of each decision.** A Drive document can be newer than its copy in the vault, and the gantt someone drew can contradict the ADR. When two sources disagree on a decision, do not pick one: it becomes a question.

## 3. Draft first, with every unknown marked

Create `Demos/<Nombre (dd-mm)>/Steering N (md).md` in the format of [steering-prep §2](../g01-cinematch-steering-prep/SKILL.md#2-the-source-note), and fill every slide you can. Anything no source gives is written in place as `[A CONFIRMAR: Qn]`, numbered, and listed in the annex with the slide it affects. Include a table mapping each earlier feedback point to the slide that answers it: it is the fastest way for the team to see the deck took the feedback.

Write the budget and EVM slides with [cinematch-steering-evm](../g01-cinematch-steering-evm/SKILL.md) in their own note, and keep only a summary of their numbers in the main note, so the two never disagree.

When the state at the cut is uncertain (it usually is two days before), **don't guess one scenario: draft both.** For example, A = what is in review merges, B = the whole sprint closes, with each figure in two columns. The team picks on the morning of the Steering by looking at Linear.

## 4. Grill, a few questions at a time

Ask with the multiple-choice tool, at most four questions per batch, each with concrete options and the recommended one first. Ask what changes the most numbers first:

1. What closes before the cut (or confirm the two-scenario plan).
2. How actual cost is measured (real hours, or the team's fixed hours).
3. Scope decisions that sources contradict or leave as proposals: what was cut, deferred or added, and by which document.
4. Roles this sprint, dates the team committed to, what is shown live in the demo.
5. Risk probabilities and impacts, and where the full register lives.

How to handle the answers:

- **Apply each batch to the draft before asking the next**, cross out the answered `Qn` with its answer, and say in one line what changed.
- **When an answer is a rule rather than a value** ("if it fits in capacity keep both, otherwise drop whichever leaves fewer hours free"), do the arithmetic yourself, decide, and show the count in the annex.
- **When someone says they can't find something**, point to the slide and row, and paste the rows into the reply. Don't re-ask the question.
- **When the team has no preference**, take the option you recommended and say so in the note.
- If the person starts asking why a number looks the way it does ("why is CV so large if the budget barely moved?"), answer it, and put the answer in that slide's speaker notes: the professors will ask the same thing.

## 5. Draw the gantt with its milestones

The professors asked for the standard twice: baseline and actual, milestones as diamonds, the critical path, a line for today, readable when projected. Build it with the bundled script, in the deck's dark look and at 16:9:

```
python scripts/gantt.py <spec.json> <folder>/gantt-steering-N.svg --png <folder>/gantt-steering-N.png
```

The spec format is in [assets/gantt-spec.md](assets/gantt-spec.md) and the Steering 2 gantt is the worked example in [assets/gantt-steering-2.json](assets/gantt-steering-2.json). Rules for filling it:

- **Rows are the deck's module taxonomy**, with their baseline points. Scope added since the original baseline goes in its own section. Scope that was cut or postponed stays as a greyed row with a red note naming the change, so the slide tells the same story as the change-control slide.
- **Milestones are the ones presented at the previous Steering**, each one placed right under the module that closes it. `base` is the date shown then, `actual` is the merge date of its last issue, or its Linear due date if it is pending. Every milestone whose name or date changed gets a line in the milestones slide saying why.
- **Segments follow what actually happened** (Linear and merge dates), not the plan. A pending segment on the critical path is `crit`.
- **Render it and look at it.** The script warns when the content is taller than the slide or the legend is wider than it. Also look for labels running off the right edge (a base date after the last delivery) and diamonds hidden behind a line.

## 6. Review the team's slides when they come back

The team builds the real slides in their own tool and often sends a screenshot back. Check, in this order:

- **Every number against the note**: typos in a bridge table show up as totals that don't add up.
- **Labels that stopped being true.** For example, "EAC = BAC / CPI (conservadora)" is conservative only while the CPI is below 1.
- **Color semantics.** Green means favorable: an index above 1, a positive SV, CV or VAC, a TCPI below 1, a negative performance deviation. A scope change is a decision, so it stays neutral. PV, EV and AC use the S-curve's identity colors, never good/bad colors, so the table and the chart match.
- **Legibility**: nothing under 18 pt when projected, no grey text on the black background, no divider line crossing a label.

## 7. Writing to the vault

The vault is synced by an automatic backup. Before replacing a note you wrote earlier, check that nobody edited it since (its modification time or its content); if someone did, merge into their version instead of overwriting it. After writing, check the change landed: a sync can bring back an older copy. Images go next to the note, the SVG as the editable source and a PNG for the deck.

## 8. Close the session

- List the open `Qn` with who can answer each one by role, and point to the delivery checklist in [steering-prep §7](../g01-cinematch-steering-prep/SKILL.md#7-before-and-after-presenting).
- Offer to save the session as `Transcripcion sesion Steering N.md` in the Steering's folder: every message verbatim, tool calls summarized in one line, no local paths or machine names. It is how the next Steering's draft learns how this one was built.

## Ejemplo de uso

**Pedido:** Necesito empezar el borrador del próximo Steering.

**Resultado:** Escribe en la carpeta del Steering en Demos/ un borrador con todo lo derivable de las fuentes, marca lo que falta y hace pocas preguntas por vez al equipo, aplicando cada respuesta al borrador.
