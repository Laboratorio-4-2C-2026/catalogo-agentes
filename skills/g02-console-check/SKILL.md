---
name: g02-console-check
description: Usar una vez por semana para levantar Zest en local, recorrer los flujos de los tickets cerrados en la semana y crear un issue en Multica si aparecen errores o warnings en la consola del navegador.
metadata:
  tipo: skill
  area:
  - qa
  fase:
  - testing
  tecnologias:
  - playwright
  - javascript
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - multica
  - chrome
  grupo: '02'
  autor:
    nombre: Ines Gassiebayle
    github: inesgassiebayle
  responsables:
  - inesgassiebayle
  madurez: experimental
  relacionados: []
---
# Chequeo semanal de errores de consola — Zest

## Objetivo
Levantar la app en local, recorrer en el navegador los flujos de **los tickets que se cerraron en los últimos 7 días** y detectar:
- `console.error` y excepciones no capturadas → **errores**
- `console.warn` → **warnings**
- requests que fallan o responden 4xx/5xx → errores (5xx) o warnings (4xx)

**Si no hay errores ni warnings, no crear nada.** Si hay, crear **un solo issue** con el detalle.

## Preparación (solo la primera vez)
```bash
mkdir -p ~/zest-agentes/console-check && cd ~/zest-agentes/console-check
cp <ruta-de-esta-skill>/console_check.mjs .
npm init -y >/dev/null && npm install playwright && npx playwright install chromium
```
Los `.env` de desarrollo tienen que estar en `~/zest-agentes/env/backend.env` y `~/zest-agentes/env/frontend.env` (copias de los `.env` locales de un dev). La cuenta de prueba va en las variables del agente: `ZEST_TEST_EMAIL` y `ZEST_TEST_PASSWORD`.

## Pasos

### 1. Actualizar el repo y levantar la app
```bash
cd ~/zest-agentes/zest && git checkout main && git pull
cp ~/zest-agentes/env/backend.env backend/.env
cp ~/zest-agentes/env/frontend.env frontend/.env

cd backend && docker compose up -d postgres
npm ci && npx prisma migrate deploy && npx prisma db seed
nohup npm run start:dev > /tmp/zest-backend.log 2>&1 &

cd ../frontend && npm ci
nohup npm run dev -- --port 5173 --strictPort > /tmp/zest-frontend.log 2>&1 &
```
Esperar a que respondan `http://localhost:3000/health` y `http://localhost:5173` (reintentar cada 5 segundos, hasta 2 minutos). Si Docker no está abierto o algo no levanta, **no crear el issue de errores**: terminar informando qué falló, con las últimas líneas de los logs.

### 2. Elegir los tickets de la semana
```bash
multica issue list --output json > issues.json
```
Quedarse con los tickets en estado Done cuya última actualización (`updated_at`) sea de los últimos 7 días. Para cada uno, leer título, descripción y criterios de aceptación (`multica issue get <id> --output json`).

Los tickets solo de backend, infraestructura o documentación, sin nada visible en la app, se saltean (listarlos en el informe como "no aplica").

### 3. Escribir los flujos
Armar `~/zest-agentes/console-check/flows.json` con un flujo por ticket que recorra lo que el ticket implementó, siguiendo sus criterios de aceptación. Formato y pasos disponibles en el encabezado de `console_check.mjs`. Rutas de la app:

| Ruta | Pantalla |
|---|---|
| `/` | Feed |
| `/recipes/new` | Crear receta |
| `/recipes/:id` | Detalle de receta |
| `/recipes/:id/edit` | Editar receta |
| `/collections` | Colecciones |
| `/collections/:id` | Detalle de colección |
| `/profile` | Perfil propio |

Para encontrar los textos de botones y labels, leer los componentes en `frontend/src/features/`. Agregar siempre un flujo base que recorra `/`, `/collections` y `/profile`, aunque no haya tickets.

### 4. Correr el chequeo
```bash
cd ~/zest-agentes/console-check && node console_check.mjs flows.json --out reporte.json
```
| Código | Qué hacer |
|---|---|
| `0` | Sin errores ni warnings: no crear issue. |
| `1` | Hay errores o warnings: seguir con el paso 5. |
| `2` | No se pudo correr (login, app caída): informar el error, sin crear el issue de errores. |

Si un flujo tiene `paso_fallido`, revisar la captura: si el problema es el flujo (un texto mal escrito), corregirlo y volver a correr. Si es un bug de la app, incluirlo en el issue.

### 5. Crear el issue
```bash
multica issue create --title "Errores de consola — semana del <DD/MM>" --description-file issue.md --priority high --output json
```
`--priority high` si hay errores; si solo hay warnings, `medium`. Formato de `issue.md`:
```markdown
Chequeo semanal en local sobre `main` (<commit corto>). Se recorrieron <N> flujos de los tickets cerrados del <DD/MM> al <DD/MM>.

## ❌ Errores (<cantidad>)
| Ticket | Pantalla | Error | Origen |
|---|---|---|---|
| ZEST-120 | /recipes/new | Cannot read properties of undefined (reading 'map') | excepción no capturada |

## ⚠️ Warnings (<cantidad>)
| Ticket | Pantalla | Warning |
|---|---|---|

## Pasos que fallaron
<flujo, paso y captura, si los hay>

## No aplica
<tickets salteados y por qué>
```
Agrupar los mensajes repetidos e indicar cuántas veces aparecieron. Después, suscribir a los suscriptores del autopilot:
```bash
multica autopilot get "$MULTICA_AUTOPILOT_ID" --output json
multica issue subscriber add <id-del-issue> --user-id <user_id>
```

### 6. Apagar todo
```bash
pkill -f "nest start" ; pkill -f "vite" ; cd ~/zest-agentes/zest/backend && docker compose stop postgres
```

## Reglas
- No modificar el código del repo ni hacer commits: solo leer y correr.
- No incluir contraseñas, tokens ni contenido de los `.env` en el issue.
- Un solo issue por corrida.

## Ejemplo de uso
**Pedido:** Revisá la consola de la app esta semana.
**Resultado:** Levanta la app en local, recorre los flujos de los tickets cerrados y reporta en un único issue los errores o warnings de consola.
