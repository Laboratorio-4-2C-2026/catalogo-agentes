---
name: g04-pr-review-ticket-scope
description: Revisión técnica de Pull Requests de GitHub contra el alcance del ticket de Linear que implementan, publicando solo comentarios inline Must fix y Should fix en español. Usar cuando el Tech Lead pide revisar PRs del equipo, corregir o limpiar comentarios fuera de alcance, o definir el orden de merge.
metadata:
  tipo: skill
  area:
  - qa
  - gestion
  fase:
  - revision
  tecnologias:
  - agnostico
  - git
  metodologia:
  - scrum
  herramientas:
  - claude-code
  - codex
  requiere:
  - github
  - linear
  grupo: "04"
  autor:
    nombre: Alexander Köttner
    github: Alexander-Kottner
  colaboradores:
  - nombre: Martin Barreiro
    github: martinbarreiroo
  responsables:
  - Alexander-Kottner
  madurez: usado-en-proyecto
  relacionados:
  - g07-code-review-tl
---

# Revisión de PR contra el alcance del ticket

El objetivo es que el dev (o su agente) pueda tomar los comentarios y corregirlos rápido. Se revisa lo
que el ticket pide, no lo que al revisor le gustaría que tuviera.

## Entradas

- Una o varias URLs o números de PR, o "las PRs abiertas de X".
- Opcional: la clave del ticket. Si no está, sacarla de la rama, el título o el cuerpo del PR
  (`[A-Z][A-Z0-9]*-\d+`).

## Flujo

1. **Traer el ticket primero.** Leer en Linear título, descripción, criterios de aceptación y
   comentarios. Ese es el alcance. Si no se puede leer el ticket, frenar y avisar: sin alcance no hay
   revisión.
2. **Traer el PR.** `gh pr view <n> --json number,title,body,headRefName,baseRefName,author,url` y el
   diff contra su base real (`gh pr diff <n>`). Leer los archivos completos donde haga falta contexto,
   y las reglas del repo (AGENTS.md, CLAUDE.md, skills del repo como la de arquitectura del backend).
3. **Probar antes de opinar.** Hacer checkout de la rama en un worktree aparte y correr los checks del
   workspace afectado (build/typecheck, lint, tests). Si el ticket es de UI, levantar la app y recorrer
   el flujo. Un hallazgo que no se verificó no se publica.
4. **Clasificar cada hallazgo:**
   - **Must fix:** rompe un criterio de aceptación, el build, los tests, la seguridad o una regla
     obligatoria del repo.
   - **Should fix:** dentro del alcance, no bloquea, pero deja deuda clara (validación faltante, patrón
     distinto al del codebase, test que falta para un endpoint nuevo).
   - Todo lo demás (nits, gustos, decisiones de producto, mejoras fuera del ticket) **no va al PR**:
     va al resumen en el chat.
5. **Publicar** solo con autorización del usuario. Comentarios inline en la línea exacta, en español
   (voseo rioplatense), con la severidad en negrita al principio y el arreglo concreto, con el código en
   bloque cuando ayude. Una sola review por PR (`gh api` a `pulls/<n>/reviews` con `comments[]`).
6. **Si ya había comentarios propios:** editarlos en el lugar (sobrescribir el cuerpo) en vez de
   responder en el hilo. Borrar los que quedaron fuera del alcance del ticket o ya no aplican.
7. **Cerrar.** Si no quedan Must fix y el usuario lo pide, aprobar con un comentario corto en español.
   Si hay varios PRs, indicar el orden de merge según dependencias (base compartida, migraciones,
   archivos que se pisan) y si alguno necesita rebase después de otro.

## Salida en el chat

Por PR: ticket, veredicto (aprobable / cambios pedidos), Must fix y Should fix publicados con su
link, lo que quedó afuera y por qué, y el orden de merge si aplica.

## Reglas

- Nunca pedir cambios que el ticket no pide. Si algo falta en el ticket, se sugiere un ticket nuevo.
- No inventar estado del ticket ni resultados de checks que no corrieron.
- No aprobar, mergear ni borrar comentarios ajenos.

## Ejemplo de uso
**Pedido:** Revisá https://github.com/PitStop-Austral/pitstop-app/pull/9 contra PIT-29 y subí solo los must y should fix.

**Resultado:** Lee el ticket en Linear, corre los checks en la rama, publica una review con los comentarios Must fix y Should fix en español sobre las líneas afectadas y deja en el chat el veredicto y los puntos que quedaron fuera del alcance.
