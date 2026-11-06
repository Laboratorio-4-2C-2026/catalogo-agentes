---
name: g02-zest-e2e-conventions
description: 'Convenciones para correr y escribir tests E2E de Zest con Playwright: repos de trabajo, levantar el stack local, selectores y apertura de PRs. Usar al preparar o ejecutar pruebas E2E.'
metadata:
  tipo: skill
  area:
  - qa
  - devops
  fase:
  - testing
  tecnologias:
  - playwright
  - docker
  - postgresql
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  grupo: '02'
  autor:
    nombre: Liz Lubelcyk
    github: lizlubelczyk
  responsables:
  - lizlubelczyk
  madurez: usado-en-proyecto
  relacionados:
  - g02-e2e-test-writer
  - g02-responsive-check
---
# Repositories

Work only in these two checkouts. Never touch any other copy on the machine,
even if one exists.

- App:   ~/multica-workspaces/zest
- Tests: ~/multica-workspaces/zest-support

Before each run, in each repo:
  git fetch origin
  git reset --hard && git clean -fd
  git checkout <target branch>

You write only in zest-support. You have no reason to commit, push, or change
a remote in zest — if you find yourself wanting to, stop the run and report
why rather than working around it.

# Bringing the stack up

1. In zest, check out the target branch.
2. docker compose up -d for Postgres.
3. Apply pending Prisma migrations — local dev database only, never RDS.
4. Seed the database.
5. Start backend and frontend. Wait for /health to return 200, up to 60s.
6. Always tear down the app and every container you started, including when
   the run fails.

# Writing specs

- Select on data-testid first. Fall back to accessible roles and labels.
  Never select on CSS classes or Tailwind utilities — they change with styling.
- If a needed element has no test id, do not invent a fragile selector.
  Record it under "Missing test ids" in your report.
- Auth is Auth0. Use the seeded test user rather than driving the login UI.
- One spec file per ticket, named for the issue identifier.

# Opening the PR

Open the pull request in zest-support via the GitHub API with curl.
Do not install or use the gh CLI.

## Ejemplo de uso
**Pedido:** Levantá el stack y corré los E2E de la rama del ticket.
**Resultado:** Actualiza los dos checkouts, levanta Postgres, migra y siembra la base local, espera /health, escribe specs con data-testid y baja todo al terminar.
