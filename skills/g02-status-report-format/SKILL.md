---
name: g02-status-report-format
description: 'Usar para cargar cada jueves el status semanal del Equipo 02 (Zest) en el Tablero de Estado del Proyecto (pestaña "Equipo 02"): semáforo con motivo y acción, tabla de Cronograma y tabla de Incidentes, a partir de Multica.'
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
  - multica
  - github
  - google-sheets
  grupo: '02'
  autor:
    nombre: Ines Gassiebayle
    github: inesgassiebayle
  responsables:
  - inesgassiebayle
  madurez: experimental
  relacionados:
  - g03-status-risks
  - g03-status-schedule
  - g03-status-incidents
  - g11-weekly-status
---
# Status Report semanal — Zest (Equipo 02)

## Qué hace
Cada jueves, en la pestaña `Equipo 02` del Tablero de Estado del Proyecto:
1. **Semáforo**: propone el color de Alcance, Cronograma, Incidentes, Calidad y Riesgos para la semana en curso, con Motivo y Acción tomada para los que estén en Amarillo o Rojo. General se calcula solo.
2. **Cronograma**: actualiza estado, avance, fechas, desvío y comentarios de las actividades clave.
3. **Incidentes**: agrega los incidentes nuevos y cierra los resueltos.

Después deja un comentario en el issue con todo lo cargado para que el PM lo revise antes de la clase.

## Fuentes

### 1. Tickets de la semana en Multica
```bash
multica issue list --output json
```
Tomar los tickets cuya **fecha de vencimiento es el jueves de esta semana** y clasificarlos:
- **Terminados**: estado Done.
- **No terminados**: separados por estado (In review, In progress, To do).

Además, anotar los tickets creados en la semana que no estaban planificados (posible cambio de alcance) y los bugs abiertos.

### 2. La propia planilla
Leer la pestaña `Equipo 02` para conocer las actividades del Cronograma, los incidentes abiertos y lo que se reportó la semana anterior (un riesgo que sigue abierto no es nuevo).

## La planilla
- Google Sheets ID: `1tA2CFxUesISCr39-MmhhdxwmitZKZBhTdOjfpSGjCec`, pestaña `Equipo 02`. **No tocar ninguna otra pestaña.**
- **Semana en curso:** Sem-01 empieza el lunes 10/08/26; `semana = (hoy − 10/08/26) // 7 + 1`. El jueves 29/10/26 es Sem-12.
- **Semáforo** (filas 8 a 14): General, Alcance, Cronograma, Incidentes, Calidad, Riesgos. Una columna por semana (Sem-12 = M). Valores: `Verde`, `Amarillo`, `Rojo`. Motivo (V) y Acción tomada (W) acumulan todas las semanas: se **agrega** una línea `Sem-12 (26/10): …`.
- **Cronograma**: Actividad clave, Estado Tarea (`Finaliz.`, `En curso`, `Pend.`), Avance %, F. Fin L. Base, F. Fin Estimado, F. Fin Real, Desvío y Comentarios. El desvío es **línea base − fin real** en días (positivo = terminó antes).
- **Incidentes**: Descripción, Estado (`Abierto`, `Cerrado`), Criticidad (`Baja`, `Media`, `Alta`), F. Alta, F. Límite, F. Cierre, Vencido (`SI` si se cerró o sigue abierto después de la F. Límite) y Resolución.

El script `update_status.py` de esta skill ubica todas estas celdas leyendo los rótulos de la planilla, agrega el texto sin borrar lo anterior, escribe los incidentes nuevos en la primera fila libre de la tabla y se niega a sobrescribir una semana ya cargada. **No escribe General, Desvío ni Vencido: son fórmulas de la planilla.** Necesita `pip install gspread` y la cuenta de servicio en `~/.config/zest/google-sa.json`. Códigos de salida: 0 ok, 2 propuesta inválida, 3 semana ya cargada, 4 sin acceso a la planilla.

## Criterios del semáforo

Criterio de la cátedra: **Verde** = no existen inconvenientes; **Amarillo** = situaciones de alerta que pueden derivar en desvíos; **Rojo** = situaciones críticas que están derivando en desvíos. Ante la duda, elegir el color más conservador.

| Área | 🟢 Verde | 🟡 Amarillo | 🔴 Rojo |
|---|---|---|---|
| **Alcance** | Sin cambios al alcance acordado | Trabajo nuevo no planificado o funcionalidades repriorizadas, sin perder entregables | Se descarta una funcionalidad comprometida o un entregable de la cátedra |
| **Cronograma** | Todos los tickets con vencimiento este jueves están terminados | Hay tickets de la semana sin terminar, pero ninguna actividad clave mueve su F. Fin Estimado | Una actividad clave mueve su fecha, o queda en riesgo un hito (MVP del 12/11) |
| **Incidentes** | Sin incidentes nuevos ni abiertos | Incidente nuevo de criticidad Baja o Media, o abierto dentro de plazo | Incidente de criticidad Alta, o incidente vencido |
| **Calidad** | CI verde en `main`, PRs con review, sin bugs críticos | CI rojo < 24 h, PRs esperando review > 48 h o bugs mayores abiertos | CI rojo > 24 h, PRs mergeadas sin review o bugs críticos abiertos |
| **Riesgos** | Sin riesgos relevantes reportados | Riesgo identificado con plan de respuesta | Riesgo alto materializado o sin plan |

