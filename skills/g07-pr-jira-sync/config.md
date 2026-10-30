# Configuración — g07-pr-jira-sync

Datos del proyecto. No hay secretos acá: el script usa el `gh` ya autenticado, en modo solo lectura.

- **Proyecto**: `<nombre del proyecto>`
- **Repo de GitHub**: `<org>/<repo>`
- **Site de Jira**: `<tuequipo>.atlassian.net`
- **Project key**: `<KEY>`
- **Estado "en curso"**: `In Progress`
- **Estado "en revisión"**: `In Review`
- **Ventana para PRs mergeados/cerrados**: `14` días (`--days`). Cubre las dos últimas entregas semanales.
- **Umbral de PR viejo**: `3` días sin actividad (`--stale-days`). Con entregas semanales, un PR quieto 3 días ya come la mitad del ciclo.
- **Variable de entorno del webhook** (solo si se pide mandar a Discord): `DISCORD_WEBHOOK_URL`
