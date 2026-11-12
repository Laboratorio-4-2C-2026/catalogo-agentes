# Contexto de Eureka para escribir tickets

Base de contexto que usa `g16-eureka-ticket-readiness`. Copiala a
`docs/tickets/CONTEXTO.md` en la copia local de `Eureka-Lab2/EurekaProject`. El
agente la lee antes de cada ticket y propone cambios cuando aprende algo nuevo.
Última revisión: 2026-11-11.

## Qué es Eureka

Registro de autoría de documentos. El usuario sube un PDF, el PDF **se cifra en
el navegador**, se sube a **Arweave** (permanente y público) y se mintea un NFT
en **Avalanche** que deja el hash y el autor con fecha on-chain. El autor puede
compartir el documento con invitados por email. Cada registro consume un
**crédito**, y los créditos se compran con **MercadoPago**.

## Stack

- Next.js 16 (App Router) + React 19, TypeScript, Zustand, TanStack Query.
- Login y wallets: **Openfort** (embedded wallets con Shield; cuenta backend =
  signer del contrato).
- Datos: **Supabase** (`supabase/schema.sql`, RLS en todas las tablas).
- Almacenamiento: **Arweave** vía Turbo (ArDrive).
- Contratos: Solidity + Foundry en `contracts/`. `EurekaPatentRegistry` y
  `EurekaMarketplace` son proxies UUPS en Fuji (43113). Direcciones en
  `contracts/DEPLOYMENTS.md`.
- Pagos: MercadoPago (preferencias + webhook).
- Tests: Vitest (unit e integración), Cypress (E2E, con Mailosaur para los
  emails), `forge test`.
- Deploy: Vercel (producción con cada push a `master`).

## Mapa del código

| Área | Dónde | Notas |
|---|---|---|
| Pantallas | `visual_pages/` | `SignInView`, `WalletStatusView`, `BuyCreditsCard`, `SelectPdfCard`, `UploadToArweaveCard`, `OpenPatentCard`, `ShareByEmailCard`, `SharePatentWithViewer`, `EmailInvitationsCard` |
| Rutas de API | `app/api/` | `mint/{reserve,execute,release}`, `get/credits`, `mercadopago/{create-preference,webhook}`, `openfort/webhook`, `patent/{list,share,identity-key,register-key,viewer-invite/*}`, `cron/{reconcile-payments,reconcile-patent-mints,check-consistency}`, `kpi` |
| Cifrado | `lib/crypto/` | DEK, sealed box, envoltura de la clave de identidad, workers |
| Mint y compartir | `lib/mint/` | reserva → ejecución → liberación; compartir por email |
| Servidor | `lib/server/` | Openfort, pagos, reconciliación, sesión, rate limit, Supabase admin |
| Arweave | `lib/turbo/`, `lib/server/turbo/` | subida, créditos de Turbo |
| Base de datos | `supabase/schema.sql` | `users`, `purchase_history`, `patent_mint_reservations`, `wallet_creation_claims`, `turbo_credit_loans`, `waitlist`, `identity_key_vault`, `payment_orders`, `kpi_report_log`, `patent_viewer_invitations`, `api_rate_limit_hits` |
| Contratos | `contracts/src/`, `contracts/script/`, `contracts/test/` | upgrades con la skill `/registry-upgrade` |

## Zonas sensibles (cada una exige criterios propios en el ticket)

| Zona | Si el ticket toca… | Tiene que decir |
|---|---|---|
| Autoría | `contracts/` | qué pasa con un hash ya registrado, qué evento se emite, si hace falta upgrade |
| Confidencialidad | `lib/crypto/`, subida a Arweave, logs | que el documento sale cifrado del navegador; que nada sensible llega a logs; compatibilidad con documentos ya cifrados |
| Créditos y pagos | `lib/mint/`, `app/api/mint/`, `app/api/mercadopago/`, `payment_orders` | doble click, webhook repetido, pago en proceso, mint abandonado: nunca cobrar dos veces ni regalar un crédito |
| Datos | `supabase/` | tabla nueva con RLS y al menos una policy; `search_path` en `SECURITY DEFINER` |

## Documentos de referencia

`docs/AGENTES.md`, `docs/AUDITORIA.md`, `docs/COMPARTIR-POR-EMAIL.md`,
`docs/consistency.md`, `docs/CONTRATOS-ACTUALIZABLES.md`,
`docs/CRIPTOGRAFIA-POSCUANTICA.md`, `docs/REGISTRO-DE-PATENTES.md`,
`docs/SECURITY-PIPELINE.md`, `docs/testing-backlog.md`, `docs/THREAT-MODEL.md`.

## Convenciones

- Tickets en Jira: proyecto **EP**, `https://eureka-project.atlassian.net/browse/EP-NN`.
- Ramas: `feat/ep-NN-descripcion-corta` (también `fix/`).
- El PR nombra el ticket en el título o en el body y completa la Definition of
  Done del template (`.github/pull_request_template.md`).
- Review obligatoria por ruta según `.github/CODEOWNERS` (contratos, cifrado,
  `supabase/` y pagos siempre tienen review humana).
- Un ticket que no entra en un sprint se parte (ej. "EP-57 parte 1").

## Equipo

| Persona | Rol | GitHub |
|---|---|---|
| Carla Boggio | Lab 4 (dirección del proyecto) | `carBoggio` |
| Valentino Gianuzzo | Lab 4 (QA y contratos) | `ValentinoGianuzzo` |
| Esteban Antonijevic | Lab 4 (TL, seguridad, datos y pagos) | `eantonijevic` |
| Nicolás Ledesma (Nico) | Lab 2 (desarrollo) | `LedesmaNicolas` |
| Bautista (Bauti) | Lab 2 (desarrollo) | `bautista237` |

Los roles de Lab 4 rotan cada mes: confirmá quién es PM/PO este mes antes de
asignar la decisión de alcance.

## Glosario

- **Patente**: el documento registrado (NFT + ciphertext en Arweave).
- **Reserva de mint**: crédito apartado mientras se registra; se ejecuta o se libera.
- **Invitado / viewer**: alguien que recibió acceso a una patente por email.
- **Signer**: cuenta backend de Openfort autorizada en el Registry para mintear.
