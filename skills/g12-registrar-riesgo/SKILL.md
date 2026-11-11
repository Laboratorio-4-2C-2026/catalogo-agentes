---
name: g12-registrar-riesgo
description: Suma un riesgo nuevo como fila del risk log del sprint, con probabilidad, impacto, respuesta y contingencia, sin duplicar uno abierto ni contradecir lo ya decidido. Usar cuando aparece algo que todavía no pasó pero puede afectar el plan, o para actualizar o cerrar un riesgo existente.
owner: '@n-mangini'
role: pm
created: '2026-11-09'
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - linear
  grupo: '12'
  autor:
    nombre: Nicolas Mangini
    github: n-mangini
  responsables:
  - n-mangini
  madurez: usado-en-proyecto
  relacionados:
  - g12-reportar-incidente
  - g12-reportar-semaforo
---

# Registrar riesgo

Un riesgo es algo que **todavía no pasó** y puede afectar el plan. Si ya pasó, es un
incidente y va con `reportar-incidente`. Esta skill convierte el relato del PM en una fila
del risk log, lista para pegar.

Ejemplo: `/registrar-riesgo si se atrasa la pantalla de acceso, se corre la integración`.

## 1. Ubicar el risk log y lo vigente

Buscar el risk log del sprint en curso (en SplitIt, `04-iteration/sprints/sprint-N/risk-log.md`
del repo de dirección de proyecto). Leer también:

- las filas existentes, para no duplicar un riesgo abierto: si ya está, se actualiza esa fila;
- el decision log y las prioridades de Linear: la respuesta tiene que aplicar lo decidido,
  no reabrirlo. Si el riesgo contradice una decisión, decirlo al PM en lugar de registrarlo.

Listo cuando se sabe si es fila nueva, actualización o cierre.

## 2. Armar la fila

Usar las columnas y escalas que ya tiene el archivo. En SplitIt:

| Columna | Cómo se llena |
|---|---|
| ID | `RSK.NN`, el siguiente libre. Nunca reusar uno cerrado. |
| F. Alta | Hoy, `DD/MM/AAAA`. |
| Descripción | Condicional: "Si pasa X, entonces Y". Nombra a quién o qué afecta. |
| Estado | Abierto · Cerrado. |
| Probabilidad / Impacto | `1 - Baja/Bajo` · `2 - Media/Medio` · `3 - Alta/Alto`. |
| Exposición | Probabilidad × Impacto con su color: 🟥 9 · 🟧 6 · 🟨 3-4 · 🟩 1-2. |
| Ranking | Reordenar los abiertos por exposición. |
| Respuesta | Mitigar · Aceptar · Evitar · Transferir. |
| Acción de respuesta | Lo que se hace **ahora**, con responsable y fecha. |
| Plan de acción / Contingencia | Qué se hace **si pasa**, con la fecha en que se mira. |

La acción y la contingencia llevan fechas concretas y personas con nombre. "Hacer seguimiento"
no es una acción.

Al cerrar un riesgo, el estado pasa a Cerrado y la contingencia termina con
"Cerrado el DD/MM: <qué pasó>".

## 3. Devolver

Mostrar la fila y, si cambió el ranking, la tabla de abiertos reordenada. Escribir en el
archivo solo si el PM lo pide. Cada riesgo nuevo es una fila: no se arman secciones aparte.

Si falta probabilidad, impacto o responsable, dejar `Por confirmar` y preguntarlo. No
inventarlos.

## Ejemplo de uso

**Pedido:** /registrar-riesgo si se atrasa la pantalla de acceso, se corre la integración

**Resultado:** Devuelve la fila nueva del risk log con ID, probabilidad, impacto, exposición, respuesta y contingencia con fechas y responsables, y la tabla de abiertos reordenada si cambió el ranking.
