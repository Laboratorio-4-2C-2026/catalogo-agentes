# Ejemplo de output — env checker sobre Study Arena

Corrida real sobre el repo de Study Arena (commit `874dc77`, 11/11/2026), sin `.env` local (se compara el ejemplo contra el código). Ningún valor se muestra.

## Raíz del repo

```
$ python3 -I check_env.py --repo .
⚠️  No existe .env (solo se compara el ejemplo contra el código)
Variables usadas en el código: 22 · en .env.example: 17 · en .env: —

🟠 JWT_SECRET                  el ejemplo trae un valor en una variable sensible   .env.example:4 (revisá que no sea un secreto real)
🟡 SPRING_DATASOURCE_PASSWORD  falta en el ejemplo   usada en backend/src/main/resources/application.properties:5 (la define docker-compose.yml:25)
🟡 SPRING_DATASOURCE_URL       falta en el ejemplo   usada en backend/src/main/resources/application.properties:3 (la define docker-compose.yml:23)
🟡 SPRING_DATASOURCE_USERNAME  falta en el ejemplo   usada en backend/src/main/resources/application.properties:4 (la define docker-compose.yml:24)
```

## Frontend

```
$ python3 -I check_env.py --repo frontend
Variables usadas en el código: 1 · en .env.example: 1 · en .env: —
✅ Sin diferencias
```

## Verificación a mano

| Hallazgo | Verificación | Conclusión |
|---|---|---|
| `JWT_SECRET` con valor en `.env.example` | 54 caracteres con palabras de placeholder; no se imprimió. | 🟡 Parece un placeholder de desarrollo. Conviene dejar `JWT_SECRET=<generar con: openssl rand -base64 32>` para que nadie lo use tal cual. |
| `SPRING_DATASOURCE_*` fuera del ejemplo | `docker-compose.yml:23-25` las define con valores de desarrollo. | 🟡 Con `docker compose up` anda. Quien corra `./gradlew bootRun` fuera de Docker no tiene esos valores: conviene documentarlas en `.env.example` o en el README. |
| `.env` en `.gitignore` | `.gitignore:81-83` ignora `.env` y `.env.*` y deja pasar `.env.example`. | ✅ |
| Frontend | `VITE_API_URL` está en `frontend/.env.example` y se usa en `frontend/src/services/apiClient.ts:12`. | ✅ |

## Bloque propuesto para `.env.example`

```
# Solo si corrés el backend fuera de Docker (con compose ya vienen definidas)
SPRING_DATASOURCE_URL=jdbc:postgresql://localhost:5432/study-arena-db
SPRING_DATASOURCE_USERNAME=<usuario de la base local>
SPRING_DATASOURCE_PASSWORD=<contraseña de la base local>
```

## Ajustes al script que salieron de esta corrida

La primera pasada daba cuatro falsos positivos: no reconocía las variables definidas en `environment:` de docker-compose, ni el `.env.example` propio del frontend, y reportaba `GITHUB_TOKEN`, que Actions provee solo. Se corrigió el script y se volvió a correr.

## Corrida en la máquina de una desarrolladora (con `.env` real)

Misma versión del script, corrida desde la raíz del repo con el `.env` local de la desarrolladora (los valores nunca se imprimen):

```
$ python3 -I check_env.py --repo .
Variables usadas en el código: 22 · en .env.example: 17 · en .env: 17

🟠 JWT_SECRET                  el ejemplo trae un valor en una variable sensible   .env.example:4 (revisá que no sea un secreto real)
🟡 SPRING_DATASOURCE_PASSWORD  falta en el ejemplo   usada en backend/src/main/resources/application.properties:5 (la define docker-compose.yml:25)
🟡 SPRING_DATASOURCE_URL       falta en el ejemplo   usada en backend/src/main/resources/application.properties:3 (la define docker-compose.yml:23)
🟡 SPRING_DATASOURCE_USERNAME  falta en el ejemplo   usada en backend/src/main/resources/application.properties:4 (la define docker-compose.yml:24)
```

Conclusión: el `.env` local tiene todas las variables que el código usa sin default; no hay nada 🔴. Esta corrida además detectó que la carpeta `backend/bin/` (salida de compilación del IDE) duplicaba resultados, y se agregó a las carpetas ignoradas.
