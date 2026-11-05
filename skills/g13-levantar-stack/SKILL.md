---
name: g13-levantar-stack
description: Levanta el stack local completo de MicroChangas (Supabase local + backend NestJS + frontend Vite) en la branch en la que esté parado el dev, con la branch actualizada, migraciones al día, usuarios demo y seed. Usalo cuando el dev pida "levantá el stack", "quiero probar mi branch localmente", "levantá el proyecto en local" o similar, o invoque el skill por nombre (levantar-stack), en microchangas-backend o microchangas-frontend.
metadata:
  tipo: skill
  area:
  - devops
  - backend
  - frontend
  fase:
  - desarrollo
  - testing
  tecnologias:
  - nestjs
  - react
  - supabase
  - prisma
  - docker
  - typescript
  metodologia:
  - agnostico
  herramientas:
  - claude-code
  - codex
  - otra
  requiere:
  - github
  grupo: "13"
  autor:
    nombre: Pablo Pagliaricci
    github: Pagliaricci
  responsables:
  - Pagliaricci
  madurez: usado-en-proyecto
  relacionados:
  - g13-validar-branch
  - g11-ver-pr-en-vivo
  - g08-firebase-emulator-seeder
---

# Levantar el stack local en la branch actual

Objetivo: que el dev pruebe **su branch** (armada desde `dev`) de punta a punta
antes de abrir la PR a `dev`. Seguí los pasos en orden y, al final, dale un
resumen corto.

Los scripts de este skill están en `scripts/`, junto a este archivo.
`<dir del skill>` es la carpeta de este `SKILL.md`; usá su ruta absoluta. Los
scripts se corren siempre **desde la raíz de `microchangas-backend`**:
`node <dir del skill>/scripts/<script>.mjs`.

## Reglas

- **No cambies de branch**, ni hagas `stash`, `reset`, `commit` ni `push`. El
  stack se levanta donde el dev está parado.
- **Todo es local.** Nunca corras comandos de Supabase sin `--local` contra
  un proyecto linkeado. Si un `.env.local` apunta a un Supabase hospedado,
  pará y avisá.
- **Pedí confirmación** antes de cualquier cosa que borre datos (`db reset`) o
  que cambie la historia de la branch (`merge` de `dev`).
- No muestres secretos (claves, contraseñas, tokens). Nombrá la variable y el
  archivo donde está.
- Los comandos son multiplataforma: usá `pnpm`, `node` y `git`. Varios devs
  usan Windows, así que no dependas de bash, `curl` ni `sed`.
- **Permisos:** varios pasos necesitan red, Docker o escribir fuera del repo
  (`git fetch`, `pnpm install`, `supabase start`, `node` con la base local). Si
  tu herramienta corre en un sandbox, pedile al dev que apruebe esos comandos.
  Si no se pueden aprobar, dale el comando exacto para que lo corra él en su
  terminal, y seguí cuando te confirme.

## 1. Ubicar los repos

El dev puede estar en el front o en el back. Buscá el otro repo como carpeta
hermana (`../microchangas-backend`, `../microchangas-frontend`). Si no
aparece, preguntale la ruta. Si no tiene clonado el front, seguí solo con el
back y avisalo.

## 2. Prerrequisitos

- `node -v` ≥ 20 y `pnpm -v`.
- Docker corriendo (`docker info`). Si no, pedile que abra Docker Desktop y
  esperá.

## 3. Branch actualizada (en cada repo)

1. Mostrá la branch actual y si hay cambios sin commitear (`git status -sb`).
2. `git fetch origin`.
3. Si la branch tiene upstream y está atrás, `git pull --ff-only`. Si falla
   porque divergió, o porque los cambios locales chocan, no lo fuerces:
   explicale qué pasa y seguí con lo que hay.
4. Contá cuánto está atrás de dev: `git rev-list --count HEAD..origin/dev`.
   Si es > 0, avisale y **preguntale** si quiere traer dev
   (`git merge origin/dev`). Explicale que conviene, porque la PR va contra
   dev y así prueba lo que se va a mergear. Si hay conflictos, se los deja a
   él. No pushees.
5. Si está parado en `main`, avisale que el equipo trabaja con branches
   desde `dev`.

## 4. Dependencias

En cada repo, `pnpm install --frozen-lockfile`. Si falla porque el lockfile no
coincide con `package.json`, corré `pnpm install` y avisale que
`pnpm-lock.yaml` cambió y que lo tiene que commitear junto con su cambio.

En el back, el `postinstall` regenera el cliente de Prisma, así que queda
alineado con el `schema.prisma` de la branch.

## 5. Supabase local

En el back, `pnpm exec supabase status`. Si no está arriba,
`pnpm supabase:start`. La primera vez descarga imágenes y tarda varios minutos:
avisale.

