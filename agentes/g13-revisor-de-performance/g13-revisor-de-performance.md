---
name: g13-revisor-de-performance
description: 'Agente de GitHub Actions que busca en el diff de la PR los patrones que hacen lenta una app: N+1, queries dentro de loops, consultas sin acotar, payloads grandes y re-renders evitables en React. Se omite solo si el diff no toca services, repositories, controllers, Prisma o fetching. Análisis estático, no mide en runtime.'
metadata:
  tipo: agente
  area:
  - backend
  - frontend
  - qa
  fase:
  - revision
  tecnologias:
  - github-actions
  - nestjs
  - prisma
  - react
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
  - g13-optimizador-de-queries
  - g11-revisar-consultas
  - g11-revisar-react-query
---

# Performance

Agente de CI de MicroChangas. Es un **reusable workflow** de GitHub Actions (`on: workflow_call`) que usa
`anthropics/claude-code-action` para llamar al modelo. Vive en un repo central de agentes y los repos de producto
(front y back) lo invocan con un caller de pocas líneas, así que cambiar un prompt o una compuerta no requiere
tocar los repos de producto.

**Ningún agente escribe en el repo de producto:** pide `contents: read` y su única salida son comentarios en la PR
y artifacts del run.

## Archivos

- [`performance.yml`](performance.yml): el workflow original, sin cambios. El prompt del agente está embebido en el
  paso `claude` (el repo de origen es privado y por eso los prompts no viven en archivos sueltos).

Origen: `.github/workflows/performance.yml` en https://github.com/MicroChangas/microchangas-agents (privado).

## Cómo funciona

- Compuerta: filtra el diff (sin tests, estilos, docs ni config) contra una regex según `project_kind`. Si ningún archivo cae en rutas donde puede haber problemas de performance, se omite sin gastar tokens.
- En back mira `*.service.ts`, `*.repository.ts`, `*.controller.ts`, `prisma/` y `.sql`; en front `api/`, `hooks/`, `services/`, `queries/`, `store/` y `.tsx`.
- El modelo revisa solo esos archivos y comenta los hallazgos con su severidad.

## Cómo se instala

1. Copiá `performance.yml` a `.github/workflows/` de un repo central de agentes (o del mismo repo de producto).
2. Cargá el secret `CLAUDE_CODE_OAUTH_TOKEN` o `ANTHROPIC_API_KEY`. `RESEND_API_KEY` es opcional (manda el resumen por mail).
3. En el repo de producto, declaralo en `.github/workflows/agents.yml` (disparado por `pull_request`). Así está en MicroChangas (backend):

```yaml
  performance:
    # Se omite si el diff no toca services, repositories, controllers ni prisma.
    permissions:
      contents: read
      pull-requests: write
      id-token: write
      actions: read
    uses: MicroChangas/microchangas-agents/.github/workflows/performance.yml@v1
    with:
      project_kind: backend
    secrets: inherit
```

Los `permissions` van sí o sí en el caller: un reusable workflow no puede pedir más de lo que le otorga quien lo
llama, e `id-token: write` nunca viene por defecto.

## Ejemplo de uso

**Pedido:** Una PR agrega un endpoint que lista las changas con sus postulaciones.

**Resultado:** El agente comenta que el service hace un `findMany` de postulaciones dentro de un loop por changa (N+1) y que la lista no tiene paginación, con la línea y una alternativa con `include`.
