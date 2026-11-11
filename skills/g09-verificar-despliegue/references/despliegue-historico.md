# Deploy v1.1.0

Estado: completado y verificado. Backend y frontend publicados desde el tag remoto v1.1.0, SHA `976d714cbc5c885b68b176f30a8b82957ddf79a8`.

## Resultado final

| Componente | Resultado |
| --- | --- |
| Release | v1.1.0 / `976d714cbc5c885b68b176f30a8b82957ddf79a8` |
| CI | Aprobado para el SHA exacto, run `37564249866` |
| Render | `dep-db393ovlk1mc739rcd8g`, live, SHA exacto; finalizó 2026-10-07 15:45:19 America/Argentina/Salta |
| Backend URL | https://zervi-backend-dev.onrender.com |
| Health | HTTP 200, status UP |
| Categorías | HTTP 200, 8 categorías |
| CORS | Preflight HTTP 200, origen https://zervi-frontend-dev.pages.dev |
| Neon/Flyway | V1-V11 aplicadas correctamente; checksums coincidentes; sin migraciones pendientes |
| Pages | `27d1a3a0-8e79-4db4-ad10-2add894275b1`, production, success; branch main y SHA exacto; commit_dirty=false |
| Publicación Pages | 2026-10-07 15:52:17 America/Argentina/Salta |
| Frontend URL estable | https://zervi-frontend-dev.pages.dev |
| URL del deployment | https://27d1a3a0.zervi-frontend-dev.pages.dev |
| Artefactos publicados | HTML y SHA-256 de assets iguales a los del build validado |
| Terraform final | validate aprobado; plan sin cambios; no se ejecutó apply |
| Mercado Pago | Vendedor confirmado como test_user; collector `3732663182`; PAYMENTS_LIVE_MODE=true coincide con los pagos consultados; no se crearon pagos ni movimientos de dinero |

Pruebas realizadas: CI remoto, configuración remota, checksums e historial Flyway, migraciones en PostgreSQL temporal, build frontend, salud, categorías, preflight CORS, deployment canónico y comparación de HTML/assets. No se realizaron pruebas autenticadas de login, publicación, carga a R2, contrataciones ni compras completas con tarjetas; no presentar esas operaciones como verificadas de punta a punta.

Warnings pendientes: tres vulnerabilidades altas en dependencias de desarrollo del frontend y ninguna en dependencias de producción en la auditoría realizada; warnings del build por tamaño del bundle y configuración de Vite. No se alteraron dependencias ni código para este release.

Los cambios locales del usuario no se incluyeron ni se descartaron; se usó el checkout remoto independiente.

## Preparación previa

- Fecha: 2026-10-07, America/Argentina/Salta.
- Repositorio remoto: https://github.com/Agustin5421/Zervi.
- Tag remoto y main: `976d714cbc5c885b68b176f30a8b82957ddf79a8`.
- CI aprobado: https://github.com/Agustin5421/Zervi/actions/runs/37564249866.
- Jobs aprobados: Frontend, Backend, CI Success, Publish backend image.
- Checkout independiente: `/tmp/zervi-v1.1.0-deploy/source`, rama main y worktree limpio.
- Checkout original dev: preservado; no se incorporaron cambios locales al release.
- Infraestructura: terraform validate aprobado y plan sin cambios; no se ejecutó apply.
- Neon: V1-V8 aplicadas, sin errores; checksums coinciden con los archivos del tag.
- Migraciones pendientes: V9 bookings, V10 reviews, V11 payments.
- Migraciones probadas en PostgreSQL 17 temporal: base vacía V1-V11 y actualización V8 a V11.
- Frontend: npm ci y build aprobados con API y Auth0 del ambiente de nube. Artefactos en el checkout temporal.
- Auditoría npm: 3 vulnerabilidades altas en dependencias de desarrollo, 0 en producción; no se modificaron dependencias.
- Wrangler preparado en `/tmp/zervi-v1.1.0-deploy/wrangler-tools`, versión 4.148.0.
- Estado público previo: health UP, categorías HTTP 200, preflight CORS HTTP 200 con origen Pages, Pages HTTP 200. Las primeras consultas fallaron; las verificaciones posteriores pasaron.
- Render: `srv-dalhl6v40ujc73e2p530`, main, autoDeploy desactivado.
- Deploy Render previo: `dep-dao743uk1f9s73au0j3g`, live, commit `a244e2f3b454b7f12e22acaa0f273f2367771a8c`.
- Pages: `zervi-frontend-dev`, production_branch main.
- Deployment Pages previo: `b0eb8afb-1084-4ec2-863b-3a8e4fd1d613`.
- Decisión del usuario: habilitar Mercado Pago y completar variables manualmente con Save only.
- Restricción posterior del usuario: usar exclusivamente pruebas; no realizar pagos en producción. Antes de desplegar, confirmar que Access Token, collector y configuración Webhook pertenecen al ambiente/cuenta de prueba. PAYMENTS_LIVE_MODE solo compara el valor del recurso remoto; no configura un sandbox ni impide cobros. No fijarlo por la intención de usar pruebas ni por pagos de una cuenta diferente.

