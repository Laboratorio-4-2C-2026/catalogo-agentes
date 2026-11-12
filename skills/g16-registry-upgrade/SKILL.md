---
name: g16-registry-upgrade
description: 'Procedimiento paso a paso y verificado para hacer el upgrade del proxy UUPS de EurekaPatentRegistry en Avalanche Fuji: validación del storage layout contra lo desplegado, tests, simulación, upgrade con confirmación, chequeos on-chain, ABI y Openfort, y el registro en DEPLOYMENTS.md. Solo se activa si se la invoca explícitamente.'
disable-model-invocation: true
metadata:
  tipo: skill
  area:
  - backend
  - devops
  fase:
  - despliegue
  - mantenimiento
  tecnologias:
  - solidity
  - foundry
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
  - g16-authorship-review
  - g16-eureka-revisor-autoria
  - g16-eureka-post-deploy
---

# Upgrade of the EurekaPatentRegistry proxy

The registry lives behind an ERC-1967 proxy with UUPS (EP-35). An upgrade keeps
the address and the state, and replaces the logic. Done wrong, it corrupts the
state of every patent already registered — owners, keys, viewers — and that
cannot be undone by redeploying: the state lives in the proxy.

Talk to the user in Spanish (rioplatense), one step at a time. Do not move to
the next step until the current one passes. If a step fails, stop, explain what
failed and what it means, and do not look for a workaround on your own.

## Hard rules

- **Never run anything with `--broadcast`, `cast send` or any other
  transaction without the user's explicit confirmation in that same message.**
  Show the exact command first and wait for "sí".
- Never print, echo or `cat` `contracts/.env` or any private key. Commands read
  them through `vm.envUint` / environment variables; you only need to check
  that the variables are set (`test -n "$PRIVATE_KEY"`), not their value.
- Only Avalanche Fuji (chain id 43113). The scripts already refuse other chains;
  do not remove that check.

## Step 0 — Preconditions

1. `contracts/script/UpgradeRegistry.s.sol` and `contracts/DEPLOYMENTS.md`
   exist. If they don't, the registry is not upgradeable yet (EP-35 not merged):
   stop and say so.
2. From `contracts/DEPLOYMENTS.md`, read and show the user: proxy address,
   current implementation, owner of the proxy, and the commit that implementation
   was built from. If the commit is not recorded, ask the user for it: without it
   there is no reference to validate the storage layout against. (Step 8 records
   it for next time.)
3. Check that `forge` is installed, that `FUJI_RPC_URL`, `PRIVATE_KEY` and
   `REGISTRY_PROXY_ADDRESS` are set in `contracts/.env`, and that the proxy owner
   on-chain matches the address of the key the user will sign with:
   `cast call $REGISTRY_PROXY_ADDRESS "owner()(address)" --rpc-url $FUJI_RPC_URL`
   vs. `cast wallet address --private-key $PRIVATE_KEY` (do not print the key).
4. Ask what the upgrade changes and why, and whether there is a ticket. Write
   it down for the DEPLOYMENTS.md entry.

## Step 1 — Read the change

Diff `contracts/src/EurekaPatentRegistry.sol` between the deployed commit and
the working tree. Explain to the user, in plain words:

- Storage: list every state variable added, removed, reordered or retyped.
  **Only additions at the end are allowed.** Removing, reordering or changing
  the type of an existing variable shifts every slot after it and corrupts the
  state: stop.
- Inheritance: adding or reordering a parent contract is just as dangerous.
  OpenZeppelin 5 parents use namespaced storage (ERC-7201), but the contract's
  own variables do not.
- Initialization: new variables that need a value must be set in a
  `reinitializer(n)` function, with `n` one higher than the last version used,
  called in the same transaction through `UPGRADE_CALLDATA`. If the upgrade is
  done without that calldata, the reinitializer stays open and anyone can call
  it first and choose the values: it must also be `onlyOwner`. Never add logic
  to the constructor beyond `_disableInitializers()`.
- `immutable` values are baked into the implementation code, not the proxy:
  point it out if the change adds one.
- EIP-712: the domain name and version must not change, or every signature the
  backend produces stops being valid.

## Step 2 — Validate the storage layout

Follow the "Upgrade del Registry" section of `contracts/DEPLOYMENTS.md`:

1. `git worktree add <tmp>/wt-desplegado <deployed commit>` (initialize its
   submodules), then in `<tmp>/wt-desplegado/contracts`: `forge build` and copy
   `out/build-info` to `<tmp>/ref/desplegado`. Remove the worktree after.
   **The folder must be named `desplegado`:** the validator finds the reference
   contract by the folder name in `desplegado:EurekaPatentRegistry`.
