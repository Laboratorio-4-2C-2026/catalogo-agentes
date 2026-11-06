---
name: g16-authorship-review
description: 'Checklist de revisión de integridad de autoría on-chain para Eureka: front-running del hash, registro duplicado, todos los caminos de registro, control de acceso y CEI, firmas EIP-712, eventos y tests de Foundry, con orden de prioridad y formato de reporte. Usar al revisar PRs de contratos Solidity; es el checklist que carga g16-eureka-revisor-autoria.'
metadata:
  tipo: skill
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
  requiere: []
  grupo: "16"
  autor:
    nombre: Esteban Antonijevic
    github: eantonijevic
  responsables:
  - eantonijevic
  madurez: usado-en-proyecto
  relacionados:
  - g16-eureka-revisor-autoria
  - g16-confidentiality-review
  - g08-classify-vulnerability
---
# Eureka authorship review

Eureka registers proof-of-authorship for intellectual property. A document is
encrypted client-side, the ciphertext is stored permanently on Arweave, and the
hash is registered on Avalanche as an NFT.

**The on-chain timestamp is the product.** Anything that lets an attacker claim
an earlier registration than the real author defeats the entire purpose of the
system, even when no funds are at risk. Weight every finding against that
property: a bug that lets someone steal or destroy authorship is critical even
when it looks minor in isolation.

You review the on-chain half only. Key management, encryption, Arweave uploads,
Supabase policies and payments belong to `confidentiality-review` — if the diff
touches those, leave them alone.

## Priority order

Review in this order and stop expanding scope once you have covered it:

1. Authorship integrity (front-running, duplicate registration, timestamp)
2. Access control and reentrancy on state-mutating functions
3. Events and everything else

## Authorship integrity

- **Hash front-running.** A pending transaction carrying a document hash is
  visible in the mempool before it is mined. If a bot can read the hash and
  submit its own registration first, it becomes the recorded author. Check
  whether registration uses a commit-reveal scheme or another mitigation. Flag
  any single-transaction registration path as critical.
- **Duplicate hash registration.** Determine what happens when the same hash is
  registered twice. Silently minting a second NFT for an existing hash creates
  two competing authorship claims for identical content. Overwriting the
  existing author is worse: it makes "who registered first" mutable.
- **Every registration path.** If more than one function writes the registry,
  check each one. Fixing a single path and leaving another open is not a fix.
- **Timestamp reliance.** `block.timestamp` is manipulable by validators within
  a small window. Confirm the proof is the block itself, and that no comparison
  logic assumes second-level precision.
- **Losing authorship.** A transfer to the zero address, or any path that leaves
  a hash owned by an address nobody controls, orphans the record permanently —
  the Arweave ciphertext behind it cannot be re-registered.

## Access control and reentrancy

- Every state-mutating `external` or `public` function needs an explicit
  modifier or role check. Flag any that changes state without one. Do not assume
  a function is safe because it is only called from the frontend.
- **Checks-Effects-Interactions.** Verify state is written before any external
  call, especially where credit burning and minting happen in the same
  transaction. Flag any external call followed by a state write.
- Unchecked return values from low-level calls. A failed transfer that still
  registers the document is a silent inconsistency.
- Any address the caller supplies and the contract then trusts — a treasury, a
  beneficiary, a recipient. If the caller picks it, the protocol does not
  control it.
- Missing zero-address checks, unbounded loops over user-supplied arrays, and
  `tx.origin` used for authentication.

## Signatures and upgrades

- If EIP-712 or meta-transactions are used, confirm the signed payload includes
  a nonce, the chain ID and the verifying contract address. Missing any of the
  three enables replay.
- If a proxy pattern is used, check storage layout ordering against the previous
  version and confirm the initializer cannot be called twice.

## Events

Every registration must emit an event with the hash and owner. The indexer and
any dispute evidence depend on it. Transfers need their own event with `from`
and `to`.

## Tests

When Foundry tests are present, check that they cover the failure paths, not
only the happy path. A registration test that never asserts on a rejected
duplicate is incomplete.

## How to report

- One comment per finding, anchored to the specific line.
- Open each with a severity tag: `[Crítico]`, `[Alto]`, `[Medio]`, `[Bajo]`.
- State the concrete consequence for Eureka, not the generic vulnerability
  class. Write "an attacker who watches the mempool can register this hash first
  and become the recorded author" rather than "front-running risk".
- Propose a specific fix. If the fix is uncertain, say what needs to be checked.
- If a finding is a suspicion rather than a confirmed issue, say so explicitly
  instead of asserting it.
- Do not comment on formatting, naming or style.
- If the diff touches no contract logic, say the change is outside your scope
  and keep the review short.

## Ejemplo de uso

**Pedido:** «Revisá este diff de `contracts/src/EurekaPatentRegistry.sol` con la skill de autoría.»

**Resultado:** Hallazgos en orden de prioridad (integridad de autoría, control de acceso y reentrancia, eventos), cada uno con `[Crítico]`, `[Alto]`, `[Medio]` o `[Bajo]`, la consecuencia concreta para Eureka y el arreglo propuesto. Si el diff no toca lógica de contratos, lo dice y termina.
