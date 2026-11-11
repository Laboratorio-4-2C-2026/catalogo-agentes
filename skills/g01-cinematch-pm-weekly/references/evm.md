# Earned value, week by week

The method was fixed at Steering 1 and applied at Steering 2. Read this file in full before changing anything.

More than one budget workbook can exist. The current one is the team workbook that includes the scope added at the last re-baseline. Older ones (the Project Charter's, or the cátedra's `10B` filled before the re-baseline) leave that scope out, so measuring against them gives a higher percentage that does not apply.

## The method

- **Unit**: development hours (HH), valued at the reference rate in the team workbook. Periods are weeks, Friday to Thursday (`pm.py calendar`).
- **PV**: the current baseline's planned hours per period. A baseline change alters PV from its cut onward, never backwards.
- **EV**: when a baseline issue closes (merged and Done, see the skill's cross-checks), it earns the points the gantt gave it, 1 point = 1 HH. Work outside the baseline earns nothing, even though it costs.
- **AC**: the team's capacity, 18 HH per period (3 developers × 6 h). If the team changes, AC changes.
- **Indices**: cumulative SPI = EV / PV and CPI = EV / AC, read at sprint close. A single week's SPI says little, because EV jumps when reviews merge together.

## The weekly increment

1. Take the period that just closed (`calendar`, "Last closed EVM").
2. In Linear, list the issues that reached Done in it, and keep those whose PR merged in it.
3. `pm.py gantt <scratch folder> --ids`, with those issues' ids, adds up their baseline points and names the ids the gantt does not have.
4. For each id not in the gantt, decide before counting it as zero:
   - **A `NEW-*` placeholder under its Linear number.** The re-baseline created placeholders that later became real issues; match by title, and by the drafts in `Issues/`.
   - **Added by a later baseline change.** A baseline change can add or remove items after the gantt was drawn; the change record says which and with how many HH.
   - Otherwise it is outside the baseline: no EV.
5. Load EV and AC in HH into the team workbook's `EVM` tab, on the cells marked for input (the rest are formulas); `pm.py evm <scratch folder>` names the cell of each missing period. Then move the cut, `FECHA DE CORTE` on the `Supuestos y Tarifas` tab, to the period just loaded: the USD rows, indicators and curves stop at it, and `evm` flags it when it lags.
6. A baseline change also touches the `Presupuesto` tab, whose BAC feeds the workbook's own indicators. `pm.py steering` lists every figure the workbook shows that no longer matches the EVM tab.

## State to keep in mind

The `EVM` and `Presupuesto` tabs are updated separately, so after a baseline change one of them can still hold the old BAC. Until both agree, the workbook's own BAC, total budget and physical progress differ from the EVM tab; `pm.py steering` shows where.

The cátedra's `10B` workbook (`pm.py evm --catedra`) can hold an older baseline than the team workbook. Check which one it holds before comparing them.
