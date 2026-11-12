---
name: g16-eureka-revisor-tests
description: 'Agente de GitHub Actions que, en los PRs que cambian lógica de Eureka, busca el comportamiento nuevo que ningún test ejercita (caminos de plata o autoría, ramas de falla, guardas de SQL probadas solo con mocks, arreglos de bugs sin test) y propone el test que falta con archivo, nombre, setup, acción y resultado esperado.'
metadata:
  tipo: agente
  area:
  - qa
  fase:
  - revision
  - testing
  tecnologias:
  - typescript
  - foundry
  - supabase
  herramientas:
  - claude-code
  requiere:
  - github
  grupo: "16"
  autor:
    nombre: Valentino Gianuzzo
    github: ValentinoGianuzzo
  responsables:
  - ValentinoGianuzzo
  madurez: experimental
  relacionados:
  - g16-tests-review
  - g08-qa-engineer
---
# eureka-tests

Agente del proyecto Eureka (Laboratorio IV, grupo 16). En el repo de Eureka se llama `eureka-tests`. Los archivos de esta carpeta (`.github/workflows/eureka-tests.yml`) están copiados sin cambios y van en las mismas rutas del repo donde se instale.

**Estado:** ya está en `master` de Eureka, pero todavía no se abrió ningún PR que lo despierte, así que no corrió en el proyecto.

## Para qué existe

Extraído sin cambios del comentario que abre el workflow:

```text
Agente de propósito específico: lo que el PR agrega y ningún test ejercita.

Eureka DoD verifica que el PR muestre evidencia de "Tests pasando", pero que
pasen no dice nada de lo que no se prueba. Un PR puede sumar un camino de
falla, una ruta o una función del contrato y dejar todos los tests en verde.
Este agente busca ese comportamiento nuevo sin cobertura y propone los casos
que faltan, empezando por los caminos que mueven plata o autoría.

No juzga si los tests pasan (eso es DoD) ni busca bugs en el código (eso es
de los otros revisores).
```

## Cómo corre

- **Se dispara:** cada PR (opened, ready_for_review, reopened) que toque `lib/`, `app/api/`, `contracts/src/` o `supabase/`.
- **Herramientas del agente:** Read,Grep,Glob,Bash(git diff:*),Bash(git log:*),Bash(git show:*),mcp__github_inline_comment__create_inline_comment, con un tope de 60 turnos.
- **Necesita:**
  - El secreto `CLAUDE_CODE_OAUTH_TOKEN` en el repo.
  - La skill `.github/skills/tests-review/SKILL.md` (en este catálogo: `g16-tests-review`).
  - `.github/copilot-instructions.md`: el contexto del producto. No se incluye porque es propio del proyecto.

## Prompt

Extraído sin cambios del paso de `anthropics/claude-code-action` en `.github/workflows/eureka-tests.yml`.

```text
Revisá este pull request como revisor de cobertura de tests del
proyecto Eureka.

Tu alcance es el comportamiento que el PR agrega o cambia y que
ningún test ejercita: rutas, funciones, ramas de error, reverts y
guardas de SQL nuevas o modificadas.

Fuera de tu alcance: si los tests pasan (eureka-dod) y si el código
tiene bugs (los otros revisores). Si el diff solo toca tests, docs,
estilos o configuración, decilo en un comentario y terminá.

Leé y aplicá:
- .github/copilot-instructions.md — contexto del producto
- .github/skills/tests-review/SKILL.md — tu checklist: dónde vive
  cada tipo de test, el orden de prioridad y qué cuenta como
  faltante

Antes de marcar un caso como faltante, buscalo en `test/`,
`contracts/test/` y `cypress/e2e/` aunque esos archivos no estén en
el diff: muchas veces ya está cubierto por un test existente.

Reglas de salida:
- Un comentario por caso faltante, anclado a la línea del
  comportamiento sin test.
- Prefijá cada uno con [Crítico], [Alto], [Medio] o [Bajo].
- Proponé el test concreto: archivo, nombre, y una línea para el
  setup, la acción y el resultado esperado.
- Si no estás seguro de que falte (puede estar cubierto
  indirectamente), decilo.
- No comentes estilo ni naming.
```

## Ejemplo de uso

**Pedido:** Se abre un PR que agrega un `catch` en la ruta de compra de créditos para cuando MercadoPago responde 500.

**Resultado:** El check **Eureka Tests** comenta en la línea del `catch` que ningún test llega a esa rama y propone el test concreto: archivo, nombre, y una línea para el setup, la acción y el resultado esperado. Si puede estar cubierto indirectamente, lo dice.
