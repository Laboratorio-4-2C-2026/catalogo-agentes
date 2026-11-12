---
name: g16-kpi-review
description: 'Checklist para revisar si un PR cambia lo que mide un KPI del reporte diario de Eureka: el catálogo inmutable, la tabla de dónde sale cada KPI (eventos on-chain, tablas y estados de Supabase, workflows) y los caminos nuevos que esquivan la fuente, con orden de prioridad y formato de reporte. Es el checklist que carga g16-eureka-revisor-kpi.'
metadata:
  tipo: skill
  area:
  - datos
  - qa
  fase:
  - revision
  tecnologias:
  - typescript
  - supabase
  - solidity
  herramientas:
  - claude-code
  requiere: []
  grupo: "16"
  autor:
    nombre: Esteban Antonijevic
    github: eantonijevic
  responsables:
  - eantonijevic
  madurez: experimental
  relacionados:
  - g16-eureka-revisor-kpi
  - g16-schema-review
  - g01-payoff-path-auditor
  - g05-watchparty-kpi-evidence
---

# Eureka KPI review

Every night `.github/workflows/kpi-report.yml` runs `scripts/kpi/report.ts`,
which computes Eureka's KPIs and sends them to the Laboratorio IV KPI platform.
The course grades the team on those numbers, and reads them in every steering.

**A KPI almost never breaks with an error.** It breaks by keeping on reporting
a number that no longer means what the catalog says. A renamed event topic
reports zero patents. A new status reports zero stuck reservations. Nobody
notices until a steering, and the history is already wrong. Weight every
finding against that.

Other reviewers own the rest. Contract security belongs to `authorship-review`,
secrets and RLS to `confidentiality-review`, credit accounting to
`credits-review`. You only care whether the KPIs still measure what they say.
If the diff cannot change any KPI, say so and stop.

## The catalog

The KPI ids are `KPI_IDS` in `scripts/kpi/utils.ts`. They are registered in
the platform catalog, and **catalog rows are immutable** except their
description, aggregation and deprecation date; there are at most 10 active
KPIs. So:

- Renaming, removing or adding an id in `KPI_IDS` is not a code change: it
  needs the catalog changed on the platform first, in dev and prod. Flag it
  `[Alto]` unless the PR says that was done.
- Changing what an existing id measures (unit, window, what is counted) without
  a new id breaks the series: days before and after the PR are not comparable.
  Flag it `[Alto]` and say which days stop being comparable.

## Where each KPI comes from

Before commenting, build this map for yourself from `scripts/kpi/report.ts`
and `app/api/kpi/route.ts`, even if they are not in the diff, and check it
against the diff:

| KPI | Source | What it silently depends on |
|---|---|---|
| `patentes_registradas` | `PatentRegistered` logs on the registry proxy, day in ART | The event signature (its topic comes from `lib/abi/eurekaPatentRegistry.ts`), the proxy address, every registration path emitting it exactly once |
| `patentes_compartidas` | `ViewerAdded` logs on the registry proxy | Every way of sharing a patent emitting it on-chain |
| `gas_consumido` | Sum of `gasUsed` of every tx that left a log on the registry | Which transactions touch the registry |
| `usuarios_con_wallet` | `count(*)` of `users` | `users.wallet_address` being `not null`: the count is only "with wallet" because of that constraint |
| `reservas_colgadas` | `patent_mint_reservations` in `reserved` older than 1 h, plus `minting` past `mint_expires_at` | The set of active statuses and the meaning of `mint_expires_at` |
| `saldo_turbo` | `getBackendBalance()` in `lib/server/turboService.ts` | Its unit (winc) |
| `latencia_p95`, `api_alcanzable` | 20 GETs to the root of `EUREKA_URL` | The root answering 2xx without a session |
| `ultima_ejecucion_antiguedad` | Last successful run of `deploy.yml` on `master` | The workflow file name and the branch |

## What to look for

Review in this order:

1. **Sources that change shape.** An event renamed or with different
   parameters, the ABI regenerated, a new registry address, a column, table or
   status renamed, the deploy workflow renamed or moved off `master`. Say which
   KPI goes wrong and what value it will report (usually zero or missing).
2. **New paths that bypass the source.** A new way to register or share that
   does not emit the event (for example, a share that stays off-chain until the
   recipient signs up), a migration path that emits a different event, a user
   row inserted before the wallet exists. The KPI keeps working and undercounts
   or overcounts.
3. **New states the query does not know.** A new reservation status that is
   active but is not `reserved` or `minting`: those reservations can hang and
   `reservas_colgadas` stays at zero.
4. **Changes to the reporter itself.** Day boundaries (`KPI_TIME_ZONE`,
   `dayBoundsInSeconds`), block range search, retries that can double count,
   a KPI that falls back to a default instead of being reported as missing.
   A missing KPI is visible; a wrong default is not.
5. **The route's contract.** `GET /api/kpi` must keep returning finite numbers
   under the same keys and keep its bearer check; `report.ts` rejects anything
   else and the whole internal block goes missing.

## How to report

- One comment per finding, anchored to the line that changes the source.
- Open each with a severity tag: `[Crítico]`, `[Alto]`, `[Medio]`, `[Bajo]`.
  A KPI that will report a wrong number from the next run is `[Alto]`; one
  that will go missing (visible in the platform) is `[Medio]`.
- Name the KPI, what it will report after the merge, and since when.
- Propose a specific fix: update the query, emit the event, register a new id.
- If a finding is a suspicion rather than a confirmed issue, say so explicitly.
- Do not comment on formatting, naming or style.
- If the diff cannot change any KPI, say so in a single comment.

## Ejemplo de uso

**Pedido:** «Revisá este diff con la skill de KPIs: renombra el evento `ViewerAdded` del registro.»

**Resultado:** Arma la tabla de fuentes de cada KPI, marca con `[Alto]` que `patentes_compartidas` va a reportar cero desde la próxima corrida porque su topic sale de ese evento, y propone actualizar el ABI y el reporter en el mismo PR.
