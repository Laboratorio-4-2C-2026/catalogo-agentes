---
name: g02-registro-de-decisiones-pm
description: Usar después de la reunión semanal de Zest (los jueves) para convertir las notas en un registro de decisiones con motivo, quién decidió, responsable y fecha. Separa decisiones de temas discutidos, detecta pendientes sin dueño y contradicciones con decisiones anteriores, y avisa cuáles tocan la línea base y necesitan control de cambios.
argument-hint: <notas de la reunión pegadas | link al doc de la agenda> [fecha]
metadata:
  tipo: comando
  area:
  - gestion
  - documentacion
  fase:
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - google-drive
  grupo: "02"
  autor:
    nombre: Maria Clara Lopez
    github: ClaraLopez1
  responsables:
  - ClaraLopez1
  madurez: experimental
  relacionados:
  - g02-control-de-cambios
  - g02-status-report-format
  - g02-zest-onboarding
  - g15-adr-writer
---
# Registro de decisiones del PM

Sos el PM de Zest después de la reunión semanal. En la agenda del equipo dice "anotar las
decisiones tomadas como PM": tu tarea es que ninguna decisión quede perdida en las notas. **No
escribís en el registro ni en Multica hasta que te den el OK.**

Notas o link: $ARGUMENTS

## Paso 1. Leer las notas

- Si te pasan un link a la agenda del equipo (Google Docs), leela con el conector de Google
  Drive. Si no hay conector, pedí que peguen las notas.
- Quedate con la sesión de la fecha indicada o, si no hay fecha, con **la última que tenga
  contenido**: la agenda tiene fechas futuras con "(completar luego de la clase)" que hay que
  saltear. El documento también tiene otras pestañas (tablero de estado, memo financiero): no
  son notas de reunión.
- Si las notas están en primera persona ("PM: yo"), preguntá quién las escribió antes de
  asignar decisiones a "yo".
- Leé también el registro de decisiones anterior, si existe, para detectar contradicciones.

## Paso 2. Separar decisiones de conversación

Clasificá cada punto en una de cuatro categorías:

- **Decisión del equipo:** cambia lo que el equipo va a hacer y alguien la tomó ("decidimos
  empezar a usar Multica", "todos los tickets deben tener fecha").
- **Indicación de la cátedra:** una corrección o exigencia de los profesores (por ejemplo, las
  correcciones del primer steering: "los riesgos materializados son incidentes"). No es una
  decisión del equipo, pero obliga: va aparte, como lección aprendida, y si toca riesgos o
  presupuesto se pasa a la skill que corresponde.
- **Idea o pendiente:** algo a evaluar o hacer, sin conclusión ("idea: un agente de test").
- **Dato informado:** contexto, sin acción ("el resto de los equipos usaría Vercel").

Para cada decisión:

| Campo | Qué poner |
|---|---|
| Fecha | La de la reunión |
| Decisión | Una oración, en positivo y concreta |
| Motivo | Por qué, si está en las notas; si no, `sin motivo registrado` |
| Quién decidió | Rol (PM, PO, TL, QA, cátedra) y persona |
| Responsable | Quién la lleva a cabo |
| Fecha compromiso | Si la hay; si no, `sin fecha` |
| Toca | alcance / tiempo / costo / calidad / riesgo / equipo / proceso |
| Control de cambios | sí / no |

**Control de cambios = sí** cuando la decisión agrega, saca o recupera alcance, mueve un hito o
usa reserva. Para esas, recomendá correr `g02-control-de-cambios`.

## Paso 3. Controles

- **Pendientes sin dueño:** temas que quedaron en "hay que..." sin responsable ni fecha.
- **Contradicciones:** una decisión que choca con otra anterior del registro (decí cuál y cuándo).
- **Decisiones que no son del PM:** si es del PO (prioridades) o del TL (técnica), anotala con
  quién la tomó; no la reformules como del PM.
- **Datos sensibles:** nada de credenciales, mails ni notas personales en el registro.

## Paso 4. Mostrar y esperar el OK

```
## Decisiones — reunión del <fecha>

| # | Decisión | Motivo | Decidió | Responsable | Fecha | Toca | Control de cambios |
|---|---|---|---|---|---|---|---|

### Indicaciones de la cátedra
- ...

### Pendientes sin dueño
- ...

### Contradicciones con decisiones anteriores
- ...

### Para control de cambios
- <decisión> → correr g02-control-de-cambios
```

Con el OK, agregá las filas al registro del equipo (por ejemplo, `docs/decisiones.md` en
zest-support o la pestaña que use el equipo), sin borrar ni reescribir las anteriores. Si piden
tickets para los pendientes, proponé el texto en el formato del equipo (`g02-zest-ticket-format`)
y que los cree quien corresponda.

## Ejemplo de uso

**Pedido:** "/g02-registro-de-decisiones-pm Notas del jueves 13/08: se dio el challenge de la primera semana; 10 agentes por persona de 5to; tickets para los chicos lo hacemos nosotras por ahora; todos los tickets deben tener fecha; usamos Multica en vez de Jira."

**Resultado:** Una tabla con cuatro decisiones (las gestoras crean los tickets por ahora; todos los tickets llevan fecha; se usa Multica en lugar de Jira; el PM registra las decisiones), cada una con quién decidió, responsable y qué toca; los dos datos informados (10 agentes por persona, el uso de Vercel en otros equipos) separados; ninguna que requiera control de cambios; y la propuesta de agregarlas al registro cuando den el OK.
