---
name: g10-branch-pr-review
description: Revisa una branch o PR contra el ticket y los criterios de aceptación, no contra nits de estilo. Usar cuando el usuario pide revisar una branch, un PR, un ticket, criterios de aceptación, si está para aprobar, qué está mal, o un comment para dejar en el PR.
metadata:
  tipo: skill
  area:
  - qa
  fase:
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - agnostico
  herramientas:
  - codex
  requiere: []
  grupo: "10"
  autor:
    nombre: Marcos Carrizo Aslanian
    github: MarcosCarrizoA
  responsables:
  - MarcosCarrizoA
  madurez: experimental
  relacionados: []
---
# Review de branch / PR

El usuario pega el ticket y, a veces, un review de un bot. Juzgá el código. El veredicto es si cumple el ticket.

Respondé en español rioplatense, corto y directo. Primero el veredicto. No expliques la PR entera salvo que la pidan.

## Qué mirar

1. Identificá la branch actual y el diff contra la base que digan. Si no dicen, usá `origin/dev`.
2. Leé el ticket y cada criterio de aceptación.
3. Leé el código que cambia. Si el texto del autor o del bot contradice el código, gana el código.
4. Si dicen que la branch sale de otra, compará contra esa, no re-revises tickets ya cerrados salvo un cambio de comportamiento.

## Qué cuenta como problema

Un problema es algo que el ticket pide y el código no hace, o que hace al revés.

No son problemas, y no pidas comment:

- extraer helpers, renombrar, newlines, imports, self-closing, duplicación de fixtures
- un review de bot desactualizado o que el código ya no tiene
- un cambio de más que no rompe un criterio

Si un criterio no se cumple al pie de la letra pero el reemplazo hace lo mismo y está explicado (otro proveedor detrás de la misma interfaz, por ejemplo), decilo en una oración. Para un trabajo de curso, eso no bloquea el merge.

Un cambio de comportamiento que el ticket no pidió se menciona en una oración. No es bloqueante si no rompe un criterio.

## Cómo responder

**Review normal.** Una o dos oraciones: cumple o no. Después solo lo que no cumple o está hecho distinto. Si está para mergear: "No hace falta comment."

**"Qué está mal" / "no me expliques la PR".** Solo la lista de diferencias. Sin recorrido del diff.

**"¿Está todo bien?" / "¿está para aprobar?".** Sí o no primero. El sí vale si el código cumple y, si probaron el camino feliz, ese camino cerró.

**Comment para el PR.** Texto listo para pegar y el archivo con las líneas donde engancharlo. Un comment. No pidas los nits.

## Si piden probar o mirar datos

No expliques cómo levantar el proyecto si dijeron que no. Dale el flujo: quién hace qué, en qué orden, con qué datos.

Si preguntan por la base o por un request:

- Un listado vacío es 200 con `[]`, no 404.
- `Cannot GET /ruta` es la ruta que no está en el servidor que respondió, no un recurso inexistente.
- Un check verde de CI no despliega. Mirá el workflow: si solo hay lint, build y test, el front de la preview y el backend desplegado pueden ser versiones distintas.
- Confirmá en la base o en el código antes de decir que un registro se creó, se aceptó o venció.

## Ejemplo de uso

**Pedido:** Revisá esta branch contra el ticket y decime si está para aprobar. Si algo no cumple, pasame un comment para pegar en el PR.
**Resultado:** Veredicto primero, según el diff y los criterios. Si está para mergear, indica que no hace falta comment. Si no, un solo comentario listo para pegar, con el archivo y las líneas.
