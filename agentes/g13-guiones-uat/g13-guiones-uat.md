---
name: g13-guiones-uat
description: 'Agente de GitHub Actions que convierte los criterios de aceptación del ticket de Multica en un guion de UAT paso a paso que puede ejecutar alguien del negocio, más un acta de aceptación para el steering que se descarga como artifact. Corre al abrir o marcar lista la PR, o con el label uat.'
metadata:
  tipo: agente
  area:
  - qa
  - gestion
  fase:
  - testing
  - revision
  tecnologias:
  - github-actions
  - agnostico
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
  - g15-uat-script-planner
  - g10-uat-planner
  - g15-pr-uat-contrast
  - g13-preparador-de-steering
  - g13-pr-review-contra-ticket
  - g15-functional-uat-executor
---

# Guiones UAT

Agente de CI de MicroChangas. Es un **reusable workflow** de GitHub Actions (`on: workflow_call`) que usa
`anthropics/claude-code-action` para llamar al modelo. Vive en un repo central de agentes y los repos de producto
(front y back) lo invocan con un caller de pocas líneas, así que cambiar un prompt o una compuerta no requiere
tocar los repos de producto.

**Ningún agente escribe en el repo de producto:** pide `contents: read` y su única salida son comentarios en la PR
y artifacts del run.

## Archivos

- [`uat.yml`](uat.yml): el workflow original, sin cambios. El prompt del agente está embebido en el
  paso `claude` (el repo de origen es privado y por eso los prompts no viven en archivos sueltos).

Origen: `.github/workflows/uat.yml` en https://github.com/MicroChangas/microchangas-agents (privado).

## Cómo funciona

- Compuerta: se omite salvo al abrir la PR, al marcarla lista para review o al ponerle el label `uat`. Un guion se escribe una vez, no en cada push.
- Trae el ticket de Multica; si la PR no tiene ticket, avisa en la PR y no llama al modelo.
- El modelo cruza los criterios con el diff y comenta el guion paso a paso (datos de prueba, pasos, resultado esperado).
- Genera `acta-uat.md` para firmar en el steering y la sube como artifact.

## Cómo se instala

1. Copiá `uat.yml` a `.github/workflows/` de un repo central de agentes (o del mismo repo de producto).
2. Cargá el secret `CLAUDE_CODE_OAUTH_TOKEN` o `ANTHROPIC_API_KEY`, `MULTICA_TOKEN` y la variable `MULTICA_WORKSPACE_ID`. `RESEND_API_KEY` es opcional (manda el resumen por mail).
3. En el repo de producto, declaralo en `.github/workflows/agents.yml` (disparado por `pull_request`). Así está en MicroChangas (backend):

```yaml
  uat:
    # Se omite salvo al abrir la PR, al marcarla lista, o con el label `uat`.
    permissions:
      contents: read
      pull-requests: write
      issues: read
      id-token: write
      actions: read
    uses: MicroChangas/microchangas-agents/.github/workflows/uat.yml@v1
    with:
      project_kind: backend
      multica_workspace_id: ${{ vars.MULTICA_WORKSPACE_ID }}
    secrets: inherit
```

Los `permissions` van sí o sí en el caller: un reusable workflow no puede pedir más de lo que le otorga quien lo
llama, e `id-token: write` nunca viene por defecto.

## Ejemplo de uso

**Pedido:** Se marca como lista para review la PR del ticket MIC-87 (postularse a una changa).

**Resultado:** El agente comenta un guion de UAT con los pasos para que la PM pruebe la postulación desde la app y deja descargable el acta de aceptación con un casillero por criterio.
