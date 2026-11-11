# Gantt spec for `scripts/gantt.py`

One JSON file per Steering. The full example is [gantt-steering-2.json](gantt-steering-2.json), the gantt shown at Steering 2.

| Key | What it is |
|---|---|
| `start` | ISO date of the first day of W1 (`2026-08-20`). Milestone dates are placed against it |
| `weeks` | `[label, first-day]` pairs, one per column, e.g. `["W9","15-10"]` |
| `today_week` | The column the cut falls on. Also where row notes start |
| `deliveries` | Vertical markers under the chart. `week` is the column whose left edge it sits on (use `n+1` for the end of the last week). `style`: `normal` (label only), `today` (red dashed line), `end` (light dashed line) |
| `sections` | Blocks of rows with a `title` and a `color` (`base`, `inc` or `crit`) |
| `sections[].rows[]` | `name`, `pts` (text on the right of the name), `segments`, optional `milestones`, `dim` (greyed row) and `note` (red text, e.g. POSTERGADO) |
| `segments` | `[first_week, last_week, kind]`, inclusive. Kinds: `done`, `pend`, `late`, `crit`, `inc`, `incdone` |
| `milestones[]` | Rows drawn right under their module: `name`, `actual` (dd-mm, real or estimated), optional `base` (dd-mm presented at the previous Steering), `kind` (`done`, `pend`, `crit`), optional `label` (text in the date column; defaults to `actual`) |
| `row_h`, `milestone_h`, `section_h`, `bar_h`, `diamond_r` | Optional sizes. Lower them if the script warns that the content is taller than 1080 px |

The legend is built from the kinds actually used, so an unused kind never shows up in it.
