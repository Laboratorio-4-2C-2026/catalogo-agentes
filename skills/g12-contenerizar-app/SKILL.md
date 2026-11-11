---
name: g12-contenerizar-app
description: Conteneriza las apps de un repo (una sola app o monorepo con varias, p. ej. front y back) y arma el pipeline de GitHub Actions que construye cada imagen y la publica en GHCR. Usar al pedir "dockerizá/contenerizá esto", "armá las imágenes", "publicá en GHCR" o antes de desplegar en un host de contenedores (Azure Container Apps, App Service, Cloud Run, etc.).
owner: '@lucasmonteverdi1'
role: tl
created: '2026-09-25'
metadata:
  tipo: skill
  area:
  - devops
  fase:
  - despliegue
  tecnologias:
  - docker
  - github-actions
  metodologia:
  - scrum
  herramientas:
  - claude-code
  - codex
  requiere:
  - github
  grupo: '12'
  autor:
    nombre: Lucas Monteverdi
    github: lucasmonteverdi1
  responsables:
  - lucasmonteverdi1
  madurez: usado-en-proyecto
  relacionados:
  - g12-preparar-deploy
---

# Contenerizar una app y publicarla en GHCR

Esta skill corre **en el repo de aplicación**, no en `splitit-agents`. No asume
lenguaje, framework ni estructura: todo sale de lo que haya en el repo.

Entrega, por cada app: un `Dockerfile` + `.dockerignore` que buildean y corren,
y un job de CI que publica la imagen en `ghcr.io`. **No despliega**: el deploy
(Azure, etc.) consume la imagen publicada y queda fuera de esta skill.

## Invocación

```
/contenerizar-app                 detecta las apps del repo
/contenerizar-app web api         solo esas carpetas
/contenerizar-app --dry-run       solo el plan (paso 2), no escribe nada
```

## Procedimiento

### 1. Detectar las apps

Una **app** es una carpeta con un manifiesto de build desplegable:
`package.json` (con script `start` o framework server: Next, Nest, Express…),
`build.gradle(.kts)`, `pom.xml`, `go.mod`, `pyproject.toml`/`requirements.txt`,
`Cargo.toml`, `*.csproj`. Buscar en la raíz y hasta 2 niveles
(`apps/*`, `services/*`, `packages/*`, `web/`, `api/`…), ignorando
`node_modules`, `build`, `dist`, `.next`, `target`.

- **Microservicio**: una sola app, en la raíz. Imagen `ghcr.io/<owner>/<repo>`.
- **Monorepo**: varias apps en subcarpetas. Imagen `ghcr.io/<owner>/<repo>/<app>`,
  con `<app>` = nombre de la carpeta.
- **Workspace JS** (lockfile y `workspaces`/`pnpm-workspace.yaml` en la raíz):
  el build context es la **raíz**, no la carpeta de la app, porque las deps se
  resuelven desde ahí. Con Turborepo usar `turbo prune <app> --docker`.

Descartar librerías sin entrypoint (paquetes que solo exportan código) y apps
que no son servidores (CLIs, scripts). Si hay dudas sobre qué es desplegable,
preguntar.

Por cada app anotar: stack, gestor de paquetes (según el lockfile), comando de
build, comando de arranque, puerto, variables que se necesitan **en build**
(p. ej. `NEXT_PUBLIC_*`, `VITE_*`: se hornean en el bundle) y en **runtime**.
Sacarlas de `.env.example`, `docker-compose.yml`, `application*.yml`, el código.

### 2. Plan

Mostrar una tabla antes de escribir:

| App | Carpeta | Stack | Dockerfile | Imagen | Build args | Puerto |
|---|---|---|---|---|---|---|

Columna Dockerfile: `existente` / `nuevo` / `ajustar (<motivo>)`. Con
`--dry-run`, terminar acá.

### 3. Dockerfile por app

**Si ya existe un `Dockerfile`, no reescribirlo.** Revisarlo contra la lista
de abajo y ajustar solo lo que falle. Otros Dockerfiles con sufijo
(`Dockerfile.vercel`, `Dockerfile.dev`) pertenecen a otro entorno: no tocarlos.

Si no existe, partir de la plantilla del stack en `plantillas.md`. Para un
stack sin plantilla, escribirlo siguiendo la misma lista:

- Multi-stage: build con toolchain completo, runtime mínimo (`-jre`, `-alpine`,
  `distroless`).
- Copiar primero los manifiestos + lockfile e instalar deps, después el código:
  así cambiar código no invalida la capa de deps.
- Instalar con lockfile congelado (`npm ci`, `pnpm install --frozen-lockfile`,
  `./gradlew`, `mvn -B`). Nunca `npm install` suelto.