## Bloqueo inicial, resuelto al retomar

En la preparación inicial solo existían claves MERCADOPAGO_* que este tag no consume. Al retomar se verificaron las siguientes claves PAYMENTS_* completas en Render:

```text
PAYMENTS_GATEWAY=mercadopago
PAYMENTS_ACCESS_TOKEN
PAYMENTS_WEBHOOK_SECRET
PAYMENTS_COLLECTOR_ID
PAYMENTS_LIVE_MODE
PAYMENTS_SUCCESS_URL=https://zervi-frontend-dev.pages.dev
PAYMENTS_FAILURE_URL=https://zervi-frontend-dev.pages.dev
PAYMENTS_PENDING_URL=https://zervi-frontend-dev.pages.dev
PAYMENTS_NOTIFICATION_URL=https://zervi-backend-dev.onrender.com/api/payments/webhook
```

PAYMENTS_LIVE_MODE debe coincidir con el live_mode real de los pagos de la cuenta; no inferirlo.

## Verificaciones al retomar

- Tag remoto, main y checkout: `976d714cbc5c885b68b176f30a8b82957ddf79a8`; rama main y worktree limpio.
- CI para ese SHA: aprobado, run `37564249866`.
- Variables obligatorias de backend, pagos, Auth0, CORS y R2: presentes; secretos no expuestos.
- Vendedor Mercado Pago: confirmado por GET /users/me como test_user; ID coincide con collector `3732663182`.
- Pago consultado en modo de solo lectura: live_mode true y collector coincidente. PAYMENTS_LIVE_MODE=true en Render; pruebas sin movimientos de dinero.
- Terraform validate aprobado y plan sin cambios.
- Flyway previo: V1-V8, todos los checksums coincidentes y success=true.
- Salud previa: primer intento agotó 50 segundos; segundo intento health UP, categorías 200, CORS 200 y Pages 200.
- Render disparado: `dep-db393ovlk1mc739rcd8g`, createdAt `2026-10-07T18:39:31.904277Z`, SHA exacto.

## Procedimiento utilizado

La ejecución de este deploy fue autorizada por el usuario y ya se completó. Los pasos siguientes documentan el procedimiento; no iniciar otro deploy solo por leer este archivo.

1. Ejecutar `/tmp/zervi_v110_ops.py payment-config` y confirmar configuración completa sin imprimir secretos.
2. Ejecutar `/tmp/zervi_v110_ops.py render-trigger` (verifica SHA remoto, worktree, configuración y requisitos antes del POST).
3. Consultar `/tmp/zervi_v110_ops.py render-status` hasta live; abortar Pages si falla Render.
4. Verificar `/tmp/zervi_v110_ops.py verify-public` y `/tmp/zervi_v110_ops.py database`; confirmar V1-V11 sin errores.
5. Ejecutar `/tmp/zervi_v110_ops.py pages-deploy`.
6. Ejecutar `/tmp/zervi_v110_ops.py pages-verify`; verifica deployment canónico, SHA, HTML y hashes de assets.
7. Repetir salud/CORS y terraform plan. Documentar IDs y resultados.

Scripts y metadata operativos del deploy están en /tmp. Los dos scripts originales se preservaron también como copias exactas en `automation/deploy/legacy/`. El script de reanudación y verificaciones adicionales está en `automation/deploy/v1_1_0/zervi_v110_resume.py`. Estas copias mantienen las rutas originales y no preservan automáticamente los artefactos temporales. La propuesta de tres agentes está en `automation/PROPUESTA_AGENTES.md`. No contienen valores de secretos. Las credenciales se cargan en memoria desde infrastructure-updated/.env.local; no imprimir archivos de credenciales, tfvars ni state.
