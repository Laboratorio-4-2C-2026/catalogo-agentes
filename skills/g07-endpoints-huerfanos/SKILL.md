---
name: g07-endpoints-huerfanos
description: "Inventaría los endpoints de los controllers Spring Boot de Study Arena y las llamadas HTTP del frontend React, y lista los endpoints que ningún front usa (código muerto o funcionalidades sin pantalla) y las llamadas del front que no tienen backend (rutas mal escritas o features a medio integrar), con archivo:línea y el ticket de Jira relacionado. Usar antes de una entrega o una limpieza; no compara la forma de los DTOs ni edita código."
metadata:
  tipo: skill
  area:
  - backend
  - frontend
  - qa
  fase:
  - revision
  - mantenimiento
  tecnologias:
  - spring-boot
  - react
  - typescript
  - python
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: "07"
  autor:
    nombre: Ana Abramowich
    github: AbramowichAna
  responsables:
  - AbramowichAna
  madurez: usado-en-proyecto
  relacionados:
  - g07-documentar-producto
  - g07-performance-con-volumen
  - g07-code-review-tl
---

# Endpoints huérfanos

Con varios tickets BE y FE en paralelo es fácil terminar con **endpoints que nadie llama** (el front se resolvió de otra forma, la feature se cayó o quedó un endpoint de prueba) y con **llamadas del front a rutas que no existen** (un typo, un endpoint renombrado o un ticket BE que todavía no se mergeó). Ninguna de las dos cosas rompe el build, así que nadie las ve hasta la demo.

Esta skill hace el inventario cruzado. **No** compara la forma de los request o response: para eso hay skills de contrato (como `g11-contrato-api` o `g09-check-front-back-contract`). Acá la pregunta es solo si existe y si se usa.

## Cuándo usar esta skill

"¿Qué endpoints no usa nadie?", "¿hay llamadas del front que fallan?", "limpieza antes de la entrega", "¿está integrado todo lo del back?", o después de un sprint con muchos tickets BE/FE separados.

## Paso 1: ubicar el código

Detectá las carpetas del backend (donde están los `@RestController`) y del frontend (por ejemplo `frontend/src`). Buscá también:
- el **prefijo base** del cliente HTTP del front (`baseURL` de axios, una constante `API_URL`, el proxy de Vite en `vite.config.ts`): si el cliente agrega `/api`, pasalo como `--base-front /api` (en Study Arena, `VITE_API_URL` termina en `/api` y las llamadas empiezan con `/v1/...`);
- `server.servlet.context-path` en `application.yml`/`.properties` (prefijo global del back).

## Paso 2: primera pasada automática

Corré el script de esta carpeta (no lo copies al repo):

```bash
python3 -I <carpeta-de-la-skill>/scan_endpoints.py --back <dir-backend> --front <dir-frontend> --base-front <prefijo> --json /tmp/endpoints.json
```

Detecta `@RequestMapping` de clase + `@Get/Post/Put/Patch/DeleteMapping` y llamadas `fetch(...)`, `axios.<verbo>(...)` y `<cliente>.<verbo>(...)` (también con tipos genéricos anidados, como `apiClient.get<ApiEnvelope<T[]>>(...)`) con rutas literales o template strings. Resuelve rutas armadas con funciones o constantes simples (`const quizPath = (...) => \`/v1/...\``, `const ENDPOINT = '/v1/...'`). Las rutas que aparecen como texto en otro lugar (por ejemplo, pasadas como parámetro a un wrapper) se listan como **"usados de forma indirecta"**: ahí el script no sabe el método, así que hay que confirmarlo a mano. Sigue siendo **heurístico**: no entiende rutas armadas en varias líneas ni constantes importadas desde otro paquete.

## Paso 3: verificar cada hallazgo a mano

El script da candidatos; el reporte sale de verificarlos uno por uno.

**Para cada endpoint "sin uso":**
1. Buscá su ruta y sus pedazos en el front (`rg -n "<segmento>" frontend/src`): puede usarse a través de un wrapper, de una constante o de una ruta armada por partes.
2. Fijate si lo usa algo que no sea el front: otro servicio, un job, Swagger para pruebas, los workflows StepCI del repo de QA o tests e2e.
3. Buscá con `git log -S"<ruta>" --oneline` cuándo apareció y en qué ticket (`STUDY-<n>` en el commit o la rama), y traé el estado del ticket de Jira si hay MCP.
4. Clasificalo:
   - 🔌 **Pendiente de integrar**: hay un ticket FE abierto que lo va a consumir. Es normal y no es deuda.
   - 🪦 **Muerto**: ningún ticket abierto, el front no lo usa y no lo usa nada más. Candidato a borrar.
   - 🧪 **De soporte**: lo usan tests, QA o tareas administrativas. Es correcto, pero conviene documentarlo.
   - ❓ **No determinado**: explicá qué falta saber.

**Para cada llamada del front "sin endpoint":**
1. Confirmá la ruta completa que se arma en runtime (prefijo + ruta).
2. Buscá un endpoint parecido (otro verbo, plural/singular, un segmento distinto): suele ser un typo o un renombre.
3. Fijate si hay un ticket BE abierto o una rama sin mergear que lo agregue (`git branch -r`, `gh pr list`).
4. Clasificalo:
   - 🐛 **Rota**: la ruta no existe y no hay nada en camino. Esto falla en runtime y es lo más urgente.
   - ⏳ **Esperando backend**: hay un ticket o PR BE en camino.
   - ✏️ **Desfasada**: existe un endpoint casi igual. Indicá cuál.

Si el stack está levantado, podés confirmar con un `curl -s -o /dev/null -w "%{http_code}"` contra el backend local: un 404 confirma que la ruta no existe (un 401 o 403 significa que sí existe).

## Output

1. Resumen: N endpoints, X usados, cuántos de forma indirecta, Y sin uso; M llamadas, Z sin endpoint.
2. **🐛 Llamadas rotas** primero, con la ruta, el `archivo:línea` del front y el endpoint más parecido.
3. Tabla de **endpoints sin uso**: método, ruta, `archivo:línea`, clasificación, ticket y acción sugerida.
4. Tabla de **llamadas sin endpoint** con lo mismo.
5. Limitaciones: qué no pudo analizar el script y qué se verificó a mano.

Ver `example-output.md` para una corrida real sobre Study Arena.

## Qué no hacer

- No borres endpoints ni cambies rutas: proponé el cambio y que lo decida el equipo (idealmente en un ticket).
- No reportes como muerto algo que no verificaste a mano.
- No dejes el script ni los JSON dentro del repo.

## Ejemplo de uso

**Pedido:** Antes de la entrega, fijate si quedaron endpoints del back sin usar o llamadas del front que no existen.

**Resultado:** Corre `scan_endpoints.py` sobre el back y el front y verifica cada candidato con `rg`, `git log -S` y Jira. Reporta, por ejemplo, una llamada rota a `/ranking/weekly` (el endpoint real es `/api/rankings/weekly`), dos endpoints pendientes de integrar con su ticket FE y uno muerto candidato a borrar, todos con su archivo:línea.
