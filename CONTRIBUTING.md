# Cómo subir piezas al catálogo

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
| `area` | `frontend` (2), `backend` (13), `mobile` (19), `datos` (2), `ia` (1), `qa` (14), `devops` (1), `seguridad` (2), `gestion` (5), `diseno` (4), `documentacion` (1) |
| `fase` | `planificacion` (4), `analisis` (3), `diseno` (6), `desarrollo` (16), `testing` (8), `revision` (14), `despliegue` (1), `mantenimiento` (4) |
| `tecnologias` | `agnostico` (7), `express` (10), `flutter` (18), `prisma` (4), `dart` (17), `docker` (1), `figma` (1), `javascript` (1), `postgresql` (3), `riverpod` (1), `supertest` (3), `typescript` (11), `vitest` (3), `zod` (1) |
| `metodologia` | `scrum` (5), `kanban` (0), `agnostico` (0) |
| `herramientas` | `claude-code` (40), `cursor` (0), `codex` (38), `otra` (1) |
| `requiere` | `jira` (4), `github` (5), `figma` (1), `google-sheets` (3), `slack` (0), `dart-mcp` (2) |
| `madurez` | `experimental` (0), `probado` (0), `usado-en-proyecto` (40) |
<!-- LISTAS:FIN -->
