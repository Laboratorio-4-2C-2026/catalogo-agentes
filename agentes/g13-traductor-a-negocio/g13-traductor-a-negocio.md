---
name: g13-traductor-a-negocio
description: 'Agente de GitHub Actions que traduce cada PR de MicroChangas al lenguaje del negocio para quien no programa (PM, profesores, steering): qué resuelve para el usuario de la app, qué riesgo trae y qué habría que probar, sin nombrar archivos ni funciones. Avisa si la PR hace más, menos o algo distinto de lo que pedía el ticket de Multica. Corre en cada push a una PR que no esté en draft.'
metadata:
  tipo: agente
  area:
  - gestion
  - documentacion
  fase:
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
  madurez: experimental
  relacionados:
  - g11-pr-business-translator
  - g13-pr-review-contra-ticket
  - g13-guiones-uat
  - g13-preparador-de-steering
---

# Traductor a negocio

Agente de CI de MicroChangas. Es un **reusable workflow** de GitHub Actions (`on: workflow_call`) que usa
`anthropics/claude-code-action` para llamar al modelo. Vive en un repo central de agentes y los repos de producto
(front y back) lo invocan con un caller de pocas líneas, así que cambiar un prompt o una compuerta no requiere
tocar los repos de producto.

**Ningún agente escribe en el repo de producto:** pide `contents: read` y su única salida son comentarios en la PR
y artifacts del run.

## Archivos

- [`negocio.yml`](negocio.yml): el workflow original, sin cambios. El prompt del agente está embebido en el
  paso `claude` (el repo de origen es privado y por eso los prompts no viven en archivos sueltos).

Origen: `.github/workflows/negocio.yml` en https://github.com/MicroChangas/microchangas-agents (privado).

## Cómo funciona

- Resuelve el código de ticket desde la rama, el título o el cuerpo de la PR y trae el ticket de Multica. Si no lo encuentra, lo deduce del diff y lo aclara.
- El modelo lee el ticket y el diff y publica un único comentario con tres partes: **Qué resuelve** (contado desde la persona que usa la app), **Riesgo** (bajo, medio o alto según qué pasaría si sale mal) y **Qué probar** (dos o tres acciones en la app).
- Si corresponde, agrega una línea "Ojo:" con algo que el negocio debería saber y no se ve en la PR (una dependencia pendiente, un cambio en algo que los usuarios ya conocían).
- No opina sobre la calidad del código: eso lo hace `g13-pr-review-contra-ticket`. Antes era un bloque adentro de ese review; se separó para que tenga su propio check y su propio mail.

## Cómo se instala

1. Copiá `negocio.yml` a `.github/workflows/` de un repo central de agentes (o del mismo repo de producto).
2. Cargá el secret `CLAUDE_CODE_OAUTH_TOKEN` o `ANTHROPIC_API_KEY`, `MULTICA_TOKEN` y la variable `MULTICA_WORKSPACE_ID`. `RESEND_API_KEY` es opcional (manda el resumen por mail).
3. En el repo de producto, declaralo en `.github/workflows/agents.yml` (disparado por `pull_request`). Así está en MicroChangas (backend):

```yaml
  negocio:
    # Traduce la PR al lenguaje del negocio, en su propio comentario. Antes esto
    # era un bloque adentro del comentario de pr-review; se separo para que sea
    # un agente con su propio check y su propio mail.
    permissions:
      contents: read
      pull-requests: write
      issues: read
      id-token: write
      actions: read
    uses: MicroChangas/microchangas-agents/.github/workflows/negocio.yml@v1
    with:
      project_kind: backend
      multica_workspace_id: ${{ vars.MULTICA_WORKSPACE_ID }}
    secrets: inherit
```

Los `permissions` van sí o sí en el caller: un reusable workflow no puede pedir más de lo que le otorga quien lo
llama, e `id-token: write` nunca viene por defecto.

## Ejemplo de uso

**Pedido:** Un dev abre la PR del ticket MIC-87 (postularse a una changa) en microchangas-frontend.

**Resultado:** El agente comenta en la PR, sin jerga, que ahora quien ve una changa puede postularse desde la app, que el riesgo es medio porque cambia una pantalla que ya se usa, y los tres pasos para probarlo.
