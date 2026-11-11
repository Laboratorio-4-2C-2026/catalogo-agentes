---
name: g07-review-ticket
description: "Skill para revisar la rama de un ticket de Jira contra sus criterios de aceptación y redactar el comentario de PR sin tocar la rama: levanta el entorno como lo define el proyecto sobre base limpia, prueba la API y la UI con Claude in Chrome, busca escenarios sin test y falsos positivos en la suite, y entrega una tabla de lo que falla con caso de control, propuesta de fix y test faltante. Pide al inicio el sitio de Jira, los comandos del entorno y la carpeta de entrega."
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

# Revisar un ticket y redactar el comentario de PR

Documento vivo: cuando una review encuentra una regla nueva y general, se agrega.

---

## Antes de empezar: datos del proyecto

Usá lo que ya esté en la conversación o en el `CLAUDE.md` / `AGENTS.md` del repo. Lo que falte, pedilo **en un solo mensaje** y no lo adivines.

| Dato | Para qué |
|---|---|
| Sitio de Jira y key del proyecto | Traer el ticket. El cloudId sale de `getAccessibleAtlassianResources`. |
| Cómo se deduce el ticket de la rama (por ejemplo `PROJ-8-algo` → `PROJ-8`) | Saber qué ticket revisar |
| Comando para levantar el entorno y para resetear la base (por ejemplo `docker compose up -d --build` y `docker compose down -v`) | Probar sobre base limpia |
| URL de health o de una ruta para saber que el back ya levantó | Esperar el arranque |
| Comando para consultar la base (por ejemplo `docker exec <contenedor> psql ...`) | Verificar persistencia |
| Comando de la suite de tests de back, y de lint y typecheck de front | Revisar los tests |
| URL local del front | Probar la UI |
| Guías de convenciones del repo, si existen | Saber qué se considera desvío |
| Carpeta ignorada por git donde dejar el markdown (si no hay, proponer una y pedir que se agregue al `.gitignore`) | Entregar sin ensuciar la rama |

## 0. Regla dura: NO SE TOCA NADA

Esto es **solo revisión**. No se hace **ningún** cambio en la rama que se está revisando:

- Nada de editar código, tests, configs ni arreglar el bug encontrado.
- Nada de commits, `git add`, amend, rebase, merge ni push.
- El fix se **propone** en el comentario de la PR, no se aplica.

La rama es de quien la está implementando: **solo esa persona la modifica**. Lo único que se escribe en disco es el markdown de entrega (§6).

Si para probar algo hiciera falta modificar el código, no se modifica: se reporta como "no verificable sin cambiar el código" y se explica por qué.

---

## 1. Traer el ticket ANTES de probar

No probar por intuición. La fuente de verdad son los **criterios de aceptación** del ticket, no lo que parezca razonable.

- Traerlo con el MCP de Atlassian (`getJiraIssue`), pidiendo `description` y `comment`.

Armar la lista de escenarios numerados del ticket y recién ahí diseñar las pruebas. Cada escenario tiene que terminar con un ✅/❌ explícito: si un escenario no se probó, se dice, no se asume.

## 2. Levantar el entorno como lo define el proyecto

Siempre con el comando del proyecto (por ejemplo Docker Compose). **No** correr la app por otro camino (directo desde la terminal o desde el IDE): eso levanta un entorno distinto al de la rama (perfil, puertos, base, variables) y las repros dejan de ser reproducibles para el resto del equipo.

Esperar a que el back responda en la URL de health antes de probar.

**Las repros finales se corren sobre base limpia**, con el comando de reset del proyecto.

Si el entorno no levanta por algo de la máquina (certificados, red, permisos), no se toca nada de la rama para destrabarlo: se avisa qué falló y se acuerda con el usuario cómo seguir.

## 2 bis. Front: con Claude in Chrome

Si el ticket toca el front, se prueba con Claude in Chrome sobre la URL local. Si en la sesión no está disponible, **decirlo antes de empezar**, no al final: los escenarios de UI quedan como "no verificados" y la revisión sigue con lo demás.

## 3. Revisar también los tests, no solo el endpoint

Mapear cada criterio de aceptación contra la suite y buscar dos cosas:

- **Escenarios sin test.**
- **Falsos positivos.** Un test unitario que arma el DTO a mano y llama al service directo **saltea la validación del controller** (por ejemplo `@Valid` en Spring), así que pasa en verde aunque el endpoint falle. Si un escenario depende del orden entre validación y lógica de negocio, solo un test de API lo detecta.

