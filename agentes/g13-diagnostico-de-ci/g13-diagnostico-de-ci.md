---
name: g13-diagnostico-de-ci
description: 'Agente de GitHub Actions que corre lint, build y tests de la PR y, si algo falla, diagnostica la causa y la comenta en la PR. Si todo pasa no llama al modelo. Pensado para los repos NestJS y React de MicroChangas, configurable por comandos.'
metadata:
  tipo: agente
  area:
  - qa
  - devops
  fase:
  - testing
  tecnologias:
  - github-actions
  - nodejs
  - typescript
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
  - g03-express-testing-agent
  - g15-test-quality-analyst
---

# Testing

Agente de CI de MicroChangas. Es un **reusable workflow** de GitHub Actions (`on: workflow_call`) que usa
`anthropics/claude-code-action` para llamar al modelo. Vive en un repo central de agentes y los repos de producto
(front y back) lo invocan con un caller de pocas líneas, así que cambiar un prompt o una compuerta no requiere
tocar los repos de producto.

**Ningún agente escribe en el repo de producto:** pide `contents: read` y su única salida son comentarios en la PR
y artifacts del run.

## Archivos

- [`testing.yml`](testing.yml): el workflow original, sin cambios. El prompt del agente está embebido en el
  paso `claude` (el repo de origen es privado y por eso los prompts no viven en archivos sueltos).

Origen: `.github/workflows/testing.yml` en https://github.com/MicroChangas/microchangas-agents (privado).

## Cómo funciona

- Instala dependencias (npm o pnpm) y corre `lint_cmd`, `build_cmd` y `test_cmd` en ese orden; los que van vacíos se saltean.
- Guarda los logs como artifact.
- Solo si algo falló (o con `analyze_on_success: true`) el modelo lee los logs y comenta la causa probable y cómo arreglarla.
- Al final refleja el estado real: si la suite falló, el check queda en rojo aunque el diagnóstico se haya publicado bien.

## Cómo se instala

1. Copiá `testing.yml` a `.github/workflows/` de un repo central de agentes (o del mismo repo de producto).
2. Cargá el secret `CLAUDE_CODE_OAUTH_TOKEN` o `ANTHROPIC_API_KEY`. `RESEND_API_KEY` es opcional (manda el resumen por mail).
3. En el repo de producto, declaralo en `.github/workflows/agents.yml` (disparado por `pull_request`). Así está en MicroChangas (backend):

```yaml
  testing:
    permissions:
      contents: read
      pull-requests: write
      id-token: write
    uses: MicroChangas/microchangas-agents/.github/workflows/testing.yml@v1
    with:
      project_kind: backend
      package_manager: pnpm
      # Sin --fix: en CI queremos que reporte, no que arregle en un runner efimero.
      lint_cmd: pnpm exec eslint "{src,apps,libs,test}/**/*.ts"
      build_cmd: pnpm run build
      test_cmd: pnpm test
    secrets: inherit
```

Los `permissions` van sí o sí en el caller: un reusable workflow no puede pedir más de lo que le otorga quien lo
llama, e `id-token: write` nunca viene por defecto.

## Ejemplo de uso

**Pedido:** Un push a una PR rompe dos tests de `changas.service.spec.ts`.

**Resultado:** El check queda en rojo y el agente comenta qué tests fallaron, la causa probable según el log y el cambio del diff que la introdujo.
