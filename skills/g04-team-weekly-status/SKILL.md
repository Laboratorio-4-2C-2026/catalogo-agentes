---
name: g04-team-weekly-status
description: 'Reporte simple del avance del equipo y del estado del producto cruzando Linear con los PRs de GitHub: qué tickets se tocaron en la semana, quién trabajó en qué y qué funcionalidades ya están integradas en main. Usar cuando el PO o el Tech Lead pregunta en qué trabajó el equipo, cómo va el sprint o en qué estado está la app.'
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - revision
  - planificacion
  tecnologias:
  - agnostico
  - git
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - linear
  - github
  grupo: "04"
  autor:
    nombre: Manuel Lostaló
    github: ManuLosta
  colaboradores:
  - nombre: Martin Barreiro
    github: martinbarreiroo
  responsables:
  - ManuLosta
  madurez: experimental
  relacionados:
  - g11-weekly-status
---

# Estado semanal del equipo

Responde "¿qué hicieron los chicos esta semana?" o "¿en qué estado está la app?" con datos, no con
memoria, y en lenguaje de producto.

## Entradas

- Período: por defecto la semana del equipo en curso (si el plan define otro inicio de semana, usar
  ese, por ejemplo de jueves a jueves).
- Alcance: semana (qué se tocó) o producto (qué está integrado).

## Flujo

1. **Linear:** listar los issues del team actualizados en el período, con estado, asignado, project y
   estimación. Para el estado del producto, listar los projects/épicas y cuántos tickets tiene cada uno
   en Done, In Progress y Backlog.
2. **GitHub:** `gh pr list --state all --search "updated:>=<fecha>"` con autor, estado, rama y fecha de
   merge. Asociar cada PR a su ticket por la clave en la rama o el título.
3. **Cruzar:** un ticket cuenta como integrado solo si su PR está mergeado en la rama principal.
   Marcar las diferencias: ticket en Done sin PR mergeado, PR mergeado con el ticket abierto, PR abierto
   hace muchos días.
4. **Redactar** en lenguaje de producto (qué puede hacer el usuario), no en lenguaje de código.

## Salida

- **Semana:** por persona, los tickets tocados con su estado y PR.
- **Producto:** funcionalidades integradas, en curso y pendientes, agrupadas por épica.
- **Desvíos:** las diferencias del paso 3, para que el PO decida si sincronizar.

Corto y simple: una línea por ticket, sin detalles técnicos salvo que se pidan.

## Reglas

- Solo lectura: no cambiar tickets ni PRs.
- No adivinar quién hizo algo: usar el asignado del ticket y el autor del PR.

## Ejemplo de uso
**Pedido:** ¿En qué trabajaron los chicos esta semana a nivel producto? Bien simple.

**Resultado:** Una lista por integrante con los tickets que tocó, su estado y su PR, un resumen de lo que ya quedó integrado en main y los tickets cuyo estado en Linear no coincide con GitHub.
