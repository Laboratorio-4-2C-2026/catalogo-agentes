# Runbook obligatorio de deploy desde `main`

**Proyecto:** Zervi  
**Ambiente:** development  
**Política:** sólo se despliega el `HEAD` remoto de `main`  
**Actualizado:** 2026-09-20

## Instrucción para personas y agentes

Antes de responder consultas o ejecutar tareas relacionadas con deploy, infraestructura, Neon, Render o Cloudflare, leer este archivo completo.

Este documento es la fuente operativa canónica. No recorrer ni buscar información por todo el workspace al comenzar. Consultar archivos adicionales solamente cuando una validación de este runbook falle, cuando haya que revisar código cambiado o cuando el usuario lo pida expresamente.

Este archivo debe quedar versionado en `main`. Mientras permanezca sin commitear, la comprobación obligatoria de worktree limpio bloqueará correctamente cualquier nuevo deploy.

Los documentos `DEPLOY_MAIN_AUDIT.md` e `infrastructure-updated/DEPLOY_HANDOFF.md` describen estados históricos y no deben usarse como estado actual.

## Regla innegociable de rama

Un deploy queda **prohibido** si no se cumplen simultáneamente estas condiciones:

1. La rama local activa es `main`.
2. `HEAD` coincide exactamente con `origin/main`.
3. El SHA elegido coincide con el `main` remoto de GitHub.
4. El worktree está limpio.
5. Render está configurado con `branch=main`.
6. Cloudflare Pages está configurado con `production_branch=main`.
7. Backend, frontend, infraestructura y verificaciones públicas pasan antes de publicar.

No desplegar desde `dev`, una feature branch, un SHA local no publicado, un merge pendiente ni un directorio con cambios sin commitear.

No usar `--branch dev`, `--branch development` ni otro nombre al publicar Pages. No cambiar Render a otra rama.

## Contexto completo del ambiente

### Rutas locales

| Contenido | Ruta |
| --- | --- |
| Workspace | `/home/xoaquin-sanchez-varsallona/Documentos/projects/zervi` |
| Repositorio de aplicación | `/home/xoaquin-sanchez-varsallona/Documentos/projects/zervi/Zervi` |
| Backend | `/home/xoaquin-sanchez-varsallona/Documentos/projects/zervi/Zervi/backend` |
| Frontend | `/home/xoaquin-sanchez-varsallona/Documentos/projects/zervi/Zervi/frontend` |
| Terraform | `/home/xoaquin-sanchez-varsallona/Documentos/projects/zervi/infrastructure-updated` |
| Credenciales locales | `infrastructure-updated/.env.local` |
| Variables Terraform locales | `infrastructure-updated/terraform.tfvars` |
| Informe de estado | `Zervi/docs/ESTADO_NEON_RENDER_CLOUDFLARE_2026-09-20.md` |
| Este runbook | `Zervi/docs/RUNBOOK_DEPLOY_MAIN.md` |

`infrastructure-updated/.env.local`, `terraform.tfvars` y `terraform.tfstate` contienen o pueden contener información sensible. No imprimirlos, copiarlos a tickets ni versionarlos.

### Repositorio

- GitHub: `https://github.com/Agustin5421/Zervi`.
- Rama autorizada para deploy: `main`.
- El SHA vigente al escribir este documento es `a244e2f3b454b7f12e22acaa0f273f2367771a8c`.
- Ese SHA es solamente una fotografía. En cada deploy se debe resolver nuevamente `origin/main`; nunca reutilizar el SHA de este documento sin verificarlo.

### Neon

- Proyecto: `zervi-development`.
- Project ID: `green-resonance-67644685`.
- Región: `aws-sa-east-1`.
- PostgreSQL: 17.
- Branch: `main`.
- Branch ID: `br-fragrant-mode-acizk0fs`.
- Endpoint ID: `ep-cool-base-acy7e0um`.
- Base: `zervi`.
- Rol de aplicación: `zervi_app`.
- Terraform administra el proyecto.
- Estado Flyway vigente: V1-V8 aplicadas correctamente.
- La próxima migración válida debe ser V9 o superior.

Historial esperado:

| Versión | Descripción |
| --- | --- |
| 1 | create users |
| 2 | create provider profiles |
| 3 | create services |
| 4 | add avatar object key |
| 5 | add services status created at index |
| 6 | add user avatar url |
| 7 | add service images |
| 8 | enable unaccent |

