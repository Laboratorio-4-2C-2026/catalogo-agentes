# Configuración — g07-code-review-tl

Datos del repo que revisa esta skill. No hay secretos acá.

- **Proyecto**: `<nombre del proyecto>`
- **Repo local**: `../<repo>` (relativo a la raíz de este repo)
- **Repo de GitHub**: `<org>/<repo>` — branch base `main`
- **Convención de branches/PRs**: `<KEY>-<n>-<slug-del-ticket>`
- **Site de Jira**: `<tuequipo>.atlassian.net`
- **Project key**: `<KEY>`
- **Stack** (ejemplo de un proyecto Spring Boot + React; reemplazalo por el tuyo):
  - Base de datos + backend (Spring Boot / Gradle): `docker compose up` en la raíz del repo (Postgres en `5432`, backend en `8080`). Las variables salen de `.env` (ver `.env.example`).
  - Tests de backend: `./gradlew test` dentro de `backend/`.
  - Frontend (Vite + React + TS): `npm install && npm run dev` dentro de `frontend/`; también `npm run lint` y `npm run build` (incluye type-check).
- **CI existente** (`.github/workflows/`): `ci-check-gradle.yml`, `frontend-ci.yml`, `cd-be-docker-publish.yml`.

Esta skill no commitea ni comenta en GitHub: el repo es de los developers. El reporte se entrega en el chat para que el TL lo pegue en el PR.
