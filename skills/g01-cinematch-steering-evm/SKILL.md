---
name: g01-cinematch-steering-evm
description: "Arma las slides de presupuesto, valor ganado y curva S de un Steering de Cinematch a partir del workbook de EVM del equipo: recalcula cada cifra desde los períodos con un solo redondeo, genera la curva S en SVG, cuenta la historia período a período y lista toda cifra del workbook que no coincide. Usala al preparar un Steering o una demo que muestre presupuesto, SPI, CPI, EAC o curva S, o para revisar si los números de una slide están bien; el resto del deck es de g01-cinematch-steering-prep."
author: Tomás
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - revision
  tecnologias:
  - python
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - google-drive
  - linear
  - github
  grupo: "01"
  autor:
    nombre: Tomás Roldán Borjas
    github: TomRolB
  responsables:
  - TomRolB
  madurez: experimental
  relacionados:
  - g01-cinematch-pm-weekly
  - g01-cinematch-steering-prep
  - g01-cinematch-baseline-change
  - g04-earned-value-presentacion
  - g02-valor-ganado-evm
---
# Cinematch Steering EVM pack

At every Steering the PM presents the budget, the earned value and the S-curve, and they have to agree with the workbook and with the previous Steering. Figures built by hand drift apart: a ratio rounded at a different step than its inputs shows the wrong second decimal, and a tab that missed a baseline change keeps the old BAC. This skill rebuilds every figure from one source, rounds once, and lists every place where the workbook shows something else. The rest of the deck, and its consistency with these slides, is [g01-cinematch-steering-prep](../g01-cinematch-steering-prep/SKILL.md).

Notes you write are in Spanish. This skill is in English.

## 0. Never write to a source

The workbook is exported read-only and never edited by this skill. When the workbook and the rebuilt figures disagree, the fix is listed for the PM to type, or the slide says which base it uses.

## 1. Before running it: the workbook has to be up to date

The script is shared with [g01-cinematch-pm-weekly](../g01-cinematch-pm-weekly/SKILL.md), which also sets it up (`doctor`, `fetch`). From that skill's folder:

1. `fetch <scratch folder>`, outside the vault.
2. `evm <scratch folder>`: every closed period up to the cut has EV and AC, and the cut cell matches the last of them. If not, load them first; the command names the cells. How EV is counted is in [references/evm.md](../g01-cinematch-pm-weekly/references/evm.md).
3. **A baseline change approved at this Steering** (a challenge, a cut, an addition) is decided before the numbers: it changes PV and the BAC from the cut onward, and it needs its ADR. Record it with [g01-cinematch-baseline-change](../g01-cinematch-baseline-change/SKILL.md) before building these slides. The numbers then measure against the new baseline, and the slide says so.

## 2. Run it

```
python ../g01-cinematch-pm-weekly/scripts/pm.py steering <scratch folder> --svg <scratch folder>/curva-s-steering-N.svg
```

`--cut N` measures at another period; by default it is the workbook's cut. A Steering falls on the Thursday that closes its period, so the work that merges that same day counts: say so on the slide, naming the issue.

The output has five blocks: budget, earned value at the cut, the four projections at completion, the period table (which is also the S-curve's data), and the consistency check.

## 3. Read the consistency block first

Each line is a figure the workbook shows that differs from the rebuilt one, with its cell. Typical causes: the cut cell not moved, or a baseline change applied to the EVM tab but not to the budget tab. Either the PM fixes the workbook by hand before the Steering, or the slide states which base each number uses. Never present a number that the workbook contradicts without saying why.

## 4. Write the note

It goes in `Demos/<Nombre (dd-mm)>/Presupuesto y Valor Ganado (corte PN).md`, with the same structure as the previous Steering's note of the same name:

- **Presupuesto**: the bridge from the original scope to the current BAC, one row per approved change, then OPEX, cost baseline, contingency, total and the margin against the Project Charter envelope.
- **Valor ganado**: SPI, CPI, TCPI and VAC; PV, EV and AC in HH and USD; the typical EAC and the capacity ceiling; the origin of the deviation against the original budget.
- **Curva S**: the chart and its table.
- **Speaker notes** for each slide, and an annex: where every number comes from, the capacity count, the projection variants, and the questions to be ready for.

Rules for the figures:

- **Copy them from the script's output.** Its rounding is half up, once, at the end; rounding again by hand changes the second decimal.
- **Tell the period story.** For each period since the last Steering, say what closed (EV) and what merged outside the baseline (AC without EV). Get it from Linear through the MCP, `prs --since`, and `gantt --ids` for the points. The period table of the previous Steering's note is the model.
- **Follow the number format of the previous note**: decimal comma for HH (`211,5 HH`), thousands comma for USD (`$8,813`), indices with two decimals.

## 5. The S-curve

The SVG is 1920×1080, in the look of the previous Steering's chart: the current PV, EV and AC with their points, the actual cost projected at capacity after the cut, the original baseline as a reference, the BAC and total budget lines, and the calendar milestones with the cut in red. Text is never under 18 px, a rule from the professors' written feedback on the first Steering.

Open it in a browser and look at it before using it: labels of milestones close together, or a budget line near the top, can collide. When it is final, put the SVG next to the note as the source, plus a PNG for the deck. Figma imports the SVG directly.

## 6. Questions to be ready for

With the numbers of this cut, be ready to explain:

- How the SPI is computed: PV is never changed backwards, and EV comes from closed issues.
- What the CPI measures, given that the actual cost is the team's capacity.
- Why the baseline changed, if it did, and what the ADR decided.
- Why EV jumped or stalled in a period: it moves when reviewed work merges.

## Ejemplo de uso

**Pedido:** Armame las slides de presupuesto, valor ganado y curva S para el próximo Steering.

**Resultado:** Verifica que el workbook esté cargado hasta el corte, corre `pm.py steering` con `--svg` y escribe la nota de Presupuesto y Valor Ganado con las cifras del script, la historia de cada período, la curva S en SVG, las preguntas para las que conviene estar listo y cada cifra del workbook que no coincide, con su celda.
