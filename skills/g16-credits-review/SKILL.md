---
name: g16-credits-review
description: 'Checklist de revisión de la contabilidad de créditos de Eureka: la máquina de estados de la reserva de minteo, la concurrencia entre rutas y la reconciliación, los resultados ambiguos (timeouts, 502) y los préstamos de Turbo, con orden de prioridad y formato de reporte. Es el checklist que carga g16-eureka-revisor-creditos.'
metadata:
  tipo: skill
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
  requiere: []
  grupo: "16"
  autor:
    nombre: Valentino Gianuzzo
    github: ValentinoGianuzzo
  responsables:
  - ValentinoGianuzzo
  madurez: usado-en-proyecto
  relacionados:
  - g16-eureka-revisor-creditos
  - g16-confidentiality-review
  - g16-authorship-review
---

# Eureka credits review

Eureka sells patent credits through MercadoPago. Registering a patent consumes
one credit: the client reserves it, encrypts and uploads the document to
Arweave, and the backend signs and pays for the on-chain mint. The backend also
lends Turbo credits so the user's wallet can pay for the Arweave upload.

**Credits are the part of the product that is paid for.** A path that gives a
credit back after the patent was minted hands out free registrations; a path
that consumes a credit without minting charges the user for nothing. Both are
real money, and neither shows up as a crash: the flow looks fine and the
balance is wrong. Weight every finding against that.

Other reviewers own the rest. Encryption, key material, webhook signatures and
webhook idempotency belong to `confidentiality-review`. Contract logic belongs
to `authorship-review`. If the diff only touches those areas, say so and stop.

## Priority order

Review in this order and stop expanding scope once you have covered it:

1. The reservation state machine
2. Concurrency between routes and background reconciliation
3. Ambiguous outcomes (network errors, platform errors, missing receipts)
4. Turbo credit loans
5. Tests

## The reservation state machine

Start by writing down, for yourself, every state a reservation can be in and
every function that moves it. Read `supabase/schema.sql` for the SQL functions
(`begin_patent_mint`, `confirm_patent_mint`, `release_patent_mint` and any
other function that updates `patent_mint_reservations` or `users.credits`) and
`lib/server/patent/` for the callers.

For each transition, check:

- **Who can trigger it.** A route the user can call directly must not be able
  to move a reservation that the server is still working on. If the user can
  release a reservation while the server is minting it, the credit comes back
  and the mint still lands.
- **What state it requires.** Every transition must be a conditional update
  (`where status = '…'`) and must report whether it happened. A read-then-write
  in application code is a race.
- **Whether the credit moves exactly once.** Giving a credit back must be tied
  to the same conditional update that closes the reservation, so a retry or a
  second caller cannot refund twice.
- **Whether the return value is checked.** A transition that returns `false`
  means someone else already closed the reservation. Ignoring it hides the exact
  inconsistency this review exists to catch. At minimum it must be logged with
  the reservation id; if it can mean "minted without a consumed credit", say so.
- **Indexes and constraints.** The "one active reservation per document"
  guarantee must cover every active state, not just the first one.

## Concurrency

Look for these interleavings explicitly, step by step:

- The user calls the release route while the execute route waits for the
  transaction receipt.
- Two tabs reserve or execute the same document.
- Reconciliation (expired reservations, reservations without a confirmation)
  runs while a mint is still in flight. A reservation must not be refunded
  while the signed authorization can still be submitted on-chain: check the
  deadline used against the authorization `expiry`.
- A reservation expires during a slow upload and a new one is opened.

## Ambiguous outcomes

The client and the server must agree on which errors are definitive.

- Only an error that the server produced on purpose, with its own error code,
  may be treated as "the mint did not happen". A 502/503/504 from the platform,
  a timeout or a network failure means "unknown": the client must not release
  the reservation and must tell the user not to retry yet.
- On the server, an exception after the transaction was sent is not a revert.
  Only a confirmed revert may refund.
- When the result is unknown, something must eventually resolve it
  (reconciliation against the chain). Check that it compares against the wallet
  the mint was sent to, using the mint event, not the current owner — the NFT
  can be resold.

## Turbo credit loans

The backend shares Turbo credits with the user wallet before an upload.

- The loan must be sized from the bytes actually uploaded (the ciphertext, not
  the plaintext).
- A failed or abandoned upload must not leave an active loan that can be reused
  for another file.
- One active loan per user: superseding must be atomic.

## Tests

A change to the state machine needs tests for the failure paths, not only the
happy path: the release-during-mint race, a double refund attempt, a platform
error on the client, and reconciliation of a reservation still in flight. Unit
tests with mocked Supabase do not prove a SQL guard; ask for an integration
test against the real functions when a guard lives in SQL.

## How to report

- One comment per finding, anchored to the specific line.
- Open each with a severity tag: `[Crítico]`, `[Alto]`, `[Medio]`, `[Bajo]`.
- Describe the concrete interleaving that breaks the balance, step by step, and
  its consequence for Eureka: "the user gets the credit back and the patent is
  minted anyway", not "race condition".
- Propose a specific fix. If the fix is uncertain, say what needs to be checked.
- If a finding is a suspicion rather than a confirmed issue, say so explicitly.
- Do not comment on formatting, naming or style.
- If the diff touches none of the areas above, say the change is outside your
  scope in a single comment.

## Ejemplo de uso

**Pedido:** «Revisá este diff de `lib/server/patent/` con la skill de créditos.»

**Resultado:** Arma la lista de estados de la reserva y qué función mueve cada uno, y reporta cada hallazgo con severidad y la secuencia concreta que deja el saldo mal, paso a paso, con el arreglo propuesto.
