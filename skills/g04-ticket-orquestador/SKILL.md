---
name: g04-ticket-orquestador
description: Crea los tickets de Linear de una semana de PitStop orquestando las skills de planeamiento, estimación, asignación, urgencia, contexto, objetivo y especificación técnica, con plan aprobado antes de crear y verificación al final. Usar cuando se pide armar o cargar los tickets de la semana o de una épica.
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
  grupo: "04"
  autor:
    nombre: Manuel Lostaló
    github: ManuLosta
  colaboradores:
  - nombre: Tomás Serra
    github: TomasSerra
  responsables:
  - ManuLosta
  madurez: experimental
  relacionados: []
---

# Orquestador de tickets

Crea los tickets de Linear de una semana de PitStop llamando a una skill por cada parte, en este orden.

## Skills que orquesta

| Paso | Skill | Qué aporta |
|---|---|---|
| 1 | `g04-planeamiento-sprint-tickets` | Qué funcionalidades entran en la semana |
| 2 | `g04-ticket-estimacion` | Puntos de cada ticket |
| 3 | `g04-ticket-asignacion` | Reparto entre devs y bloqueos |
| 4 | `g04-ticket-urgencia` | Prioridad según los bloqueos |
| 5 | `g04-ticket-contexto` | Contexto |
| 6 | `g04-ticket-objetivo` | Objetivo, criterios simples, por dónde empezar, glosario |
| 7 | `g04-ticket-especificacion-tecnica` | Bloque técnico |
| 8 | `g04-imagenes-para-ticket` | Capturas de referencia, después de crear el ticket |

Si alguna no está instalada, decirlo antes de seguir: no improvisar su parte.

## Fuentes de verdad

Revisar antes de planificar:

- `project-plan/features.yaml` — el backlog: epicas y funcionalidades en orden de
  prioridad, con titulo y descripcion escritos por el PM desde la app.
- `project-plan/team.yaml` — equipo, roles, capacidad, semanas, ids de Linear,
  stack y coordenadas del repo.
- `project-plan/design-system.md` — **los colores, las tipografias y los estilos de
  PitStop**. Todo ticket que toque la UI describe lo visual con los nombres de ahi:
  tokens de color (`primary`, `muted-foreground`, `border`), variantes de `Text`
  (`title`, `body`, `caption-strong`), tamanos de `Icon` y radios. Nunca con
  hexadecimales sueltos ni con clases de Tailwind inventadas en el momento.
- `../CLAUDE.md` — el project charter: objetivo, alcance, fuera de alcance, KPIs.
- `../PitStop Prototype/` — **especificacion de la UI**, no la implementacion.
- `../capacitacion/APP-CONTEXT.md` — convenciones de codigo y reglas de trabajo
  con desarrolladores junior.
- `../pitstop-stack/` — **el template de repo** (`project.repos.template` en
  `team.yaml`). El MVP no se arma desde cero: se crea desde ahi con `create-turbo`.
  Antes de escribir cualquier ticket de infraestructura o de setup, abrir el template
  y ver que trae ya — package.json de la raiz y de cada app, `turbo.json`, la config
  de lint y formato, `.github/` y `docs/`. **Nunca pedir trabajo que el template ya
  resuelve**, y nunca proponer una herramienta distinta a la que el template usa.
  (`../changuito/` es una copia del mismo template, la que se uso en la capacitacion.)
- **Linear** — trabajo existente, estado, asignados, puntos y duplicados.


Usar el servidor MCP de Linear conectado al workspace `pitstop-austral` (team `PIT`). Si hay más de un servidor de Linear, confirmar cuál antes de crear nada.

Nunca crear tickets para trabajo ya terminado ni ya cubierto por un ticket existente.

## Estructura del cuerpo

El ticket tiene **dos bloques separados por una linea horizontal**, y cada uno esta
escrito para un lector distinto.

Las secciones de arriba del separador salen de los pasos 5 y 6, y las de abajo del paso 7.

## Convenciones de Linear del team PIT

Al crear un issue con `save_issue`:

| Campo | Valor |
|---|---|
| `team` | `PIT` |
| `title` | En espanol, sin prefijo de area y sin jerga (ver "El titulo se lee sin abrir el ticket") |
| `state` | **`Backlog` siempre.** No se le asigna cycle (ver abajo) |
| `project` | **Obligatorio.** El `linear_project` de la epica |
| `priority` | **Obligatorio.** Es el orden de ejecucion de la semana (ver abajo) |
| `estimate` | 1, 2, 3, 4 o 5 |
| `dueDate` | El jueves de cierre de la semana |
| `labels` | `Fullstack` + una de `Feature` / `Improvement` / `Bug` |
| `assignee` | El `linear_user_id` del dev, o nada si es `null` |
| `blockedBy` | Solo dependencias reales que sigan pendientes |

**Ningun ticket se crea sin project y sin priority.** El project identifica la epica
y la priority le dice al dev que agarrar primero. Si la epica tiene
`linear_project: null`, crear primero el project en Linear con el nombre de la epica
(o preguntar cual quiere el PM), anotarlo en `features.yaml` y recien despues crear
los tickets.

