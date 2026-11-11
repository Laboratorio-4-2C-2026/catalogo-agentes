---
name: g01-cinematch-baseline-change
description: "Registra un cambio de línea base de Cinematch (recorte, diferimiento fuera del proyecto, agregado de alcance, trabajo de un challenge o replanificación de horas entre períodos) en todos los lugares donde tiene que impactar: el registro con su impacto en alcance, cronograma y costo, el nuevo BAC y el PV por período desde el corte, el changelog de la línea base, Decisiones Técnicas, el Tablero y la lista de cambios de Linear para el PO. Usala cuando se decide o propone cortar, mover o sumar alcance, o cuando el plan, el deck y el workbook no coinciden después de un cambio; decidir qué cortar es de g01-cinematch-issue-management."
author: Tomás
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
  - google-drive
  - linear
  grupo: "01"
  autor:
    nombre: Tomás Roldán Borjas
    github: TomRolB
  responsables:
  - TomRolB
  madurez: experimental
  relacionados:
  - g01-cinematch-pm-weekly
  - g01-cinematch-steering-evm
  - g01-cinematch-issue-management
  - g02-control-de-cambios
  - g11-analizar-cambio-alcance
---
# Cinematch baseline change

A baseline change that was decided but never recorded is the most expensive drift there is. The workbook keeps measuring against the old plan, the gantt shows another, the deck a third, and every number presented afterwards needs an explanation. The method here: one change record, the numbers recomputed from the cut forward, and every document that holds the baseline updated, or listed for its owner, on the same day.

Notes you write are in Spanish. This skill is in English.

## 0. Never write to a source

The workbooks and the gantt are exported read-only with [g01-cinematch-pm-weekly](../g01-cinematch-pm-weekly/SKILL.md) (`fetch`). The PM types the new values. Linear changes are listed for the PO. This skill writes only notes in the vault.

## 1. Is it a baseline change?

It is when scope enters or leaves the baseline, or when planned hours move between periods, and someone with the authority approved it: the team at a planning session, or the professors at a Steering.

It is not, and is recorded elsewhere:

- **An issue split or re-estimated inside its gantt task**, with the task's points unchanged: that is planning ([g01-cinematch-issue-management](../g01-cinematch-issue-management/SKILL.md)). How a split task earns value is in [evm.md](../g01-cinematch-pm-weekly/references/evm.md).
- **An issue cancelled because another one already covers it**: no scope left. It goes to `Decisiones Técnicas.md` only.
- **Management work**: it never enters the baseline, which capitalises developer effort only.
- **A delay on its own**: it is a deviation, and SPI shows it. Moving late work into later periods becomes a baseline change only when it is approved as one, and even then the deviation already measured stays where it is.

## 2. Gather before computing

1. **The decision**: what enters, what leaves, what moves, who approved it and when. `python ../g01-cinematch-pm-weekly/scripts/pm.py calendar` gives the period the change cuts at and maps gantt weeks to EVM periods.
2. **The baseline points of every item**: `pm.py gantt <scratch folder> --ids ...` prints each task's points and week. An id the gantt does not have is resolved with the placeholder rule in [evm.md](../g01-cinematch-pm-weekly/references/evm.md) before treating it as zero.
3. **The current baseline**: `pm.py evm <scratch folder>` prints PV, EV and AC per period, and the BAC.
4. **The capacity left**: 18 HH per period (3 developers × 6 h) for every period after the cut, in the same unit as the baseline.

An item that already earned value cannot leave the baseline: its EV stays. Only what is not done can be cut or moved.

## 3. Compute the new baseline