Si falla por un puerto ocupado, probablemente tiene otro proyecto de Supabase
corriendo. Mostrale cuál (`docker ps`) y proponé
`pnpm exec supabase stop --project-id <otro>`.

## 6. Variables de entorno

```
node <dir del skill>/scripts/env-local.mjs --frontend ../microchangas-frontend
```

Crea o completa los `.env.local` de los dos repos contra el Supabase local.
Usa placeholders y bypass para Didit si no hay credenciales reales. No pisa lo
que el dev ya cargó. Si sale con error porque algo apunta a un Supabase remoto,
pará y mostrale el mensaje.

## 7. Migraciones

```
node <dir del skill>/scripts/migraciones.mjs
```

- **`soloEnLaBase` no vacío:** la base tiene migraciones que esta branch no
  tiene, porque vienen de otra branch o se renombraron. La base no refleja la
  branch. Explicáselo y **preguntale** si resetear:
  `pnpm exec supabase db reset --local`. Esto borra todos los datos locales,
  incluidos los usuarios, pero los pasos 8 y 9 los recrean. Si dice que no,
  seguí y dejá la advertencia en el resumen.
- **`pendientes` no vacío (y sin reset):** `pnpm exec supabase migration up --local`.
  Si se queja de migraciones "before the last migration", que se mergearon
  con un número menor, repetí con `--include-all`.
- **Migración editada:** si
  `git diff --name-status origin/dev...HEAD -- supabase/migrations` muestra
  una migración **modificada** (`M`) que ya estaba aplicada, el cambio no se
  aplica solo. Proponé el reset, igual que arriba.
- **Recordatorio para la PR:** si la branch agrega o cambia migraciones y
  `prisma/schema.prisma` no cambió respecto de `origin/dev`, recordale correr
  `pnpm db:pull` y commitear el schema. Es el flujo del README.

## 8. Usuarios demo

```
node <dir del skill>/scripts/usuarios-demo.mjs
```

Crea o resincroniza `Demo Worker`, `Demo Worker 2` (worker), `Demo Client` y
`Demo Client 2` (client), con el email confirmado. La contraseña queda en
`.env.local` del back como `DEMO_USERS_PASSWORD`.

## 9. Seed

En el back, `pnpm db:seed`. No borra nada y se puede correr muchas veces. Deja
changas, postulaciones, asignaciones y calificaciones para que el dashboard de
`Demo Worker` tenga datos.

## 10. Levantar back y front

- Revisá que 3000 y 5173 estén libres. Si están ocupados por una corrida
  anterior del stack, preguntale si la cortás o la reusás. Si es otra cosa,
  avisale.
- Back: `pnpm start:dev`. Front: `pnpm dev`, en el repo del front. Los dos son
  procesos que no terminan.
  - Si tu herramienta puede dejar procesos corriendo en segundo plano,
    levantalos así y esperá a que el log del back diga
    `Nest application successfully started`.
  - Si no puede, porque corta los comandos que no terminan o porque el sandbox
    no los deja vivos, **no los corras vos**. Pedile al dev que abra dos
    terminales y corra uno en cada una:
    `cd <ruta>/microchangas-backend && pnpm start:dev` y
    `cd <ruta>/microchangas-frontend && pnpm dev`. Esperá a que te confirme y
    seguí con la verificación.

## 11. Verificar

```
node <dir del skill>/scripts/usuarios-demo.mjs --verificar
```

Hace el health check, el login con `demo.worker@microchangas.test` y llama a
`/auth/me`. Si algo falla, leé el log del back y diagnosticá antes de
reportar. Comprobá también que http://localhost:5173 responda.

## 12. Resumen para el dev

Corto, en este orden:

- Branch de cada repo, el último commit, y si quedó atrás de `origin/dev`.
- Migraciones aplicadas, o si hubo reset. Cualquier advertencia del paso 7.
- Usuarios demo: los emails, los roles y dónde está la contraseña. No la
  muestres.
- URLs: front http://localhost:5173 · API http://localhost:3000 ·
  Swagger http://localhost:3000/api-docs · Supabase Studio
  http://127.0.0.1:54323 · mails de prueba en `MAILPIT_URL` de
  `pnpm exec supabase status`.
- Cerrá con lo que tiene que hacer antes de la PR a `dev`, si quedó algo:
  lockfile, `db:pull`, merge de dev.

## Ejemplo de uso

**Pedido:** Levantá el stack en mi branch, quiero probarla antes de abrir la PR.

**Resultado:** Actualiza la branch (sin cambiarla ni commitear), avisa si quedó atrás de dev, aplica las migraciones pendientes en el Supabase local, crea los usuarios demo, corre el seed y verifica con un login real; cierra con las URLs del front, la API y Supabase Studio y lo que falte antes de la PR.