### Cómo redactar Motivo y Acción
- **Motivo**: concreto y con datos, como venía haciendo el equipo. Ej.: "Retraso en 4 de 9 tickets de la semana: 3 IN REVIEW con PR abierta (#41, #43, #44) y 1 IN PROGRESS."
- No nombrar a personas; hablar de tickets, actividades o roles ("el developer de frontend").

## Criterios para el Cronograma
Para cada actividad clave con tickets en la semana:
- **Avance %** = tickets terminados de la actividad ÷ tickets totales de la actividad (redondeado).
- **Estado**: `Finaliz.` si llegó al 100%, `En curso` si tiene avance, `Pend.` si no arrancó.
- **F. Fin Real**: la fecha en que se cerró el último ticket, solo si la actividad se finalizó.
- **F. Fin Estimado**: se mueve solo si, con lo que falta, ya no llega a la fecha actual. Explicarlo en el comentario.
- **Comentario**: "X de Y tickets cerrados" y qué falta.

Las actividades nuevas no se agregan: se sugieren en el comentario del issue.

## Criterios para Incidentes
- **Nuevo**: algo que ya pasó y afectó al trabajo (deploy caído, servicio externo, bloqueo, ticket mal asignado, ausencia no prevista). Lo que todavía no pasó es un **riesgo**, no un incidente.
- **Criticidad**: Baja (no frena a nadie), Media (frena tickets o atrasa días), Alta (frena al equipo o compromete una entrega).
- **F. Límite**: por defecto, una semana después de la F. Alta.
- **Cerrar**: cuando Multica muestra que se resolvió. Poner la F. Cierre real y la resolución.
- Revisar también los incidentes que siguen en `Abierto` de semanas anteriores.

## Pasos
1. Calcular la semana en curso. Si su columna del semáforo ya tiene valores, no sobrescribir: comentar en el issue y terminar.
2. Juntar los datos de las cuatro fuentes.
3. Armar `propuesta.json` (formato abajo).
4. Probar sin escribir: `python update_status.py propuesta.json --dry-run`
5. Si todo está bien, escribir: `python update_status.py propuesta.json`
6. Comentar en el issue y cerrarlo.

### Formato de propuesta.json
```json
{
  "semaforo": {
    "Alcance":    {"color": "Verde"},
    "Cronograma": {"color": "Amarillo",
                   "motivo": "Retraso en 3 de 8 tickets de la semana: 2 IN REVIEW con PR abierta (#41, #43) y 1 IN PROGRESS.",
                   "accion": "Se pidió en el grupo priorizar la revisión de los PR #41 y #43."},
    "Incidentes": {"color": "Verde"},
    "Calidad":    {"color": "Verde"},
    "Riesgos":    {"color": "Amarillo",
                   "motivo": "Semana de parciales para dos developers antes del MVP del 12/11."}
  },
  "cronograma": [
    {"actividad": "Planificación semanal", "estado": "En curso", "avance": 40,
     "comentario": "3 de 8 tickets cerrados. Falta la vista semanal y el guardado."}
  ],
  "incidentes": {
    "nuevos": [
      {"descripcion": "Falla del deploy en Render por variables de entorno faltantes",
       "criticidad": "Media", "f_alta": "27/10/26", "f_limite": "03/11/26"}
    ],
    "cerrar": [
      {"descripcion": "Vencimiento del free trial", "f_cierre": "29/10/26",
       "resolucion": "El cronograma quedó reconstruido en la planilla del equipo."}
    ]
  }
}
```
`descripcion` en `cerrar` es un fragmento que tiene que coincidir con **una sola** fila de la tabla.

### Comentario en el issue
```markdown
## Status Report — Sem-12 (26/10) cargado

**Semáforo:** General 🟡 · Alcance 🟢 · Cronograma 🟡 · Incidentes 🟢 · Calidad 🟢 · Riesgos 🟡

| Área | Motivo | Evidencia |
|---|---|---|
| Cronograma | ... | MULTICA TICKET N # |
| Riesgos | ... | |

**Cronograma:** Planificación semanal 0% → 40% (3 de 8 tickets).
**Incidentes:** 1 nuevo (Falla del deploy en Render, Media) · 1 cerrado (free trial).

### Para revisar antes de clase
- Celdas con `[A completar por el PM]`: ...
- Actividades nuevas sugeridas para el Cronograma: ...
- Datos faltantes: ...
```

## Reglas
- Solo se escribe la columna de la semana en curso, se agrega texto en Motivo, Acción y Comentarios, y se modifican filas de Cronograma e Incidentes. Nada más.
- No sobrescribir una semana ya cargada ni borrar texto de semanas anteriores.
- No inventar números, incidentes ni acciones.
- No nombrar ni evaluar a personas.

## Ejemplo de uso
**Pedido:** Cargá el status de esta semana en el tablero.
**Resultado:** Define el formato del semáforo con motivo y acción, la tabla de Cronograma y la de Incidentes, y las reglas para no sobrescribir semanas ya cargadas.
