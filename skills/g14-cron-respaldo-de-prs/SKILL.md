---
name: g14-cron-respaldo-de-prs
description: Instala el respaldo programado de g14-bot-review-vaivendev; requiere el generador de ese bot. Es un cron de GitHub Actions que cada 6 horas busca PRs abiertos con review pedida al bot y sin su review para el último commit —los que tienen conflicto de merge y no disparan el evento pull_request— y les corre la review pendiente. Usala cuando el bot por eventos deja PRs sin revisar.
metadata:
  tipo: skill
  area:
  - devops
  - qa
  fase:
  - revision
  - despliegue
  tecnologias:
  - python
  - git
  metodologia:
  - agnostico
  herramientas:
  - claude-code
  requiere:
  - github
  grupo: '14'
  autor:
    nombre: Macarena Alimena
    github: MackyAlimena
  colaboradores: []
  responsables:
  - MackyAlimena
  madurez: usado-en-proyecto
  relacionados:
  - g14-bot-review-vaivendev
---

# Cron de respaldo de PRs

GitHub Actions **no dispara `pull_request` cuando el PR tiene conflicto de merge**. Un bot de review que sólo escucha eventos deja esos PRs sin revisar sin avisar. Este cron es la red: barre los PRs abiertos y corre la review que falta.

En VaiVen corre en el repo del bot (`vaiven-austral/vaivendev`) contra el repo del producto (`vaiven-austral/vaiven-app`): 143 corridas, todas exitosas, entre el 24/09 y el 03/11/2026.

## Archivos

Esta skill no trae copia propia: los dos archivos viven, en una sola copia, en la pieza `g14-bot-review-vaivendev`.

- `workflows/cron-respaldo.yml` del bot — workflow: `schedule` cada 6 h (`0 */6 * * *`) y `workflow_dispatch` para correrlo a mano. Hace checkout del repo del bot y, opcional, del kit de contexto; corre `cron-check.py`.
- `scripts/cron-check.py` del bot — la lógica, sin dependencias fuera de la stdlib y la CLI `gh`.

## Qué hace `cron-check.py`

1. Lista los PRs abiertos de `TARGET_REPO` con `gh pr list --json number,headRefOid,reviewRequests,title,headRefName`.
2. Se queda con los que tienen **review pedida a `BOT_LOGIN`**.
3. Para cada uno, busca en las reviews publicadas el marcador `<!-- code-reviewer-de-prs:sha:<SHA> -->` del **último commit**. Si está, lo omite: ese SHA ya se revisó.
4. A los pendientes les corre `scripts/generar-review.py --pr <n> --sha <sha> --repo <repo>`, el mismo generador que usa el workflow por evento.
5. Sale 0 si no hay pendientes o si terminó; 1 si no pudo listar PRs. Un error en un PR se imprime y sigue con el siguiente.

El marcador por SHA es lo que lo hace **idempotente**: si el evento ya revisó, el cron no duplica; si llega un commit nuevo, el cron lo ve como pendiente.

## Instalación

1. Desde `g14-bot-review-vaivendev`, copiá `workflows/cron-respaldo.yml` a `.github/workflows/` y `scripts/cron-check.py` a `scripts/` del repo del bot.
2. El generador de reviews (`scripts/generar-review.py`) tiene que estar en ese mismo `scripts/` y publicar el marcador con ese formato exacto. Viene con `g14-bot-review-vaivendev`. Si tu bot usa otro marcador, cambialo en los dos lados.
3. Cargá como **secretos** del repo: un token del bot con permiso de lectura de PRs y escritura de reviews en el repo destino, y las claves que necesite el generador (modelo, Jira). Variables de entorno, nunca en el código.
4. Ajustá `TARGET_REPO` y `BOT_LOGIN` en el `env` del paso.
5. Corré a mano una vez con *Run workflow* y leé el log: tiene que listar cada PR como «necesita review» u «Omitiendo».

## Cómo verificarlo

```bash
gh run list -R <org>/<repo-del-bot> --workflow cron-respaldo.yml -L 50
gh run view <id> -R <org>/<repo-del-bot> --log
```

Para probar el caso real: abrí un PR con conflicto, pedí review al bot, esperá el próximo disparo (o corrélo a mano) y comprobá que aparece la review con el marcador del SHA actual.

## Reglas

- **El bot comenta, no aprueba ni mergea.** La review se publica con `event="COMMENT"`; el merge lo hace una persona.
- Si `gh pr list` falla, el job falla en rojo: no lo tapes con `continue-on-error`, es la única señal de que el token venció.
- El cron programado de Actions puede demorarse; no lo uses para nada con plazo de minutos.

## Ejemplo de uso

**Pedido:** El bot de review no comentó el PR #57 porque tiene conflicto con main; dejá un respaldo que no dependa del evento.

**Resultado:** Instala el workflow y el script en el repo del bot, carga los secretos necesarios, lo corre a mano y muestra en el log que el PR #57 quedó como pendiente y recibió la review con el marcador de su último SHA.
