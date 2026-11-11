# Cómo subir piezas al catálogo

## Antes de empezar: acceso al repo

- Anotate en la [planilla de inscripción](https://docs.google.com/spreadsheets/d/1tA2CFxUesISCr39-MmhhdxwmitZKZBhTdOjfpSGjCec/edit?gid=672555901#gid=672555901) con tu usuario de GitHub.
- La cátedra te invita a la organización `Laboratorio-4-2C-2026` como member y a este repo con permiso de escritura. Todos los integrantes tienen el mismo rol: solo la cátedra invita gente.
- Te llegan dos mails de GitHub, uno de la organización y otro del repo. **Aceptá los dos**: hasta que lo hagas no podés subir nada.

## Pasos

1. Abrí tu herramienta (Claude Code, Cursor o Codex) en la carpeta donde tenés tus piezas.
2. Pegá el prompt de `prompts/1-preparar-piezas.md` y completá los DATOS DEL EQUIPO.
3. Revisá la tabla que te devuelve la IA y corregí lo que haga falta.
   - **Recomendado:** pedile a tu herramienta que revise las fichas con la skill `skills/g03-revisor-de-fichas/SKILL.md` (modo local). Propone mejoras de clasificación, descripción, ejemplo y piezas relacionadas, y solo aplica las que aceptes.
4. En tu copia del repo, creá una rama que empiece con tu número de grupo: `git checkout -b g03-carga-inicial`. Si alguna ficha no dice el grupo, el bot lo toma del nombre de la rama.
5. Copiá las carpetas `gNN-…` a `skills/`, `agentes/` o `comandos/`. Si no sabés dónde va cada una, subilas donde quieras: el bot las mueve a su lugar, les pone el prefijo del grupo y avisa en el comentario (necesitan tener ficha).
6. `git add`, `git commit` y `git push -u origin <tu-rama>`.
7. Abrí el Pull Request en GitHub hacia `main`.
8. Esperá el comentario automático: si hay errores, corregilos y volvé a hacer push.
9. Cuando esté todo en orden, aceptá el PR (botón **Merge**).

Reglas:

- Trabajá **en una rama del repo, no en un fork**: el bot necesita poder corregir tu rama.
- Tocá **solo las piezas de tu grupo** (las que empiezan con tu prefijo).
- No edites a mano `taxonomia.yml`, `sitio/` ni las tablas de categorías: se actualizan solos.
- Si en una ficha ponés como autor o colaborador a alguien que todavía no está en `integrantes.yml`, el bot lo suma solo al grupo de la pieza (con su nombre y usuario de GitHub) cuando revisa el PR.

Para actualizar una pieza que ya está, usá `prompts/2-actualizar-pieza.md`.

## Valores disponibles

Preferí siempre estos valores. Si ninguno encaja, podés escribir uno nuevo: se suma solo al aceptar el PR.

<!-- LISTAS:INICIO -->
| Campo | Valores (cantidad de piezas que lo usan) |
|---|---|
| `area` | `frontend` (93), `backend` (116), `mobile` (20), `datos` (22), `ia` (11), `qa` (157), `devops` (47), `seguridad` (22), `gestion` (225), `diseno` (41), `documentacion` (64) |
| `fase` | `planificacion` (126), `analisis` (80), `diseno` (56), `desarrollo` (96), `testing` (89), `revision` (231), `despliegue` (22), `mantenimiento` (51), `integracion` (5) |
| `tecnologias` | `agnostico` (281), `express` (22), `flutter` (18), `prisma` (34), `dart` (17), `docker` (20), `figma` (3), `javascript` (3), `postgresql` (37), `riverpod` (1), `supertest` (4), `typescript` (96), `vitest` (7), `zod` (1), `n8n` (2), `supabase` (22), `firebase` (14), `firestore` (3), `git` (29), `jest` (7), `nodejs` (13), `react` (61), `python` (28), `nextjs` (15), `playwright` (18), `nestjs` (34), `tanstack-query` (1), `auth0` (3), `flyway` (7), `junit` (2), `kotlin` (12), `postman` (1), `spring-boot` (16), `testcontainers` (1), `tailwindcss` (7), `vite` (5), `github-actions` (5), `k6` (2), `turborepo` (1), `cypress` (1), `terraform` (1) |
| `metodologia` | `scrum` (376), `kanban` (10), `agnostico` (40) |
| `herramientas` | `claude-code` (417), `cursor` (53), `codex` (181), `otra` (116) |
| `requiere` | `jira` (55), `github` (151), `figma` (3), `google-sheets` (11), `slack` (0), `dart-mcp` (2), `chrome` (19), `discord` (14), `google-drive` (15), `engram` (70), `linear` (112), `playwright` (8), `talksmith` (2), `openrouter` (10), `multica` (43), `supabase` (1), `platformance` (1), `cloudflare` (1), `neon` (5), `render` (1), `agentation` (5), `codegraph` (28), `stitch` (8) |
| `madurez` | `experimental` (218), `probado` (17), `usado-en-proyecto` (269), `prototipo` (3) |
<!-- LISTAS:FIN -->
