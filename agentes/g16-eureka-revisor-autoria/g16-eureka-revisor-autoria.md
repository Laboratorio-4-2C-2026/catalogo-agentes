---
name: g16-eureka-revisor-autoria
description: 'Agente de GitHub Actions (Claude Code Action) que revisa los PRs que tocan los contratos Solidity de Eureka y deja comentarios en línea, con severidad, sobre la integridad de la autoría on-chain: front-running del hash, registros duplicados, control de acceso y eventos. Usar en proyectos con un registro on-chain donde lo que importa es quién registró primero.'
metadata:
  tipo: agente
  area:
  - seguridad
  - backend
  fase:
  - revision
  tecnologias:
  - solidity
  - foundry
  herramientas:
  - claude-code
  requiere:
  - github
  grupo: "16"
  autor:
    nombre: Esteban Antonijevic
    github: eantonijevic
  responsables:
  - eantonijevic
  madurez: usado-en-proyecto
  relacionados:
  - g16-authorship-review
  - g16-eureka-revisor-confidencialidad
  - g08-security-reviewer
  - g11-security-agent
---
# eureka-authorship

Agente del proyecto Eureka (Laboratorio IV, grupo 16). En el repo de Eureka se llama `eureka-authorship`. Los archivos de esta carpeta (`.github/workflows/eureka-authorship.yml`) están copiados sin cambios y van en las mismas rutas del repo donde se instale.

## Para qué existe

Extraído sin cambios del comentario que abre el workflow:

```text
Agente de propósito específico: integridad de autoría on-chain.
Que nadie pueda robar, duplicar ni perder la prueba de quién registró primero.

La mitad off-chain —claves, cifrado, Arweave, RLS, pagos— es de
eureka-confidentiality. Los dos se reparten por `paths`, así que un PR que
toca solo contratos paga una sola review.
```

## Cómo corre

- **Se dispara:** cada PR (opened, ready_for_review, reopened) que toque `contracts/**`.
- **Herramientas del agente:** Read,Grep,Glob,Bash,mcp__github_inline_comment__create_inline_comment, con un tope de 30 turnos.
- **Necesita:**
  - El secreto `CLAUDE_CODE_OAUTH_TOKEN` en el repo.
  - La skill `.github/skills/authorship-review/SKILL.md` (en este catálogo: `g16-authorship-review`).
  - `.github/copilot-instructions.md` y `.github/instructions/contracts.instructions.md`: el contexto del producto y las reglas de contratos de Eureka. No se incluyen porque son propios del proyecto; hay que escribir los del repo donde se use.

## Prompt

Extraído sin cambios del paso de `anthropics/claude-code-action` en `.github/workflows/eureka-authorship.yml`.

```text
Revisá este pull request como revisor de integridad de autoría del
proyecto Eureka.

Tu alcance son **solo los archivos Solidity y los tests de Foundry**
del diff. Si el PR toca cifrado, claves, Arweave, Supabase o pagos,
ignoralo: eso lo revisa otro agente.

Leé y aplicá:
- .github/copilot-instructions.md — contexto del producto
- .github/instructions/contracts.instructions.md — reglas
  obligatorias de contratos
- .github/skills/authorship-review/SKILL.md — tu checklist, con el
  orden de prioridad de los hallazgos

Reglas de salida:
- Un comentario por hallazgo, anclado a la línea exacta.
- Prefijá cada uno con [Crítico], [Alto], [Medio] o [Bajo].
- Explicá la consecuencia concreta para Eureka, no la clase
  genérica de vulnerabilidad.
- Si es una sospecha y no un hallazgo confirmado, decilo.
- No comentes estilo ni naming.
- Si el diff no toca lógica de contratos, decilo en un solo
  comentario y terminá.
```

## Ejemplo de uso

**Pedido:** Se abre un PR que agrega en `contracts/src/` una segunda función que registra un hash en una sola transacción.

**Resultado:** El check **Eureka Authorship** deja un comentario por hallazgo anclado a la línea, por ejemplo `[Crítico]` porque un bot que mira el mempool puede registrar ese hash primero y quedar como autor, con el arreglo propuesto. Si el diff no toca lógica de contratos, deja un único comentario diciéndolo.
