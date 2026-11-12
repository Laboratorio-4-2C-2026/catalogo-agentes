---
name: g16-ux-review
description: 'Checklist de revisión de textos, estados de la interfaz y accesibilidad básica para Eureka: feedback durante operaciones lentas o que fallan, mensajes de error, jerga, accesibilidad verificable en el código y consistencia. Es el checklist que carga g16-eureka-revisor-ux.'
metadata:
  tipo: skill
  area:
  - frontend
  - diseno
  fase:
  - revision
  tecnologias:
  - react
  - nextjs
  herramientas:
  - claude-code
  requiere: []
  grupo: "16"
  autor:
    nombre: Valentino Gianuzzo
    github: ValentinoGianuzzo
  responsables:
  - ValentinoGianuzzo
  madurez: experimental
  relacionados:
  - g16-eureka-revisor-ux
  - g01-screen-state-ux-reviewer
  - g07-auditoria-accesibilidad
---

# Eureka UX review

Eureka's users register intellectual property. Most of them do not know what a
wallet, a hash or a mint is, and they should not need to. Under the hood every
registration encrypts a document, uploads it to Arweave and writes to a
blockchain, and every one of those steps can be slow or fail. A user who sees
jargon, a frozen button or an error that does not say what to do next gives up,
and a registration that is abandoned halfway may already have spent a credit.

This review looks at what the user reads and sees. It does not look at
security, credits or contract logic: other reviewers own those. If the diff
touches no user-facing code, say so in a single comment and stop.

## Priority order

1. Feedback during slow or failing operations
2. Error messages
3. Jargon in user-facing text
4. Accessibility basics
5. Consistency of the copy

## Feedback during slow or failing operations

For every action that calls the API, signs, uploads or waits for the chain:

- **Loading state.** The control that started it is disabled or shows progress
  while it runs. A clickable button during a mint invites a double submit.
- **Long waits.** Uploads and on-chain confirmations take seconds or minutes.
  The user must see that something is happening and, if possible, which step it
  is on ("Cifrando…", "Subiendo…", "Registrando…").
- **Success.** The user can tell it worked and what comes next.
- **Failure.** Every `catch` or error branch ends in something the user sees.
  A failure that only goes to `console.error` is a finding.
- **Empty states.** A list that can be empty says so and offers the next
  action ("Todavía no registraste patentes" + the button to register one).

## Error messages

A good error says what happened in user terms and what to do now. Flag:

- Raw technical errors shown to the user: `error.message` from a library, HTTP
  codes, revert reasons, stack traces.
- Messages that do not say what to do ("Ocurrió un error").
- Messages that invite a retry when retrying is unsafe. When the result of a
  mint is unknown (timeout, 502), the user must be told to wait, not to retry.

## Jargon

The product copy is in Spanish with voseo ("Seleccioná", "Comprá"). Flag text
the user reads that exposes implementation details without explaining them:

- wallet / address / dirección 0x…, hash, bytes32, mint / mintear, NFT,
  transacción, gas, firma, nonce, keypair, clave pública, DEK, ciphertext,
  Arweave, Turbo, Openfort, Avalanche, Fuji, contrato, token id.

Some of these are unavoidable in specific places (a certificate that shows the
hash on purpose, a settings page that shows the wallet). In those cases the
term must come with a short explanation in the same sentence or a tooltip.
Propose the user-facing wording, for example "registrar" instead of "mintear",
"tu cuenta" instead of "tu wallet".

Text that is only for developers (logs, `console.*`, comments, test names) is
out of scope.

## Accessibility basics

Only what can be verified from the code:

- Inputs have an associated label (`<label htmlFor>`, `aria-label` or
  `aria-labelledby`). A placeholder is not a label.
- Icon-only buttons and links have an accessible name.
- Images that carry meaning have `alt`; decorative ones have `alt=""`.
- Clickable elements are buttons or links, not `div`s with `onClick`.
- Status that changes without a page load (upload progress, "copiado", errors)
  is announced (`aria-live`, `role="status"` or `role="alert"`).
- Modals move focus inside, can be closed with the keyboard and return focus.
- State is not conveyed by color alone (a red border with no text).

Do not guess color contrast from class names.

## Consistency

Flag when the same thing is named two ways in the diff or against the existing
screens (for example "patente" and "registro" for the same object, or "créditos"
and "saldo"), and when a new string switches from voseo to tú or usted.

## How to report

- One comment per finding, anchored to the specific line.
- Open each with a severity tag: `[Crítico]`, `[Alto]`, `[Medio]`, `[Bajo]`.
  - `[Crítico]`: the user can lose money or a registration because of what the
    screen shows (a retry invited on an unknown mint result, a double submit).
  - `[Alto]`: a failure the user never sees, or a step with no feedback at all.
  - `[Medio]`: jargon or an error that does not say what to do.
  - `[Bajo]`: accessibility details and copy consistency.
- Describe what the user sees and why it is a problem for them, then propose
  the exact text or the specific change.
- If a finding is a suspicion rather than a confirmed issue, say so.
- Do not comment on visual design taste, formatting, naming or code style.

## Ejemplo de uso

**Pedido:** «Revisá con la skill de UX esta pantalla nueva de registro.»

**Resultado:** Hallazgos en orden de prioridad (feedback, errores, jerga, accesibilidad, consistencia), cada uno con severidad, qué ve el usuario y el texto o cambio concreto que propone.
