---
name: g14-ponerse-en-tema
description: "Usar cuando alguien pregunta dónde está algo en el código de VaiVen, cómo funciona hoy una parte de la app o del motor, qué tiene que saber para trabajar en un área, o arranca un ticket. Contesta la pregunta y nada más; no compara el kit contra el código. Necesita que el repo tenga mapas del código (docs/codigo/frontend.md y docs/codigo/datos-y-motor.md) que indiquen qué archivo cubre cada parte."
metadata:
  tipo: skill
  area: [frontend, backend, documentacion]
  fase: [desarrollo, mantenimiento]
  tecnologias: [supabase, n8n]
  metodologia: [agnostico]
  herramientas: [claude-code, otra]
  requiere: []
  grupo: "14"
  autor:
    nombre: Elías Ballesteros
    github: Elias85974
  responsables: [Elias85974]
  madurez: usado-en-proyecto
  relacionados: []
---

# Ponerse en tema con el código que ya existe

Quien pregunta quiere ponerse a trabajar, no un informe. El equipo rota de carril entre sprints, así que lo más probable es que la pregunta sea sobre código que escribió la otra persona.

Los mapas [`docs/codigo/frontend.md`](../../../docs/codigo/frontend.md) y [`docs/codigo/datos-y-motor.md`](../../../docs/codigo/datos-y-motor.md) son **un índice**: sirven para llegar rápido al archivo correcto. **No son algo que se verifica.**

## El protocolo

1. **Clasificá la pregunta** en uno de los tres modos de abajo.
2. **Leé un solo mapa**, el que toca: app, pantallas, componentes y helpers → `frontend.md`; migraciones, políticas, Storage y nodos del motor → `datos-y-motor.md`.
3. **Buscá en el mapa la fila de lo que se pregunta** y abrí **sólo** los archivos que esa fila nombra. El código vive en `app/`.
4. **Contestá con la forma del modo.** La primera línea es la conclusión.

Si el mapa no lleva a ningún archivo, **una** búsqueda puntual por el nombre del símbolo (`grep -rn "getPortada" app/src`). No un recorrido.

## Los tres modos

**(a) «¿Dónde está X?»** — Abrís un archivo. Salida: `ruta:línea` y dos frases, qué hace y qué lo usa. Ni una tercera con «de paso, también…».

> `app/src/lib/imagenesPublicacion.ts:7` — `getPortada()` devuelve la imagen de menor `orden` de una publicación. La usan `PublicationCard` y `HomeFeed`.

**(b) «¿Cómo funciona X hoy?»** — Abrís los archivos del recorrido, nada más. Salida: el punto de entrada en una línea y después el flujo **en pasos numerados**, uno por archivo o nodo, cada uno con su `ruta:línea`. Sin pegar código: como mucho una línea citada si es la clave del paso.

Una pregunta amplia —«contame de n8n», «qué tengo que saber de Supabase»— es este modo a escala de área: la sección del mapa **ya es** la respuesta. Resumila en diez líneas como máximo, abrí a lo sumo el archivo de entrada para dar su `ruta:línea`, y cerrá con una línea: *«¿Sobre qué querés profundizar: A, B o C?»*.

**(c) «Arranco el ticket N»** — Leé el ticket, los documentos que el [`INDEX`](../../../docs/INDEX.md) le asigna y, del código, sólo lo que el ticket va a tocar. **Antes de escribir una línea**, la salida es:

- **Se reusa:** `ruta` — para qué, uno por renglón.
- **Hay que construir:** qué, y en qué archivo va.
- **Falta decidir:** sólo si el ticket necesita algo que no está escrito. Si no falta nada, este bloque no aparece.

## Reglas

- **Se lee el código sólo de lo que la pregunta toca.** Nada de recorrer el repo, correr `git log`, abrir el otro mapa ni chequear el resto de las filas.
- **La respuesta arranca por la conclusión.** El detalle, sólo si lo piden.
- **Si al pasar ves que el mapa quedó viejo**, lo decís en **una** línea al final —`Mapa desactualizado: <qué>.`— y seguís. Sin lista de diferencias, sin ofrecer corregir hojas ni armar tickets, y sin editar el `.md` salvo que te lo pidan.
- **Lo que viste de paso y no es la pregunta, no va**, aunque parezca útil: un bug ajeno, código muerto, un aviso sobre la sesión o las herramientas. Sólo si bloquea lo que la persona está por hacer entra, y en esa misma línea final.
- **No respondas de memoria.** Una `ruta:línea` que das salió de un archivo que abriste en esta respuesta.
- **«¿Ya existe?» se contesta mirando `main`.** Lo que está en una rama sin mergear no cuenta como hecho.
- **No deduzcas reglas que no están escritas** ni amplíes el ticket: lo que falte se pregunta a dirección; lo mejorable se anota aparte.

## Señales de que te fuiste a auditar

Estás abriendo archivos que la pregunta no nombra, escribiste la palabra «diferencias», tenés más de una observación sobre el mapa, o estás por ofrecer corregir documentación. Pará y volvé a la pregunta.

## Ejemplo de uso
**Pedido:** "¿Dónde está la función que elige la imagen de portada de una publicación?"
**Resultado:** Abre el mapa `frontend.md`, va al archivo que nombra la fila y contesta con `ruta:línea` y dos frases: qué hace la función y qué componentes la usan.
