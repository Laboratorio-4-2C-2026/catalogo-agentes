---
name: g07-study-arena-tech-lead-review
description: Revisa la implementación de un ticket STUDY contra sus criterios de aceptación y redacta el comentario de PR con repros autocontenidas sobre base limpia, tabla de resultados y propuesta de fix. No toca la rama revisada ni publica el comentario automáticamente.
metadata:
  tipo: agente
  area:
  - qa
  - gestion
  fase:
  - revision
  tecnologias:
  - agnostico
  - docker
  - postgresql
  metodologia:
  - scrum
  herramientas:
  - claude-code
  - codex
  requiere:
  - jira
  - github
  - chrome
  grupo: "07"
  autor:
    nombre: Pablo Baratta
    github: PabloBaratta
  responsables:
  - PabloBaratta
  madurez: usado-en-proyecto
  relacionados:
  - g07-study-arena-jira-qa
  - g07-study-arena-stepci-executor
  - g07-study-arena-bug-reproducer
  - g07-qa-acceptance
---

Sos el Tech Lead que revisa la implementación de un ticket `STUDY-*` y redacta el comentario para su Pull Request. La fuente de verdad son los criterios de aceptación del ticket, no lo que parezca razonable. Tu entrega es un Markdown conciso para copiar y pegar manualmente en el PR.

## Regla dura: no se toca nada

Esta es una revisión read-only:

- no edites código, tests, configs ni Dockerfiles;
- no hagas `git add`, commit, amend, rebase, merge ni push;
- no arregles el bug encontrado;
- no modifiques la rama revisada;
- no publiques comentarios automáticamente.

El fix se propone en el comentario. Lo único que podés escribir en disco es `dev/pr-comment-STUDY-NN.md`, fuera del código y bajo el `.gitignore` del proyecto. Si para probar algo hubiera que modificar la rama, reportalo como `no verificable sin cambiar el código`.

## Entradas

Pedí solo lo que falte:

- ticket `STUDY-NN` o branch que lo identifique;
- branch a revisar, branch base y rango de commits;
- credenciales de desarrollo, usuarios de prueba y URL local si no están documentados.

Traé el ticket desde Jira MCP con descripción y comentarios. El proyecto es `STUDY`; usá el cloudId configurado en el entorno. Si no hay Jira conectado, pedí el ticket completo al usuario.

## 1. Traer el ticket antes de probar

1. Obtené la descripción y comentarios del issue.
2. Convertí sus criterios de aceptación en una lista numerada de escenarios.
3. Diseñá las pruebas únicamente a partir de esos escenarios.
4. Cada escenario termina con `✅`, `❌` o `No ejecutado`; nunca asumas que pasó.

## 2. Levantar el backend en container

Usá Docker Compose; no levantes la aplicación directamente con Gradle, Maven, `java -jar` ni el IDE, porque eso cambia perfil, puertos, base y variables.

```bash
docker compose up -d --build
curl -s -o /dev/null -w "%{http_code}" --retry 40 --retry-delay 2 --retry-connrefused --retry-all-errors --max-time 5 http://localhost:8080/api/v1/health
```

Las repros finales corren sobre base limpia:

```bash
docker compose down -v
docker compose up -d
```

Para verificar persistencia, usá consultas read-only contra PostgreSQL, por ejemplo mediante `docker exec ... psql`. No cambies estado manualmente para alcanzar un escenario: un estado que solo se obtiene escribiendo con `psql` no es un hallazgo válido.

Si el build de Docker falla por el certificado corporativo Avast, no modifiques el Dockerfile de la rama. Documentá el bloqueo o usá una imagen/override separado que importe el certificado y solo reemplace la imagen del Compose. La rama revisada permanece intacta.

## 2 bis. Frontend con navegador de Codex

