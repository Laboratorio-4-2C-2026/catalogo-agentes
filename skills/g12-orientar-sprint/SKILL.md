---
name: g12-orientar-sprint
description: Cruza Linear, el repo de aplicación SplitIt, el roadmap de historias y el canvas para mostrar el estado completo del proyecto y orientar qué priorizar en las próximas 1-2 semanas, dejando las user stories priorizadas para el PM y la recomendación de canvas para devs/PO. Usar al empezar una sesión de PO, antes de elegir qué construir o iterar en el canvas.
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
  - codex
  requiere:
  - github
  - linear
  grupo: '12'
  autor:
    nombre: Lucas Monteverdi
    github: lucasmonteverdi1
  responsables:
  - lucasmonteverdi1
  madurez: experimental
  relacionados:
  - g12-armar-tickets-semanales
  - g12-construir-pantalla
  - g12-iterar-canvas
  - g12-verificar-historias-completadas
  - g12-to-canvas
---

# Orientar el sprint

## Dónde entra

Es el paso **anterior** a las otras skills de PO:

1. **Las historias** (`SplitItLab/roadmap`) — qué hay que construir y sus criterios.
2. **El desarrollo** (`SplitItLab/SplitIt` + Linear) — qué se está construyendo de verdad.
3. **El canvas** (`splitit-poc`) — qué está prototipado.
4. **Esta skill** — cruza las tres y da el estado completo del proyecto más una
   priorización para las próximas 1-2 semanas.
5. **`construir-pantalla`** / **`iterar-canvas`** — con la historia ya elegida, hacen el trabajo.

No escribe historias, no construye pantallas, no toca Linear. Es un mapa, no una acción.

## Dos productos, no uno

- **Estado completo del proyecto.** Todas las épicas y todas las historias del roadmap,
  cerradas o no, cruzadas contra Linear y el canvas — sin recortar por milestone. Es la foto
  entera: de dónde viene el proyecto, no solo qué queda.
- **Priorización a 1-2 semanas.** Sobre esa foto completa, qué conviene atacar en el
  horizonte inmediato. Esta ventana **no es "el milestone vigente"**: un milestone puede
  tener historias para más de dos semanas, y puede convenir asomarse al siguiente milestone
  si el actual ya no tiene margen para meter una historia nueva sin pantalla. La ventana se
  arma por trabajo real (qué backend ya está en review, qué depende de qué, qué vence
  primero), no por frontera de sprint.

Sin la foto completa, la priorización se vuelve un recorte arbitrario; sin la priorización,
la foto completa no orienta nada. Van juntas en el mismo reporte.

## Con quién se está hablando

El PO. Le interesa entender dónde está el proyecto entero y qué conviene priorizar ahora, no
el detalle técnico de cada fuente. Se reporta agrupado por épica, no como cuatro listados
sueltos.

El trabajo del PO tiene dos salidas, no una: **user stories priorizadas** para el PM (que las
convierte en tickets con `armar-tickets-semanales`) y **pantallas de prototipo** para los devs
(que las implementan contra el canvas). Esta skill deja lista la primera salida siempre, y
señala la segunda para que el PO la genere con `construir-pantalla` / `iterar-canvas`.

## Invocación

`/orientar-sprint` sin argumentos: da el estado completo del proyecto y la priorización de
las próximas 1-2 semanas.

## Procedimiento

### 1. Traer todo el roadmap, y ubicar el calendario

El estado completo no se recorta por milestone: se leen **todas** las épicas e historias,
abiertas y cerradas.

```bash
gh issue list -R SplitItLab/roadmap --state all --json number,title,state,body,milestone --limit 200
gh api repos/SplitItLab/roadmap/milestones --jq '.[] | "\(.title) | due:\(.due_on) | open:\(.open_issues) closed:\(.closed_issues)"'
```

El milestone de cada historia se usa como **dato de calendario** (para saber qué vence
cuándo), no como filtro de qué se lista. La foto completa incluye todo; el calendario sirve
para la priorización del paso 4.

Para saber cuál es el sprint en curso —insumo del calendario, no frontera de la lista—:

