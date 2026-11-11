---
name: g01-cinematch-kpi-watch
description: "Verifica si el reporte diario de KPIs de Cinematch llegó hoy a la plataforma de KPIs de la cátedra, leyendo las corridas y los artifacts del workflow KPI Report, y dice qué tiene que pasar antes de la medianoche si no llegó. Usala para saber si hoy salieron los KPIs, si un día está en riesgo o perdido, o por qué bajó la nota diaria; a diferencia del control semanal, mira el día en curso y nunca corre el workflow."
author: Tomás
metadata:
  tipo: skill
  area:
  - gestion
  - devops
  fase:
  - revision
  tecnologias:
  - python
  - github-actions
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
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
  - g02-kpi-compliance-check
  - g04-chequeo-de-kpis
---
# Cinematch KPI watch

The KPI challenge is graded per **reception day**, every day of the challenge: a day on which the platform received nothing scores zero, and nothing done later recovers it. The weekly control ([g01-cinematch-pm-weekly](../g01-cinematch-pm-weekly/SKILL.md)) looks back at the week; this skill looks at today, while there is still time to save it.

Notes you write are in Spanish. This skill is in English.

## 0. Never write to a source

This skill only reads the app repository, the platform's data branch and the workflow's artifacts. It never runs, re-runs or cancels the workflow, never touches a secret, and never writes to the platform. When a day is at risk, it names the action and who can take it; a person takes it. The management team does not commit to the app repository.

## 1. Run it

```
python ../g01-cinematch-pm-weekly/scripts/pm.py kpi-watch
```

The script is shared with `g01-cinematch-pm-weekly`, which also sets it up: run its `doctor` once. `gh` needs read access to the app repository and to the platform repository (both in [project.json](../g01-cinematch-pm-weekly/project.json)).

**When.** The workflow is scheduled twice a day, the second run being a retry the platform ignores if the first arrived. GitHub starts scheduled runs late, by hours: the script reads the cron from the workflow file and prints the longest delay of the last week. Run the watch once in the evening, after the first run has had time to start, and again before midnight if it says WAITING or AT RISK. A run that starts after midnight counts for the next day.

## 2. What it reads, and how each source lags

| Source | What it proves | Lag |
|---|---|---|
| The platform's `data` branch | What the platform received, which is what is graded | Usually shows today's values only the next day |
| The `KPI Report` runs in the app repository | Whether a run happened and how it ended | None |
| Each run's artifact (`kpi-report-<date>`) | The body sent and the platform's answer: a 2xx with the KPI list means the platform accepted them | None; kept 90 days |

The artifact is the only same-day proof. It also tells a real report from a manual `register-catalog` run or a dry run, which a successful run alone does not. A run that could not measure some KPI still sends the rest and ends in error, so a red run does not mean nothing arrived, and the artifact says what did.

## 3. States and what to do

| State | Meaning | Action |
|---|---|---|
| COMPLETE | The data branch shows every catalog KPI for the day | None |
| SENT | The platform accepted every KPI per the artifacts; the data branch has not caught up | None. Confirm the next day, or on the compliance panel |
| RUNNING | A run is in progress | Check again when it ends |
| WAITING | No run yet today, and a scheduled one may still start | Check again after the time the script gives |
| AT RISK | No accepted report for some KPIs and nothing left that will send them | See below, before midnight |
| INCOMPLETE | A closed day on which some KPIs never arrived | Record it as an incident |
| LOST | A closed day on which nothing arrived | Record it as an incident |

**AT RISK, in order:**

1. Read why the last run failed with the `gh run view ... --log-failed` command the script prints (read-only). Typical causes are configuration: a missing repository secret, or the backend's KPI endpoint not configured on the server, which only someone with access to the server fixes.
2. If the cause is fixed or was transient, ask someone with write access to the app repository (a developer or a repository admin) to run the workflow by hand: Actions, `KPI Report`, Run workflow, command `report`, dry run off. The scheduled retry fails the same way when the cause is configuration, so do not just wait for it.
3. Run the watch again once that run ends, and check that the artifact shows every KPI accepted.

## 4. Record it

- **A closed day INCOMPLETE or LOST** is an incident: it goes into the Tablero's Incidentes block, with the KPIs that did not arrive, and into the week's control in `Seguimiento PM/`: which days, which KPIs, the cause, and who fixed it.
- **A day saved by a manual run** is worth one line in the week's control, with the cause, because the same cause can come back.
- A day that went well needs no note.

## 5. Things that look wrong and are not

- **Today shows 0 received in the evening.** The data branch lags; the artifacts decide.
- **Two successful runs in one day.** The retry is ignored by the platform when the first one arrived.
- **A complete day with a grade below 10.** The day is complete against the catalog registered then: if that catalog was smaller than the ADR promised, the day scores fewer KPIs. That is a catalog problem for the weekly control, not a delivery problem.

## Ejemplo de uso

**Pedido:** ¿Salieron hoy los KPIs?

**Resultado:** Corre `pm.py kpi-watch` y devuelve el estado del día (COMPLETE, SENT, RUNNING, WAITING, AT RISK) con la prueba del artifact de cada corrida; si está AT RISK, muestra cómo leer la causa del último fallo y quién tiene que correr el workflow a mano antes de la medianoche.