2. In `contracts/`: `forge clean && forge build`, then
   `npx @openzeppelin/upgrades-core validate out/build-info --contract EurekaPatentRegistry --reference desplegado:EurekaPatentRegistry --referenceBuildInfoDirs <tmp>/ref/desplegado --unsafeAllow constructor,missing-initializer`.
   On Windows run `npx` from PowerShell, not Git Bash. Do not skip
   `forge clean`: after an incremental build the validator fails with "does not
   contain storage layout for all contracts", which is not a layout problem.
3. Anything other than a pass is a stop. Show the validator output as is.

## Step 3 — Tests

In `contracts/`: `forge test`, and the fork tests with `FUJI_RPC_URL` set
(`forge test --match-path 'test/*Fork*'`). All green, or stop. If the change
adds behavior, check there is at least one test for it that runs through the
proxy (the helper is `test/utils/EurekaDeployer.sol`).

## Step 4 — Simulate

Run the upgrade script **without** `--broadcast`:

`forge script script/UpgradeRegistry.s.sol --rpc-url $FUJI_RPC_URL --sender <owner>`

The script checks that the implementation changed and that marketplace, signer
and EIP-712 domain did not. Show the result and the estimated gas.

## Step 5 — Upgrade (needs confirmation)

Show the exact command with `--broadcast` and ask: "¿Ejecuto el upgrade en
Fuji?". Only after an explicit yes, run it. Save the implementation address and
the transaction hashes from the output.

## Step 6 — Verify on-chain

Read-only checks with `cast`, comparing against step 0:

- Implementation slot points to the new implementation:
  `cast storage $REGISTRY_PROXY_ADDRESS 0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc --rpc-url $FUJI_RPC_URL`
- `owner()`, `eurekaSignerAddress()`, `eurekaMarketplace()` and
  `DOMAIN_SEPARATOR()` unchanged; `paused()` false.
- One patent registered before the upgrade still returns the same data with
  `getPatent(bytes32)`.
- Verify the new implementation on Routescan with the `forge verify-contract`
  command in `DEPLOYMENTS.md`.
- If the user has the production variables locally, run
  `node scripts/postDeployCheck.mjs` from the repo root and show the table.

About `SmokeFuji.s.sol`: it mints and sells a real patent on Fuji and needs the
private key of the on-chain signer. If the signer is the Openfort backend
account (EP-58), there is no local key and the smoke cannot run; in that case
recommend registering one patent end-to-end from staging instead.

## Step 7 — ABI and Openfort (only if the ABI changed)

Compare `forge inspect EurekaPatentRegistry abi` with
`lib/abi/eurekaPatentRegistry.ts`. If they differ:

1. Regenerate `lib/abi/eurekaPatentRegistry.ts` as its header explains, keeping
   `as const`.
2. Update the ABI of the existing contract in Openfort — do not register a new
   one; the address did not change. The Openfort contract id of the proxy is
   recorded in `DEPLOYMENTS.md` (EP-35 registered it as
   `con_1f5616c6-5b0b-430d-8e73-f5daf9492ec9`). This needs the Openfort secret
   key: tell the user what to run instead of running it yourself.
3. `npx tsc --noEmit` and `npm run test:unit` must pass with the new ABI.

## Step 8 — Record it

Update `contracts/DEPLOYMENTS.md`: add a row to the implementations table with
address, block, commit, ticket and upgrade transaction, and mark the previous one
as replaced. Record the Openfort contract id if it was missing. Then propose a
branch and a PR with the ABI and documentation changes, with the tx hashes in
the body.

## If something goes wrong after the upgrade

As long as the new implementation did not write to new storage in a way the old
one cannot read, rolling back is another upgrade to the previous implementation
address (it is in the table). `UpgradeRegistry.s.sol` always deploys a new
implementation, so the rollback is a direct call from the owner:
`cast send $REGISTRY_PROXY_ADDRESS "upgradeToAndCall(address,bytes)" <previous implementation> 0x --rpc-url $FUJI_RPC_URL --private-key $PRIVATE_KEY`,
with the same confirmation rule as step 5, followed by the checks of step 6. If the state was already written in
a new format, do not roll back blindly: stop and escalate. Pausing (`pause()`,
owner only) stops registrations while it is analyzed.

## Ejemplo de uso

**Pedido:** «/registry-upgrade: hay que subir la implementación nueva del registro que se mergeó ayer.»

**Resultado:** Recorre los pasos verificando cada uno (cambio, storage layout, tests, simulación) y frena antes de mandar la transacción de upgrade hasta que se la confirmen; después verifica on-chain y deja la entrada en `contracts/DEPLOYMENTS.md`.
