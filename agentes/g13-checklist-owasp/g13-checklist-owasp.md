---
name: g13-checklist-owasp
description: 'Agente de GitHub Actions que, para historias sensibles (auth, permisos, datos personales, pagos, uploads), arma un checklist basado en OWASP ASVS a medida de la PR y la verifica ítem por ítem. Decide solo si la historia es sensible mirando el diff y el ticket de Multica.'
metadata:
  tipo: agente
  area:
  - seguridad
  - backend
  - frontend
  fase:
  - revision
  tecnologias:
  - github-actions
  - nestjs
  - react
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
  - g13-modelador-de-amenazas-stride
  - g08-security-reviewer
  - g11-security-agent
  - g11-revisar-privacidad
---

# Checklist OWASP

Agente de CI de MicroChangas. Es un **reusable workflow** de GitHub Actions (`on: workflow_call`) que usa
`anthropics/claude-code-action` para llamar al modelo. Vive en un repo central de agentes y los repos de producto
(front y back) lo invocan con un caller de pocas líneas, así que cambiar un prompt o una compuerta no requiere
tocar los repos de producto.

**Ningún agente escribe en el repo de producto:** pide `contents: read` y su única salida son comentarios en la PR
y artifacts del run.

## Archivos

- [`owasp.yml`](owasp.yml): el workflow original, sin cambios. El prompt del agente está embebido en el
  paso `claude` (el repo de origen es privado y por eso los prompts no viven en archivos sueltos).

Origen: `.github/workflows/owasp.yml` en https://github.com/MicroChangas/microchangas-agents (privado).

## Cómo funciona

- Compuerta con dos señales: rutas sensibles en el diff (auth, guard, jwt, role, payment, upload, prisma…) o palabras de riesgo en el título y la descripción del ticket.
- Si ninguna aparece, se omite sin llamar al modelo.
- Si corre, el modelo arma el checklist ASVS que aplica a esa PR y marca cada ítem como cumple, no cumple o no aplica, con evidencia del código.

## Cómo se instala

1. Copiá `owasp.yml` a `.github/workflows/` de un repo central de agentes (o del mismo repo de producto).
2. Cargá el secret `CLAUDE_CODE_OAUTH_TOKEN` o `ANTHROPIC_API_KEY`, `MULTICA_TOKEN` y la variable `MULTICA_WORKSPACE_ID`. `RESEND_API_KEY` es opcional (manda el resumen por mail).
3. En el repo de producto, declaralo en `.github/workflows/agents.yml` (disparado por `pull_request`). Así está en MicroChangas (backend):

```yaml
  owasp:
    # Se omite si ni el diff ni el ticket tocan auth, permisos, datos personales
    # o pagos.
    permissions:
      contents: read
      pull-requests: write
      issues: read
      id-token: write
      actions: read
    uses: MicroChangas/microchangas-agents/.github/workflows/owasp.yml@v1
    with:
      project_kind: backend
      multica_workspace_id: ${{ vars.MULTICA_WORKSPACE_ID }}
    secrets: inherit
```

Los `permissions` van sí o sí en el caller: un reusable workflow no puede pedir más de lo que le otorga quien lo
llama, e `id-token: write` nunca viene por defecto.

## Ejemplo de uso

**Pedido:** Una PR del back agrega el guard que restringe la edición de una changa a su dueño.

**Resultado:** El agente comenta un checklist ASVS de control de acceso (verificación del dueño en el servidor, IDs ajenos, respuestas 403 vs 404) con cada ítem verificado contra el diff.