- **Δ HH per item and the net Δ.** New BAC = old BAC + net Δ.
- **PV per period from the cut onward.** Take each item out of the period where the gantt planned it, and put new or moved items into the period where they are now planned. **Periods up to the cut never change** (evm.md: PV never changes backwards).
- **Fit.** The PV left after the cut has to fit the capacity left. If it does not, the change is incomplete: say how many hours are still over, and that another cut is needed.
- **What moves at the cut, and what does not.** PV, EV and AC to date are untouched, so the SPI and CPI to date stay the same. The BAC changes, so the Avance Global (EV / BAC) moves without anything new closing, and TCPI, EAC and VAC move with it. Say this wherever the new figures appear.
- **What moves later.** A cut lowers PV from the cut onward, so the next periods' SPI improves without anyone working faster. Every report after the change says it measures against the new version.
- **USD** at the reference rate of the team workbook. Round once, at the end, half up, as [g01-cinematch-steering-evm](../g01-cinematch-steering-evm/SKILL.md) does.

## 4. Write the record

**In `Cronograma/Cronograma.md`**, the baseline changelog: one entry per approved change set, newest on top, titled `## yyyy-mm-dd · Línea base vN: <qué cambió>`. The version increases even when the net Δ is zero, because the distribution of PV changed. The entry holds:

- A table: Acción (entra, sale, se mueve), Elemento, Δ HH, Justificación.
- BAC before and after, and the PV per period from the cut, old and new.
- The capacity check.
- What was deliberately protected, and why (usually the critical path).
- Who approved it and when.
- What was deferred out of the project, said as a cut. "Later" with no period left in the project is a cut.

**A change driven by a challenge or a technical decision** also gets an ADR with an `Impacto en el alcance` section: action, element, justification, the hours by team, and why this item was chosen over the next candidate. The changelog entry links it.

**In `Decisiones Técnicas.md`**: the decision, its rationale and the alternatives rejected.

The previous version is never deleted. The changelog is history, and the notes that described the old plan get `SUPERADO por` with a link to the new entry.

## 5. Where else it lands

| Place | What changes | Who |
|---|---|---|
| Team workbook, `EVM` tab | PV per period from the cut, BAC | PM types it |
| Team workbook, `Presupuesto` tab | BAC and total budget, which the workbook's own indicators read | PM types it |
| Gantt in Drive | Tasks removed, added or moved | Whoever keeps the gantt |
| Tablero | The week's Alcance signal, with the change as evidence; the F. Fin L. Base of every affected Actividad clave (it moves only with a baseline change); the Avance Global against the new BAC; a comment on the affected rows | PM, through the [weekly control](../g01-cinematch-pm-weekly/SKILL.md) |
| Linear | Issues that leave the baseline, new issues, new due dates (each the Thursday of its week) | PO, from the list this skill writes |
| The next Steering | One row in the scope slide's change log, and one in the budget bridge | [g01-cinematch-steering-prep](../g01-cinematch-steering-prep/SKILL.md) and [g01-cinematch-steering-evm](../g01-cinematch-steering-evm/SKILL.md) |
| The risk register | Only if the change retires a real project risk or creates one | The register's owner |

Everything the PM has to type goes into `TODO/TODO PM.md`, under the current `# Semana N (dd/mm)` section, with the exact cells.

## 6. Verify

After the PM types the values: `fetch` into a new folder, `diff` against the export taken before, then `evm` and `steering`. The consistency block of `steering` must show the `EVM` and `Presupuesto` tabs agreeing on the new BAC. The export is the only proof that the workbook says what was decided.

## 7. Traps

- **Changing the PV of closed periods.** It rewrites the past and makes the SPI meaningless.
- **Updating the `EVM` tab and forgetting `Presupuesto`.** The workbook's own indicators keep the old BAC, and the deck shows two different totals.
- **Recording the change only in the deck or in a weekly control.** The changelog is where it will be looked for.
- **Presenting an SPI that improved after a cut as recovery.** It improved because PV dropped. Say so.

## Ejemplo de uso

**Pedido:** En el Steering aprobaron sacar una funcionalidad del alcance. ¿Cómo queda la línea base?

**Resultado:** Calcula el Δ HH, el nuevo BAC y el PV por período desde el corte con el chequeo de capacidad, escribe la entrada del changelog de la línea base y la decisión, y lista lo que el PM tiene que cargar en el workbook (con celdas) y los cambios de Linear para el PO.
