---
name: g13-pr-review-contra-ticket
description: 'Agente de GitHub Actions que revisa cada PR de MicroChangas contra el ticket de Multica: verifica los criterios de aceptación uno por uno, más correctitud, seguridad y mantenibilidad, y comenta inline. Abre con un bloque ''Para el negocio'' legible por alguien que no programa. Corre en cada push a una PR que no esté en draft.'
metadata:
  tipo: agente
  area:
  - qa
  - backend
  - frontend
  fase:
  - revision
  tecnologias:
  - github-actions
  - nestjs
  - react
  - typescript
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  - multica
  grupo: "13"
  autor:
    nombre: Tobias Berger
    github: TotoBerger
  responsables:
  - TotoBerger
  madurez: usado-en-proyecto
  relacionados:
  - g15-pr-code-reviewer
  - g04-pr-review-ticket-scope
  - g11-pr-business-translator
  - g13-validar-branch
---

# PR Review contra el ticket

Agente de CI de MicroChangas. Es un **reusable workflow** de GitHub Actions (`on: workflow_call`) que usa
`anthropics/claude-code-action` para llamar al modelo. Vive en un repo central de agentes y los repos de producto
(front y back) lo invocan con un caller de pocas líneas, así que cambiar un prompt o una compuerta no requiere
tocar los repos de producto.

**Ningún agente escribe en el repo de producto:** pide `contents: read` y su única salida son comentarios en la PR
y artifacts del run.

## Archivos

- [`pr-review.yml`](pr-review.yml): el workflow original, sin cambios. El prompt del agente está embebido en el
  paso `claude` (el repo de origen es privado y por eso los prompts no viven en archivos sueltos).

Origen: `.github/workflows/pr-review.yml` en https://github.com/MicroChangas/microchangas-agents (privado).

## Cómo funciona

- Resuelve el código de ticket desde la rama, el título o el cuerpo de la PR (`MIC-87` o `MC-106`).
- Trae el ticket de la API de Multica. Si falla, el review igual corre y avisa que no pudo verificar los criterios.
- El modelo lee el diff completo contra la base, comenta inline y publica un resumen con un bloque *Para el negocio* (qué resuelve, riesgo, qué probar).
- Las PRs en draft no se revisan, para no gastar tokens en código que todavía se mueve.

## Cómo se instala

1. Copiá `pr-review.yml` a `.github/workflows/` de un repo central de agentes (o del mismo repo de producto).
2. Cargá el secret `CLAUDE_CODE_OAUTH_TOKEN` o `ANTHROPIC_API_KEY`, `MULTICA_TOKEN` y la variable `MULTICA_WORKSPACE_ID`. `RESEND_API_KEY` es opcional (manda el resumen por mail).
3. En el repo de producto, declaralo en `.github/workflows/agents.yml` (disparado por `pull_request`). Así está en MicroChangas (backend):

```yaml
  pr-review:
    # Los permisos van SI O SI aca. Un reusable workflow no puede pedir mas de lo
    # que le otorga quien lo llama, y sin este bloque el caller hereda el default
    # del repo (solo lectura) y el run muere al arrancar, en 1 segundo y sin logs.
    # `id-token` ademas nunca lo da el default: siempre hay que declararlo.
    permissions:
      contents: read
      pull-requests: write
      issues: read
      id-token: write
      actions: read
    uses: MicroChangas/microchangas-agents/.github/workflows/pr-review.yml@v1
    with:
      project_kind: backend
      multica_workspace_id: ${{ vars.MULTICA_WORKSPACE_ID }}
    secrets: inherit
```

Los `permissions` van sí o sí en el caller: un reusable workflow no puede pedir más de lo que le otorga quien lo
llama, e `id-token: write` nunca viene por defecto.

## Ejemplo de uso

**Pedido:** Un dev abre la PR `MIC-87 Postulación a changas` hacia `dev` en microchangas-backend.

**Resultado:** El agente comenta en la PR una tabla con cada criterio de aceptación del ticket MIC-87 (cumple / no cumple / no verificable), observaciones inline sobre el diff y un bloque 'Para el negocio' con el riesgo y qué probar.