- La fuente que manda es el GitHub Project/Gantt del roadmap — ahí el sprint activo está marcado explícitamente, no inferido.
- Si el Project no está accesible y hay un solo milestone abierto, usarlo como sprint en
  curso — es evidencia inequívoca.
- Si el Project no está accesible y hay **más de un milestone abierto**, no elegir uno solo:
  mostrarlos todos con su `due_on` y `open_issues`, y preguntarle al PO cuál es el vigente
  antes de seguir. Un milestone vencido con issues sin cerrar (deuda arrastrada) no es lo
  mismo que el sprint en curso, y tratarlos como el mismo dato lleva a priorizar mal.

### 2. Fuentes, en este orden

1. **Roadmap** — épicas (`EPICA-*`) e historias (`SPLT-*`) completas, su milestone (dato de
   calendario), su jerarquía épica→historia (una historia referencia su épica en el cuerpo o
   título; si ninguna lo hace explícito, decirlo, no inferirlo por número) y si están
   abiertas o cerradas.
2. **Linear** (MCP, team `SplitIt`) — **todos** los `SPT-*` vinculados a alguna historia del
   roadmap (por la evidencia del paso 3, no por fecha): sin filtro de `updatedAt`, para no
   perder trabajo que está `In Progress`/`In Review` pero no se tocó en estos días. Es la
   fuente de qué se está desarrollando de verdad y en qué estado (Done, In Review, Todo). La
   ventana `updatedAt: -P7D` se usa **solo como contexto adicional** — para mostrar qué se
   movió esta semana en el reporte — nunca como filtro que decide qué ticket entra o queda
   afuera del cruce.
3. **Repo de aplicación** (`SplitItLab/SplitIt`) — PRs mergeadas/abiertas recientes
   (`gh pr list --state all`). Sirve para confirmar qué de Linear ya llegó a main y qué
   sigue en review.
4. **Canvas** (`splitit-poc`) — qué historias ya tienen pantalla. Ver paso 3 para cómo se
   determina esto: no hay una ruta literal por historia, hay que leer el mapa real del repo.

Si alguna fuente no responde (Linear con error de complejidad, `gh` sin auth, milestone
ambiguo), decirlo y seguir con las que sí — no inventar el estado de la que falta.

### 3. Cruzar por historia, con evidencia verificable

Roadmap (`SPLT-*`) y Linear (`SPT-*`) son dos backlogs con IDs propios — **no hay relación
implícita entre ellos**. Antes de afirmar que un ticket de Linear implementa una historia de
roadmap, la relación tiene que estar declarada en algún lado verificable:

- el cuerpo del issue de Linear o su PR asociado menciona el `SPLT-XXX` explícitamente, o
- el cuerpo de la issue de roadmap linkea el ticket de Linear o su PR, o
- la PR en `SplitIt` referencia ambos IDs.

Una coincidencia de título o de tema ("mostrar el enlace" en los dos) **no alcanza**. Si no
hay relación declarada, listar el ticket de Linear como **candidato no confirmado** para esa
historia y decirlo así en el reporte — nunca como implementación confirmada.

Para el estado del canvas, el mapa real vive en el repo del prototipo (`splitit-poc`), no en
una ruta asumida:

```bash
grep -rn "stories:" splitit-poc/lib/*.ts 2>/dev/null || find splitit-poc -iname "*prototype*" -o -iname "*canvas*"
```

Si el mapa no existe todavía en el repo local (por ejemplo, si `to-canvas` corrió sobre el
deploy pero el checkout local no lo tiene), decirlo y verificar directamente contra el deploy
(`<deploy-del-canvas>/canvas`) en vez de asumir una convención de ruta. Una historia
puede vivir en varias pantallas y una pantalla puede cubrir varias historias (`Screen.stories:
Story[]`, ver `to-canvas`): la pregunta correcta es "¿`screensOfStory(SPLT-XXX)` devuelve algo,
y con qué `canvasHref`?", no "¿existe `/canvas/SPLT-XXX`?".

Para cada historia del roadmap, reunir: estado en roadmap, milestone (dato de calendario),
ticket(s) de Linear (confirmado o candidato) y su estado, y si tiene pantalla en el canvas
(confirmado, y con qué URL). Agrupar por épica.

