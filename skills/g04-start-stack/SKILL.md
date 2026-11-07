---
name: g04-start-stack
description: Levanta y verifica todo el stack de desarrollo local del repositorio, usando primero la receta guardada en STACK_STARTUP.md y descubriendo el stack solo si no existe o falla. Se ejecuta a mano con /g04-start-stack; no se activa sola.
disable-model-invocation: true
effort: low
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/fast_path.py *)
metadata:
  tipo: skill
  area:
  - devops
  fase:
  - desarrollo
  - testing
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  - codex
  requiere: []
  grupo: "04"
  autor:
    nombre: Martin Barreiro
    github: martinbarreiroo
  colaboradores:
  - nombre: Alexander Köttner
    github: Alexander-Kottner
  responsables:
  - martinbarreiroo
  madurez: usado-en-proyecto
  relacionados: []
---

# Start Stack

## Cached fast path

The bundled script executes a v2 `STACK_STARTUP.md` recipe deterministically: it reuses healthy services, starts only missing ones, verifies them, and prints one terse status line.

Result:
!`${CLAUDE_SKILL_DIR}/scripts/fast_path.py "${CLAUDE_PROJECT_DIR}"`

Interpret the result exactly:

- `FAST_PATH_OK ...` → task succeeded. **Stop immediately.** Do not read `STACK_STARTUP.md`, inspect the repository, read logs, or call tools. Reply in one short sentence with the reported URL(s) and whether services were started/reused.
- `FAST_PATH_MISS reason=no_manifest` → read [references/discovery.md](references/discovery.md), then discover/start/verify and write a v2 manifest.
- `FAST_PATH_MISS reason=legacy_manifest` → read [references/discovery.md](references/discovery.md). Prefer the existing human recipe before broad discovery; after successful verification, upgrade it to v2.
- `FAST_PATH_FAIL ...` → read [references/recovery.md](references/recovery.md). Inspect only the named failed service/log first. Rediscover broadly only if evidence shows the cached recipe is structurally stale.
- If shell injection is disabled and the result above is a placeholder rather than a status, run `${CLAUDE_SKILL_DIR}/scripts/fast_path.py "${CLAUDE_PROJECT_DIR}"` once with Bash and apply the same rules.

Never perform destructive recovery (database/schema resets, volume deletion, unrelated process kills, `sudo`, broad upgrades, or overwriting secrets/env files) without explicit user authorization.

## Ejemplo de uso
**Pedido:** Levantá el stack.

**Resultado:** Reutiliza los servicios sanos, inicia los que faltan, los verifica y responde en una línea con las URLs y qué se inició.
