---
name: g12-preparar-deploy
description: Revisa un cambio antes de desplegarlo y devuelve un go/no-go con evidencia por punto — cambios de esquema y su migración, estado en memoria que se pierde al reiniciar, variables de entorno por ambiente, dominios y cookies, jobs programados y vuelta atrás. Usar antes de desplegar o reiniciar un servicio; no despliega ni corrige.
owner: '@lucasmonteverdi1'
role: tl
created: '2026-11-09'
metadata:
  tipo: skill
  area:
  - devops
  fase:
  - despliegue
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  - codex
  requiere: []
  grupo: '12'
  autor:
    nombre: Lucas Monteverdi
    github: lucasmonteverdi1
  responsables:
  - lucasmonteverdi1
  madurez: experimental
  relacionados:
  - g12-contenerizar-app
  - g12-actualizar-modelo-de-datos
---

# Preparar deploy

## Para qué

Muchas fallas no vienen del código sino del deploy: un reinicio que borra datos que vivían en
memoria, una variable que falta en un ambiente, un cambio de dominio que deja de mandar la
cookie, una migración que no estaba. Casi todas se ven antes si alguien mira. Esta skill mira.

## Entrada

La PR, la rama o el rango de commits a desplegar, y el ambiente destino. Si falta el
ambiente, preguntarlo: la mitad de los checks dependen de él.

## Descubrir antes de revisar

Leer en el repo, sin asumir:

- Cómo se despliega: workflows de CI, Dockerfiles, configuración de la plataforma de hosting.
- Dónde viven las migraciones y con qué herramienta se aplican (Flyway, Liquibase, Prisma,
  Alembic, Rails, etc.), y cómo valida el esquema el ORM al arrancar.
- La configuración por ambiente y qué variables lee el código.
- Jobs programados (cron, schedulers, colas).
- ADRs, runbooks o un registro de incidentes previos: lo que ya falló una vez se revisa primero.

Si el repo ya tiene reglas propias de deploy o migraciones, esas mandan sobre las de acá.

## Checks

Cada uno sale **OK**, **Riesgo**, **Bloquea** o **Sin verificar**, con archivo y línea o
comando como evidencia.

1. **Esquema.** Si el diff toca modelos o el esquema, ¿trae su migración en el mismo cambio?
   ¿La versión no choca con una ya aplicada? ¿Producción valida el esquema en vez de dejar que
   el ORM lo modifique? Una migración destructiva (drop, rename, `NOT NULL` sin default) es
   **Bloquea** hasta que haya plan de datos.
2. **Estado en memoria.** Buscar contadores, caches, colas o métricas que viven solo en el
   proceso. Si el deploy reinicia el proceso, ¿qué se pierde y a quién le importa? Si alimenta
   un reporte o una facturación, es **Riesgo** salvo que ya se persista.
3. **Variables de entorno.** Listar las variables nuevas o cambiadas que lee el código y
   confirmar que estén definidas en el ambiente destino. Nombrar aparte las que impiden el
   arranque si faltan o son inválidas. Un valor de un ambiente apuntando a otro (dev contra la
   base de prod, o al revés) es **Bloquea**.
4. **Dominios, CORS y cookies.** Si cambian URLs, orígenes permitidos, `SameSite` o el dominio
   de la API, verificar que el front y el back sigan pudiendo compartir sesión. Front y back en
   dominios registrables distintos es **Riesgo**: algunos navegadores (Safari) bloquean cookies
   de terceros.
5. **Ventana.** Jobs programados cerca del momento del deploy. Desplegar encima de una
   corrida es **Riesgo**.
6. **Vuelta atrás.** ¿Se puede volver a la versión anterior sin tocar la base? Si la migración
   no es reversible, decirlo.

## Salida

```
Deploy de <rama/PR> a <ambiente> — GO | GO con riesgos | NO GO

| # | Check | Resultado | Evidencia | Qué hacer |
```

Después, una línea por cada paso a hacer antes de desplegar (cargar una variable, esperar a
que pase un job, persistir un dato). No proponer refactors que no hagan al deploy.

## Qué no hace

No despliega, no carga variables, no corre migraciones contra ninguna base. Lo que requiere
acceso a la plataforma se marca **Sin verificar**, diciendo qué mirar.

## Ejemplo de uso

**Pedido:** Revisá la PR 58 antes de desplegarla a producción.

**Resultado:** Devuelve GO, GO con riesgos o NO GO con una tabla de checks (esquema, estado en memoria, variables, dominios y cookies, jobs, vuelta atrás) y evidencia por punto; no despliega nada.