- Tags de imagen base con versión mayor fija (`node:22-alpine`,
  `eclipse-temurin:21-jre`), no `latest`.
- Correr como usuario no root.
- Respetar `PORT` si la app lo lee; `EXPOSE` del puerto real.
- `CMD`/`ENTRYPOINT` en forma exec (`["java","-jar","app.jar"]`) para que la app
  reciba SIGTERM.
- **Cero secretos en la imagen**: ni `COPY .env`, ni `ARG`/`ENV` con claves. Las
  credenciales entran en runtime por variables del host. Solo los valores
  públicos que el framework hornea en build van como `ARG`.
- Los tests no corren dentro del `docker build` (`-x test`, `-DskipTests`): ya
  los corre el CI.

`.dockerignore` junto al Dockerfile (o en la raíz si el context es la raíz):
excluir `.git`, deps instaladas, salidas de build, `.env*` (salvo
`.env.example`), IDE.

### 4. Verificar local

Por cada app, desde la raíz del repo:

```bash
docker build -t <app>:local <context> [-f <dockerfile>] [--build-arg K=V]
docker run --rm -p <puerto>:<puerto> --env-file <env de prueba> <app>:local
```

Y confirmar que responde (`curl -fsS localhost:<puerto><health o />`). Si la
app necesita una base u otro servicio para arrancar, usar el
`docker-compose.yml` del repo si existe; si no, alcanza con que el proceso
levante y falle recién al conectar, y decirlo en el informe.

Si no hay Docker disponible, decirlo y no marcar el paso como verificado.

### 5. Pipeline de GitHub Actions

Una imagen se publica solo si los tests de esa app pasaron. Entonces:

- **Si ya hay un workflow de CI para la app** (corre sus tests), agregarle el
  job `image` de `plantillas.md` con `needs: <job de CI>`. No duplicar
  triggers ni checks.
- **Si no hay**, crear `.github/workflows/<app>-image.yml` con el workflow
  completo de `plantillas.md`: trae un job `test` (con el comando de tests
  del repo: `npm test`, `./gradlew test`, `./mvnw -B test`, `go test ./...`…)
  y `image` con `needs: test`. Si la app no tiene tests, no inventarlos ni
  sacar el `needs`: publicar igual es justo lo que esta regla evita. Dejar
  el job `test` corriendo al menos el build y avisarlo en el informe.

Reglas:

- Rama: usar la **default branch del repo** (`gh repo view --json
  defaultBranchRef -q .defaultBranchRef.name`), no copiar `main` a ciegas.
  Si ya hay workflows, usar las ramas que disparan esos.

- Monorepo: filtro `paths` por carpeta de la app (más el propio workflow y
  cualquier carpeta compartida que la app use), para que un cambio en `web/`
  no rebuildee `api`. Microservicio: sin filtro.
- En `pull_request` se buildea **sin push** (valida el Dockerfile). Se publica
  en `push` a la rama principal, en tags `v*` y en `workflow_dispatch`.
- Tags: `sha-<corto>` siempre; `latest` en la rama principal; `X.Y.Z` y `X.Y`
  en tags semver. El entorno de prod debe fijar un `sha-*` o semver, nunca
  `latest`.
- Auth con `GITHUB_TOKEN` y `permissions: packages: write`: no hace falta
  crear secretos.
- Build args públicos desde variables de repo/entorno (`${{ vars.X }}`),
  nunca hardcodeados. Si el valor cambia por entorno (URL de la API de prod vs
  pre-prod), eso implica una imagen por entorno: avisarlo en el informe.
- Cache de capas `type=gha` con `scope=<app>` para que las apps no se pisen.

Si `actionlint` está instalado, correrlo sobre los workflows tocados.

### 6. Informe

Cerrar con:

- Tabla del paso 2 con el estado final (verificado / no verificado y por qué).
- Archivos creados y modificados.
- Pasos manuales que quedan, solo los que apliquen:
  - Crear las variables de repo usadas como build args
    (Settings → Secrets and variables → Actions → Variables).
  - Los paquetes de GHCR nacen **privados**: o hacerlos públicos
    (Package settings → Visibility), o darle al host un PAT con
    `read:packages` para hacer pull.
  - Variables de runtime que el host tiene que setear (lista, sin valores).

## Cuándo no usarla

- El repo ya publica imágenes a otro registry y no se pidió migrar: preguntar.
- La app es 100 % estática y el host sirve estáticos (Pages, Static Web Apps):
  un contenedor no aporta; decirlo.

## Ejemplo de uso

**Pedido:** /contenerizar-app --dry-run

**Resultado:** Detecta las apps del repo y muestra el plan por app (stack, Dockerfile existente o nuevo, imagen en GHCR, build args, puerto); sin --dry-run escribe los Dockerfiles y el workflow que publica las imágenes.
