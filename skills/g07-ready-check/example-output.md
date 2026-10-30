# Ejemplo de output — Ready Check

> Generado sobre un board real; los nombres de las personas son ficticios.

✅ **Ready check — StudyArena — 30/10**

Revisé los tickets To Do de las entregas del 05/11 y del 12/11, más sus bloqueantes, y (a pedido) el backlog sin comprometer.

## Resumen
0 🟢 · 1 🟡 · 1 🔴 en lo comprometido. Lo urgente: **STUDY-79 no tiene dueño ni fecha y frena dos tickets que vencen el 05/11.** Para el 12/11 todavía no hay nada asignado: el planning de esa entrega está pendiente.

## ⛓️ Cadenas de bloqueo que ponen en riesgo una entrega
- [STUDY-106](https://tuequipo.atlassian.net/browse/STUDY-106) (To Do, vence 05/11) ← [STUDY-105](https://tuequipo.atlassian.net/browse/STUDY-105) (In Progress, vence 05/11) ← [STUDY-79](https://tuequipo.atlassian.net/browse/STUDY-79) (To Do, sin dueño, sin fecha).
  **Acción:** asignar STUDY-79 hoy y ponerle una fecha anterior al 05/11, o sacar a STUDY-105 la parte que depende de él. Además, STUDY-106 vence el mismo día que su bloqueante: no queda margen para integrar.

## 🔴 No ready

**[STUDY-106](https://tuequipo.atlassian.net/browse/STUDY-106) — Generación de preguntas con IA en el modal de cuestionario** (Julia, vence 05/11)
- ❌ **Dependencias a tiempo**: bloqueado por STUDY-105, que vence el mismo día (cero margen para integrar) y depende a su vez de STUDY-79, sin dueño (ver cadena).
- ✅ User story, alcance y fuera de alcance, contrato consumido y 20 escenarios en Gherkin.
- **Corrección:** el ticket está bien escrito; el problema es de planificación. Destrabar STUDY-79 esta semana o mover STUDY-106 a la entrega del 12/11.

## 🟡 Casi

**[STUDY-79](https://tuequipo.atlassian.net/browse/STUDY-79) — Generación de tarjetas con IA a partir de un archivo del grupo**
- ❌ **Dueño**: sin asignar.
- ❌ **Fecha de entrega**: sin due date, pero bloquea a STUDY-105, que vence el 05/11.
- ✅ Objetivo, criterios (9 escenarios en Gherkin) y contrato de API: completos.
- **Corrección:** se resuelve en minutos, pero es lo más urgente del board: decidir quién lo toma y ponerle una fecha **anterior al 05/11**.

## Backlog sin comprometer

- **[STUDY-94](https://tuequipo.atlassian.net/browse/STUDY-94) — Mostrar Rankings Pasados** 🔴 — descripción vacía: sin user story, sin criterios, sin épica. Antes de comprometerlo, el PO tiene que responder: ¿qué rankings (del grupo, globales, de qué período)? ¿dónde se muestran? ¿qué pasa si no hay rankings pasados?
- **[STUDY-80](https://tuequipo.atlassian.net/browse/STUDY-80) — Generación de tarjetas con IA en el modal de mazo** 🟡 — completo, pero ⚠️ **dependencia no linkeada**: su "Contrato consumido" usa el endpoint de STUDY-79 (To Do) y no hay link "is blocked by". **Corrección:** linkear STUDY-80 ← STUDY-79.
- **[STUDY-81](https://tuequipo.atlassian.net/browse/STUDY-81) — Sesión de usuario compartida entre pestañas** 🟡 — completo; solo le faltan dueño y fecha para comprometerlo.
- **[STUDY-49](https://tuequipo.atlassian.net/browse/STUDY-49) — Ver invitaciones actuales** 🟡 — completo, con un criterio vago:
  > Then el valor se muestra correctamente.

  **Propuesta (redacción mía, a validar por el PO):** *Then el nombre se muestra exactamente como está guardado, con tildes y apóstrofes, sin caracteres escapados ni reemplazados.*

## Lo que no se pudo evaluar
- Estimación: el equipo no usa story points (criterio desactivado en `config.md`).
- No se juzgó la solución técnica de ningún ticket: eso queda para el code review.
