---
name: g16-eureka-revisor-confidencialidad
description: 'Agente de GitHub Actions (Claude Code Action) que revisa los PRs del front, la API, Supabase, los tests y los workflows de Eureka buscando fugas de claves o de contenido: cifrado en el cliente, derivación de claves, RLS y SECURITY DEFINER, autenticación de rutas, webhooks de MercadoPago y secretos alcanzables desde un workflow. Usar cuando los documentos se cifran en el cliente y lo que se sube no se puede borrar.'
metadata:
  tipo: agente
  area:
  - seguridad
  - backend
  - frontend
  fase:
  - revision
  tecnologias:
  - nextjs
  - typescript
  - supabase
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
  - g16-confidentiality-review
  - g16-eureka-revisor-autoria
  - g11-revisar-privacidad
  - g15-pr-code-reviewer
---
# eureka-confidentiality

Agente del proyecto Eureka (Laboratorio IV, grupo 16). En el repo de Eureka se llama `eureka-confidentiality`. Los archivos de esta carpeta (`.github/workflows/eureka-confidentiality.yml`) están copiados sin cambios y van en las mismas rutas del repo donde se instale.

## Para qué existe

Extraído sin cambios del comentario que abre el workflow:

```text
Agente de propósito específico: confidencialidad y acceso off-chain.
Que el contenido del documento y las claves no lleguen a nadie más que su
autor, sabiendo que lo que sube a Arweave no se borra nunca.

La mitad on-chain —front-running, hash duplicado, eventos— es de
eureka-authorship. Los dos se reparten por `paths`.

Las rutas son las de este repo: el front vive en la raíz (app/, lib/), no
bajo front/. supabase/ todavía no existe; está listado para que el día que
aparezcan las migraciones el agente se despierte solo.
```

## Cómo corre

- **Se dispara:** cada PR (opened, ready_for_review, reopened) que toque `app/**`, `lib/**`, `supabase/**`, `visual_pages/**`, `test/**`, `.github/workflows/**`.
- **Herramientas del agente:** Read,Grep,Glob,Bash,mcp__github_inline_comment__create_inline_comment, con un tope de 60 turnos.
- **Necesita:**
  - El secreto `CLAUDE_CODE_OAUTH_TOKEN` en el repo.
  - La skill `.github/skills/confidentiality-review/SKILL.md` (en este catálogo: `g16-confidentiality-review`).
  - `.github/copilot-instructions.md`, `.github/instructions/crypto.instructions.md` y `.github/instructions/data-api.instructions.md`: contexto y reglas propias de Eureka, no incluidos.

## Prompt

Extraído sin cambios del paso de `anthropics/claude-code-action` en `.github/workflows/eureka-confidentiality.yml`.

```text
Revisá este pull request como revisor de confidencialidad y acceso
del proyecto Eureka.

Tu alcance del diff son dos cosas:

1. **app/, lib/ y supabase/**: derivación de claves, cifrado,
   subidas a Arweave, policies y migraciones de Supabase, rutas de
   API, sesiones de Openfort y webhooks de MercadoPago.
2. **.github/workflows/**: a qué destinos externos escribe el
   workflow, qué secretos quedan alcanzables desde un push a una
   rama cualquiera, si usa `pull_request_target` con checkout del
   código del PR, y si las acciones de terceros están pineadas.

Si el PR toca contratos Solidity, ignoralos: eso lo revisa otro
agente.

Leé y aplicá:
- .github/copilot-instructions.md — contexto del producto
- .github/instructions/crypto.instructions.md y
  .github/instructions/data-api.instructions.md — reglas
  obligatorias; usá cada una según el `applyTo` que declara
- .github/skills/confidentiality-review/SKILL.md — tu checklist, con
  el orden de prioridad de los hallazgos

Reglas de salida:
- Un comentario por hallazgo, anclado a la línea exacta.
- Prefijá cada uno con [Crítico], [Alto], [Medio] o [Bajo].
- Explicá la consecuencia concreta para Eureka, no la clase
  genérica de vulnerabilidad.
- Si es una sospecha y no un hallazgo confirmado, decilo.
- No comentes estilo ni naming.
- Si el diff no toca nada sensible, decilo en un solo comentario y
  terminá.
```

## Ejemplo de uso

**Pedido:** Un PR agrega en `lib/` un `console.log` del objeto que se sube a Arweave y crea una tabla en `supabase/` sin habilitar RLS.

**Resultado:** El check **Eureka Confidentiality** deja comentarios en línea con severidad y la consecuencia para Eureka (por ejemplo, que el material que abre el ciphertext queda en los logs y el ciphertext está en Arweave para siempre) y otro sobre la tabla sin RLS, cada uno con el arreglo propuesto.
