---
name: g02-storytelling-de-demo
description: 'Usar para preparar o ensayar la demo de Zest en un steering, en Lab II, en un demo day o en el final: verifica qué está terminado, arma la historia con una persona y entrega el paquete completo (guion clic por clic con quién habla y qué hacer si falla, versiones de 30 s, 2 y 5 minutos, preguntas probables, plan B y checklists). También hace de público para ensayar.'
metadata:
  tipo: skill
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
  - multica
  grupo: "02"
  autor:
    nombre: Maria Clara Lopez
    github: ClaraLopez1
  responsables:
  - ClaraLopez1
  madurez: usado-en-proyecto
  relacionados:
  - g04-guion-de-demo
  - g09-preparar-demo-sprint
  - g05-watchparty-steering-rehearsal
  - g02-demo-data-generator
  - g02-deck-de-steering
---

# Storytelling y demo: de funcionalidades a una historia

La persona dice qué quiere mostrar ("colecciones y el planificador", "todo lo del
Sprint 3") y para quién (steering, Lab II, demo day, final). La skill arma el
**paquete de demo completo**: la historia, el guion clic por clic con lo que dice
cada presentador, versiones cortas, preguntas probables con respuesta, plan B y
checklists. También sirve para **ensayar**: hace de profesor y devuelve feedback.
Responde en español.

## Archivos de este módulo

| Archivo | Qué tiene |
|---|---|
| Este archivo | El proceso y las reglas |
| [`storytelling/README.md`](./guia-de-uso.md) | Guía para personas: cómo pedirle cosas |
| [`storytelling/frameworks.md`](./frameworks.md) | Estructuras: hacé lo último primero, sparkline, SCAR, tarjeta funcionalidad → valor, versiones por duración |
| [`storytelling/personas.md`](./personas.md) | Sofi y Lucía, y los datos de la demo (cuentas, recetas, colecciones) |
| [`storytelling/demo-kit.md`](./demo-kit.md) | Formato del paquete, mapa de fallas de Zest, checklists, banco de preguntas, modo ensayo |
| `../docs/product.md` (`zest-support/docs/product.md`) | Pitch, problema, KPIs, alcance, lista de NOs, qué está construido |

## El proceso

### 1. Entrevista corta

Antes de escribir, preguntá **solo lo que falte**, en un solo mensaje y como
máximo cuatro preguntas:

- ¿Para quién es? (steering, Lab II, demo day, final)
- ¿Cuánto dura todo y cuánto la demo?
- ¿Quién presenta y quién maneja la compu?
- ¿Qué cambió desde la última presentación? (para el hilo entre steerings)

Si la persona ya lo dijo, no lo vuelvas a preguntar. Si responde solo una
parte, **no repreguntes**: seguí con supuestos razonables y escribilos arriba de
todo del paquete ("Supuse que...") para que los corrija.

### 2. Verificar qué existe

Para cada funcionalidad pedida, confirmá que está **terminada y en producción**:

- Código de la app en `main` (`frontend/src/features/` del repo `zest`, si está
  clonado al lado; **solo lectura**).
- Para saber qué viene en camino: las ramas y los PRs abiertos (solo lectura) y
  los tickets en curso, en Multica o en el cronograma del equipo, con sus fechas.
- Multica: el ticket en `done`. `in_review` no se demuestra.
- La sección "Qué está construido" de `docs/product.md`.

Lo que no esté terminado se cuenta como "lo que viene", nunca como demo. Si no
podés verificarlo, preguntá: no lo des por hecho.

**Si algo pedido no está terminado pero tiene fecha antes de la presentación,**
armá dos guiones: **A** con esa funcionalidad y **B** sin ella (contada como
"lo que viene"). Los pasos comunes se escriben una vez, y el checklist fija el
día del ensayo general como el momento de elegir A o B.

### 3. Tarjetas funcionalidad → valor

Llená una tarjeta por funcionalidad ([`frameworks.md`](./frameworks.md)
§4). La que no tiene dolor, prueba visible o KPI no entra.

### 4. Elegir la estructura

| Situación | Estructura |
|---|---|
| Poco tiempo o público no técnico | Hacé lo último primero |
| Steering o cierre, donde importa el porqué | Sparkline, con SCAR por funcionalidad |
| Lab II | Recorrido de la persona + cómo está hecho cada paso |
| Final de la materia | Sparkline, y cada beat conectado con un concepto de la cátedra |

Decí cuál elegiste y por qué, en una línea.

### 5. Armar el paquete

Con el formato de [`demo-kit.md`](./demo-kit.md) §1. Reglas del
guion:

- **Una protagonista**, de principio a fin (Sofi, salvo que se pida otra cosa).
- **Ordenado por el recorrido de la persona**: descubrir → guardar → organizar →
  planificar. Nunca por módulo ni por backlog.
- **Un clic por fila**, con lo que tiene que verse después, así quien presenta se
  da cuenta enseguida si algo falló.
- **Columna "Si falla"** en cada paso que toque backend, login, imágenes o red
  (mapa de fallas, `demo-kit.md` §2).
- **Quién habla en cada fila** si presentan varias personas, con el pase entre
  ellas escrito ("Les dejo con Santi, que les muestra...").
- **Datos de [`personas.md`](./personas.md)**, siempre los mismos.
- **Números solo con fuente**: los del proyecto salen de
  `project-management.md` (skill `g02-valor-ganado-evm`); los KPIs de producto, del
  reporte de KPIs.
- **Versiones de 30 s, 2 min y 5 min** del mismo mensaje.
- **Cierre**: volver al gancho, el KPI que se mueve y el próximo hito. En un
  steering, cerrar con lo que se le pide al comité, si hay algo.

Guardá el paquete en `decks/<evento>/demo.md` (por ejemplo,
`decks/steering-3/demo.md`), al lado del deck, y avisá dónde quedó. Si el
paquete alimenta un deck, agregá un esquema de una línea por slide para la skill
`steering-deck.md` (skill `g02-deck-de-steering`), que lo lee de ahí.

Antes de guardarlo, recordá que este repo es público: nada de credenciales,
mails ni datos de usuarios reales.

### 6. Ensayo (si lo piden)

El modo ensayo de [`demo-kit.md`](./demo-kit.md) §5: hacé de público,
cronometrá, preguntá y devolvé primero el cambio más importante.

## Adaptar al público

| Público | Énfasis | Evitar |
|---|---|---|
| Steering (Lab IV) | Valor entregado contra el plan, decisiones, trade-offs, riesgos; la historia enmarca la demo | Detalle técnico |
| Lab II | Cómo se construyó: arquitectura, calidad (tests, CI), el trabajo de los devs | Métricas de gestión |
| Demo day / usuarios | Solo la persona y su recorrido | Métricas, stack, jerga |
| Final de la materia | Cada beat conectado con un concepto (alcance, calidad, riesgos...) | Leer la lista de pantallas |

## Reglas que no se negocian

- **Solo se demuestra lo que existe** y está en producción.
- **Nunca se promete algo de la lista de NOs** (social, IA, app mobile,
  importar de redes, pagos): si preguntan, se dice que está fuera de alcance y
  por qué.
- **Vocabulario real de la app**: los textos que muestra la app hoy. El
  prototipo (`design/zest/Zest.dc.html`) solo para pantallas que todavía no
  existen, y avisando que el texto puede cambiar (el prototipo está en inglés y
  la app en español).
- **Los datos tienen que existir con ese nombre**: por ejemplo, el catálogo de
  ingredientes está en inglés, así que un filtro por ingrediente busca "lemon",
  no "limón".
- **Ningún número sin fuente.**
- **Nunca una cuenta real** de alguien del equipo ni datos de usuarios reales.
- **No se modifica el repo `zest`**: la skill solo lo lee.

## Datos de la demo

Para cargar los datos que necesita la historia, usá la skill del grupo
`g02-demo-data-generator`: genera recetas, colecciones y usuarios ficticios a
partir del esquema real. Esta skill solo dice qué datos hacen falta.

## Ejemplo de uso

**Pedido:** "Armame la demo del Steering 3 con colecciones y el planificador: 10 minutos, presentan Santi y Thiago."

**Resultado:** Revisa el código y el cronograma, detecta que el planificador todavía no está terminado y arma dos guiones (A con el planificador, B sin él), con la historia de Sofi, tarjetas funcionalidad → valor, un guion clic por clic con quién habla y qué hacer si falla cada paso, versiones cortas, preguntas probables, plan B y checklists para el ensayo y el día.
