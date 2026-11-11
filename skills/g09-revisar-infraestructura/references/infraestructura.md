# Infraestructura local de Zervi

Esta carpeta prepara Infrastructure as Code para el environment `development` de Zervi:

- PostgreSQL 17 en Neon.
- Un Web Service de Render basado en una imagen Docker pública preconstruida.
- Un proyecto Cloudflare Pages preparado para Direct Upload.

Terraform se ejecuta exclusivamente desde una computadora local. No hay GitHub Actions, GitHub Apps, repositorios conectados, auto-deploy por push, Auth0, DNS, dominios personalizados ni despliegues mediante `local-exec`.

## Estado actual y límites conocidos

Los módulos están desactivados de forma predeterminada. Un `terraform plan` con las tres flags en `false` debe indicar que no hay cambios.

Limitación de inicialización: Terraform configura todos los providers requeridos antes de evaluar el `count` de los módulos. Los providers Neon 0.14.0 y Render 1.8.0 rechazan un plan si no encuentran sus credenciales, incluso cuando sus módulos están desactivados. Por eso el plan agregado necesita `NEON_API_KEY`, `RENDER_API_KEY` y `render_owner_id`; las flags siguen garantizando que no se planifiquen recursos. No se usan claves ficticias ni credenciales dentro de HCL.

El provider `render-oss/render` 1.8.0 no acepta `free` en el atributo `plan` de `render_web_service`. Su esquema admite `starter`, `standard`, `pro`, `pro_plus`, `pro_max` y `pro_ultra`, que son opciones pagas. Por seguridad, Render debe permanecer desactivado hasta que:

1. una versión estable del provider admita `free`; o
2. se elija conscientemente un plan soportado y se autorice su costo antes de ejecutar `apply`.

Render sí ofrece Web Services gratuitos en otros flujos, pero no se inventa un valor que el provider rechaza.

`kislerdm/neon` es un provider comunitario y no cuenta con soporte oficial de Neon. Neon patrocina el proyecto, pero eso no equivale a soporte oficial. La versión fijada permite solicitar PostgreSQL 17 y expone como sensibles la URI y contraseña iniciales.

Cloudflare 5.22.0 permite crear un proyecto Pages de Direct Upload omitiendo por completo `source`. No se requiere una cuenta GitHub conectada.

## Requisitos previos

- Terraform 1.14.x. El provider de Neon 0.14.0 requiere Terraform 1.14.x; el rango configurado es `>= 1.14.0, < 2.0.0`.
- Una cuenta Neon y una API key.
- Una cuenta Render, una API key y el owner/workspace ID.
- Para Cloudflare, una API token con permisos `Pages Read` y `Pages Write`, más el account ID.
- Node.js y las dependencias del frontend para un futuro Direct Upload con Wrangler.

