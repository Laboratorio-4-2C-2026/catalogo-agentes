---
name: g13-e2e-playwright
description: 'Agente de GitHub Actions para el frontend de MicroChangas que saca del ticket de Multica los recorridos de usuario, los escribe como specs de Playwright, levanta la app en el runner y los corre de verdad. Cuando uno falla, dictamina si está mal el test o está mal la app, sin ablandar aserciones. Propone los specs en un comentario y no commitea nada. Corre al abrir o marcar lista la PR, o con el label e2e.'
metadata:
  tipo: agente
  area:
  - qa
  - frontend
  fase:
  - testing
  tecnologias:
  - github-actions
  - playwright
  - react
  - vite
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
  madurez: probado
  relacionados:
  - g12-generar-tests-e2e
  - g02-e2e-test-writer
  - g10-playwright-matching-test-generator
  - g13-generador-de-unit-tests
  - g13-guiones-uat
  - g11-test-agent
---

# E2E Playwright

Agente de CI de MicroChangas. Es un **reusable workflow** de GitHub Actions (`on: workflow_call`) que usa
`anthropics/claude-code-action` para llamar al modelo. Vive en un repo central de agentes y los repos de producto
(front y back) lo invocan con un caller de pocas líneas, así que cambiar un prompt o una compuerta no requiere
tocar los repos de producto.

**Ningún agente escribe en el repo de producto:** pide `contents: read` y su única salida son comentarios en la PR
y artifacts del run.

## Archivos

- [`e2e.yml`](e2e.yml): el workflow original, sin cambios. El prompt del agente está embebido en el
  paso `claude` (el repo de origen es privado y por eso los prompts no viven en archivos sueltos).

Origen: `.github/workflows/e2e.yml` en https://github.com/MicroChangas/microchangas-agents (privado).

## Cómo funciona

- Compuerta: corre al abrir, reabrir o marcar lista la PR, o con el label `e2e`, y solo si hay contra qué correr (`base_url` de un entorno desplegado, o `serve_cmd` para levantar la app en el runner).
- Construye la app desde la PR y la sirve en el runner (`vite preview --host 127.0.0.1`). Instala Playwright con `npm i --no-save`, que no toca `package.json` ni el lockfile.
- **Planner:** saca del ticket los recorridos a cubrir. **Generator:** los escribe en `e2e-agente/specs/`, una carpeta que solo existe durante el job, y los corre. El backend no está levantado, así que la API se stubbea con `page.route()`; eso los hace determinísticos y permite probar lista vacía o error 500.
- **Healer** (solo dictamina): cuando un spec falla, dice si el error está en el test o en la app. Tiene prohibido ablandar una aserción o marcarla como skip: si la app está rota, lo reporta como hallazgo.
- Un paso posterior compara el árbol antes y después y avisa si tocó algo fuera de `e2e-agente/`. Sube el reporte de Playwright como artifact y publica los specs en un comentario para que un dev los copie.
- Solo se declara en el frontend: el backend no puede levantarse en el runner sin base de datos (se le puede pasar un `base_url` desplegado).

## Cómo se instala

1. Copiá `e2e.yml` a `.github/workflows/` de un repo central de agentes (o del mismo repo de producto).
2. Cargá el secret `CLAUDE_CODE_OAUTH_TOKEN` o `ANTHROPIC_API_KEY`, `MULTICA_TOKEN` y la variable `MULTICA_WORKSPACE_ID`. `RESEND_API_KEY` es opcional (manda el resumen por mail).
3. En el repo de producto, declaralo en `.github/workflows/agents.yml` (disparado por `pull_request`). Así está en MicroChangas (frontend):

```yaml
  e2e:
    # Planifica recorridos desde el ticket, los escribe como specs de Playwright
    # y los corre contra la app levantada en el propio runner. Playwright se
    # instala ahi con --no-save: no toca package.json ni el lockfile. Los specs
    # no se commitean, se proponen en un comentario.
    #
    # Se omite salvo al abrir o marcar lista la PR, o con el label `e2e`.
    permissions:
      contents: read
      pull-requests: write
      issues: read
      id-token: write
      actions: read
    uses: MicroChangas/microchangas-agents/.github/workflows/e2e.yml@v1
    with:
      project_kind: frontend
      multica_workspace_id: ${{ vars.MULTICA_WORKSPACE_ID }}
      package_manager: npm
      build_cmd: npm run build
      # --host 127.0.0.1 no es opcional: sin eso vite escucha en `localhost`,
      # que puede resolver solo a IPv6, y el sondeo del agente nunca conecta.
      serve_cmd: npx vite preview --port 4173 --strictPort --host 127.0.0.1
      serve_port: 4173
    secrets: inherit
```

Los `permissions` van sí o sí en el caller: un reusable workflow no puede pedir más de lo que le otorga quien lo
llama, e `id-token: write` nunca viene por defecto.

## Ejemplo de uso

**Pedido:** Se marca como lista para review la PR del ticket MIC-87 (postularse a una changa) en microchangas-frontend.

**Resultado:** El agente comenta los recorridos que sacó del ticket, el resultado de cada spec corrido contra la app de la PR (incluido el caso de error 500 de la API) y el código de los specs para que el dev los agregue; si uno falla, explica si el bug es de la app o del test.
