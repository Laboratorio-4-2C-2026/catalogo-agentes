---
name: g07-env-checker
description: "Compara las variables de entorno de Study Arena entre .env.example, el .env local y lo que realmente leen application.yml de Spring Boot, el frontend Vite, docker-compose y los workflows de GitHub Actions, sin mostrar nunca los valores, y lista las que faltan, sobran o están vacías, las del front sin prefijo VITE_ y los posibles secretos expuestos en el bundle. Usar cuando el stack no levanta, cuando alguien se suma al proyecto o antes de mergear un PR que agrega una variable."
metadata:
  tipo: skill
  area:
  - devops
  - seguridad
  fase:
  - desarrollo
  - mantenimiento
  - revision
  tecnologias:
  - spring-boot
  - vite
  - docker
  - github-actions
  - python
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: "07"
  autor:
    nombre: Ana Abramowich
    github: AbramowichAna
  responsables:
  - AbramowichAna
  madurez: usado-en-proyecto
  relacionados:
  - g07-code-review-tl
  - g07-role-handoff
  - g07-performance-con-volumen
---

# Env checker

"A mí me anda" suele ser una variable de entorno: alguien agregó `JWT_SECRET` en su `.env`, la usó en `application.yml`, mergeó, y al resto el backend no le levanta. O al revés: el front lee `import.meta.env.API_URL`, que Vite nunca expone porque no empieza con `VITE_`.

Esta skill compara las tres fuentes (el ejemplo versionado, tu `.env` local y el código) y te dice exactamente qué falta y dónde se usa. **Nunca muestra valores**: solo nombres.

## Cuándo usar esta skill

- "No me levanta el back/front", "me tira error de configuración", "¿qué me falta en el .env?"
- Cuando alguien nuevo clona el repo.
- En la revisión de un PR que agrega o cambia variables (corré el chequeo sobre la rama del PR).

## Paso 1: correr el chequeo

Desde la raíz del repo (el script se corre desde la carpeta de la skill, no se copia al repo):

```bash
python3 -I <carpeta-de-la-skill>/check_env.py --repo . --env .env --example .env.example
```

Si el front tiene su propio ejemplo (en Study Arena, `frontend/.env.example`), corré una segunda vez con `--repo frontend`. En la corrida de la raíz, las variables documentadas en el `.env.example` de un subproyecto no se reportan como faltantes. Si no hay `.env`, el script usa `.env.local` (la convención de Vite) cuando existe.

Qué detecta:
- usos en `application*.yml`/`.properties` (`${VAR}` y `${VAR:default}`), `System.getenv("VAR")`, `import.meta.env.VAR`, `process.env.VAR`, `docker-compose*.yml` (`${VAR}`, `${VAR:-default}`) y `${{ secrets.VAR }}` en `.github/workflows`;
- si cada uso tiene **valor por defecto** (si lo tiene, que falte es menos grave);
- las variables que `docker-compose.yml` define con un valor fijo en `environment:` (en Study Arena, `SPRING_DATASOURCE_*`): cuentan como definidas para el stack levantado con Compose y bajan a 🟡, porque solo faltan si alguien corre el backend fuera de Docker;
- `GITHUB_TOKEN` se ignora porque GitHub Actions lo provee solo.

## Paso 2: interpretar y verificar

El script es una primera pasada. Antes de reportar, verificá:

- 🔴 **Falta en tu .env y no tiene default**: confirmá mirando el `archivo:línea` que de verdad se usa en el arranque (y no en un perfil de Spring que no se usa localmente, como `application-prod.yml`). Si es de un perfil que no corre localmente, bajala a ⚪ y aclaralo.
- 🔴 **No expuesta por Vite**: el front lee una variable sin `VITE_`, así que siempre va a ser `undefined`. Es un bug seguro.
- 🔴 **Posible secreto en el front**: una variable `VITE_*` con nombre de secreto (`KEY`, `TOKEN`, `SECRET`…). Todo `VITE_*` se incrusta en el JavaScript público. Si es realmente un secreto, tiene que vivir en el backend.
- 🟠 **El ejemplo trae un valor en una variable sensible**: revisá **sin imprimirlo** si parece un secreto real (largo, aleatorio) o un placeholder obvio. Si parece real, hay que rotarlo, porque ya está en el historial de git.
- 🟠 **Vacía en tu .env**.
- 🟡 **Falta en el ejemplo pero tiene default**: no rompe, pero quien llega no sabe que existe.
- ⚪ **Sobrantes**: en el ejemplo o en tu `.env` y sin uso en el código. Pueden ser restos.
- **Variables del CI**: se listan aparte porque se configuran como secrets en GitHub, no en `.env`.

Si se usó `git log -S"<VAR>" --oneline`, podés decir en qué commit o PR se agregó una variable que falta, y quién la puede pasar.

## Paso 3: proponer arreglos

- Para cada variable faltante en `.env.example`: la línea a agregar, **con un placeholder** y un comentario de qué es y de dónde se saca (`JWT_SECRET=<generar con: openssl rand -base64 32>`).
- Para tu `.env`: qué variables agregar y de dónde sacar el valor (generarlo, pedírselo a quién, o copiarlo de un gestor de secretos). **No** lo escribas vos con un valor inventado, salvo que sea algo que se genera (como un secreto local de JWT) y el usuario lo pida.
- Para los usos sin `VITE_` o con secretos en el front: el cambio propuesto en el código (renombrar la variable o mover la llamada al backend).
- Si un PR agregó una variable sin actualizar `.env.example`, redactá el comentario para el PR (sin publicarlo).

Aplicá cambios a `.env.example` solo con un "sí" explícito. **Nunca** commitees ni muestres el `.env`.

## Output

1. Resumen: cuántas variables usa el código, cuántas hay en el ejemplo y cuántas en tu `.env`.
2. Hallazgos por severidad: variable, tipo, dónde se usa y la acción.
3. El bloque listo para pegar en `.env.example`.
4. Las variables a configurar como secrets del CI, si faltan.

Ver `example-output.md` para una corrida real sobre Study Arena.

## Qué no hacer

- No muestres, copies ni pegues valores del `.env` en el chat, en commits ni en comentarios.
- No commitees `.env`. Si `.env` no está en `.gitignore`, avisalo como 🔴.
- No inventes valores para secretos reales.

## Ejemplo de uso

**Pedido:** Cloné el repo y el backend no levanta, dice que falta una propiedad.

**Resultado:** Corre `check_env.py` y encuentra que `JWT_SECRET` se usa sin default en `application.yml:6`, falta en el `.env` y además el `.env.example` trae un valor que parece real. También marca que el front lee `API_URL` sin prefijo `VITE_`. Propone las líneas para el `.env.example` con placeholders y cómo generar el secreto, sin mostrar ningún valor.
