---
name: g12-cerrar-semana
description: Cierra la semana en el seguimiento del sprint con PV, EV y AC acumulados, y escribe el resumen en la celda Notas con SPI, CPI, qué se entregó, qué faltó y las horas de cada dev. Usar el día de corte semanal, o cuando el PM pide completar la fila de una semana.
owner: '@n-mangini'
role: pm
created: '2026-11-09'
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - linear
  - github
  grupo: '12'
  autor:
    nombre: Nicolas Mangini
    github: n-mangini
  responsables:
  - n-mangini
  madurez: usado-en-proyecto
  relacionados:
  - g12-calcular-valor-ganado
  - g12-reportar-semaforo
  - g12-asignar-capacidad-sobrante
---

# Cerrar semana

Completa la fila de la semana que cerró en el registro semanal del seguimiento. El resumen
va **dentro de la celda Notas**: no se arma una sección aparte.

## 1. Juntar los datos

Leer las reglas del propio seguimiento antes de calcular: ahí está qué cuenta como valor,
cuándo se gana y a qué semana va cada hora. En SplitIt (`sprints/sprint-N/seguimiento.md`):

- **PV:** el de la tabla "PV por semana". El plan es fijo: un ticket atrasado o reasignado
  deja su valor en la semana original.
- **EV:** un ticket suma todo su valor cuando se mergea, y nada antes. Merge hasta el lunes
  23:59 (hora Argentina) cuenta para la semana.
- **AC:** las horas de la línea `actual:` de cada PR con la etiqueta del sprint, en la
  semana en que **se abrió** la PR. Incluye lo que está fuera del presupuesto.
- **Planeado por dev:** la estimación en Linear de sus tickets con la etiqueta de la semana.

Sacar merges y horas de las PR (`gh pr list --state merged --label "sprint 3" --json ...`) y
el estado de los tickets de Linear. Actualizar la columna Merge y Horas reales de la tabla de
valor por ticket, y anotar debajo cualquier caso raro (ticket partido, reasignado, adelantado).

Listo cuando cada ticket de la semana tiene merge o motivo de por qué no, y cada PR abierta
en la semana tiene sus horas asignadas.

## 2. Escribir la nota

Una celda, en este orden:

1. `SPI x,xx · CPI x,xx.`
2. Una oración con el resultado de la semana.
3. Cada dev: horas reales contra planeadas, qué entregó, qué adelantó y qué bugs tomó.
4. Qué faltó, con su valor en horas y cuándo se espera.

Tono: "llevó más/menos de lo previsto", nunca "sobreestimó/subestimó". Un CPI alto con
capacidad sin usar se explica como tal, no como eficiencia. Los números van con coma decimal.

Ejemplo: "SPI 0,92 · CPI 1,04. Se entregó casi todo lo planeado y un dev adelantó
trabajo de la semana siguiente. Dev 1: 8 h contra 5: …".

## 3. Devolver

Mostrar la fila completa y los cambios en la tabla de tickets. Si falta un dato (horas sin
informar en una PR, ticket sin estado claro), dejarlo marcado y preguntar: la semana no
se cierra con números supuestos.

## Ejemplo de uso

**Pedido:** Cerrá la semana 10 del sprint 3 en el seguimiento.

**Resultado:** Actualiza merges y horas reales por ticket desde las PR y Linear, y escribe en la celda Notas el SPI, el CPI y una línea por dev; si falta un dato, lo marca y pregunta en vez de suponerlo.
