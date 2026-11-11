---
name: g14-valor-ganado-desde-jira
description: Calcula el valor ganado (PV, EV, AC, SPI, CPI, ETC, EAC, TCPI) en horas de desarrollo a partir de las estimaciones, fechas y worklogs de Jira leídos por API, con su trayectoria por corte y la trazabilidad de cada número. Usala para preparar la slide de valor ganado de un steering o sprint review y su respaldo ante preguntas.
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - revision
  - planificacion
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - jira
  grupo: '14'
  autor:
    nombre: Elías Ballesteros
    github: Elias85974
  colaboradores: []
  responsables:
  - Elias85974
  madurez: usado-en-proyecto
  relacionados:
  - g14-preparador-de-steering
  - g02-valor-ganado-evm
  - g12-calcular-valor-ganado
---

# Valor ganado desde Jira

Medí si lo gastado compró lo que tenía que comprar. Tres curvas en la misma unidad —**horas del recurso escaso** (en VaiVen, horas de los devs)— y los índices que salen de ellas.

## Criterio, antes de tocar un número

Fijalo por escrito y no lo cambies a mitad de cálculo:

| Curva | Qué suma | Fuente |
|---|---|---|
| **PV** | Estimación original de cada actividad, en su **fecha de línea base** | Estimación de la tarea madre en Jira + fecha base del tablero o del sprint |
| **EV** | **La misma estimación**, en la **fecha real** en que la actividad quedó lista (en VaiVen, «lista para revisión»). Sin avances parciales: una actividad suma recién cuando termina | Estado y fecha de transición en Jira, o el tablero compartido |
| **AC** | Worklogs por **fecha de registro** | API de Jira |

- **El EV se valúa al presupuesto de la tarea, no a lo que costó.** Una tarea de 6 h que llevó 7,4 aporta 6 de EV y 7,4 de AC. Esa separación *es* el desvío de costo.
- **Lo que no tiene registro se imputa a su plan y se declara.** En VaiVen la capacitación (26,4 h) no tenía worklogs: toma su plan, y es el único número imputado.
- **Qué queda afuera**, dicho explícitamente (en VaiVen: las horas de dirección).
- **BAC** = el presupuesto que mide la curva. Si la capacidad real no lo alcanza, se rebasea **una vez**, se declara en la slide como «Línea base ajustada» y se explica (VaiVen, Steering 2: 180 → 170 h = capacitación + 12 semanas × 12 h).

## Pasos

1. **Credenciales del entorno.** Usuario y token de Jira desde un `.env` ignorado por git (`JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`). Nunca los imprimas ni los pegues en el resultado.
2. **Listá las actividades** del período con JQL (`POST /rest/api/3/search/jql`, campos `timeoriginalestimate`, `status`, `parent`, `created`). La unidad es la **tarea madre**: las subtareas suman a su madre.
3. **Bajá los worklogs** de cada issue (`GET /rest/api/3/issue/{key}/worklog`, paginando). Guardá `started` y `timeSpentSeconds`; convertí a horas con un decimal.
4. **Fecha real de cada actividad**: la transición a «lista para revisión» (`expand=changelog`) o la del tablero, si el tablero es la fuente pactada. Si Jira y el tablero difieren, gana el criterio fijado y se anota (VaiVen: `SCRUM-35` en «Pruebas» en Jira, lista el 16/09 en el tablero).
5. **Antes de calcular, buscá huecos de registro**: actividades terminadas con 0 h o muy por debajo de su estimación. Pedí a los devs que carguen y **recalculá**. En VaiVen, cargar los worklogs pendientes de cuatro issues movió el CPI del Steering 2 de 1,08 a 1,01.
6. **Calculá por corte semanal** (PV, EV y AC acumulados en cada fecha) y los índices del corte actual:
   - `SV = EV − PV`, `SPI = EV / PV` (plazo; < 1 = atraso)
   - `CV = EV − AC`, `CPI = EV / AC` (costo; < 1 = más caro)
   - `ETC = BAC − EV`, `EAC = AC + ETC` (a tasa presupuestada) y `EAC = BAC / CPI` (si el desvío se mantiene), `VAC = BAC − EAC`, `TCPI = (BAC − EV) / (BAC − AC)`
   - `% completado = EV / BAC`, `% consumido = AC / BAC`
7. **Sensibilidad del número imputado**: recalculá AC y CPI con el imputado a ±10 % y +20 %. Es el flanco real de la slide.
8. **Verificá la aritmética** de cada fila contra su fuente antes de pasarla a la presentación, y marcá el bloque `[verificado — API de Jira, <fecha>]`.

## Salida

1. **Tabla por actividad**: estimado · registrado · fecha base → fecha real.
2. **Tabla por corte** (PV, EV, AC) para la curva; en la slide, PV sólo hasta el corte actual, la extensión al BAC queda en el respaldo.
3. **Recuadro**: SPI, CPI, SV, CV y «AC de BAC h».
4. **Una frase**: «En fecha, y 1,2 h por encima de lo estimado sobre 70 h entregadas».
5. **Respaldo**: indicadores derivados, sensibilidad y preguntas probables con respuesta corta (ver `docs/presentaciones/steering-1-2026-09-17-defensa-presupuesto-valor-ganado.md` como modelo).

## Reglas

- **Contá la trayectoria, no sólo el número final.** Un SPI de 1,00 al cierre de un hito es esperable por construcción; la prueba de que la medición es real está en los cortes intermedios (VaiVen: 0,69 el 26/08, por costo sin valor, y recuperación a 1,00).
- **No llames «reserva» a la diferencia entre el BAC y lo planificado en tickets** si no está declarada: es un supuesto.
- **Puente a dinero sólo si lo piden**: EV y AC × tarifa del charter. El desvío en dólares suele desactivar la discusión.
- Un número se corrige una vez, con su fuente, y se cierra.

## Qué NO hacer

- No uses el tiempo restante de Jira ni avances porcentuales como EV.
- No mezcles horas de dirección con horas de desarrollo en la misma curva.
- No escribas en Jira: esta skill sólo lee.

## Ejemplo de uso

**Pedido:** Calculá el valor ganado al 15/10 para el Steering 2 con los worklogs de Jira; el BAC es 170 h.

**Resultado:** Devuelve la tabla por actividad y por corte, el recuadro (SPI 0,99 con EV 118,4 contra PV 120,2; CPI 1,01 con AC 116,7), ETC 51,6 h, EAC, la frase de la slide y la lista de issues con worklogs faltantes que hay que cargar antes de entregar.