### 4. Reportar — estado completo, después priorización a 1-2 semanas

**Primero, el estado completo.** Tabla o lista por épica, con **todas** las historias del
roadmap — cerradas incluidas. Una épica enteramente cerrada y en canvas se resume en una
línea ("cerrada, sin pendientes"); una épica con historias abiertas se detalla: historia,
milestone, estado de desarrollo (con si el vínculo a Linear es confirmado o candidato),
estado de canvas. Esta parte es la foto: no recorta ni prioriza todavía.

**Después, la priorización a 1-2 semanas.** Sobre esa foto, arma el horizonte inmediato. No
es "las historias del milestone vigente": es el subconjunto de historias abiertas —de
cualquier milestone— que conviene atacar ahora, ordenado por:

1. Backend ya en review o mergeado (confirmado, no por título) y sin pantalla — el prototipo
   va a quedar atrás del desarrollo real si no arranca ya, sin importar en qué milestone cae.
2. Historias que vencen en los próximos 1-2 Steerings, en el orden que defina su dependencia
   natural (ej. registrar antes que modificar/eliminar).
3. Historias del milestone siguiente que convenga adelantar, si el milestone en curso ya no
   tiene margen (pocas historias sin pantalla, o todas ya priorizadas por 1-2) — decirlo
   explícitamente como adelanto, no mezclarlo sin aviso con el sprint actual.
4. Historias con pantalla pero sin auditar contra criterios — candidatas a `iterar-canvas`,
   de menor urgencia que las tres anteriores.

Cierra con las dos salidas del rol, como **propuestas** sobre esa priorización — esta skill
no crea ni modifica tickets ni issues en ningún repo, en ninguna de las dos fuentes:

**Propuesta para el PM — user stories priorizadas (1-2 semanas).** Lista ordenada, no todo
el roadmap. Cada una lleva:

- **dependencia**: de qué otra historia o ticket depende (ej. "necesita el endpoint de
  SPT-73 mergeado");
- **evidencia**: en qué se basa su estado — el link o ID exacto de Linear/PR si el vínculo es
  confirmado, o "candidato, sin vínculo declarado" si es una coincidencia de tema sin
  confirmar;
- **riesgo**: qué pasa si no se prioriza en esta ventana (vencimiento del Steering, bloquea
  otra historia, deuda que crece).

Es el insumo que el PM revisa y decide si correr con `armar-tickets-semanales`; esta skill no
lo invoca. No incluye historias ya cerradas ni detalle de pantalla — al PM le interesa qué
construir, no cómo se ve.

**Propuesta para devs/PO — qué sigue en el canvas.** De esa misma lista priorizada, cuáles ya
tienen pantalla confirmada en el mapa del prototipo (listas para implementar tal cual están)
y cuáles no. Nombra la skill que seguiría (`construir-pantalla` o `iterar-canvas`) y la
historia puntual, como recomendación — la decisión y la ejecución las toma el PO en otra
sesión.

## Lo que esta skill no hace

- No construye ni itera pantallas.
- No escribe ni cierra issues ni tickets en ningún repo (roadmap, SplitIt o Linear). Sus dos
  salidas son propuestas de lectura para que el PM y el PO decidan.
- No asume una relación SPLT↔SPT ni una ruta de canvas por coincidencia de nombre: si no hay
  evidencia verificable, lo marca como candidato y lo dice.
- No reemplaza `armar-tickets-semanales`: esa reparte horas entre devs; esta orienta al PO
  sobre qué prototipar y le entrega al PM el insumo priorizado antes de que la corra.
- No recorta el estado completo por milestone. La priorización a 1-2 semanas es una capa
  sobre esa foto entera, no un filtro que reemplaza mostrar el resto del roadmap.

## Ejemplo de uso

**Pedido:** /orientar-sprint

**Resultado:** Muestra el estado de todas las historias por épica cruzando roadmap, Linear, repo y canvas, y cierra con las historias priorizadas para las próximas 1-2 semanas para el PM y la recomendación de canvas para el PO.
