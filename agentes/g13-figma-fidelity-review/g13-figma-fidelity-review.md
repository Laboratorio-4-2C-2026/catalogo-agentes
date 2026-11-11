---
name: g13-figma-fidelity-review
description: 'Agente de GitHub Actions para el frontend de MicroChangas que compara el nodo de Figma linkeado en el ticket de Multica contra los tokens de Tailwind y el código del componente (colores, padding, gap, radius, tipografía) y comenta las diferencias en la PR. Opcionalmente mide computed styles reales con Playwright.'
metadata:
  tipo: agente
  area:
  - frontend
  - diseno
  - qa
  fase:
  - revision
  tecnologias:
  - github-actions
  - react
  - tailwindcss
  - figma
  - playwright
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  - figma
  - multica
  grupo: "13"
  autor:
    nombre: Tobias Berger
    github: TotoBerger
  responsables:
  - TotoBerger
  madurez: usado-en-proyecto
  relacionados:
  - g11-revisar-diseno
  - g09-design-reviewer
  - g12-revisar-diseno
  - g03-figma-inspect-design
---

# Figma Fidelity

Agente de CI de MicroChangas. Es un **reusable workflow** de GitHub Actions (`on: workflow_call`) que usa
`anthropics/claude-code-action` para llamar al modelo. Vive en un repo central de agentes y los repos de producto
(front y back) lo invocan con un caller de pocas líneas, así que cambiar un prompt o una compuerta no requiere
tocar los repos de producto.

**Ningún agente escribe en el repo de producto:** pide `contents: read` y su única salida son comentarios en la PR
y artifacts del run.

## Archivos

- [`figma-review.yml`](figma-review.yml): el workflow original, sin cambios. El prompt del agente está embebido en el
  paso `claude` (el repo de origen es privado y por eso los prompts no viven en archivos sueltos).

Origen: `.github/workflows/figma-review.yml` en https://github.com/MicroChangas/microchangas-agents (privado).

## Cómo funciona

- Saca el `node-id` de Figma del ticket de Multica y baja ese nodo con la API de Figma (necesita `figma_token`).
- Por defecto la comparación es **estática**: JSON del nodo vs `tailwind.config.js` vs fuente del componente.
- Si se pasa `preview_path` (ej. `/register`), buildea la app y Playwright extrae computed styles reales del DOM.
- Guarda la evidencia como artifact del run y comenta en la PR qué valores no coinciden.

## Cómo se instala

1. Copiá `figma-review.yml` a `.github/workflows/` de un repo central de agentes (o del mismo repo de producto).
2. Cargá el secret `CLAUDE_CODE_OAUTH_TOKEN` o `ANTHROPIC_API_KEY`, `MULTICA_TOKEN` y la variable `MULTICA_WORKSPACE_ID` y `FIGMA_TOKEN` y la variable `FIGMA_FILE_KEY`. `RESEND_API_KEY` es opcional (manda el resumen por mail).
3. En el repo de producto, declaralo en `.github/workflows/agents.yml` (disparado por `pull_request`). Así está en MicroChangas (frontend):

```yaml
  figma:
    permissions:
      contents: read
      pull-requests: write
      issues: read
      id-token: write
    uses: MicroChangas/microchangas-agents/.github/workflows/figma-review.yml@v1
    with:
      figma_file_key: ${{ vars.FIGMA_FILE_KEY }}
      multica_workspace_id: ${{ vars.MULTICA_WORKSPACE_ID }}
      tokens_file: tailwind.config.js
      # Dejar vacio = comparacion estatica (Figma vs tokens vs codigo).
      # Poner una ruta, ej "/register", habilita computed styles reales del DOM.
      preview_path: ''
    secrets: inherit
```

Los `permissions` van sí o sí en el caller: un reusable workflow no puede pedir más de lo que le otorga quien lo
llama, e `id-token: write` nunca viene por defecto.

## Ejemplo de uso

**Pedido:** Se abre una PR de microchangas-frontend para el ticket de la pantalla de registro, que linkea su frame de Figma.

**Resultado:** El agente comenta en la PR una tabla de propiedades (color, padding, gap, radius, tipografía) con el valor de Figma, el del código y si coinciden, y deja el JSON del nodo como artifact.