Es un caso típico: un test de normalización del email pasaba en verde llamando al service, y el endpoint devolvía 400 porque la validación corría antes del trim. El único escenario sin test de API era el único que fallaba.

## 4. Reglas para el comentario

- **Autocontenido**: la repro no puede asumir datos ya cargados. Arranca de base limpia y crea lo que necesita.
- **Sin datos sensibles**: nada de nombres ni mails reales. Usar `Test User`, `user@example.com`, `other@example.com`.
- **Los casos van como tabla de ✅/❌ / input / esperado / obtenido.** La primera columna, sin encabezado, lleva ✅ o ❌ por fila, para ver de un vistazo cuál es la que falla. El script de `curl` o de la consulta a la base que los generó no va: se corre para producir el dato, no se pega en el comentario.
- **Cuando el obtenido coincide con el esperado, las dos celdas dicen lo mismo, palabra por palabra.** Si difieren en la redacción, el lector tiene que comparar para darse cuenta de que la fila pasa.
- **Incluir el caso de control**: la variante que sí funciona va como una fila más de esa tabla (por ejemplo, que sin espacios ande prueba que el problema es solo el trim).
- **Sin razonamiento propio.** Va el dato y la evidencia, no cómo se llegó ni por qué importa. Afuera queda lo que interpreta ("el control acota el diagnóstico"), lo que proyecta impacto ("eso cae al fondo de la lista") y lo que justifica el fix elegido frente a la alternativa. Sí queda el hecho pelado que hace falta para aplicarlo (por ejemplo "esta clase no es thread-safe: se instancia por llamada").
- **Solo lo que falla.** Nada de secciones tipo "lo que está muy bien". En la tabla de criterios van únicamente los que fallan; los que cumplen se resumen en una línea arriba ("Los criterios 1 a 7 y 9 a 24 se verificaron y cumplen"). Igual con cualquier tabla de inventario: las filas ✅ se colapsan en una frase.
- **Con propuesta de fix**, y si hubo hueco de cobertura, también el test que faltaba. El bloque ```diff lleva solo las líneas del cambio, sin los encabezados `--- a/` / `+++ b/` / `@@`: el archivo y la línea van en el texto que precede al bloque, y un hunk por bloque.
- **Arranca con el título** `## <KEY>-NN — <summary del ticket>`, tal cual figura en Jira.
- Formato: tabla con los criterios + secciones por hallazgo. **Lo más conciso posible**: al terminar, releer cada oración y borrar la que no sea input, output, evidencia o diff.

## 5. Alcance: qué reportar y qué no

**Reportar lo que incumple un criterio de aceptación.** Dejar afuera el ruido de robustez que no está en el ticket, salvo que se pida. Ejemplos de lo que normalmente **no** se reporta:

- JSON malformado, falta de `Content-Type` o método HTTP incorrecto que devuelven 500 en vez de 400/415/405 porque un handler genérico se los traga.
- Una race condition en un alta duplicada que da 500 en vez de 409 cuando la integridad de datos igual queda a salvo por un constraint.

Si en algún ticket esto sí importa, va a estar pedido en el ticket.

**La falta de tests automatizados en el front no se reporta si el proyecto no tiene infraestructura de tests de front.** El §3 aplica a la parte que sí tiene suite.

**Si la implementación se desvía del ticket y el error está en el ticket, el punto va como propuesta.** Sale de la numeración de hallazgos y va en su propia sección "Propuesta — …", con toda la evidencia técnica y el fix sugerido, pero sin las referencias a lo que el ticket pedía ni el señalamiento de que estaba mal redactado. El ticket lo escribe el mismo equipo: marcarlo como incumplimiento le carga al implementador un error que no cometió.

**Una desviación de la guía de front que no rompe ningún criterio de aceptación no va al comentario.**

**Un estado que solo se alcanza escribiéndolo a mano en la base no es hallazgo.**

## 6. Entrega

Markdown en la carpeta ignorada por git, para copiar y pegar a mano en la PR. Por ejemplo `<carpeta>/pr-comment-<KEY>-NN.md`.

No se publica automáticamente: el comentario aparecería con la cuenta de GitHub del usuario, así que lo pega él cuando lo revisó.

## Ejemplo de uso

**Pedido:** "Revisá la implementación de PROJ-8 contra el ticket y armame el comentario para la PR."
**Resultado:** pide los comandos del entorno y la carpeta de entrega si faltan, trae el ticket de Jira, levanta la rama sobre base limpia, prueba cada escenario y revisa los tests de API. Deja el comentario con solo lo que falla, el caso de control, la propuesta de fix y el test faltante.
