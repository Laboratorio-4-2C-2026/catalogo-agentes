---
name: g13-generador-de-unit-tests
description: 'Agente de GitHub Actions que detecta código nuevo de la PR sin tests al lado, escribe los unit tests, los corre de verdad en el runner hasta que pasen y los publica en un comentario para que un dev los pegue. No commitea: solo tiene permiso de lectura y verifica que no haya tocado código de producción.'
metadata:
  tipo: agente
  area:
  - qa
  - backend
  - frontend
  fase:
  - testing
  tecnologias:
  - github-actions
  - jest
  - vitest
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
  - g08-backend-test-engineer
  - g03-express-test-builder-agent
  - g11-test-agent
  - g13-diagnostico-de-ci
---

# Generador de unit tests

Agente de CI de MicroChangas. Es un **reusable workflow** de GitHub Actions (`on: workflow_call`) que usa
`anthropics/claude-code-action` para llamar al modelo. Vive en un repo central de agentes y los repos de producto
(front y back) lo invocan con un caller de pocas líneas, así que cambiar un prompt o una compuerta no requiere
tocar los repos de producto.

**Ningún agente escribe en el repo de producto:** pide `contents: read` y su única salida son comentarios en la PR
y artifacts del run.

## Archivos

- [`unit-tests.yml`](unit-tests.yml): el workflow original, sin cambios. El prompt del agente está embebido en el
  paso `claude` (el repo de origen es privado y por eso los prompts no viven en archivos sueltos).

Origen: `.github/workflows/unit-tests.yml` en https://github.com/MicroChangas/microchangas-agents (privado).

## Cómo funciona

- Compuerta: corre al abrir o marcar lista la PR (o con el label `tests`), y solo si hay archivos agregados o modificados sin un `.spec`/`.test` al lado. Excluye DTOs, entities, módulos, configs, stories, etc.
- Escribe los tests en el checkout efímero del runner y los corre archivo por archivo (`jest` con pnpm, `vitest` con npm, o `test_one_cmd`).
- Un paso posterior compara el árbol antes y después: si el agente tocó algo que no es un test, lo avisa en la PR.
- Publica los tests que pasan en un comentario. No hace commit ni push.

## Cómo se instala

1. Copiá `unit-tests.yml` a `.github/workflows/` de un repo central de agentes (o del mismo repo de producto).
2. Cargá el secret `CLAUDE_CODE_OAUTH_TOKEN` o `ANTHROPIC_API_KEY`. `RESEND_API_KEY` es opcional (manda el resumen por mail).
3. En el repo de producto, declaralo en `.github/workflows/agents.yml` (disparado por `pull_request`). Así está en MicroChangas (backend):

```yaml
  unit-tests:
    # Se omite salvo al abrir o marcar lista la PR, y solo si hay codigo nuevo
    # sin tests al lado. Escribe los tests en el runner y los corre ahi: no
    # commitea nada, los propone en un comentario para que un dev los pegue.
    permissions:
      contents: read
      pull-requests: write
      id-token: write
      actions: read
    uses: MicroChangas/microchangas-agents/.github/workflows/unit-tests.yml@v1
    with:
      project_kind: backend
      package_manager: pnpm
    secrets: inherit
```

Los `permissions` van sí o sí en el caller: un reusable workflow no puede pedir más de lo que le otorga quien lo
llama, e `id-token: write` nunca viene por defecto.

## Ejemplo de uso

**Pedido:** Se abre una PR que agrega `postulaciones.service.ts` sin su spec.

**Resultado:** El agente comenta un `postulaciones.service.spec.ts` que ya corrió en verde en el runner, listo para que el dev lo copie a su branch.
