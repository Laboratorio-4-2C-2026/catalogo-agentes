---
name: g16-schema-review
description: 'Checklist para revisar cambios a un schema.sql de Supabase que se aplica pegándolo entero en el SQL editor: cambios que en producción no hacen nada, sentencias que fallan la segunda vez, datos existentes que violan una constraint nueva, overloads de funciones que quedan vivos y compatibilidad con el código desplegado. Es el checklist que carga g16-eureka-revisor-esquema.'
metadata:
  tipo: skill
  area:
  - datos
  - backend
  fase:
  - revision
  tecnologias:
  - supabase
  - postgresql
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
  - g16-eureka-revisor-esquema
  - g16-confidentiality-review
  - g11-revisar-migracion
  - g05-watchparty-supabase-migration-review
---

# Eureka schema review

Eureka has no migrations. `supabase/schema.sql` is "the consolidated, idempotent
final state" of the database, and a person applies it by **pasting the whole
file into the Supabase SQL editor**, against a production database that already
has data. The same file also has to build a fresh database from zero.

So every change to the file has to work three ways:

1. On an empty database.
2. On production as it is today, which ran every previous version of the file.
3. Run a second time on top of itself.

**A broken schema change rarely fails loudly.** The usual failure is a
statement that "succeeds" and does nothing: `create table if not exists` on a
table that already exists ignores the new column, and the code that needs it
fails in production while the PR looked green. Weight every finding against
that.

Other reviewers own the rest. RLS policies, `search_path` on `SECURITY DEFINER`
functions and grants to `anon`/`authenticated` belong to
`confidentiality-review`. The reservation state machine and anything that moves
`users.credits` belong to `credits-review`. You only care whether the script
applies, re-applies and leaves production in the state the code expects. If the
diff does not touch the schema, say so and stop.

## What to look for

Review the diff of `schema.sql` against the previous version of the file
(`git show HEAD~1:supabase/schema.sql` or the PR base), in this order:

### 1. Changes that do nothing on production

- A column added inside an existing `create table if not exists (...)`. On
  production the table exists, so the column never gets created. It needs an
  `alter table … add column if not exists` after the `create table`. This is
  the most likely finding: flag it `[Alto]`.
- A changed default, `not null`, `check` or `unique` inside an existing
  `create table`. Same problem: it only applies to new databases.
- A changed index definition with the same name and `create index if not
  exists`. The old index stays. It needs `drop index if exists` first (the
  file already does this for `patent_mint_reservations_one_active_per_document`).

### 2. Statements that fail on a second run

The whole file is pasted at once; one failure aborts the rest and leaves
production half applied. Every statement must be re-runnable:

- `create policy`, `create trigger`, `add constraint` need a matching
  `drop … if exists` before them.
- `create table`, `create index`, `add column` need `if not exists`.
- `create or replace function` cannot change the return type or parameter
  names of an existing function: it needs a `drop function if exists` with the
  old signature first.
- `insert` of seed data needs `on conflict do nothing` (or equivalent).

### 3. Changes that fail on today's data

- `not null` on a column that has nulls in production, or a new `check` or
  `unique` that existing rows violate. Ask what the data looks like and whether
  a backfill (`update …`) must run before the constraint.
- A type change that cannot cast existing values.

### 4. Function signatures that leave an old overload behind

Changing the parameters of a function with `create or replace` does not
replace it: it creates a second function with the same name, and the old one
stays on production with its old behavior and its old grants. The file must
`drop function if exists name(old types)` (as it does for `fail_patent_mint`),
and the `revoke` must name the new signature. Flag an orphaned overload
`[Alto]`: the code may keep calling the old one.

### 5. Order and compatibility with the deployed code

- A function, policy or index that references a column, table or type defined
  later in the file fails on an empty database.
- The schema is applied by hand, so for some time production runs the new
  schema with the old code, or the old schema with the new code. Dropping or
  renaming a column, table, status or function that the code on `master` still
  uses breaks production in that window. Check with Grep across `app/`, `lib/`
  and `scripts/` for every name the diff removes or renames. Prefer expand
  first (add the new thing), migrate the code, contract later (remove the old).
- A new value in a `check` on `status` that the code does not handle yet, or a
  status the code writes that the `check` does not allow.

### 6. Instructions for the person who applies it

If the change needs anything beyond pasting the file — a backfill, a specific
order relative to the Vercel deploy, a one-off statement — the PR body must
say so. If it does not, ask for it.

## How to report

- One comment per finding, anchored to the specific line of `schema.sql`.
- Open each with a severity tag: `[Crítico]`, `[Alto]`, `[Medio]`, `[Bajo]`.
  A change that leaves production different from what the code expects, or
  aborts the script halfway, is `[Alto]`; one that destroys data is
  `[Crítico]`.
- Say which of the three runs breaks (empty database, production today, second
  run) and what production looks like afterwards.
- Propose the specific statement that fixes it.
- If a finding depends on data you cannot see, say so explicitly and say what
  query would settle it.
- Do not comment on formatting, naming or style.

## Ejemplo de uso

**Pedido:** «Revisá este diff de `supabase/schema.sql` con la skill de esquema.»

**Resultado:** Hallazgos con `[Crítico]`, `[Alto]`, `[Medio]` o `[Bajo]` que dicen cuál de las tres corridas rompe (base vacía, producción hoy, segunda corrida), cómo queda producción y la sentencia que lo arregla. Si depende de datos que no ve, dice qué query lo resuelve.
