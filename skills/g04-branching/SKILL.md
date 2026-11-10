---
name: g04-branching
description: 'Define y aplica la estrategia de ramas de un equipo con tickets de Linear y PRs: nombres, base, rama por ticket, trabajo encadenado, conflictos y orden de merge. Usar al crear ramas, resolver conflictos, coordinar PRs dependientes o limpiar ramas viejas.'
metadata:
  tipo: skill
  area:
  - devops
  - gestion
  fase:
  - desarrollo
  - revision
  tecnologias:
  - git
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  grupo: "04"
  autor:
    nombre: Martin Barreiro
    github: martinbarreiroo
  responsables:
  - martinbarreiroo
  madurez: experimental
  relacionados: []
---

# Branching

Evita pisarse y mantiene `main` siempre sana. Las reglas del repo (AGENTS.md, Definition of Done) mandan sobre estas.

## Modelo

- `main` está protegida y siempre debe poder desplegarse. No se trabaja ni se pushea directo.
- **Una rama por ticket, un PR por rama.** Si crece, se parte en verticales, no en capas.
- Nombre con la clave del ticket: `feat/PIT-31-cliente-axios` o `fix/PIT-40-...`, según la convención del repo.

## Flujo

1. **Crear:** `git fetch origin`, inspeccionar cambios locales y crear desde `origin/main` actualizada. Si hay trabajo sin commitear ajeno a la tarea, no mezclarlo: usar un worktree.
2. **Trabajo encadenado:** si el ticket depende de un PR abierto, elegir:
   - Esperar el merge, si el resto puede avanzar. Es la opción por defecto.
   - Basarse en esa rama y abrir el PR contra ella. Al mergearse la otra, actualizar y cambiar la base con `gh pr edit --base main`.
3. **Actualizar:** traer `main` con frecuencia, siguiendo la política del repo (merge o rebase). No reescribir historia de una rama que otra persona usa.
4. **Conflictos:** leer los dos lados y el motivo de cada cambio. Conservar ambas intenciones y correr los checks después. Con migraciones de Prisma, cuidar el orden y no editar las que ya se aplicaron.
5. **Orden de merge entre varios PRs:** primero los que otros necesitan, después migraciones en orden y al final los que tocan los mismos archivos, con un rebase entre medio.
6. **Limpiar:** borrar ramas mergeadas.

## Reglas

- No usar `--force`: si hace falta tras un rebase, usar `--force-with-lease` y solo en ramas propias.
- No usar `reset --hard` ni borrar ramas sin confirmar que no hay trabajo sin subir.
- Sin aprobación y checks en verde no se mergea.

## Ejemplo de uso
**Pedido:** Mi ticket depende de la PR de Juan, ¿de dónde saco la rama?

**Resultado:** Revisa el estado de la PR, recomienda basarse en su rama o esperar el merge, da los comandos exactos y explica qué hacer cuando la otra PR se mergee.
