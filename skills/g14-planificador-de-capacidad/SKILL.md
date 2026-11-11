---
name: g14-planificador-de-capacidad
description: "Determina la capacidad real de devs de dedicación parcial para un hito o una semana (parciales, horas efectivas, reserva), re-estima con tripletes contra main y propone opciones de recorte antes de secuenciar. Usala cuando el total estimado no entra en la capacidad; entrega los límites al planificador de semana, que es quien secuencia, publica y arma las tareas madre."
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
  requiere: []
  grupo: "14"
  autor:
    nombre: Anapaola Borda
    github: AnaB2
  colaboradores: []
  responsables:
  - AnaB2
  madurez: usado-en-proyecto
  relacionados: []
---

# Planificador de capacidad

**Asignar y estimar son dos operaciones distintas.** La asignación (6 h por dev por semana) es una decisión de reparto; la estimación es una predicción. Cuando un plan se presenta, las dos colapsan en un número y la tentación es cerrar la diferencia por el lado barato: inflar. Esta skill cierra la diferencia sin perder la información.

En VaiVen: dos devs a 6 h/semana, hitos de 4 semanas = `4 × 6 × 2 = 48,0 h`, 24 por carril. Evidencia: `docs/planning/hito-4-cronograma.md`, `docs/bitacora/2026-08-17-una-semana-vacia-se-llena-con-alcance-no-con-decimales.md`, `docs/bitacora/2026-09-16-un-ticket-se-estima-contra-el-codigo-no-contra-el-plan.md`.

## Procedimiento

1. **Capacidad.** Semanas × horas × devs, por carril. Marcá las semanas con parciales, entregas de otras materias o feriados.
2. **Leé cada ficha contra `main` antes de sumar.** En el Hito 4 de VaiVen, 24 fichas sumaban 42,0 h y buena parte ya existía en el código: 10 se dieron de baja (fusionadas o sin línea en el charter). Un `[por-verificar]` del tipo «esto ya podría estar hecho» se verifica **antes** de sumar horas.
   - «Ya existe como MVP» no es «terminado»: lo que queda (llevarlo a Figma, validar errores, probar) se estima así.
   - Un paso de verificación no es un ticket: va como criterio de aceptación del ticket que lo produce.
3. **Re-estimá con triplete** (optimista / probable / pesimista) y desglose por paso, en la ficha del ticket: `1,5 h — triplete 1,0 / 1,5 / 2,25 · migración 0,4 · políticas 0,25 · …`. Para una tarea nueva para quien la hace (primer despliegue), usá la estimación de quien la hace por primera vez.
4. **Compará contenido mínimo contra capacidad** y elegí la salida:

   | Situación | Qué se hace | Qué NO se hace |
   |---|---|---|
   | Contenido < capacidad | Traer **alcance real ya estimado** (pulido contra Figma, QA, errores, adelantar el hito siguiente) y marcarlo como lo primero que sale | Inflar estimaciones; mostrar semanas vacías |
   | Contenido > capacidad | Recortar por la regla de alcance (sólo entra lo que cita una línea del charter), fusionar tickets, pasar a reserva | Comprimir horas para que entre |
   | Semana con parciales | **Los tickets de menor fricción**, no menos horas nominales; o una semana liviana declarada como replanificación | Dejar la semana en 0 h |

5. **Declará el colchón.** La diferencia entre contenido mínimo y capacidad se nombra: «48,0 h nominales, contenido mínimo ~34,5 h, la diferencia es colchón declarado por parciales» (Hito 4). Una reserva útil es una lista de tickets nombrados con fecha de corte, no horas ociosas.
6. **Un número se re-abre una sola vez.** Si hay que corregir una estimación, se corrige con su triplete y se cierra.
7. **Registrá horas reales aparte** para no contaminar la calibración siguiente: si los devs trabajaron 7–8 h contra 6, se anota como medición, no se reescriben las estimaciones hacia atrás.

## Salida

- Techo de horas por carril y semana, con colchón, y la lista de tickets que entran en ese techo. El orden dentro de la semana y la publicación los decide g14-planificador-de-semana.
- Lista de **lo que salió** (a otra semana, a reserva, de baja) con el motivo.
- Lo que quedó `[asumido]` o `[por-verificar]` (p. ej. «la semana 4 a ~4 h es replanificación nuestra, no velocidad medida»).

## Qué NO hacer

- No usar una sobrecarga anterior supuesta como argumento para cargar más.
- No decidir sola un cambio de alcance o de fechas del charter: preparar las opciones con trade-offs y llevarlas al PM.
- No mezclar horas en el cuerpo de los tickets: viven en la ficha y en el campo de estimación de Jira.

## Ejemplo de uso

**Pedido:** La semana 4 los devs tienen un examen y una entrega de otra materia; aliviala sin dejarla vacía.

**Resultado:** Propone la semana a ~4,0 h por dev con tickets de baja fricción, recorta o funde lo que no cita una línea del charter, abre tickets armazón para los arreglos del ensayo, y deja escrito que las 4 h son replanificación y no velocidad medida (como el commit 53b7162 de VaiVen).
