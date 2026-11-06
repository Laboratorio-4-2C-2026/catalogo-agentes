---
name: g13-validar-branch
description: Valida localmente lo que construyó el dev en su branch y deja la evidencia en la PR. En el back corre requests reales contra los endpoints nuevos o cambiados y publica los resultados. En el front saca screenshots de las pantallas tocadas (desktop y mobile) y las publica como comentario. Usalo cuando el dev pida "validá mi branch", "agregá evidencia a la PR", "sacá screenshots de lo que hice" o similar, o invoque el skill por nombre (validar-branch), en microchangas-backend o microchangas-frontend.
metadata:
  tipo: skill
  area:
  - qa
  - backend
  - frontend
  fase:
  - testing
  - revision
  tecnologias:
  - nestjs
  - react
  - playwright
  - supabase
  metodologia:
  - agnostico
  herramientas:
  - claude-code
  - codex
  - otra
  requiere:
  - github
  - playwright
  grupo: "13"
  autor:
    nombre: Pablo Pagliaricci
    github: Pagliaricci
  responsables:
  - Pagliaricci
  madurez: usado-en-proyecto
  relacionados:
  - g13-levantar-stack
  - g11-qa-con-capturas
  - g15-functional-uat-executor
---

# Validar la branch y dejar evidencia en la PR

Objetivo: antes de pedir review, que la PR muestre **que lo construido funciona**.
En el back, resultados de endpoints. En el front, screenshots de las pantallas.

Los scripts están en `scripts/`, junto a este archivo. `<dir del skill>` es la
carpeta de este `SKILL.md`; usá su ruta absoluta. Corré cada uno desde la raíz
del repo que indica. Usan código del skill `levantar-stack`, que tiene que
estar instalado en la misma carpeta de skills.

## Reglas

- **No modifiques código ni commitees en la branch del dev.** Este skill
  valida y reporta. Si encontrás un bug, reportalo. Arreglalo solo si el dev
  te lo pide.
- **Pedí confirmación antes de publicar** en la PR, mostrando el resumen.
- **Sin secretos en la PR:** nada de tokens, contraseñas ni contenido de
  `.env*`. `api.mjs` ya oculta los campos sensibles, pero revisá lo que vas a
  publicar.
- Todo es local: la API en `localhost:3000` y el front en `localhost:5173`,
  contra el Supabase local.
- Comandos multiplataforma (`node`, `pnpm`, `git`, `gh`). Varios devs usan
  Windows.
- **Permisos:** varios pasos necesitan red, Docker o escribir fuera del repo
  (`gh`, `git push` de las evidencias, descargar Playwright, abrir Chromium). Si
  tu herramienta corre en un sandbox, pedile al dev que apruebe esos comandos.
  Si no se pueden aprobar, dale el comando exacto para que lo corra él en su
  terminal, y seguí cuando te confirme.
- Los archivos de trabajo (casos, screenshots, borradores) van a una carpeta
  temporal del sistema, fuera de los repos:
  `node -e "console.log(require('os').tmpdir())"` + `/microchangas-validacion/<branch>`.

## 1. Prerrequisitos

- Stack arriba: `http://localhost:3000/identity/health` responde `ok` y
  `http://localhost:5173` responde. Si no, seguí primero el skill
  `levantar-stack` y volvé. Tiene que estar levantado **en esta branch**.
- `gh auth status` está OK, porque se necesita para leer y comentar la PR. Si
  no, pedile al dev que corra `gh auth login`.

## 2. Entender qué se construyó

En cada repo (front y back, carpetas hermanas):

1. Branch actual, `git fetch origin` y el diff contra dev:
   `git diff --stat origin/dev...HEAD` y después el diff completo de lo
   relevante.
2. Si hay **cambios sin commitear**, avisale: la evidencia va a mostrar algo
   que la PR todavía no tiene. Preguntale si sigue igual o si commitea
   primero.
3. La PR de la branch: `gh pr view --json number,url,title,body,baseRefName`.
   Si no hay PR, seguí igual. Al final guardás el reporte y le explicás cómo
   publicarlo.
4. **Criterios de aceptación:** buscalos en el body de la PR. El ticket
   (`MIC-123`) suele estar en el nombre de la branch o en el título. Si no
   aparecen, pedíselos al dev en una sola pregunta, o seguí validando contra
   el diff y avisá que no hubo criterios.

Mostrale en 3 a 6 líneas qué vas a validar: endpoints y pantallas, y contra
qué criterios. Después seguí.

## 3. Back: endpoints

Si el back no tiene cambios contra dev, salteá esta sección.

1. Del diff, sacá los endpoints nuevos o modificados: controllers, DTOs,
   guards, y services que cambian una respuesta. La forma exacta de los
   requests está en Swagger: `http://localhost:3000/api-docs-json`.
