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
| `area` | `frontend` (20), `backend` (37), `mobile` (19), `datos` (3), `ia` (8), `qa` (50), `devops` (9), `seguridad` (9), `gestion` (54), `diseno` (9), `documentacion` (21) |
| `fase` | `planificacion` (31), `analisis` (22), `diseno` (15), `desarrollo` (41), `testing` (28), `revision` (53), `despliegue` (9), `mantenimiento` (10) |
| `tecnologias` | `agnostico` (64), `express` (18), `flutter` (18), `prisma` (4), `dart` (17), `docker` (3), `figma` (2), `javascript` (1), `postgresql` (4), `riverpod` (1), `supertest` (3), `typescript` (44), `vitest` (3), `zod` (1), `n8n` (1), `supabase` (9), `firebase` (10), `firestore` (3), `git` (1), `jest` (4), `nodejs` (4), `react` (13), `python` (1), `nextjs` (6), `playwright` (1) |
| `metodologia` | `scrum` (108), `kanban` (0), `agnostico` (1) |
| `herramientas` | `claude-code` (144), `cursor` (53), `codex` (38), `otra` (2) |
| `requiere` | `jira` (14), `github` (27), `figma` (1), `google-sheets` (3), `slack` (0), `dart-mcp` (2), `chrome` (4), `discord` (4), `google-drive` (1), `engram` (33), `linear` (22), `playwright` (1), `talksmith` (2) |
| `madurez` | `experimental` (2), `probado` (0), `usado-en-proyecto` (142) |
<!-- LISTAS:FIN -->
