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
| `area` | `frontend` (108), `backend` (137), `mobile` (21), `datos` (28), `ia` (18), `qa` (187), `devops` (59), `seguridad` (29), `gestion` (257), `diseno` (48), `documentacion` (87) |
| `fase` | `planificacion` (141), `analisis` (91), `diseno` (64), `desarrollo` (102), `testing` (109), `revision` (279), `despliegue` (29), `mantenimiento` (66), `integracion` (5) |
| `tecnologias` | `agnostico` (317), `express` (22), `flutter` (18), `prisma` (40), `dart` (17), `docker` (25), `figma` (5), `javascript` (3), `postgresql` (44), `riverpod` (1), `supertest` (4), `typescript` (117), `vitest` (9), `zod` (1), `n8n` (10), `supabase` (31), `firebase` (15), `firestore` (3), `git` (37), `jest` (9), `nodejs` (14), `react` (81), `python` (46), `nextjs` (15), `playwright` (23), `nestjs` (47), `tanstack-query` (1), `auth0` (3), `flyway` (7), `junit` (2), `kotlin` (12), `postman` (1), `spring-boot` (22), `testcontainers` (1), `tailwindcss` (9), `vite` (8), `github-actions` (17), `k6` (2), `turborepo` (1), `cypress` (1), `terraform` (1) |
| `metodologia` | `scrum` (440), `kanban` (10), `agnostico` (59) |
| `herramientas` | `claude-code` (499), `cursor` (54), `codex` (182), `otra` (118) |
| `requiere` | `jira` (70), `github` (175), `figma` (5), `google-sheets` (12), `slack` (0), `dart-mcp` (2), `chrome` (20), `discord` (14), `google-drive` (15), `engram` (70), `linear` (113), `playwright` (9), `talksmith` (2), `openrouter` (13), `multica` (49), `supabase` (1), `platformance` (1), `cloudflare` (1), `neon` (5), `render` (1), `agentation` (5), `codegraph` (28), `stitch` (8), `canva` (1), `gemini` (2), `vertex-ai` (2) |
| `madurez` | `experimental` (248), `probado` (28), `usado-en-proyecto` (311), `prototipo` (3) |
<!-- LISTAS:FIN -->