2. Armá `casos.json` (formato en la cabecera de `scripts/api.mjs`). Por
   endpoint, según aplique:
   - **Caso feliz** con el rol correcto, y verificá que el cuerpo tenga lo
     que pide el criterio, no solo el status.
   - **Validación**: body inválido o incompleto → 400.
   - **Sin token** → 401.
   - **Rol equivocado** → 403, si el endpoint restringe roles.
   - **Recurso ajeno**, si aplica: un `worker2` no puede tocar lo del
     `worker`.
   - Para encadenar (crear y después leer), usá `guardar` y `{variable}`.
   Usuarios: `worker`, `worker2`, `client`, `client2`, `anonimo`. El seed deja
   datos para que `worker` tenga dashboard.
3. Desde la raíz del back: `node <dir del skill>/scripts/api.mjs <casos.json>`.
4. Si un caso falla, distinguí: ¿está mal el caso (body, ruta, expectativa)
   o el código? Corregí el caso y repetí. Si el problema es del código, queda
   como ❌ con una línea de diagnóstico, mirando el log del back.

## 4. Front: screenshots

Si el front no tiene cambios contra dev, salteá esta sección.

1. Del diff, sacá las pantallas afectadas y mapealas a rutas con
   `src/routes/index.tsx`. Si un componente compartido cambió, buscá dónde se
   usa. El rol para cada ruta sale de `allowedRoles` en `ProtectedRoute`.
2. Armá `tomas.json` (formato en la cabecera de `scripts/screenshots.mjs`).
   Incluí el estado principal y los estados que construyó el dev: error de
   validación, vacío, modal abierto, éxito. Usá `pasos` para llegar a cada
   uno. Nombres cortos y descriptivos (`nueva-changa-validacion`).
3. Desde la raíz del front:
   `node <dir del skill>/scripts/screenshots.mjs <tomas.json> <carpeta>`.
   La primera vez instala Playwright y Chromium (~150 MB): avisale.
4. **Mirá cada imagen** antes de publicarla. Revisá que muestre lo esperado y
   no una pantalla en blanco, un error, un spinner o un redirect al login. Si
   sale mal, ajustá la toma (pasos, esperas, rol) y repetí. Anotá los
   problemas visuales que veas, como cortes en mobile o textos desbordados.

## 5. Armar los comentarios

Un comentario por PR, en español, corto. Empezá con:

```
### ✅ Validación local · `<branch>` @ `<sha corto>`
<N de M casos OK> · validado con el skill validar-branch contra el stack local (Supabase local + datos demo)
```

Usá ❌ en el título si algo falló.

**Back:** una tabla `Caso | Como | Request | Esperado | Obtenido | ` con ✅/❌
por fila. Después, criterio por criterio, cuál lo cubre. Las respuestas van en
`<details>` y solo de los casos que aporten, nunca todas.

**Front:** por pantalla, una línea que diga qué muestra y qué criterio cubre.
Después, desktop y mobile lado a lado:

```
| Desktop | Mobile |
|---|---|
| <img src="URL_DESKTOP" width="560"> | <img src="URL_MOBILE" width="220"> |
```

Cerrá con los problemas encontrados, si hubo. Si el feature toca los dos
repos, linkeá una PR desde la otra.

## 6. Publicar (con confirmación)

1. Mostrale al dev el resumen: cuántos casos OK, cuántas pantallas y los
   problemas. Preguntale si lo publicás en la PR #N.
2. Screenshots: desde la raíz del front,
   `node <dir del skill>/scripts/subir-evidencias.mjs <png> [<png> ...]`.
   Sube las imágenes a la branch `evidencias` del repo (huérfana: nunca se
   mergea y no dispara deploys ni workflows) y devuelve una URL por archivo.
   Reemplazá las URLs en el comentario.
3. Escribí el comentario en un archivo y publicalo:
   `gh pr comment <N> --body-file <archivo>`, en cada repo que corresponda.
4. Si no hay PR: dejá el reporte en la carpeta temporal y decile la ruta.
   Cuando abra la PR a `dev`, puede pedirte que lo publiques.

## 7. Resumen final

En la terminal, corto: qué pasó y qué falló, los links a los comentarios
publicados, y qué tendría que resolver antes de pedir review.

## Ejemplo de uso

**Pedido:** Validá mi branch y dejá la evidencia en la PR.

**Resultado:** En el back corre requests reales contra los endpoints nuevos o cambiados (caso feliz, 400, 401, 403 y recurso ajeno) y arma una tabla de resultados; en el front saca screenshots desktop y mobile de las pantallas tocadas. Con tu confirmación lo publica como comentario en la PR.