Reglas de migración:

- Nunca editar, renumerar, borrar ni reutilizar V1-V8.
- Nunca ejecutar `flyway repair` para ocultar una diferencia.
- Nunca borrar `flyway_schema_history` ni resetear el esquema como parte de un deploy normal.
- Toda modificación futura del esquema debe agregarse como una migración nueva y forward-only.
- Si Flyway detecta un checksum distinto, abortar el deploy y diagnosticar antes de tocar Neon.

### Render

- Servicio: `zervi-backend-dev`.
- Service ID: `srv-dalhl6v40ujc73e2p530`.
- URL: `https://zervi-backend-dev.onrender.com`.
- Repositorio: `https://github.com/Agustin5421/Zervi`.
- Rama requerida: `main`.
- Root directory: `backend`.
- Runtime: Docker.
- Dockerfile: `backend/Dockerfile`.
- Plan: Free.
- Región: Virginia.
- Health check: `/actuator/health`.
- Auto-deploy: desactivado.
- Render no está en el state Terraform porque el provider fijado no soporta el plan Free.
- Último deploy confirmado al escribir este archivo: `dep-dao743uk1f9s73au0j3g`, commit `a244e2f...`, estado `live`.

Familias de variables configuradas en Render:

- `PORT`, `SERVER_PORT`.
- `SPRING_PROFILES_ACTIVE`, `SPRING_DOCKER_COMPOSE_ENABLED`.
- `SPRING_DATASOURCE_URL`, `SPRING_DATASOURCE_USERNAME`, `SPRING_DATASOURCE_PASSWORD`.
- `AUTH0_ISSUER_URI`, `AUTH0_AUDIENCE`.
- `CORS_ALLOWED_ORIGINS`.
- `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET_NAME`, `R2_PUBLIC_BASE_URL`, `R2_ENDPOINT`, `R2_AVATAR_MAX_SIZE`.

Nunca imprimir los valores sensibles ni reemplazar la lista completa de variables si solamente se necesita cambiar una configuración.

### Cloudflare Pages

- Proyecto: `zervi-frontend-dev`.
- URL estable: `https://zervi-frontend-dev.pages.dev`.
- Rama de producción requerida: `main`.
- Modalidad: Direct Upload con Wrangler, sin integración Git.
- Terraform administra el contenedor del proyecto y su `production_branch`.
- El contenido se publica manualmente con Wrangler.
- Deployment confirmado al escribir este archivo: `b0eb8afb-1084-4ec2-863b-3a8e4fd1d613`.
- URL inmutable de ese deployment: `https://b0eb8afb.zervi-frontend-dev.pages.dev`.
- No hay dominio personalizado.

Variables públicas necesarias para construir el frontend:

```text
VITE_API_URL=https://zervi-backend-dev.onrender.com
VITE_AUTH0_DOMAIN=zervi.us.auth0.com
VITE_AUTH0_CLIENT_ID=rkbBpDZZd43V2seDY9lbPE2IZ7EdJx9D
VITE_AUTH0_AUDIENCE=https://api.zervi.local
```

Son valores públicos de una SPA. Nunca agregar `AUTH0_CLIENT_SECRET` al frontend.

### Cloudflare R2

- Bucket: `zervi-development-images`.
- Administrado por Terraform.
- Usado por el backend mediante la API compatible con S3.
- Guarda avatares e imágenes de servicios.
- Las credenciales viven en `.env.local` y en Render; no se incluyen aquí.

### Auth0 y CORS

- Issuer: `https://zervi.us.auth0.com/`.
- Audience: `https://api.zervi.local`.
- Origen web permitido: `https://zervi-frontend-dev.pages.dev`.
- El backend usa JWT Bearer; no usa cookies para autenticación.

## Credenciales requeridas

El archivo `infrastructure-updated/.env.local` debe contener, sin imprimir valores:

```text
NEON_API_KEY
RENDER_API_KEY
TF_VAR_render_owner_id
CLOUDFLARE_API_TOKEN
TF_VAR_cloudflare_account_id
R2_ACCOUNT_ID
R2_ACCESS_KEY_ID
R2_SECRET_ACCESS_KEY
R2_BUCKET_NAME
R2_PUBLIC_BASE_URL
R2_ENDPOINT
R2_AVATAR_MAX_SIZE
```

Comprobar presencia sin mostrar valores:

