---
name: g07-crear-ticket
description: "Skill para redactar y crear un ticket en Jira con escenarios que el usuario acepta antes de escribir: lee el repo en modo solo lectura para nombrar las cosas como se llaman de verdad, resuelve decisiones y gaps en un Gate 1, hace aceptar la lista de escenarios en un Gate 2, redacta con Given/When/Then y audita trazabilidad antes de crear. Pide al inicio el sitio de Jira, el proyecto y el repo."
metadata:
  tipo: skill
  area:
  - gestion
  - qa
  fase:
  - planificacion
  - analisis
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - jira
  grupo: "07"
  autor:
    nombre: Julieta Garberoglio
    github: JulietaG13
  responsables:
  - JulietaG13
  madurez: usado-en-proyecto
  relacionados: []
---

# Crear un ticket

El ticket se escribe **al final**, nunca al principio. Primero se resuelven las decisiones, después se aceptan los escenarios, recién entonces se redacta y se crea en Jira.

Partí de que el ticket lo va a leer una IA antes que una persona: muchos developers se lo pasan a una IA en vez de leerlo entero. Por eso tiene que ser **preciso como especificación** y **fácil de recorrer como texto**: resumen arriba, escenarios cortos con Given/When/Then separados y cero ambigüedad sobre qué queda afuera.

## Antes de empezar: datos del proyecto

Usá lo que ya esté en la conversación o en el `CLAUDE.md` / `AGENTS.md` del repo. Lo que falte, pedilo **en un solo mensaje** y no lo adivines.

| Dato | Para qué |
|---|---|
| Sitio de Jira (por ejemplo `miequipo.atlassian.net`) | Buscar y crear tickets. El cloudId sale de `getAccessibleAtlassianResources`, no hace falta pedirlo. |
| Key del proyecto y tipo de issue (por ejemplo `PROJ`, `Task`) | Buscar vecinos y crear |
| Labels que usa el equipo para separar back y front (por ejemplo `BE` / `FE`) | Etiquetar el ticket |
| Ruta del repo del producto | Leer el código y las guías |
| Guías de convenciones del repo, si existen (de back, de front, `CONTRIBUTING`) | Saber qué ya resuelve el proyecto |
| Uno o dos tickets de referencia ya aprobados | Copiar el formato y el registro del equipo |

## Reglas que no se negocian

1. **Nada asumido.** Cada afirmación normativa del ticket final tiene que rastrearse a: (a) algo que dijo el usuario en esta conversación, (b) un ticket existente que se cita por key, o (c) una decisión que el usuario aceptó explícitamente en el Gate 1. Si no entra en ninguna de las tres, no se escribe: va a la lista de decisiones abiertas. **El código del repo no es una cuarta fuente** (ver Fase 0).
2. **Ningún escenario sin aceptar.** Solo se redactan los escenarios que el usuario aprobó en el Gate 2, con el alcance con el que los aprobó. No se agregan "obvios" después.
3. **Nada de inventar contratos.** Si el ticket consume un endpoint, el JSON se copia del ticket que lo definió. Si ese ticket no existe todavía, es un gap: se reporta, no se improvisa.
4. **No avanzar de fase sin respuesta.** Si el usuario no contestó un gate, se espera. Nunca se completa por él.

## Fase 0 — Contexto (antes de proponer nada)

- Preguntar o confirmar qué feature es, si es de back o de front (label), y de qué épica o pantalla cuelga.
- Buscar en Jira los tickets vecinos y ya entregados que tocan lo mismo, con una JQL como:
  `project = <KEY> AND (summary ~ "<término>" OR description ~ "<término>") ORDER BY created DESC`.
- Leer completos los que definen los contratos o pantallas que este ticket toca, para citarlos por key y copiar sus JSON tal cual.
- Si hay un ticket par (el de back que define el endpoint que consume el de front, o al revés), leerlo entero: es la fuente del contrato.
- **Leer el repo**, en modo solo lectura.

Si Jira responde lento o con un error 5xx, reintentar una vez después de un minuto y seguir. No reemplazar la búsqueda por suposiciones.

### Leer el repo

Si no tenés acceso al repo, decilo antes de empezar y pedilo: sin el repo, la Fase 0 queda a medias y el ticket sale con nombres inventados.

Qué leer:

- **La guía del lado que toca el ticket**, si el proyecto tiene una. Fija stack y convenciones, y evita pedir algo que el proyecto ya resuelve de otra forma.
- **El código de la zona que toca el ticket**, para nombrar las cosas como se llaman de verdad. Ubicá las piezas recorriendo el repo, sin suponer la estructura:
  - **Back:** los controllers o routers del dominio (rutas y verbos reales), los DTOs o schemas (nombres exactos de campos), las entidades o modelos (estados), los códigos de error que ya existen y dónde se mapean a HTTP, y los tests (qué ya está cubierto).
  - **Front:** la página o ruta, los componentes existentes, el servicio o cliente HTTP y cómo tipa los errores, los tipos compartidos y los límites de validación ya definidos.

Cómo se usa lo que se leyó: **el código es contexto, no fuente normativa.**

- Sirve para tres cosas: nombrar con precisión (endpoint, pantalla, componente, campo, código de error), ver qué ya está implementado para no especificarlo de nuevo, y detectar gaps.
- Ninguna regla del ticket se justifica con "el código lo hace así". Si algo que el ticket necesita decidir solo está en el código, va al **Gate 1 como decisión abierta**, citando el archivo donde se vio, y se escribe recién cuando el usuario la acepta.
- Nunca se modifica nada del repo en esta skill.

## Gate 1 — Decisiones y gaps

Presentar en un solo mensaje, corto y numerado:

**A. Alcance propuesto** — 2-3 líneas: qué entra, qué no.

**B. Decisiones abiertas** — toda regla que haga falta para escribir el ticket y que no esté ya decidida en otro ticket, incluidas las que solo aparecen en el código. Una línea por decisión, con la opción que se recomienda y la alternativa; si sale del repo, nombrar el archivo. Ejemplos del tipo de cosa que va acá: quién puede ejecutar la acción, qué pasa con recursos borrados lógicamente, qué código HTTP corresponde a cada rechazo, si una operación modifica o no el estado de otra feature, qué pasa con empates o valores en cero, si hay que refrescar algo en el cliente.

**C. Gaps detectados** — cosas que el ticket necesita y ningún ticket existente cubre. Por cada gap, tres salidas: *(1)* lo incluyo en este ticket, *(2)* lo dejo explícito como fuera de alcance citando quién debería cubrirlo, *(3)* queda para un ticket nuevo. El usuario elige; nunca elegir por él.

Si las decisiones son de opción cerrada, preguntarlas con opciones para elegir. Esperar la respuesta antes de seguir.

## Gate 2 — Lista de escenarios

Presentar **solo los títulos**, numerados y agrupados por sección, una línea cada uno. Sin Given/When/Then todavía: la idea es que se lean todos de un saque.

```
Autorización
 1. Acceso exitoso con membresía activa
 2. Usuario sin membresía → 403, sin generar token
 3. Autorización antes que estado (no filtrar el estado vía 409)
Estado del recurso
 4. Recurso en estado programado → 409 con su código de error
...
```

Cerrar con: *"Decime cuáles saco, cuáles cambian de alcance y qué falta. Escribo solo los que queden."*

Si la lista pasa de **12 escenarios**, avisar antes de la aceptación: proponer qué grupo se podría partir en otro ticket y dejar que el usuario decida. No partir por cuenta propia.

Los escenarios se derivan de lo decidido, no de un checklist genérico. Fuentes habituales según el lado:

- **Back:** camino feliz; identidad tomada del contexto autenticado (nunca del cliente); 400 por formato inválido (nunca 500); 401 sin auth; 403 por permisos, evaluado **antes** que el estado; 404 por inexistente o borrado lógico (recurso y su padre); 409 por estado inválido, con código explícito; idempotencia y llamadas repetidas; efectos que la operación **no** debe tener sobre otras features; formato de respuesta común del proyecto, si tiene uno.
- **Front:** estado de carga; render del camino feliz; estado vacío distinguido del error; un mensaje distinto por cada código HTTP (400/403/404, y 5xx o red con reintento); limpieza de estado al cambiar el parámetro de ruta; no repetir requests por re-render; accesibilidad (teclado con foco visible y semántica para lector de pantalla). Si el proyecto ya resuelve algo de forma global (por ejemplo el 401 en un interceptor), queda fuera de alcance y se dice.

## Fase 3 — Redacción

Formato fijo, en el idioma y el registro de los tickets de referencia.

