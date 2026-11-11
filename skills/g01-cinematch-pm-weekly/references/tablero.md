# The Tablero

`Tablero_Estado_Proyecto` is the cátedra's shared Google Sheet. Each team edits only its own tab (ours is in [project.json](../project.json)). The `RESUMEN` tab is the professors' view: it shows every team's colors for one selected week, so never edit it. The `listas` tab holds the dropdown values.

## Blocks of the team tab

| Block | What goes in it | Where the value comes from |
|---|---|---|
| Header | Project, PM, members, remote or not | The rotation. Update the PM at each sprint start |
| ESTADO SEMANAL | One column per week, headed by its report Monday and week number. Rows: General and the five areas | Section 5 of the skill. General follows from the five areas |
| Motivo / Acción tomada | One cell per area, not per week: it describes the area's current yellow or red | Cause and concrete action, rewritten whenever the color changes |
| Avance Global [%] | The project's physical progress | EV / BAC from the EVM ([evm.md](evm.md)), the same figure presented at the Steering |
| Fecha de Fin Prevista | When the project is expected to end | The Entrega 3 date, unless the schedule says otherwise |
| Actividades Clave | One row per module: Estado (Finaliz., En curso, Pend.), Avance, end dates (baseline, estimated, actual), Desvío in days, comment | Linear: closed baseline points of the module, last merge for the actual date |
| INCIDENTES | Problems that happened: description, Estado (Abierto, Cerrado), Criticidad (Baja, Media, Alta), dates, resolution | What went wrong this week, including KPI days lost |
| PRODUCTO > URL | The production URL | The deployed frontend |

## Rules the checks enforce

- **General**: Rojo with one red area or three yellows, Amarillo with one yellow, Verde otherwise (printed on the RESUMEN tab). A red General can come from this rule alone, not from a crisis call.
- **Desvío** is the template's formula, `=IF(L<>"",J-L,"")`: F. Fin L. Base minus F. Fin Real, in days. **Positive means finished early, negative late**, and an open activity has no Desvío. Never type it by hand: a typed value easily carries the opposite sign. If a row lost the formula, restore it. A delay on an open activity shows as a F. Fin Estimado later than its F. Fin L. Base, explained in Comentarios.
- **Finaliz.** needs 100% and a F. Fin Real. Anything not finished with a F. Fin Estimado in the past is late, and its estimate must be moved.
- **An open incident** needs a F. Límite; past it, it is overdue. Criticidad Alta means escalating to the professors.