Instalar Terraform siguiendo la [documentación oficial](https://developer.hashicorp.com/terraform/install) y comprobar:

```bash
terraform version
```

No se incluyó ni descargó un binario de Terraform dentro del repositorio.

## Credenciales

Los provider blocks no reciben API keys. Cada provider utiliza su variable de entorno estándar:

```bash
export NEON_API_KEY="..."
export RENDER_API_KEY="..."
export CLOUDFLARE_API_TOKEN="..."
```

Para el uso local, las credenciales existentes están guardadas en `.env.local`, archivo ignorado por Git y protegido con permisos de lectura/escritura únicamente para su propietario. Cargarlo en la terminal actual antes de ejecutar Terraform:

```bash
cd infrastructure
set -a
source .env.local
set +a
```

Comprobar que las variables existen sin imprimir sus valores:

```bash
test -n "${NEON_API_KEY}" && echo "NEON_API_KEY cargada"
test -n "${RENDER_API_KEY}" && echo "RENDER_API_KEY cargada"
test -n "${TF_VAR_render_owner_id}" && echo "Render owner cargado"
test -n "${TF_VAR_neon_region}" && echo "Región Neon cargada"
```

Al cerrar la terminal desaparecen del entorno, pero permanecen guardadas en `.env.local` para la siguiente sesión. Para retirarlas de una terminal abierta:

```bash
unset NEON_API_KEY RENDER_API_KEY TF_VAR_render_owner_id TF_VAR_neon_region CLOUDFLARE_API_TOKEN
```

No guardar esos valores en archivos versionados ni en `terraform.tfvars`. `.env.local`, `infra/neon.txt` e `infra/render.txt` están ignorados, pero siguen siendo texto plano local; es preferible migrarlos posteriormente a un gestor de credenciales.

Los identificadores no secretos se configuran como variables:

```bash
export TF_VAR_render_owner_id="..."
export TF_VAR_cloudflare_account_id="..."
```

Ubicación de credenciales:

- Neon: crear una API key desde la configuración de la cuenta u organización en Neon Console.
- Render: crear una API key desde Account Settings; el owner/workspace ID aparece en la configuración del workspace.
- Cloudflare: crear una API token limitada a la cuenta objetivo y a Pages Read/Write. El account ID aparece en el dashboard de la cuenta.

No hace falta otra API credential para preparar esta infraestructura. Una imagen pública de Render tampoco requiere credenciales de registry. Una futura imagen privada de GHCR o Docker Hub sí las requerirá.

## Estado local y archivos de variables

Terraform guardará el estado localmente en `infrastructure/terraform.tfstate`. Aunque los outputs estén marcados como `sensitive`, el estado puede contener URI, usuario y contraseña de Neon en texto recuperable. No compartirlo, adjuntarlo en tickets ni subirlo a Git.

Crear el archivo local a partir del ejemplo:

```bash
cd infrastructure
cp terraform.tfvars.example terraform.tfvars
```

`terraform.tfvars` está ignorado. `.terraform.lock.hcl` no está ignorado y debe versionarse después del primer `terraform init` para fijar checksums de providers.

Los valores `VALOR_A_DEFINIR` son bloqueos intencionales. Consultar valores actuales antes de habilitar un módulo:

- Neon: [regiones disponibles](https://neon.com/docs/introduction/regions).
- Render: [regiones](https://render.com/docs/regions) y el esquema fijado del [Web Service provider](https://registry.terraform.io/providers/render-oss/render/1.8.0/docs/resources/web_service).
- Cloudflare: account ID del dashboard.

## Flujo básico

Desde `infrastructure/`:

```bash
terraform init
terraform fmt -recursive
terraform fmt -recursive -check
terraform validate
terraform plan
```

Revisar siempre el plan completo antes de cualquier cambio real. Los comandos mutantes se documentan para uso manual, pero no deben ejecutarse sin autorización explícita:

```bash
terraform apply
terraform destroy
```

Para guardar un plan revisable:

```bash
terraform plan -out=zervi-development.tfplan
terraform show zervi-development.tfplan
```

Los archivos `*.tfplan` están ignorados porque pueden contener datos sensibles.

## Probar todas las plataformas desactivadas

El ejemplo ya contiene:

```hcl
enable_neon       = false
enable_render     = false
enable_cloudflare = false
```

Ejecutar:

```bash
export NEON_API_KEY="..."
export RENDER_API_KEY="..."
export TF_VAR_render_owner_id="..."
terraform init
terraform validate
terraform plan
```

El resultado esperado es `No changes` y cero recursos a crear.

Aunque no se crean recursos, Neon y Render requieren esas credenciales para configurar sus plugins. Cloudflare no necesita token mientras su módulo esté desactivado. Esta es una limitación de los providers actuales dentro de un único root Terraform.

## Probar Neon primero

Configurar una región válida y habilitar únicamente Neon:

```bash
export NEON_API_KEY="..."
export TF_VAR_enable_neon=true
export TF_VAR_neon_region="REGION_ID_VERIFICADO"
terraform plan
```

El plan debe contener solamente `module.neon[0].neon_project.this`. El proyecto incluye:

- nombre `zervi-development`;
- PostgreSQL 17;
- historial de restauración de 6 horas (`21600` segundos), el máximo del plan Free;
- branch principal `main`;
- base `zervi`;
- rol `zervi_app`;
- endpoint compute predeterminado.

El valor `neon_history_retention_seconds` queda explícito para evitar el valor predeterminado de 24 horas del provider, que la API rechaza en el plan Free. No aumentarlo por encima de `21600` mientras se use ese plan.

La conexión exige SSL y se expone como output sensible. Para recuperar manualmente un output después de un apply autorizado:

```bash
terraform output -raw neon_jdbc_connection_url
```

Este comando revela el valor solicitado en la terminal. No pegar su salida en logs ni documentación.

Una consulta GET inocua confirma la API key sin crear recursos:

```bash
curl --fail-with-body --silent --show-error \
  --header "Authorization: Bearer ${NEON_API_KEY}" \
  --header "Accept: application/json" \
  "https://console.neon.tech/api/v2/projects?limit=1"
```

Un `terraform plan` de un recurso nuevo no necesariamente autentica contra la API. La confirmación definitiva del flujo Terraform ocurre durante refresh de recursos existentes o un `apply` autorizado.

## Preparar Render desde una imagen pública

Para crear ahora un Web Service gratuito con Render CLI y dejar su importación para cuando el provider soporte `free`, seguir [RENDER_FREE.md](./RENDER_FREE.md).

Render puede probarse independientemente configurando valores sensibles mediante variables de entorno de Terraform:

```bash
export RENDER_API_KEY="..."
export TF_VAR_render_owner_id="..."
export TF_VAR_enable_render=true
export TF_VAR_render_region="REGION_VERIFICADA"
export TF_VAR_render_plan="PLAN_SOPORTADO"
export TF_VAR_docker_image_url="REGISTRY/IMAGEN:VERSION_INMUTABLE"
export TF_VAR_database_url="jdbc:postgresql://HOST/zervi?sslmode=require"
export TF_VAR_database_username="..."
export TF_VAR_database_password="..."
export TF_VAR_cors_allowed_origins="https://zervi-frontend-dev.pages.dev"
terraform plan
```

No usar `latest`. Una futura referencia recomendada para Zervi tiene esta forma:

```text
ghcr.io/ORGANIZACION/zervi-backend:COMMIT_SHA
```

No se configura GHCR ni Docker Hub automáticamente. Antes de usar una imagen de prueba, comprobar que sea pública, tenga una versión explícita, escuche en el puerto configurado y responda `200` en `/actuator/health`. Una imagen de prueba solo valida la creación y conectividad del servicio Render; no valida el backend Zervi.

El provider recibe `PORT=10000`, `SPRING_PROFILES_ACTIVE=development` y, cuando tienen valor, `DATABASE_URL`, `DATABASE_USERNAME`, `DATABASE_PASSWORD` y `CORS_ALLOWED_ORIGINS`.

El backend actual todavía usa valores locales fijos en `application.yaml`. Antes de publicar su imagen real habrá que adaptar Spring para consumir estas variables, escuchar en `${PORT}` y aplicar CORS. Esa modificación está fuera del alcance de esta etapa IaC.

La autenticación de Render puede comprobarse sin crear recursos:

```bash
curl --fail-with-body --silent --show-error \
  --header "Authorization: Bearer ${RENDER_API_KEY}" \
  --header "Accept: application/json" \
  "https://api.render.com/v1/users"
```

No ejecutar `apply` con un plan pago sin revisar costos y dar autorización explícita.

## Cloudflare Pages sin Git

Crear primero una token Pages Read/Write y obtener el account ID. Después:

```bash
export CLOUDFLARE_API_TOKEN="..."
export TF_VAR_cloudflare_account_id="..."
export TF_VAR_enable_cloudflare=true
terraform plan
```

El recurso no incluye `source`, repositorio ni integración Git. La token puede comprobarse sin crear recursos:

```bash
curl --fail-with-body --silent --show-error \
  --header "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
  "https://api.cloudflare.com/client/v4/user/tokens/verify"
```

Una vez creado el proyecto mediante un apply autorizado, Terraform administra el contenedor Pages y Wrangler administra su contenido. Desde `frontend/`, el despliegue manual futuro será:

```bash
VITE_API_URL="https://zervi-backend-dev.onrender.com" npm run build
npx wrangler pages deploy dist \
  --project-name zervi-frontend-dev \
  --branch main
```

Crear el proyecto con Terraform no publica el frontend. Después de generar `dist`, es necesario ejecutar el comando de Wrangler anterior para realizar el primer deployment y evitar que el subdominio de Pages responda con `Host Error`.

Terraform no ejecuta esos comandos. Como Vite reemplaza `VITE_*` durante el build, establecer `frontend_api_url` en Pages no modifica un `dist` ya compilado: hay que pasar el valor al `npm run build`. Todas las variables `VITE_*` son públicas y nunca deben contener contraseñas o tokens.

Para actualizar la configuración declarativa:

```bash
export TF_VAR_frontend_api_url="https://zervi-backend-dev.onrender.com"
export TF_VAR_cors_allowed_origins="https://zervi-frontend-dev.pages.dev"
terraform plan
```

Si una futura versión del provider dejara de aceptar Direct Upload sin `source`, crear el proyecto manualmente con Wrangler y luego importarlo:

```bash
npx wrangler pages project create zervi-frontend-dev --production-branch main
terraform import 'module.cloudflare[0].cloudflare_pages_project.this' 'ACCOUNT_ID/zervi-frontend-dev'
```

No ejecutar ese fallback mientras el recurso actual funcione.

## Habilitar más de una plataforma

Si Neon y Render están habilitados juntos, el módulo Render recibe automáticamente la URL JDBC, usuario y contraseña producidos por Neon. Esos valores permanecen sensibles, pero se guardarán en el estado local.

Si Render se habilita sin Neon, suministrar `database_url`, `database_username` y `database_password` mediante variables `TF_VAR_*`. No ponerlos en `terraform.tfvars`.

Cloudflare puede habilitarse sin Render dejando `frontend_api_url = ""`. Agregar la URL solamente cuando el backend tenga una URL real.

## Costos y destrucción

`terraform plan` no crea recursos. `terraform apply` sí crea recursos reales y puede generar costos o consumir cuotas gratuitas. `terraform destroy` elimina recursos administrados y puede destruir datos.

Antes de cualquiera de esos comandos:

1. revisar flags, región, plan e imagen;
2. revisar el plan completo;
3. respaldar datos relevantes;
4. confirmar precios y límites actuales en cada plataforma;
5. obtener autorización explícita.

## Problemas frecuentes

- `terraform: command not found`: instalar Terraform 1.14.x y volver a abrir la terminal.
- `401` o `403`: comprobar que la variable de entorno esté exportada en la misma shell y tenga los permisos correctos.
- Render rechaza `free`: limitación real del esquema 1.8.0; mantener el módulo desactivado.
- Render rechaza el owner: verificar que el owner/workspace ID corresponda a la API key.
- Cloudflare rechaza Pages: limitar la token a la cuenta correcta y conceder Pages Read/Write.
- Neon rechaza la región: consultar el `region_id` actual en la documentación/API, no usar el nombre visible del dashboard por intuición.
- El backend no inicia: la imagen debe consumir `PORT` y las variables de base, y `/actuator/health` debe ser accesible sin autenticación.
- El frontend apunta a una URL anterior: recompilar `dist` con el nuevo `VITE_API_URL` antes del Direct Upload.

## Evolución futura

### Estado remoto

Cuando la prueba local sea estable:

1. elegir un backend remoto con bloqueo y cifrado;
2. agregar su bloque `backend` sin credenciales embebidas;
3. ejecutar `terraform init -migrate-state` manualmente;
4. verificar que el estado local se haya migrado y conservar un backup seguro hasta confirmar.

### Imagen y automatización

Publicar el backend con una etiqueta inmutable, preferentemente el SHA del commit, y actualizar `docker_image_url`. Si el registry es privado, crear y administrar sus credenciales explícitamente en otra etapa.

GitHub Actions y las GitHub Apps de Render/Cloudflare podrán incorporarse más adelante como una etapa separada. En ese momento se definirán permisos mínimos, secretos del repositorio, construcción de imágenes, Direct Upload y políticas de aprobación. Esta configuración no presupone ni crea esas integraciones.

## Recursos no automatizados

- Instalación local de Terraform.
- Creación y rotación de API keys/tokens.
- Selección de región y cualquier plan pago.
- Publicación de la imagen Docker Zervi.
- Adaptación de Spring a las variables de runtime.
- Build y despliegue de `frontend/dist` con Wrangler.
- GitHub Apps, GitHub Actions, dominios, DNS, Auth0 y backend remoto de estado.

## Cloudflare R2 para imágenes

La infraestructura incluye un bucket R2 independiente del proyecto de Cloudflare Pages. Esto permite habilitar Pages y R2 por separado.

Configurar en `terraform.tfvars`:

```hcl
enable_r2   = true
r2_location = null
```

Con `project_name = "zervi"` y `environment = "development"`, Terraform crea:

```text
zervi-development-images
```

`r2_location = null` deja que Cloudflare elija automáticamente la ubicación. Si se quiere dar una preferencia, el provider fijado admite `apac`, `eeur`, `enam`, `weur`, `wnam` y `oc`.

El token usado mediante `CLOUDFLARE_API_TOKEN` necesita, además de los permisos de Pages si Pages está habilitado, el permiso `Workers R2 Storage Write` para administrar buckets R2.

Este Terraform crea el bucket, pero no crea credenciales S3 para la aplicación. El backend necesitará posteriormente un Access Key ID y Secret Access Key de R2, idealmente limitados a este bucket, para subir y leer objetos mediante la API compatible con S3.