```bash
cd /home/xoaquin-sanchez-varsallona/Documentos/projects/zervi/infrastructure-updated
set -a
source .env.local
set +a

test -n "${NEON_API_KEY:-}"
test -n "${RENDER_API_KEY:-}"
test -n "${CLOUDFLARE_API_TOKEN:-}"
test -n "${TF_VAR_cloudflare_account_id:-}"
```

## Fase 1: bloqueo obligatorio a `main`

Ejecutar desde el repositorio de aplicación:

```bash
cd /home/xoaquin-sanchez-varsallona/Documentos/projects/zervi/Zervi
git fetch origin main

CURRENT_BRANCH="$(git branch --show-current)"
LOCAL_SHA="$(git rev-parse HEAD)"
REMOTE_MAIN_SHA="$(git rev-parse origin/main)"
REMOTE_ADVERTISED_SHA="$(git ls-remote origin refs/heads/main | awk '{print $1}')"

test "$CURRENT_BRANCH" = "main"
test "$LOCAL_SHA" = "$REMOTE_MAIN_SHA"
test "$LOCAL_SHA" = "$REMOTE_ADVERTISED_SHA"
test -z "$(git status --porcelain --untracked-files=all)"
```

Si cualquier `test` falla, **abortar**. No construir ni desplegar.

Para actualizar una rama local atrasada:

```bash
git switch main
git pull --ff-only origin main
```

No hacer merge, rebase, commit, stash ni descarte automático durante el proceso de deploy. Si hay cambios locales, pedir decisión al usuario.

Guardar el SHA validado para todos los pasos posteriores:

```bash
MAIN_SHA="$(git rev-parse HEAD)"
```

El mismo `MAIN_SHA` debe aparecer finalmente en Render y en el deployment de Pages.

## Fase 2: verificar configuración remota antes de probar

### Render debe apuntar a `main`

```bash
cd /home/xoaquin-sanchez-varsallona/Documentos/projects/zervi/infrastructure-updated
set -a
source .env.local
set +a

curl -fsS \
  -H "Authorization: Bearer ${RENDER_API_KEY}" \
  -H "Accept: application/json" \
  "https://api.render.com/v1/services/srv-dalhl6v40ujc73e2p530" \
  | jq '{id,name,branch,repo,rootDir,autoDeploy,suspended}'
```

Abortar si `branch` no es `main`, el repositorio no es el esperado o el root no es `backend`.

### Pages debe tener producción en `main`

```bash
curl -fsS \
  -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
  "https://api.cloudflare.com/client/v4/accounts/${TF_VAR_cloudflare_account_id}/pages/projects/zervi-frontend-dev" \
  | jq '.result | {name,production_branch,latest_deployment}'
```

Abortar si `production_branch` no es `main`.

### Terraform no debe proponer cambios inesperados

```bash
cd /home/xoaquin-sanchez-varsallona/Documentos/projects/zervi/infrastructure-updated
terraform plan -detailed-exitcode -no-color
```

- Exit 0: continuar.
- Exit 2: revisar el plan completo. Continuar solamente si el cambio es esperado y autorizado.
- Exit 1: abortar.

Nunca ejecutar `terraform apply` como efecto secundario de una consulta. Requiere un plan revisado y autorización explícita.

## Fase 3: validar todo antes del deploy

### Backend

```bash
cd /home/xoaquin-sanchez-varsallona/Documentos/projects/zervi/Zervi/backend
./gradlew clean test spotlessCheck bootJar --no-daemon
```

Debe finalizar con `BUILD SUCCESSFUL`.

Si hay migraciones nuevas:

1. Confirmar que sean V9 o superiores.
2. Confirmar que ninguna V1-V8 haya cambiado.
3. Probar una base vacía.
4. Probar una base con el historial vigente.
5. Revisar que el cambio sea compatible con rollback de aplicación o documentar que no lo es.

### Frontend

```bash
cd /home/xoaquin-sanchez-varsallona/Documentos/projects/zervi/Zervi/frontend
npm ci
npm run lint
npm test

env \
  VITE_API_URL=https://zervi-backend-dev.onrender.com \
  VITE_AUTH0_DOMAIN=zervi.us.auth0.com \
  VITE_AUTH0_CLIENT_ID=rkbBpDZZd43V2seDY9lbPE2IZ7EdJx9D \
  VITE_AUTH0_AUDIENCE=https://api.zervi.local \
  npm run build
```

