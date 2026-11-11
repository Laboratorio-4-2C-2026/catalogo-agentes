# Bot de review de PRs (vaivendev)

Revisor automático de Pull Requests que corre en **GitHub Actions**, fuera del repo de producto. Comenta; no aprueba, no commitea y no mergea. El merge lo hace una persona.

## Arquitectura

| Pieza | Dónde vive | Qué hace |
|---|---|---|
| Timbre: [`workflows/pedir-review.yml`](workflows/pedir-review.yml) | Repo de **producto**, `.github/workflows/` (lo agregan los devs; dirección lo entrega, no lo commitea ahí). Secreto `DISPATCH_VAIVEN_REVIEW`: PAT del bot con `Actions: write` solo sobre el repo del bot | Ante `review_requested` a la cuenta del bot, hace `workflow_dispatch` al repo del bot con PR, SHA y base |
| [`workflows/revisar-pr.yml`](workflows/revisar-pr.yml) | Repo del bot | Clona solo `docs/` del kit de contexto y corre `generar-review.py` |
| [`workflows/cron-respaldo.yml`](workflows/cron-respaldo.yml) + [`scripts/cron-check.py`](scripts/cron-check.py) | Repo del bot | Cada 6 h busca PRs con review pedida y sin review en el SHA actual (cubre conflictos que no disparan evento). Copia canónica: la instala `g14-cron-respaldo-de-prs` |
| [`scripts/generar-review.py`](scripts/generar-review.py) | Repo del bot | Arma el prompt, llama al modelo, filtra y publica |
| [`config/ruteo-kit.json`](config/ruteo-kit.json) | Repo del bot | Qué documentos del kit entran según las rutas del diff |

Credenciales: todas como **secrets de GitHub** (`BOT_GITHUB_TOKEN`, `OPENROUTER_API_KEY`, `GEMINI_API_KEY`, `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`). En local, `.env` a partir de [`env.example`](env.example). Ninguna va en el código.

## Qué hace en cada PR

1. **Identifica el ticket** buscando `SCRUM-<n>` en rama, título y cuerpo. Si no lo encuentra, publica solo ese aviso y no revisa.
2. **Lee el ticket completo de Jira**, convirtiendo el ADF con saltos de línea y conservando los links a otros tickets (`inlineCard`). Sin eso el modelo leía los criterios pegados en una línea y exigía alcance de otro ticket.
3. **Inyecta solo el kit que corresponde**: `definition-of-done.md` siempre; el resto por glob de rutas (migraciones → esquema y permisos; `n8n/` → contrato del motor; `src/` → frontend y tokens). Tope de 40.000 caracteres; el cuerpo de la review dice qué documentos usó y cuáles quedaron afuera. El ticket va **después** del kit: el alcance lo fija el ticket.
4. **Lee el estado de CI** desde workflow runs (el PAT fine-grained no tiene `checks:read`).
5. **Evalúa cuatro categorías**: A criterios de aceptación (cumple / no cumple / sin evidencia; «cumple» solo con la línea del diff que lo prueba), B lógica y casos borde, C seguridad (OWASP + SPA con Supabase: RLS en tablas nuevas, sin `service_role` en el front), D Definition of Done ítem por ítem.
6. **Filtra antes de publicar** (`filtrar_comentarios`): cada comentario trae un campo `evidencia` copiado literal del diff; si no aparece en el diff, o cita código que no está ni en el diff ni en el kit, se descarta. Topes por tipo: 6 `suggestion`+`question`, 2 `nitpick`, 1 `praise`; los `issue` no tienen tope. Un mismo patrón va en un solo comentario. Test: `python3 scripts/test_filtros.py`.
7. **Publica una review** con comentarios inline y `event=COMMENT`, salvo que ya exista una del bot sobre ese SHA.

## Reglas que salieron del uso real

- **Si el modelo falla, el bot no publica nada.** Un «no pude revisar» quitaría la review pedida y el cron de respaldo dejaría de ver el PR.
- **Antes de culpar al modelo, leé el prompt que efectivamente recibe** (`--dry-run`). Los errores de alcance venían de la entrada, no del razonamiento.
- **Una review se juzga contra el código, no por su largo.** Verificá cada hallazgo contra el commit revisado antes de concluir que un revisor es peor.
- **El modelo se elige con una corrida sobre un PR real**, no por precio. Cadena actual: modelo principal y respaldos en OpenRouter, Gemini como último respaldo, con un solo tope de tiempo (300 s).
- Con razonamiento activado, poné tope propio a los tokens de razonamiento: sin él, un modelo gastó todo el presupuesto pensando y devolvió vacío.
- Una cifra de consumo (minutos de Actions, costo) se contrasta con la API de billing antes de repetirla.

## Qué no hacer

- No commitear en la rama del dev ni aprobar: el bot comenta, la persona decide.
- No mandar el kit entero al modelo: exige piezas de tickets posteriores.
- No guardar claves en `.env` versionado ni en el workflow.

## Probarlo en local

```bash
python3 scripts/generar-review.py --pr 43 --dry-run   # imprime el payload, no publica
python3 scripts/generar-review.py --pr 43 --no-kit    # para comparar sin contexto
python3 scripts/test_filtros.py
```

Evidencia del proyecto: `docs/bitacora/2026-09-23-el-bot-fallaba-por-cosas-que-no-eran-el-modelo.md` y `docs/bitacora/2026-09-27-mas-comentarios-no-era-peor-review.md` del repo de dirección de VaiVen.
