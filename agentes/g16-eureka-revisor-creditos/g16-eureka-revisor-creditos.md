---
name: g16-eureka-revisor-creditos
description: 'Agente de GitHub Actions que revisa los PRs que tocan el minteo y los créditos de Eureka (rutas de reserva, ejecución y liberación, reconciliación, préstamos de Turbo y las funciones de Supabase que mueven el saldo) y comenta en línea, con severidad, las secuencias que regalan un crédito o lo cobran sin mintear. Usar cuando un producto vende créditos que se consumen con una operación on-chain.'
metadata:
  tipo: agente
  area:
  - backend
  - seguridad
  fase:
  - revision
  tecnologias:
  - supabase
  - typescript
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
  madurez: usado-en-proyecto
  relacionados:
  - g16-credits-review
  - g16-eureka-revisor-confidencialidad
  - g16-eureka-revisor-autoria
  - g08-security-reviewer
---
# eureka-credits

Agente del proyecto Eureka (Laboratorio IV, grupo 16). En el repo de Eureka se llama `eureka-credits`. Los archivos de esta carpeta (`.github/workflows/eureka-credits.yml`) están copiados sin cambios y van en las mismas rutas del repo donde se instale.

## Para qué existe

Extraído sin cambios del comentario que abre el workflow:

```text
Agente de propósito específico: la contabilidad de créditos.

Los créditos son lo que el usuario paga. Un camino que devuelve un crédito
después de mintear regala registros; uno que lo consume sin mintear le cobra
al usuario por nada. Ninguno de los dos rompe nada a la vista: el flujo anda
y el saldo queda mal.

Nace de la review de la PR #33 (EP-58): se podía liberar la reserva mientras
el servidor minteaba, y el crédito volvía con la patente ya registrada. Pasó
por Authorship y Confidentiality sin que lo marcaran, porque no es un problema
de contrato ni de cifrado: es una carrera entre estados de una reserva.

Firmas e idempotencia de los webhooks siguen siendo de eureka-confidentiality.
Este agente mira la máquina de estados de la reserva, la concurrencia entre
rutas y los préstamos de Turbo.
```

## Cómo corre

- **Se dispara:** cada PR (opened, ready_for_review, reopened) que toque las rutas de minteo y créditos (`app/api/mint/**`, `app/api/get/credits/**`, `app/api/mercadopago/**`), `lib/mint/**`, `lib/server/patent/**`, `lib/server/turbo/**`, `lib/turbo/**`, `lib/server/purchaseService.ts`, `lib/useCredits.ts`, `lib/useArweaveUpload.ts` o `supabase/**`.
- **Herramientas del agente:** Read,Grep,Glob,Bash(git diff:*),Bash(git log:*),Bash(git show:*),mcp__github_inline_comment__create_inline_comment, con un tope de 60 turnos.
- **Necesita:**
  - El secreto `CLAUDE_CODE_OAUTH_TOKEN` en el repo.
  - La skill `.github/skills/credits-review/SKILL.md` (en este catálogo: `g16-credits-review`).
  - `.github/copilot-instructions.md` y `.github/instructions/data-api.instructions.md`: el contexto del producto y las reglas de datos y API de Eureka. No se incluyen porque son propios del proyecto.

## Prompt

Extraído sin cambios del paso de `anthropics/claude-code-action` en `.github/workflows/eureka-credits.yml`.

```text
Revisá este pull request como revisor de créditos del proyecto
Eureka.

Tu alcance es la contabilidad de créditos: la máquina de estados de
las reservas de minteo, las rutas que reservan, ejecutan o liberan,
la reconciliación de reservas colgadas, los préstamos de Turbo y las
funciones de Supabase que mueven `users.credits`.

Fuera de tu alcance: cifrado, claves, firma e idempotencia de
webhooks (eso es de eureka-confidentiality) y la lógica de los
contratos (eureka-authorship). Si el diff solo toca eso, decilo en
un comentario y terminá.

Leé y aplicá:
- .github/copilot-instructions.md — contexto del producto
- .github/instructions/data-api.instructions.md — reglas
  obligatorias para app/, lib/ y supabase/
- .github/skills/credits-review/SKILL.md — tu checklist, con el
  orden de prioridad de los hallazgos

Antes de comentar, armá la lista de estados de la reserva y de qué
función mueve cada uno, leyendo `supabase/schema.sql` y
`lib/server/patent/` aunque no estén en el diff: la mayoría de los
bugs de créditos están en cómo un cambio interactúa con un estado
que ya existía.

Reglas de salida:
- Un comentario por hallazgo, anclado a la línea exacta.
- Prefijá cada uno con [Crítico], [Alto], [Medio] o [Bajo].
- Contá la secuencia concreta que deja el saldo mal, paso a paso, y
  su consecuencia para Eureka.
- Si es una sospecha y no un hallazgo confirmado, decilo.
- No comentes estilo ni naming.
```

## Ejemplo de uso

**Pedido:** Se abre un PR que deja al usuario liberar su reserva de minteo desde el cliente cuando la subida tarda.

**Resultado:** El check **Eureka Credits** comenta en la línea de la ruta, por ejemplo con `[Crítico]`, la secuencia paso a paso: el usuario libera mientras el servidor espera el recibo, el crédito vuelve y la patente se mintea igual. Propone atar la devolución al mismo `update … where status = …` que cierra la reserva.
