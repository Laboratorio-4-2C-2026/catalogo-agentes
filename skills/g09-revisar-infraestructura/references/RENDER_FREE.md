# Render Free ahora, Terraform después

Este runbook crea `zervi-backend-dev` como Web Service gratuito desde una imagen Docker pública utilizando Render CLI. El servicio permanecerá temporalmente fuera del estado Terraform y se importará cuando una versión estable de `render-oss/render` acepte `plan = "free"`.

No requiere GitHub App, repositorio conectado, auto-deploy por commits ni credenciales de un registry privado.

> No ejecutar todavía `terraform import` con `render-oss/render` 1.8.0. Esa versión rechaza `free` en la configuración y no puede administrar correctamente el servicio gratuito.

## 1. Requisitos

- Render CLI actualizado. Consultar la [instalación oficial](https://render.com/docs/cli).
- La API key de Render en `RENDER_API_KEY`.
- Una imagen Docker pública y versionada del backend.
- Una región válida de Render.
- Los datos de conexión de Neon.
- El backend preparado para escuchar en `PORT` y consumir las variables de entorno declaradas abajo.

Comprobar la CLI:

```bash
render version
render help services create
```

Nunca usar `latest`. La futura imagen de Zervi debería tener una referencia inmutable como:

```text
ghcr.io/ORGANIZACION/zervi-backend:COMMIT_SHA
```

Si todavía se usa una imagen pública de prueba, recordar que solo valida Render: no valida el backend Zervi ni su conexión a Neon.

## 2. Autenticación y workspace

Exportar la API key solamente en la terminal actual:

```bash
export RENDER_API_KEY="..."
```

Confirmar la identidad y seleccionar el workspace correcto:

```bash
render whoami
render workspaces --output text
render workspace set
render workspace current
```

## 3. Preparar variables locales

Definir los valores en la terminal. La shell guardará en el historial los nombres de las variables, no los valores que se expandan posteriormente:

```bash
export ZERVI_RENDER_REGION="REGION_VERIFICADA"
export ZERVI_DOCKER_IMAGE="ghcr.io/ORGANIZACION/zervi-backend:COMMIT_SHA"
export ZERVI_DATABASE_URL="jdbc:postgresql://HOST/zervi?sslmode=require"
export ZERVI_DATABASE_USERNAME="zervi_app"
export ZERVI_DATABASE_PASSWORD="..."
export ZERVI_CORS_ALLOWED_ORIGINS="https://zervi-frontend-dev.pages.dev"
```

Las variables exportadas pueden ser visibles para procesos del mismo usuario mientras estén activas. Cerrar la terminal o ejecutar los `unset` indicados al final cuando se termine.

## 4. Revisar antes de crear

Confirmar:

- `ZERVI_DOCKER_IMAGE` es pública y tiene tag inmutable.
- La imagen es compatible con `linux/amd64`.
- La aplicación escucha en `0.0.0.0` usando `PORT`.
- `/actuator/health` responde HTTP 200 sin autenticación.
- La URL JDBC incluye `sslmode=require`.
- El origen CORS coincide exactamente con la URL real de Cloudflare Pages.
- El workspace seleccionado es el correcto.
- El plan indicado será `free`.

La configuración Spring actual de Zervi todavía contiene valores locales fijos. Antes de usar la imagen real hay que adaptarla para consumir `DATABASE_URL`, `DATABASE_USERNAME`, `DATABASE_PASSWORD`, `CORS_ALLOWED_ORIGINS` y `PORT`.

## 5. Crear el Web Service gratuito

Este comando crea un recurso real. Ejecutarlo únicamente después de revisar todos los valores:

```bash
render services create \
  --name zervi-backend-dev \
  --type web_service \
  --runtime image \
  --image "${ZERVI_DOCKER_IMAGE}" \
  --region "${ZERVI_RENDER_REGION}" \
  --plan free \
  --health-check-path /actuator/health \
  --env-var PORT=10000 \
  --env-var SPRING_PROFILES_ACTIVE=development \
  --env-var "DATABASE_URL=${ZERVI_DATABASE_URL}" \
  --env-var "DATABASE_USERNAME=${ZERVI_DATABASE_USERNAME}" \
  --env-var "DATABASE_PASSWORD=${ZERVI_DATABASE_PASSWORD}" \
  --env-var "CORS_ALLOWED_ORIGINS=${ZERVI_CORS_ALLOWED_ORIGINS}" \
  --output json
```

La salida debe contener el ID `srv-...` y la URL `https://...onrender.com`. Guardar el ID en un lugar seguro; no es secreto, pero será necesario para la importación.

Una imagen preconstruida no tiene auto-deploy por commits. Para actualizarla se deberá cambiar manualmente la referencia de imagen o disparar el flujo correspondiente con Render CLI.

## 6. Verificar el servicio

Listar el servicio y observar sus logs:

```bash
render services --output text
render logs --resources srv-IDENTIFICADOR --tail
```

Desde otra terminal, verificar el health check:

```bash
curl --fail-with-body \
  "https://zervi-backend-dev.onrender.com/actuator/health"
```

Las instancias gratuitas se suspenden después de un período sin tráfico. La primera respuesta después de la suspensión puede tardar aproximadamente un minuto.

## 7. Conectar Cloudflare Pages

Cuando la URL de Render funcione, configurar Terraform:

```bash
cd infrastructure
export TF_VAR_frontend_api_url="https://zervi-backend-dev.onrender.com"
export TF_VAR_cors_allowed_origins="https://zervi-frontend-dev.pages.dev"
terraform plan
```

Para Direct Upload, `VITE_API_URL` debe estar presente durante el build local:

```bash
cd ../frontend
VITE_API_URL="https://zervi-backend-dev.onrender.com" npm run build
npx wrangler pages deploy dist --project-name zervi-frontend-dev
```

Wrangler no es ejecutado por Terraform. Todas las variables `VITE_*` quedan públicas en el frontend compilado.

## 8. Mantener Render fuera de Terraform por ahora

Conservar:

```hcl
enable_render = false
```

Terraform puede seguir administrando Neon y Cloudflare. No declarar el servicio gratuito como `starter`, no usar `ignore_changes` para ocultar el plan y no importarlo con la versión 1.8.0.

Los cambios manuales realizados con Render CLI no serán detectados por Terraform mientras el servicio permanezca fuera de su estado.

## 9. Comprobar soporte futuro del provider

Antes de actualizar, consultar el esquema publicado de `render_web_service`. `free` debe aparecer explícitamente entre los valores aceptados de `plan`.

Actualizar de forma controlada:

```bash
cd infrastructure
terraform init -upgrade
terraform providers
terraform validate
```

Revisar los cambios de `.terraform.lock.hcl`. No continuar si el esquema todavía rechaza:

```hcl
plan = "free"
```

Cuando haya soporte, actualizar la restricción de versión en `versions.tf` y la validación del módulo Render para incluir `free`. Después ejecutar nuevamente:

```bash
terraform init
terraform fmt -recursive
terraform validate
```

## 10. Importar el servicio existente

Configurar los valores para que Terraform describa exactamente el servicio existente:

```bash
export TF_VAR_enable_render=true
export TF_VAR_render_owner_id="OWNER_ID"
export TF_VAR_render_region="REGION_USADA_AL_CREAR"
export TF_VAR_render_plan="free"
export TF_VAR_docker_image_url="ghcr.io/ORGANIZACION/zervi-backend:COMMIT_SHA"
export TF_VAR_database_url="jdbc:postgresql://HOST/zervi?sslmode=require"
export TF_VAR_database_username="zervi_app"
export TF_VAR_database_password="..."
export TF_VAR_cors_allowed_origins="https://zervi-frontend-dev.pages.dev"
```

Primero ejecutar un plan. Debe mostrar la intención de crear una dirección Terraform, porque todavía no fue importada:

```bash
terraform plan
```

Importar usando el ID guardado:

```bash
terraform import \
  'module.render[0].render_web_service.this' \
  'srv-IDENTIFICADOR'
```

Luego ejecutar:

```bash
terraform plan
```

No ejecutar `apply` hasta que el plan posterior a la importación sea revisado. Idealmente debe indicar `No changes`. Si propone reemplazar el servicio, cambiar el plan, eliminar variables o modificar la imagen inesperadamente, detenerse y reconciliar la configuración antes de continuar.

## 11. Limpiar variables de la terminal

Al terminar:

```bash
unset RENDER_API_KEY
unset ZERVI_RENDER_REGION
unset ZERVI_DOCKER_IMAGE
unset ZERVI_DATABASE_URL
unset ZERVI_DATABASE_USERNAME
unset ZERVI_DATABASE_PASSWORD
unset ZERVI_CORS_ALLOWED_ORIGINS
unset TF_VAR_database_url
unset TF_VAR_database_username
unset TF_VAR_database_password
```

## Límites del plan gratuito

Antes de crear el servicio, revisar la [documentación vigente del plan gratuito](https://render.com/docs/free). Entre sus límites actuales:

- suspensión por inactividad;
- 750 horas gratuitas mensuales compartidas por workspace;
- filesystem efímero;
- sin disco persistente;
- límites de ancho de banda y uso saliente;
- posible suspensión o facturación por excedentes, según la configuración de pago del workspace.

No usar una instancia gratuita para producción ni asumir que sus condiciones permanecerán sin cambios.
