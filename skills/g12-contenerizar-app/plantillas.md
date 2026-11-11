# Plantillas de contenerizar-app

Puntos de partida, no archivos para copiar a ciegas: ajustar versiones, puerto,
nombre del jar y gestor de paquetes a lo que el repo usa de verdad.

## Next.js

Requiere `output: "standalone"` en `next.config.*`. Si el repo ya se despliega
en Vercel, activarlo solo fuera de Vercel para no cambiar ese deploy:
`...(!process.env.VERCEL ? { output: "standalone" } : {})`.

```dockerfile
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

FROM node:22-alpine AS build
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
# Valores públicos que Next hornea en el bundle. Uno por variable NEXT_PUBLIC_*.
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

FROM node:22-alpine
WORKDIR /app
ENV NODE_ENV=production NEXT_TELEMETRY_DISABLED=1 PORT=3000 HOSTNAME=0.0.0.0
USER node
COPY --from=build --chown=node:node /app/public ./public
COPY --from=build --chown=node:node /app/.next/standalone ./
COPY --from=build --chown=node:node /app/.next/static ./.next/static
EXPOSE 3000
CMD ["node", "server.js"]
```

Si no hay carpeta `public/`, sacar esa línea. Con pnpm:
`COPY package.json pnpm-lock.yaml ./` + `RUN corepack enable && pnpm install --frozen-lockfile`.
Con yarn: `yarn.lock` + `corepack enable && yarn install --immutable`.

## Node genérico (Express, Nest, Fastify…)

```dockerfile
FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
# Quitar si el proyecto no tiene paso de build (JS plano).
RUN npm run build && npm prune --omit=dev

FROM node:22-alpine
WORKDIR /app
ENV NODE_ENV=production
USER node
COPY --from=build --chown=node:node /app ./
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

`CMD` = lo que corre el script `start` del `package.json`, llamado con `node`
directo (no `npm start`, que no reenvía SIGTERM).

## Spring Boot (Gradle)

```dockerfile
FROM eclipse-temurin:21-jdk AS build
WORKDIR /app
COPY gradlew settings.gradle* build.gradle* ./
COPY gradle gradle
RUN chmod +x gradlew && ./gradlew dependencies --no-daemon -q > /dev/null || true
COPY src src
# Exactamente un boot jar: si hay 0 o más de uno, el build falla acá y no en runtime.
RUN ./gradlew bootJar --no-daemon -x test \
 && jars="$(find build/libs -maxdepth 1 -name '*.jar' ! -name '*-plain.jar')" \
 && [ "$(echo "$jars" | grep -c .)" -eq 1 ] && cp "$jars" app.jar

FROM eclipse-temurin:21-jre
WORKDIR /app
RUN useradd --system --uid 1001 app
USER app
COPY --from=build /app/app.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-XX:MaxRAMPercentage=75.0", "-XX:+ExitOnOutOfMemoryError", "-jar", "app.jar"]
```

`MaxRAMPercentage` hace que la JVM respete el límite de memoria del
contenedor en vez del de la máquina.

## Spring Boot (Maven)

Igual que Gradle, cambiando el stage de build:

```dockerfile
FROM eclipse-temurin:21-jdk AS build
WORKDIR /app
COPY mvnw pom.xml ./
COPY .mvn .mvn
RUN chmod +x mvnw && ./mvnw -B dependency:go-offline -q
COPY src src
RUN ./mvnw -B package -DskipTests \
 && jars="$(find target -maxdepth 1 -name '*.jar' ! -name '*-sources.jar' ! -name '*-javadoc.jar' ! -name '*-tests.jar' ! -name 'original-*.jar')" \
 && [ "$(echo "$jars" | grep -c .)" -eq 1 ] && cp "$jars" app.jar
```

Mismo criterio que Gradle: un solo boot jar o el build falla. Si el repo
genera otro jar extra (shade, classifier propio), excluirlo en el `find`.

## Workflow completo (app sin CI previo)

`.github/workflows/<app>-image.yml`. En microservicio: borrar los `paths`,
`context: .` e `images: ghcr.io/${{ github.repository }}`.

`<rama-default>` es la default branch del repo (`main`, `master`, `develop`…),
no un literal.

```yaml
name: <app> image

on:
  push:
    branches: [<rama-default>]
    tags: ["v*"]
    paths: ["<carpeta>/**", ".github/workflows/<app>-image.yml"]
  pull_request:
    branches: [<rama-default>]
    paths: ["<carpeta>/**", ".github/workflows/<app>-image.yml"]
  workflow_dispatch:

concurrency:
  group: <app>-image-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    defaults:
      run:
        working-directory: <carpeta>
    steps:
      - uses: actions/checkout@v4
      # Setup del toolchain con cache, según el stack:
      #   actions/setup-node@v4   (cache: npm|pnpm|yarn, cache-dependency-path: <carpeta>/<lockfile>)
      #   actions/setup-java@v4   (distribution: temurin, cache: gradle|maven)
      #   actions/setup-go@v5 / actions/setup-python@v5
      - run: <instalar deps>   # npm ci · (gradle/maven no necesitan paso aparte)
      - run: <comando de tests del repo>

  image:
    needs: test
    # (pegar acá el resto del job de la sección siguiente)
```

Los filtros `paths` no se evalúan en pushes de tags: un tag `v*` publica todas
las apps, que es lo que se quiere en un release.

## Job `image` (para agregar a un workflow existente o al de arriba)

Siempre lleva `needs:` apuntando al job de tests: el del CI existente o el
`test` del workflow de arriba. Un job `image` sin `needs` no se commitea.

```yaml
  image:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-buildx-action@v3

      - uses: docker/login-action@v3
        if: github.event_name != 'pull_request'
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}/<app>
          tags: |
            type=sha
            type=raw,value=latest,enable={{is_default_branch}}
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - uses: docker/build-push-action@v6
        with:
          context: <carpeta>
          # file: <carpeta>/Dockerfile   # solo si el context es la raíz (workspace JS)
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          # build-args: |
          #   NEXT_PUBLIC_API_URL=${{ vars.NEXT_PUBLIC_API_URL }}
          cache-from: type=gha,scope=<app>
          cache-to: type=gha,mode=max,scope=<app>
```

`metadata-action` pasa el nombre a minúsculas (GHCR lo exige) y agrega las
labels OCI que linkean el paquete al repo.