Criterios:

- `npm ci` exitoso.
- Lint sin errores. Warnings conocidos deben informarse.
- Todos los tests exitosos.
- Build exitoso.
- Revisar vulnerabilidades informadas por `npm ci`; no ejecutar `npm audit fix` automáticamente.

### Salud previa del ambiente

```bash
curl -fsSL --max-time 120 \
  https://zervi-backend-dev.onrender.com/actuator/health

curl -fsSL --max-time 60 \
  https://zervi-backend-dev.onrender.com/api/categories

curl -fsSL --max-time 30 \
  https://zervi-frontend-dev.pages.dev/
```

Si el ambiente previo está caído, registrar el problema antes del deploy para no atribuirlo erróneamente al release nuevo.

## Fase 4: desplegar Render desde el SHA exacto de `main`

No desplegar solamente "el último commit" de forma implícita. Enviar `commitId=${MAIN_SHA}`.

Si Render no apunta a `main`, corregirlo antes del deploy:

```bash
curl -fsS -X PATCH \
  -H "Authorization: Bearer ${RENDER_API_KEY}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  --data '{"branch":"main","autoDeploy":"no"}' \
  "https://api.render.com/v1/services/srv-dalhl6v40ujc73e2p530"
```

Desplegar el SHA validado:

```bash
curl -fsS -X POST \
  -H "Authorization: Bearer ${RENDER_API_KEY}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  --data "{\"commitId\":\"${MAIN_SHA}\"}" \
  "https://api.render.com/v1/services/srv-dalhl6v40ujc73e2p530/deploys"
```

Notas:

- Render no permite desplegar un servicio suspendido. Reanudarlo primero si corresponde.
- No combinar `commitId` y `clearCache` en una solicitud no validada.
- Esperar hasta que el deploy quede `live`.
- Si queda `build_failed`, `update_failed`, `canceled` o no saludable, abortar Pages. No publicar un frontend que dependa de un backend fallido.

Consultar deploys:

```bash
curl -fsS \
  -H "Authorization: Bearer ${RENDER_API_KEY}" \
  -H "Accept: application/json" \
  "https://api.render.com/v1/services/srv-dalhl6v40ujc73e2p530/deploys?limit=5" \
  | jq '.[] | .deploy | {id,status,createdAt,finishedAt,commit}'
```

Antes de continuar, comprobar que el deploy `live` tenga exactamente `commit.id == MAIN_SHA`.

## Fase 5: verificar Render antes de publicar Pages

```bash
curl -fsSL --max-time 120 \
  https://zervi-backend-dev.onrender.com/actuator/health

curl -fsSL --max-time 60 \
  https://zervi-backend-dev.onrender.com/api/categories

curl -sS --max-time 60 -o /dev/null -D - -X OPTIONS \
  -H "Origin: https://zervi-frontend-dev.pages.dev" \
  -H "Access-Control-Request-Method: GET" \
  https://zervi-backend-dev.onrender.com/api/categories
```

Resultados requeridos:

- Health HTTP 200 y `status=UP`.
- Categorías HTTP 200.
- Preflight HTTP 200.
- Header `access-control-allow-origin: https://zervi-frontend-dev.pages.dev`.

### Verificar Flyway sin leer datos personales

```bash
cd /home/xoaquin-sanchez-varsallona/Documentos/projects/zervi/infrastructure-updated
NEON_URI="$(terraform output -raw neon_connection_uri)"

docker run --rm postgres:17-alpine \
  psql "$NEON_URI" -X -At -F '|' \
  -c "SELECT version, description, success FROM flyway_schema_history ORDER BY installed_rank;"
```

Abortar si alguna migración tiene `success=false`, falta una versión esperada o aparece una versión duplicada/inconsistente.

## Fase 6: publicar Cloudflare Pages desde el mismo SHA

Confirmar nuevamente antes de subir:

```bash
cd /home/xoaquin-sanchez-varsallona/Documentos/projects/zervi/Zervi
test "$(git branch --show-current)" = "main"
test "$(git rev-parse HEAD)" = "$MAIN_SHA"
test "$(git rev-parse origin/main)" = "$MAIN_SHA"
test -z "$(git status --porcelain --untracked-files=all)"
```

Publicar el `dist` ya validado:

```bash
cd /home/xoaquin-sanchez-varsallona/Documentos/projects/zervi/Zervi/frontend
set -a
source ../../infrastructure-updated/.env.local
set +a
export CLOUDFLARE_ACCOUNT_ID="${TF_VAR_cloudflare_account_id}"

npx wrangler pages deploy dist \
  --project-name zervi-frontend-dev \
  --branch main \
  --commit-hash "$MAIN_SHA" \
  --commit-message "Deploy main ${MAIN_SHA}"
```

La opción `--branch main` es obligatoria. Si Wrangler informa que el worktree está sucio, abortar y resolverlo; no usar `--commit-dirty=true` en un deploy normal.

## Fase 7: verificación posterior obligatoria

### Pages

```bash
curl -fsS \
  -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
  "https://api.cloudflare.com/client/v4/accounts/${TF_VAR_cloudflare_account_id}/pages/projects/zervi-frontend-dev" \
  | jq '.result | {
      name,
      production_branch,
      latest_deployment,
      canonical_deployment
    }'

curl -fsSL --max-time 30 \
  https://zervi-frontend-dev.pages.dev/
```

Confirmar:

- `production_branch == main`.
- El deployment nuevo tiene `environment=production` y `status=success`.
- Es el deployment canónico.
- La URL estable responde HTTP 200.
- El HTML referencia el asset generado en el build actual.

### Integración completa

Repetir:

- Health del backend.
- Endpoint público.
- Preflight CORS.
- Historial Flyway.
- `terraform plan` sin cambios.

Cuando sea posible, probar manualmente:

- login/logout Auth0;
- búsqueda de servicios;
- alta/edición de perfil;
- carga de avatar a R2;
- publicación de servicio;
- carga de imagen de servicio.

## Criterios de aborto

Abortar inmediatamente si ocurre cualquiera de estos casos:

- rama distinta de `main`;
- `HEAD`, `origin/main` y GitHub no coinciden;
- worktree sucio;
- tests, lint, formato o build fallan;
- migración histórica modificada;
- Terraform propone destrucciones o cambios no esperados;
- Render no apunta a `main`;
- Pages no apunta a `main`;
- deploy de Render no termina `live`;
- commit live de Render no coincide con `MAIN_SHA`;
- health, endpoint público o CORS fallan;
- Flyway reporta error o inconsistencia;
- Pages genera un preview en lugar de producción;
- el deployment canónico de Pages no es el nuevo;
- falta una credencial o se requiere imprimir un secreto para continuar.

No intentar "arreglar rápido" con `flyway repair`, reset de base, cambio de rama, `git reset --hard`, descarte de archivos, `npm audit fix`, `terraform apply` no revisado ni rotación de credenciales. Detenerse y consultar al usuario.

## Rollback

Un rollback requiere autorización explícita.

- Render: volver a desplegar un commit anterior conocido o usar el endpoint de rollback sobre un deploy exitoso.
- Pages: volver a construir y publicar el mismo commit que se quiera restaurar, siempre identificando el SHA.
- Neon: las migraciones son forward-only. No borrar filas de Flyway ni bajar el esquema manualmente.
- Antes de revertir aplicación, confirmar que el commit anterior sea compatible con el esquema actual.

Si una migración nueva ya fue aplicada y rompe compatibilidad hacia atrás, crear una migración correctiva hacia adelante; no restaurar ciegamente un binario viejo.

## Registro mínimo de cada deploy

Al finalizar, agregar al informe de estado o a un handoff:

```text
Fecha y zona horaria:
MAIN_SHA:
Rama local:
origin/main:
Backend tests/build:
Frontend lint/tests/build:
Terraform plan:
Render service ID:
Render deploy ID y estado:
Render commit live:
Render health:
Flyway versión final:
Pages project:
Pages deployment ID y estado:
Pages production_branch:
Pages URL canónica:
CORS:
Pruebas funcionales realizadas:
Warnings o deuda pendiente:
```

## Estado base conocido al 2026-09-20

```text
main: a244e2f3b454b7f12e22acaa0f273f2367771a8c
Render branch: main
Render deploy: dep-dao743uk1f9s73au0j3g
Render status: live
Render health: UP
Neon Flyway: V1-V8 OK
Pages production_branch: main
Pages deployment: b0eb8afb-1084-4ec2-863b-3a8e4fd1d613
Pages status: success
Terraform: No changes
```

Este bloque es una referencia histórica. Cada deploy debe volver a obtener el SHA y los estados remotos; nunca asumir que siguen iguales.
