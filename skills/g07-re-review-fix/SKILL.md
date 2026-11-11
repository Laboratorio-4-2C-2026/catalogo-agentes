---
name: g07-re-review-fix
description: "Verifica los commits de corrección de una PR contra el comentario de review anterior, sin tocar la rama: corre cada hallazgo con la misma repro sobre base limpia, vuelve a correr los escenarios vecinos al cambio, corre la suite y comprueba que los tests nuevos fallen contra el commit viejo, y redacta el comentario de seguimiento. Usar ante pedidos como \"el dev subió el fix, revisalo\". Pide al inicio el comentario anterior, Jira y los comandos del entorno."
metadata:
  tipo: skill
  area:
  - qa
  - backend
  - frontend
  fase:
  - revision
  tecnologias:
  - agnostico
  - git
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - jira
  - chrome
  grupo: "07"
  autor:
    nombre: Julieta Garberoglio
    github: JulietaG13
  responsables:
  - JulietaG13
  madurez: usado-en-proyecto
  relacionados: []
---

# Re-review de un fix

Segunda vuelta de una review: el developer subió commits que dicen arreglar lo que marcó el comentario anterior. La pregunta es **"¿quedó arreglado, y no se rompió nada?"**, no "¿está bien todo el ticket?". La review completa ya se hizo.

Documento vivo.

---

## Antes de empezar: datos del proyecto

Usá lo que ya esté en la conversación o en el `CLAUDE.md` / `AGENTS.md` del repo. Lo que falte, pedilo **en un solo mensaje** y no lo adivines.

| Dato | Para qué |
|---|---|
| El comentario de la primera review (archivo o texto) | Saber qué hallazgos verificar |
| El commit que se revisó la primera vez, si el comentario no lo dice | Delimitar el fix |
| Sitio de Jira y key del ticket | Releer los criterios |
| Comando para levantar el entorno y para resetear la base | Repros sobre base limpia |
| Comando para consultar la base | Verificar persistencia |
| Comando de la suite de back, y de lint y typecheck de front | Revisar los tests |
| URL local del front, si el ticket lo toca | Probar con Claude in Chrome |
| Carpeta ignorada por git para la entrega | Dejar el markdown |

## 0. Regla dura: no se toca la rama

Igual que en la primera review: nada de editar, commitear, rebasear ni pushear. Si un fix está mal, se propone el diff en el comentario. Lo único que se escribe es el markdown de entrega.

## 1. Juntar las tres fuentes

1. **El comentario anterior.** Hacer la lista de hallazgos numerados, y las propuestas aparte.
2. **El ticket** en Jira, con `description` y `comment`. Puede haber cambiado desde la primera review.
3. **El rango de commits del fix**: `git log --oneline <sha revisado>..HEAD` y `git diff --stat <sha revisado>..HEAD`.

Con el diff a la vista, anotar qué archivos y qué funciones tocó el fix. De eso sale el §3.

## 2. Cada hallazgo, con su misma repro

- Base limpia, con el comando de reset del proyecto.
- Correr **exactamente** los inputs de la tabla original, incluido el caso de control.
- Un hallazgo queda resuelto solo si **todas** sus filas ❌ pasan a ✅ y el control sigue en ✅.
- Si el developer resolvió el hallazgo por otro camino que el propuesto, está bien siempre que las filas pasen. Se dice qué cambió en una línea, sin opinar sobre la elección.
- Si el ticket toca el front, las pruebas de UI van con Claude in Chrome. Si no está disponible en la sesión, decirlo antes de empezar.

## 3. Escenarios vecinos

Volver a correr los escenarios del ticket que pasan por el código que tocó el diff, aunque en la primera vuelta hayan dado ✅. Un caso típico: cambiar el tipo de un campo de la respuesta arregla un hallazgo y rompe otro escenario que dependía del formato viejo.

Regla práctica: todo escenario cuyo endpoint, service, componente o hook aparece en el `git diff --stat`.

## 4. Suite y cobertura del fix

- **Back:** la suite completa. Anotar total y fallas.
- **Front:** lint y typecheck. Si el proyecto no tiene tests de front, su falta no se reporta.
- **Si la primera review pidió un test**, comprobar que de verdad cubre el arreglo: en una copia aparte, nunca en la rama, dejar los tests nuevos y volver a la versión de `<sha revisado>` solo las clases de producción que tocó el fix. Los tests nuevos tienen que fallar ahí. Si pasan, no están probando el arreglo, y eso va como hallazgo.

## 5. El comentario

Arranca con `## <KEY>-NN — <summary del ticket>` y una línea de estado:

> Verificado `<sha>` sobre base limpia. Los hallazgos 1 a N quedaron resueltos y los M escenarios cumplen. La suite pasa: T tests, 0 fallas.

Después, según lo que haya:

- **Todo resuelto:** una viñeta por hallazgo, con el dato que lo prueba (status code, cuerpo, nombre del test que lo cubre). Nada más.
- **Hallazgo que sigue fallando:** la misma tabla ✅/❌ / input / esperado / obtenido de la primera review, con las filas actuales, y el diff del fix.
- **Algo que rompió el fix:** su propia sección `## Escenario N`, con tabla, control y diff, como un hallazgo nuevo.
- **Algo nuevo que no estaba en la primera review y no lo causó el fix:** va como `## Propuesta — …`. Se aclara si también está en el commit viejo ("también está en `<sha revisado>`, no lo introduce la corrección").

Las reglas de redacción son las mismas que en la primera review:
- Datos neutros (`Test User`, `user@example.com`).
- Sin razonamiento propio, y solo lo que falla en detalle.
- Cuando esperado y obtenido coinciden, se escriben palabra por palabra igual.
- Bloques `diff` sin encabezados `---`/`+++`/`@@`, un hunk por bloque.

## 6. Entrega

`<carpeta>/pr-comment-<KEY>-NN-fix.md`, para copiar y pegar a mano en la PR. Si hay una segunda corrección, `-fix-2.md`.

## Ejemplo de uso

**Pedido:** "El dev subió `82cafda` con el fix de PROJ-48, revisalo contra mi comentario."
**Resultado:** vuelve a correr las repros de cada hallazgo sobre base limpia, repite los escenarios que pasan por los archivos del diff, corre la suite y comprueba que los tests nuevos fallan contra el commit viejo. Deja un comentario corto que confirma cada punto con su evidencia, o muestra lo que sigue fallando con su fix.