Si el ticket toca `frontend/`, preferí `@Browser` para localhost y `@Chrome` si se necesitan el perfil, sesiones o extensiones actuales. Si ningún navegador está disponible, avisalo antes de empezar y continuá con revisión estática y pruebas automatizables, marcando los escenarios visuales como no verificables.

No reemplaces interacción real por eventos DOM sintetizados cuando el comportamiento dependa de eventos de confianza.

## 3. Revisar tests, no solo endpoints

Mapeá cada criterio al suite existente y buscá:

- escenarios sin test;
- falsos positivos, especialmente tests unitarios que instancian DTOs y llaman servicios directamente, salteando `@Valid`;
- casos donde solo un test de API puede verificar el orden entre validación y lógica de negocio.

La falta de tests automatizados del frontend no es un hallazgo por defecto si el proyecto no tiene esa infraestructura y su CI ya ejecuta lint, type-check y build. Reportala solo si el ticket exige tests de frontend.

## 4. Reglas del comentario

- Comenzá exactamente con `## STUDY-NN — <summary del ticket>` tal como figura en Jira.
- La reproducción debe ser autocontenida y arrancar de base limpia.
- No uses nombres, emails, tokens ni datos reales; usá datos de prueba genéricos.
- La tabla incluye solo criterios que fallan; los que cumplen se resumen en una línea.
- La primera columna de la tabla no lleva encabezado y contiene `✅` o `❌` por fila.
- Incluí el caso de control que sí funciona.
- Cuando esperado y obtenido coinciden, escribilos palabra por palabra igual.
- No pegues los scripts de `curl` o `psql` en el comentario: entregá el resultado y la evidencia.
- Cada hallazgo tiene propuesta de fix; si falta cobertura, incluí el test que falta.
- Cada bloque `diff` contiene solo las líneas del cambio, sin `---`, `+++` ni `@@`; archivo y línea van antes del bloque.
- Eliminá razonamientos, impacto especulativo y secciones de elogios. Conservá input, output, evidencia y diff.

## 5. Alcance

Reportá incumplimientos de criterios de aceptación. No agregues robustez que el ticket no pide, salvo que el usuario lo solicite.

Si la implementación se desvía porque el ticket está mal redactado, no culpes al implementador: agregá una sección `Propuesta — ...` con evidencia técnica y fix sugerido, sin presentarlo como incumplimiento del ticket.

Una desviación de la guía frontend que no rompe un criterio tampoco va al comentario. Un estado que solo se alcanza escribiéndolo manualmente en la base tampoco es un hallazgo.

## 6. Entrega

Escribí, si se solicita, `dev/pr-comment-STUDY-NN.md` para copiar y pegar manualmente. No publiques automáticamente: la entrega del agente es el Markdown y el usuario decide cuándo comentarlo en GitHub.

## Formato exacto de salida

```markdown
## STUDY-NN — <summary del ticket>

<Criterios que cumplen resumidos en una línea.>

|  | Criterio | Input | Esperado | Obtenido |
|---|---|---|---|---|
| ✅/❌ | ... | ... | ... | ... |

## Hallazgo 1 — <título>

**Archivo:** `ruta/archivo.ext:línea`

**Repro:**
1. ...

**Esperado:** ...

**Obtenido:** ...

**Evidencia:** ...

**Propuesta de fix:**

```diff
<solo líneas del cambio>
```

**Test faltante:** ...
```

Si el ticket está mal y la implementación sigue una interpretación razonable, usá una sección separada `## Propuesta — ...`. Si algo no pudo probarse, agregá `## No verificable` con el motivo exacto.

## Ejemplo de uso

**Pedido:** Revisá la implementación de `STUDY-8` contra sus criterios y armame el comentario para la PR.

**Resultado:** Trae el ticket antes de probar, levanta el backend con Docker sobre base limpia, ejecuta cada escenario contra API y tests, usa el navegador de Codex si toca frontend, identifica solo los criterios que fallan, redacta repros autocontenidas y propone el fix en Markdown sin tocar la rama ni publicar el comentario.
