---
name: g10-empty-loading-error-states-checker
description: Auditar si cada página del frontend maneja explícitamente sus estados de carga, vacío y error, en vez de dejarlos en blanco. Usar al terminar una página nueva en `frontend/src/pages` o antes de revisar su PR.
metadata:
  tipo: skill
  area:
  - frontend
  fase:
  - revision
  tecnologias:
  - react
  - typescript
  metodologia:
  - agnostico
  herramientas:
  - claude-code
  requiere: []
  grupo: "10"
  autor:
    nombre: Victoria Martin Botter
    github: vmartinbotter
  responsables:
  - vmartinbotter
  madurez: experimental
  relacionados:
  - g10-a11y-component-reviewer
  - g01-screen-state-ux-reviewer
  - g08-frontend-state-flow-auditor
---
# Empty / Loading / Error States Checker

Revisar cada página de `frontend/src/pages` (home, trips, tripDetails, matches, matchDetail, schedule, profile, addSubject, questionnaire) y confirmar que maneja de forma explícita los tres estados que toda vista que pide datos puede tener: cargando, vacía y con error.

## Qué revisar

1. Identificar de dónde vienen los datos de la página (hook propio, `context/`, o llamada directa). Ver qué estados expone esa fuente (`isLoading`, `error`, longitud de los datos).
2. Para el estado de **carga**: confirmar que se muestra `ConexiaLoader` o un indicador equivalente, no una pantalla en blanco ni un salto brusco de layout.
3. Para el estado **vacío**: páginas de listas (trips, matches, schedule) deberían usar o tener un equivalente a `emptytripsstate` cuando no hay datos, en vez de mostrar una lista vacía sin explicación.
4. Para el estado de **error**: confirmar que un fallo de red o de la API no deja la página colgada o sin feedback, y que existe alguna forma de reintentar (botón, recarga) salvo que el flujo no lo permita.
5. Señalar específicamente páginas que muestren los tres estados mezclados (ej. renderizar la lista vacía como si fuera "cargando" para siempre).

## Salida esperada

Tabla: `página` | `carga` | `vacío` | `error` | `observación`, marcando cada columna como ✅ manejado, ⚠️ parcial o ❌ falta. No modificar código: solo reportar, salvo pedido explícito.

## Ejemplo de uso

**Pedido:** Revisá si la página de matches maneja bien el estado de carga, sin resultados y de error de red.
**Resultado:** Tabla indicando qué estados están bien manejados en la página de matches y cuáles faltan, con la observación concreta de cada caso.
