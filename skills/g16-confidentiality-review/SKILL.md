---
name: g16-confidentiality-review
description: 'Checklist de revisión de confidencialidad off-chain para Eureka: cifrado en el cliente, derivación de claves, nonces, subidas irreversibles a Arweave, RLS y SECURITY DEFINER en Supabase, service_role, Openfort y webhooks de MercadoPago. Usar al revisar PRs de front, API o Supabase; es el checklist que carga g16-eureka-revisor-confidencialidad.'
metadata:
  tipo: skill
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
  requiere: []
  grupo: "16"
  autor:
    nombre: Esteban Antonijevic
    github: eantonijevic
  responsables:
  - eantonijevic
  madurez: usado-en-proyecto
  relacionados:
  - g16-eureka-revisor-confidencialidad
  - g16-authorship-review
  - g11-revisar-privacidad
---
# Eureka confidentiality review

Eureka registers proof-of-authorship for intellectual property. A document is
encrypted client-side, the ciphertext is stored permanently on Arweave, and the
hash is registered on Avalanche as an NFT. Credits are bought with MercadoPago.
Key derivation uses ICP vetKeys.

**Arweave storage is permanent and public.** A leaked key does not expose a
document temporarily — it exposes it forever, with no way to delete or rotate
the stored ciphertext. Weight every finding against that property: anything that
could put plaintext or key material where someone else can reach it is critical,
even when it looks minor in isolation.

You review the off-chain half only. Contract logic, front-running and
on-chain authorship belong to `authorship-review` — if the diff touches
Solidity, leave it alone.

## Priority order

Review in this order and stop expanding scope once you have covered it:

1. Key management and encryption boundaries
2. Access control (Supabase RLS, API route auth, Openfort sessions)
3. Payment and credit accounting
4. Everything else

## Key management and encryption

- **Encryption happens in the client.** Confirm the payload leaves the browser
  already encrypted. If ciphertext is produced server-side, the server can read
  the document, which contradicts the product claim that content is never
  revealed.
- Flag any code path where plaintext document content, a derived key or a
  vetKeys secret could reach a log, an error message, an analytics call or a
  database column. This includes `console.*` and objects passed whole to a
  logger.
- **Derivation inputs.** Check that they cannot be influenced by another user in
  a way that produces a colliding or predictable key. Concatenating
  user-controlled strings without an unambiguous separator is a collision
  waiting to happen.
- **Changing the derivation scheme is breaking.** Documents encrypted under the
  old scheme must remain decryptable. If a PR changes the domain, the inputs or
  the algorithm without versioning and a migration path, it is critical: that
  ciphertext is already on Arweave and cannot be re-uploaded.
- **Primitives.** A unique IV or nonce per operation from a CSPRNG. Reusing a
  nonce with the same key under AES-GCM breaks confidentiality and
  authentication at once. No hand-rolled cryptography, no `Math.random()` for
  key material.
- **Arweave uploads are irreversible.** Flag any path that could upload before
  encryption completes or before validation passes.

## Supabase

- **`SECURITY DEFINER` functions bypass RLS.** Every such function must pin
  `search_path` explicitly. An unpinned `search_path` is a privilege-escalation
  vector — treat it as critical.
- Any new table must have RLS enabled and at least one policy. A table with RLS
  enabled and no policy denies everything; a table without RLS enabled exposes
  everything. Both are bugs, and the second is a leak.
- Verify the `service_role` key is never referenced in client-reachable code. In
  Next.js, check it is not read in a component, a `NEXT_PUBLIC_` variable, or
  any module imported by the client bundle.
- The share-access feature grants read access to a lawyer or partner. Confirm
  grants are scoped to a single document, revocable, and enforced by a policy
  rather than by frontend filtering.

## API routes and Openfort

- Route handlers and server actions must authenticate independently. Do not rely
  on the caller being a logged-in UI.
- Openfort session tokens must be validated server-side before any privileged
  action.
- Flag any secret behind a `NEXT_PUBLIC_` prefix.

## MercadoPago and credits

- Webhook handlers must verify the request signature before acting on the
  payload. An unverified webhook lets anyone grant themselves credits.
- Webhooks are delivered more than once by design. Confirm the handler is
  idempotent — a replayed notification must not credit the account twice.
- Amounts, currency and product identity must be read from the MercadoPago
  response server-side, never from client-supplied values.
- Credit spending needs a transactional guard. Two concurrent registrations with
  one credit remaining must not both succeed. Look for a row-level lock, a
  conditional update or a database constraint — not a read-then-write.

## Tests

A change to key derivation needs a test that decrypts a document produced under
the previous scheme. Without it the regression surfaces in production, and by
then the ciphertext is on Arweave with no way back.

## How to report

- One comment per finding, anchored to the specific line.
- Open each with a severity tag: `[Crítico]`, `[Alto]`, `[Medio]`, `[Bajo]`.
- State the concrete consequence for Eureka, not the generic vulnerability
  class. Write "this key ends up in the logs, and the ciphertext it opens is on
  Arweave forever" rather than "sensitive data exposure".
- Propose a specific fix. If the fix is uncertain, say what needs to be checked.
- If a finding is a suspicion rather than a confirmed issue, say so explicitly
  instead of asserting it.
- Do not comment on formatting, naming or style.
- If the diff touches none of the areas above, say the change is outside your
  scope and keep the review short.

## Ejemplo de uso

**Pedido:** «Revisá con la skill de confidencialidad el PR que cambia la derivación de claves en `lib/`.»

**Resultado:** Hallazgos con severidad y consecuencia concreta. Si el esquema de derivación cambia sin versionado ni migración lo marca como crítico, porque el ciphertext ya está en Arweave, y pide un test que descifre un documento del esquema anterior.