La priority sale del paso 4.

### El cycle no se asigna: es incompatible con Backlog

Linear **no permite que un issue en estado `Backlog` pertenezca a un cycle**. Los dos
campos se pisan:

- Si se manda `cycle`, el ticket sale del Backlog y pasa a `Todo`.
- Si se manda `state: Backlog`, Linear lo saca del cycle.

**El equipo eligio Backlog.** Los tickets de la semana se crean en `Backlog`, **sin**
cycle, y quien los empieza los pasa a `Todo`. El sprint queda identificado por el
project de la epica y por la `dueDate`, no por el cycle.

Dos trampas mas de `save_issue` con el cycle, por si alguna vez se decide asignarlo:
acepta el `cycle_id` de `team.yaml` sin quejarse y despues **no lo asigna** (hay que
pasar el **numero**: `cycle: 1` para el Sprint 1), y su respuesta omite el `cycleId`
cuando quedo sin asignar, asi que el ticket parece bien creado y no esta en ningun
sprint.

### Verificacion obligatoria al terminar

Despues de crear todos los tickets, correr un `list_issues` sobre el team `PIT`
pidiendo `["id", "status", "priority", "estimate", "project", "dueDate", "assignee",
"labels"]` y confirmar campo por campo que ninguno quedo vacio y que los cinco
siguen en `Backlog`. La respuesta de `save_issue` no alcanza como verificacion:
omite los campos que quedaron sin setear en vez de marcarlos.

Los bugs de un sprint van al project `Fixes - SN` con label `Bug`.

### El titulo se lee sin abrir el ticket

El titulo dice **que queda funcionando cuando el ticket termina**, y tiene que
entenderse desde el tablero, sin abrirlo.

- Nombres propios de herramientas, si: Firebase, Prisma, Neon, Base UI, GitHub
  Actions. Un junior los googlea y entiende que son.
- Jerga de concepto, no: *guard*, *ID token*, *design system*, *CI*, *espejado*,
  *boilerplate*, *scaffolding*. Si el concepto no se puede evitar, va acompanado
  de lo que hace: "con chequeos automaticos en cada PR", no "con CI".

## Flujo de trabajo

Antes de crear nada en Linear:

1. Determinar la semana a planificar y su fecha limite.
2. Leer `features.yaml` y `team.yaml`.
3. Recorrer el backlog en orden hasta juntar la capacidad de la semana.
4. Leer las descripciones y abrir los archivos del prototipo de cada funcionalidad
   elegida. Si alguna tiene UI y no tiene `prototype`, avisarlo antes de seguir.
5. Inspeccionar los issues de Linear relacionados, incluidos los cancelados.
6. Armar el reparto minimizando bloqueos.
7. **Mostrar el plan de la semana con el titulo final de cada ticket, los SP por
   dev, el total y la fecha limite, y esperar confirmacion.** El titulo se muestra
   tal cual va a quedar en Linear, para que el PM lo pueda objetar antes de que se
   cree nada.
8. Recien ahi crear los tickets.
9. **Actualizar `features.yaml`**: a cada funcionalidad que quedo con ticket se le
   escriben sus `ticket_refs`, se le cambia el `status` de `todo` a **`backlog`** y, si
   sus fechas no coinciden con la semana planificada, se le corrigen `starts` y `ends`.
   Es un paso obligatorio del cierre: es como el PM ve desde la app que ya se
   subieron. Un ticket creado en Linear sin su funcionalidad en `backlog` es un
   trabajo a medias.
10. Informar que tickets quedaron sin asignar y por que.

Nunca marcar una funcionalidad como `in_progress` o `done` al crear su ticket:
`in_progress` lo pone quien empieza a trabajarla y `done` sale cuando la
implementacion cumple la definicion de terminado de `team.yaml` (rama, PR aprobado y
mergeado, build limpio, probado corriendo la app).

Si las herramientas de Linear no estan disponibles, generar el plan completo pero
**no** afirmar que se crearon los tickets.

## Reglas finales

- No duplicar issues. Los PIT-1 a PIT-18 ya existen y son de la Capacitacion: no se
  tocan, no se reestiman y no se reciclan. Los cancelados (PIT-6, PIT-12) quedan
  cancelados.
- La escala vieja de la Capacitacion (1 y 2 puntos) no se normaliza.
- No inventar trabajo terminado.
- No crear tickets de relleno ni artificialmente chicos.
- No generar trabajo para nada de `out_of_scope`.
- No cambiar el orden de prioridad del backlog ni los requerimientos del producto
  mientras se planifica. Eso lo decide el PM desde la app.

## Ejemplo de uso
**Pedido:** Armá los tickets de la semana que viene.

**Resultado:** Muestra el plan con títulos, puntos por dev, total y fecha límite; al confirmarlo crea los tickets en Backlog con su project y prioridad, verifica los campos en Linear y actualiza features.yaml.
