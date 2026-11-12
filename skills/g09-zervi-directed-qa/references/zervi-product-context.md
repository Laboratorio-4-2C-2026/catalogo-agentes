# Zervi Product Context

This is a static product and QA baseline, not proof of runtime behavior. It reflects source exploration on branch `ZRV-76-edit-service-frontend` at commit `e4714d59db321df466b1e8aadb225ef0c6b699b5`. Before relying on it, verify the current branch, commit, environment, enabled backend capabilities, and observed runtime behavior.

## Product Purpose

Zervi is an Argentine marketplace for discovering local service providers and hiring services from published listings.

## Actors

| Actor | Relevant boundary |
|---|---|
| Guest | Uses public discovery and may be redirected through authentication for protected actions. |
| Authenticated client | Uses client-facing actions such as favorites and bookings where available. |
| Provider | Manages a provider profile and owned services. |
| Service owner | May edit or deactivate only services they own. |
| Service non-owner | Must not receive owner-only controls or mutation access. |

There is no admin UI in this snapshot.

## Identity Invariants

- An Auth0 `sub`, a local user UUID, and a provider-profile UUID are distinct identifiers. Never substitute one for another.
- Never expose Auth0 subjects as display names.
- Database-backed roles and ownership are authoritative. Do not infer authorization from UI state, route shape, or unverified token claims alone.

## Main Journeys

- Public search, results, service detail, and provider profile.
- Authentication with return to the intended deep link.
- Provider onboarding and provider-profile maintenance.
- Service publication, editing, and deactivation.
- Favorites.
- Booking creation, list, detail, history, and ordered transitions when the backend is available in the active branch and environment.

## Cross-Cutting Invariants

- Enforce owner permissions at UI and API boundaries.
- Show only `ACTIVE` services in public discovery.
- Verify persistence after reload, revisit, and a new navigation path.
- Check stale-data, cache, back/forward navigation, and cross-page consistency.
- Preserve valid booking transition order and reject invalid or repeated transitions.
- Detect partial writes across multi-request saves and uploads; verify persisted state after failure or retry.
- Expect equivalent meaning and capability on mobile and desktop unless a deliberate difference is documented.
- Cover loading, error, empty, and success states with truthful feedback and recovery paths.
- Require accessible names, keyboard operation, focus behavior, and semantic controls.

## Severity Rubric

Assign severity from demonstrated or credible impact, not from ticket wording or priority:

| Severity | Impact |
|---|---|
| P0 | Safety, data, or security failure, or a total product blocker. |
| P1 | Core flow or authorization failure without a viable workaround. |
| P2 | Significant incorrect or degraded behavior with a workaround or limited scope. |
| P3 | Minor visual, copy, or usability issue. |

## Known Snapshot Limitations

- Favorites are memory-only and do not survive a full reload.
- Search aids such as suggestions or locations are static.
- Provider gallery media is mocked.
- There is no real reviews domain.
- The provider-profile hire call to action is incomplete.
- Service-management and deactivation UI is incomplete.
- Service editing excludes images.
- Footer links are placeholders.
- Booking frontend code may exist while its backend is unavailable, depending on branch and environment.

Treat these as known limitations, not automatic defects. Report contradictions, misleading behavior, or requirements that promise more than the limitation allows.

## Risk And Browser Safety

- Use only origins explicitly approved by the user. Do not follow or probe other pages or origins.
- Never log, quote, screenshot, or export access tokens, refresh tokens, cookies, authorization headers, or localStorage contents.
- Visit external Auth0 pages only when the user permits that origin.
- Default to read-only exploration. Mutations require explicit authorization and disposable test data.
- The first successful authentication can provision a local database user; treat first login as a mutation.
- Never use real personal data. Use clearly synthetic names, contact details, media, and booking content.

## Source Orientation

Use these paths only as concise orientation in operator-supplied implementation, not bundled dependencies; verify current files before making claims:

- Frontend: `frontend/src/routes`, `frontend/src/pages`, `frontend/src/services`, `frontend/src/auth`
- Backend: `backend/src/main/kotlin/zervi/backend/{security,listing,provider,user}`
- Database: `backend/src/main/resources/db/migration`

Snapshot stack: React 19, Vite, React Router, React Query, Kotlin, Spring Boot, Auth0, PostgreSQL, Flyway, and R2. No runtime journey was executed to produce this document.