```markdown
**User Story:** Como <rol>, quiero <qué>, para <por qué>.

## Resumen

* **Qué:** <una línea>
* **Dónde:** <endpoint o pantalla/ruta + componente>
* **Contrato:** <endpoint> — definido en <KEY>-NN
* **Depende de:** <KEY>-NN, <KEY>-NN
* **No entra:** <lo que queda afuera, con el ticket que lo cubre si existe>

## Descripción

<Máximo 3 párrafos cortos. Qué hace y por qué, las reglas de negocio que se decidieron,
y las fronteras con otros tickets. Cero relleno.>

## Contrato de API        <!-- Back: definido acá. Front: "## Contrato consumido", copiado del ticket de back -->

<JSON de la respuesta exitosa y de cada error, tal como en el ticket que lo define.>

## Tareas y requerimientos técnicos

* <Bullets accionables, agrupados si son muchos (Componentes UI / Integración con la API / Navegación y estado).>

## Criterios de Aceptación

### <Grupo>

**Escenario 1: <Título>**

* **Given** <contexto>,
* **When** <acción>,
* **Then** <resultado observable>.

**Escenario 2: <Título>**

* **Given** ...,
* **When** ...,
* **Then** ...
```

Reglas de redacción:

- **Formato de escenario fijo**: título `**Escenario N: <Título>**`, línea en blanco, y tres bullets `* **Given** …,` / `* **When** …,` / `* **Then** ….`, con una línea en blanco entre escenarios. La numeración es corrida en todo el ticket (no reinicia por grupo) y los grupos van como `### <Grupo>`.
- **Un escenario = una cosa.** Cada bullet es una sola oración. Si el *Then* necesita más de una oración, el escenario está haciendo dos cosas: partirlo y avisar, porque cambia la lista aceptada.
- **Referencias a escenarios** siempre como "Escenario N", nunca "EN".
- **Sin código dentro de títulos en negrita.** Jira corta la negrita si el título o un label en `**…**` contiene backticks. En títulos de escenario, de grupo y en labels en negrita, el nombre va como texto plano.
- El *Then* describe algo **observable y verificable**, no una intención.
- Citar siempre por key cuando se referencia otra pantalla, endpoint o decisión. Nunca "el endpoint de grupos".
- Los estados y códigos de error se nombran literal (`403 Forbidden`, el código tal cual), no en prosa, y con el nombre que ya existe en el repo si existe.
- Si algo quedó afuera, aparece en **No entra** o en una línea explícita de la descripción. Un silencio no es un fuera de alcance.
- Nada de secciones vacías ni de "a definir": si hace falta definirlo, se vuelve al Gate 1.

## Fase 4 — Auditoría antes de crear

Revisar el borrador contra esta lista y reportar el resultado en dos o tres líneas:

1. **Trazabilidad:** cada requerimiento y cada escenario sale de una decisión aceptada, de un ticket citado o de algo que dijo el usuario. Nada apoyado solo en el código. Listar cualquier línea que no cumpla y borrarla o preguntarla.
2. **Cobertura:** están todos los escenarios aceptados en el Gate 2, y ninguno que no se haya aceptado.
3. **Fronteras:** todo endpoint, pantalla o entidad mencionada existe en un ticket citado por key, o está marcada como gap resuelto en el Gate 1.
4. **Consistencia del contrato:** el JSON del ticket es idéntico al del ticket que lo definió (mismos campos, mismos nombres, mismos códigos).
5. **Nombres reales:** endpoints, componentes, campos y códigos se escriben como aparecen en el repo; si el ticket pide uno nuevo, se dice que es nuevo.
6. **Formato:** resumen presente, descripción ≤ 3 párrafos, escenarios con el formato `**Escenario N: Título**` + bullets Given/When/Then, referencias como "Escenario N" y ningún backtick dentro de texto en negrita.

## Fase 5 — Crear en Jira

Mostrar el ticket final en el chat y crearlo con `createJiraIssue`:

- El proyecto y el tipo de issue que dio el usuario.
- `summary`: corto y descriptivo, en el estilo de los tickets de referencia, sin prefijo de back o front.
- `labels`: el de back o el de front, según corresponda.
- Descripción: el markdown redactado.

Devolver la key y el link. Si la creación falla, entregar el markdown listo para pegar y decir qué falló.

## Si se piden los dos tickets (back y front)

Se hacen **en orden**: primero el de back completo (define el contrato), después el de front consumiendo ese contrato ya creado y citándolo por key. Cada uno pasa por sus dos gates. Nunca redactar el de front contra un contrato que todavía no fue aceptado.

## Ejemplo de uso

**Pedido:** "Armame el ticket de back para que un miembro pueda abandonar una sesión."
**Resultado:** pide los datos de Jira y del repo que falten, lee los tickets vecinos y el código de sesiones, presenta alcance, decisiones abiertas y gaps, y después la lista de títulos de escenarios para aceptar. Redacta el ticket con contrato y Given/When/Then, lo audita y lo crea en Jira devolviendo la key y el link.
