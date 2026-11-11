---
name: g01-steering-feedback-triage
description: "Convierte el feedback crudo de un Steering, una demo o una revisión de clase en TODOs clasificados y asignados por rol en el vault del equipo: lo captura textual, busca la causa real en el artefacto presentado, lo clasifica por destino (Linear, deck, equipo directivo, postura a definir) y lo distribuye en los archivos TODO de cada rol sin duplicar el razonamiento. Usala cuando hay notas de un Steering o una demo y hay que decidir a dónde va cada punto."
author: Tomás
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: "01"
  autor:
    nombre: Tomás Roldán Borjas
    github: TomRolB
  responsables:
  - TomRolB
  madurez: usado-en-proyecto
  relacionados:
  - g01-cinematch-steering-prep
---
# Steering feedback triage

Raw feedback is not a task list. Almost every comment describes a symptom, and several different comments usually share a single cause. Turning them into TODOs before interpreting them produces tasks that fix nothing.

The note content itself is written in Spanish.

## 1. Capture it verbatim, with an author

The note goes in `Demos/<Nombre (dd-mm)>/Feedback.md`, with `author:` in the frontmatter.

Write what was said, as it was said, including who said it and what it referred to. Sub-bullets are what carry that context. Everything else depends on this step: a comment stripped of who said it and which slide it was about cannot be interpreted later.

Do not tidy it up and do not turn it into tasks yet. Keep every point; if the team sees one differently, that view goes as its own sub-bullet.

## 2. Put the artifact next to it

Copy the deck that was presented into the same folder, as `Steering N.pdf`. The feedback and the thing it reacts to travel together.

Without this, step 3 is impossible, and months later nobody can reconstruct which slide each comment was about.

## 3. Find the cause, do not restate the comment

Read the deck slide by slide against the feedback, and for each point ask what in the artifact produced it. Two things come out of this that a literal reading never gives you:

- **Different comments with a single cause.** Several comments about scope and schedule can be one problem: a scope slide that lists modules and a schedule slide that lists workstreams are two taxonomies of the same scope. Fixing one alone changes nothing.
- **Comments whose fix is not where they point.** A remark about how a figure reads can come from missing context: a percentage shown without its planned figure beside it reads as being behind, and the fix is the planned figure, not the wording.

Cite slides by their title, since that is how whoever reads later will look for them.

## 4. Classify by destination, still without an owner

Four buckets. Owners come later, in step 6, once every point has a destination.

| Bucket | What lands there |
|---|---|
| **A Linear** | Product or code work. Ends up as an issue. |
| **Al deck** | How we present: consistency across slides, legibility, how things are named. |
| **Al equipo directivo** | Our own process: checklists, metrics we committed to showing. |
| **Postura a definir** | Open questions where the team's view still has to be worked out, to discuss at the next meeting. |

The fourth bucket is the one most often lost: an open question that is not written down comes back unanswered at the next meeting.

## 5. Write the classification into the feedback note itself

At the end of `Feedback.md`, under `# Dónde va cada punto`, with one section per bucket. In prose, not tables: the reasoning needs to explain why, and a cell has no room for that.

The why lives here and nowhere else. The TODOs will link back to this note.

## 6. Distribute by role, not by person

Roles rotate monthly, so an item assigned to a person is orphaned when the rotation happens. Items go to `TODO/TODO <Rol>.md`.

- **PO** owns Linear: creating the issues is theirs, even if someone else executes them.
- **QA** takes testing and CI.
- **Tech Lead** takes the technical work and the data that PM later presents.
- **General** takes what belongs to everyone by design, plus deck and demo work.

Record dependencies in both directions. If a QA investigation blocks a PO issue, say so in both files.

Each item carries the action and a link back to `Feedback.md`. **Do not repeat the reasoning**, which already lives in step 5.

## 7. Pick the section by date

The TODO files use `# Semana N (dd/mm)` sections. Weeks start on Thursdays, and Semana 1 was 13/08. To find which week you are in, look at the last section of `TODO/TODO QA.md`, the file that stays most current, and continue from there. Do not invent empty week sections.

**Exception for demo work.** Deck and delivery work does not belong to one particular week; it is what has to be ready before the next demo. That goes under `# Para el Steering N (dd/mm)`, and it is worth stating in the note that the exception is deliberate, so it does not read as an oversight.

## 8. Separate what is not a task

A standard and a position are never completed. As checkboxes, someone ticks them off and they are lost.

- The **deck rules** that come out of step 3 go into their own note once agreed.
- The **positions** from the fourth bucket go into their own note.

What stays in the TODO is the task of writing that note, not the note itself.

## Ejemplo de uso

**Pedido:** Te paso mis notas del feedback del último Steering, ¿a dónde va cada punto?

**Resultado:** Guarda el feedback textual en `Feedback.md` junto al PDF presentado, agrupa los comentarios por su causa en el deck, los clasifica en los cuatro destinos explicando por qué, y carga cada ítem en el TODO del rol que corresponde con un link a la nota.
