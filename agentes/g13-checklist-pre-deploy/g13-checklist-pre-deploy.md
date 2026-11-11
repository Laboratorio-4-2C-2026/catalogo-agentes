---
name: g13-checklist-pre-deploy
description: 'Agente de GitHub Actions que corre solo en las PRs que apuntan a la rama que despliega (main): junta la evidencia dura (checks de CI, migraciones, regeneración del schema, rollback documentado) y dictamina si la PR está en condiciones de salir a producción. Opcionalmente bloquea el merge. Usar cuando se quiere un control automático antes de cada release a producción.'
metadata:
  tipo: agente
  area:
  - devops
  - qa
  - backend
  fase:
  - despliegue
  - revision
  tecnologias:
  - github-actions
  - supabase
  - prisma
  - postgresql
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  grupo: "13"
  autor:
    nombre: Tobias Berger
    github: TotoBerger
  responsables:
  - TotoBerger
  madurez: usado-en-proyecto
  relacionados:
  - g15-release-criteria-evidence-checker
  - g11-revisar-despliegue
  - g08-release-checklist
  - g10-migration-safety-reviewer
  - g08-ready-for-prod-agent
---

# Checklist pre-deploy

Agente de CI de MicroChangas. Es un **reusable workflow** de GitHub Actions (`on: workflow_call`) que usa
`anthropics/claude-code-action` para llamar al modelo. Vive en un repo central de agentes y los repos de producto
(front y back) lo invocan con un caller de pocas líneas, así que cambiar un prompt o una compuerta no requiere
tocar los repos de producto.

**Ningún agente escribe en el repo de producto:** pide `contents: read` y su única salida son comentarios en la PR
y artifacts del run.

## Archivos

- [`pre-deploy.yml`](pre-deploy.yml): el workflow original, sin cambios. El prompt del agente está embebido en el
  paso `claude` (el repo de origen es privado y por eso los prompts no viven en archivos sueltos).

Origen: `.github/workflows/pre-deploy.yml` en https://github.com/MicroChangas/microchangas-agents (privado).

## Cómo funciona

- Compuerta: se omite salvo que la PR apunte a `production_branch` (por defecto `main`).
- Un script junta lo verificable sin modelo: estado de los checks, migraciones nuevas, si el schema se regeneró con ellas, si la PR documenta rollback.
- El modelo queda para lo que no es mecánico: si la migración rompe el código que ya está corriendo y si el rollback es creíble.
- Con `bloquear: true` el job falla si hay bloqueantes, para usarlo como required check.

## Cómo se instala

1. Copiá `pre-deploy.yml` a `.github/workflows/` de un repo central de agentes (o del mismo repo de producto).
2. Cargá el secret `CLAUDE_CODE_OAUTH_TOKEN` o `ANTHROPIC_API_KEY`. `RESEND_API_KEY` es opcional (manda el resumen por mail).
3. En el repo de producto, declaralo en `.github/workflows/agents.yml` (disparado por `pull_request`). Así está en MicroChangas (backend):

```yaml
  pre-deploy:
    # Se omite salvo en las PRs que apuntan a `main`, que es la rama que
    # dispara el deploy. `bloquear: false` por ahora: primero miramos si
    # dictamina bien, despues se decide si se vuelve un check obligatorio.
    permissions:
      contents: read
      pull-requests: write
      id-token: write
      checks: read
      actions: read
    uses: MicroChangas/microchangas-agents/.github/workflows/pre-deploy.yml@v1
    with:
      project_kind: backend
      production_branch: main
      bloquear: false
    secrets: inherit
```

Los `permissions` van sí o sí en el caller: un reusable workflow no puede pedir más de lo que le otorga quien lo
llama, e `id-token: write` nunca viene por defecto.

## Ejemplo de uso

**Pedido:** Se abre la PR de release `dev → main` en microchangas-backend con dos migraciones nuevas.

**Resultado:** El agente comenta un dictamen 'sale / no sale' con la tabla de evidencia (CI, migraciones, schema, rollback) y marca como bloqueante que una migración borra una columna que el código en producción todavía lee.
