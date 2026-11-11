---
name: g14-chequeo-trazabilidad-pr-ticket
description: Verifica que cada PR, rama y commit del repo de producto nombre su ticket de Jira (`SCRUM-<n>`), que las tres capas de la convención (hooks de Husky, checks de GitHub Actions y template de PR) estén vigentes, y reporta las excepciones. Usala antes de una revisión de sprint o un steering, o cuando un PR llega sin poder saberse de qué ticket viene.
metadata:
  tipo: skill
  area:
  - gestion
  - qa
  fase:
  - revision
  tecnologias:
  - git
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  - jira
  grupo: "14"
  autor:
    nombre: Martina de Jesus
    github: mardejesus
  colaboradores: []
  responsables:
  - mardejesus
  madurez: usado-en-proyecto
  relacionados: []
---

# Chequeo de trazabilidad PR ↔ ticket

Sin trazabilidad, cada revisión empieza con «¿de qué ticket es esto?», y ese costo lo pagan los devs, que son el recurso escaso. La convención de VaiVen se apoya en tres capas; este chequeo comprueba que existan y que se cumplan. **Solo lee y reporta**: no reescribe commits, no renombra ramas y no edita PRs.

## La convención que se audita

| Capa | Dónde | Qué exige |
|---|---|---|
| Pre-commit (Husky) | `.husky/pre-commit` | La rama empieza con `SCRUM-<n>` (o es `main`) y el build pasa |
| Commit-msg (Husky) | `.husky/commit-msg` | El mensaje incluye `SCRUM-<n>` |
| CI (GitHub Actions) | `check-branch-name.yml`, `check-commit-messages.yml`, `check-build.yml` | Espejan lo anterior del lado del servidor: nadie se saltea el hook local |
| Template de PR | `.github/pull_request_template.md` | Ticket, qué hace, checklist de DoD, pruebas/capturas |

Adaptá el prefijo (`SCRUM`) a la clave del proyecto de Jira.

## Pasos

1. **Las capas existen en `origin/main`**:
   ```bash
   git fetch origin
   git ls-tree -r --name-only origin/main | grep -E '^\.husky/(pre-commit|commit-msg)$|^\.github/(workflows/check-|pull_request_template)'
   ```
   Leé el contenido de cada hook y workflow: que el archivo exista no prueba que la regex sea la correcta.
2. **PRs del período** (abiertos y mergeados):
   ```bash
   gh pr list --repo <org>/<repo> --state all --limit 50 --json number,title,headRefName,body,mergedAt
   ```
   Para cada uno, buscá `SCRUM-\d+` en rama, título y cuerpo. Registrá dónde aparece y si coincide entre los tres.
3. **Commits de cada PR**:
   ```bash
   gh pr view <n> --repo <org>/<repo> --json commits --jq '.commits[].messageHeadline'
   ```
   Marcá los que no nombran ticket. Los merge commits automáticos se listan aparte, no como falta.
4. **Los checks corrieron**: `gh pr checks <n>` o los workflow runs del PR. Un PR mergeado con el check de nombre en rojo es un hallazgo más grave que un commit sin ID.
5. **El ticket existe y corresponde**: consultá `SCRUM-<n>` en Jira (MCP o API) y verificá que exista y que el título del PR tenga relación con él. Detectá también **ramas apiladas**: un PR cuya rama arranca de otra rama sin mergear trae commits de otro ticket que no son del autor.

## Salida

```
Trazabilidad — <repo> — <fecha> — origin/main <sha>

Capas: hooks ✅/❌ · workflows ✅/❌ · template ✅/❌

| PR | Rama | Título | Cuerpo | Commits sin ID | Checks | Ticket en Jira | Observación |
|----|------|--------|--------|----------------|--------|----------------|-------------|

Resumen: N PRs, M con ID consistente, K excepciones.
```

Cada excepción con su evidencia (comando y salida). Si todo está limpio, decilo con los números, no con «está todo bien».

## Reglas

- Una afirmación de «todo PR trae su ID» se apoya en la corrida de esta sesión, no en la convención escrita.
- No atribuyas a un dev commits que vienen de una rama apilada.
- El arreglo (hook nuevo, renombrar rama) lo hace el dev: la pieza propone, no toca el repo de producto.

Evidencia en VaiVen: `docs/qa/cierre-steering-1.md` § 1 (convención verificada en `vaiven-app` el 16/09; los PRs revisados ese sprint siguieron el formato sin excepción).

## Ejemplo de uso

**Pedido:** Antes del steering, verificá que todos los PRs del sprint tengan su ticket de Jira en rama, título y commits.

**Resultado:** Devuelve el estado de las tres capas en `origin/main` y una tabla por PR con dónde aparece el `SCRUM-<n>`, commits sin ID, estado de los checks y si el ticket existe en Jira, con el resumen de excepciones.
