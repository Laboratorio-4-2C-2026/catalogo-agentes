---
name: g07-performance-con-volumen
description: "Mide cómo crece el tiempo de respuesta de los endpoints de Study Arena (Spring Boot + Postgres) a medida que crece la cantidad de datos: carga volúmenes escalonados (por ejemplo 1.000, 10.000 y 100.000 filas) en una base Docker aislada, mide p50 y p95 de cada endpoint, cuenta las queries por request para detectar N+1, corre EXPLAIN ANALYZE en las lentas y propone índices, paginación o cambios de consulta. Usar antes de una entrega o cuando una pantalla se pone lenta; mide volumen de datos, no carga concurrente."
metadata:
  tipo: skill
  area:
  - backend
  - datos
  - qa
  fase:
  - testing
  - revision
  tecnologias:
  - spring-boot
  - postgresql
  - docker
  - python
  metodologia:
  - scrum
  herramientas:
  - claude-code
  - cursor
  requiere: []
  grupo: "07"
  autor:
    nombre: Ana Abramowich
    github: AbramowichAna
  responsables:
  - AbramowichAna
  madurez: usado-en-proyecto
  relacionados:
  - g07-seed-mundo-gamificado
  - g07-endpoints-huerfanos
  - g07-study-arena-stepci-executor
---

# Performance con volumen de datos

En desarrollo la base tiene 5 usuarios y todo responde en 20 ms. Con 10.000 usuarios, el ranking global trae todo a memoria, el perfil hace una query por cada logro (N+1) y la búsqueda de salas recorre la tabla entera porque no hay índice. Nada de eso se ve hasta que hay datos.

Esta skill responde **cómo escala cada endpoint cuando crece la base**. No es una prueba de carga (muchos usuarios a la vez): las requests se hacen de a una, para que el único factor que cambie sea el volumen de datos. Para concurrencia hay otras skills en el catálogo (por ejemplo `g04-load-testing`).

## Cuándo usar esta skill

"¿Cómo escala el ranking?", "¿qué pasa con 10.000 usuarios?", "¿qué endpoints se ponen lentos con muchos datos?", "esta pantalla tarda", antes de una entrega o antes de mergear un ticket que agrega una consulta pesada.

## Paso 0: entorno aislado (obligatorio)

**Nunca** cargues volumen en la base de desarrollo de nadie ni en una base remota.

1. Levantá una copia aislada del stack con otro nombre de proyecto de Compose, así tiene sus propios volúmenes y no toca los datos de desarrollo:
   `docker compose -p studyarena-perf up -d` (si los puertos chocan con el stack normal, bajá el normal o usá un override con otros puertos).
2. Verificá que el esquema esté creado (con Flyway, que aplicó todas las migraciones; en Study Arena lo arma Hibernate al arrancar) y que el backend responde.
3. Si `.env` apunta a un host que no es `localhost` o `db`, frená y preguntá.
4. **Cortá todo lo que sale hacia afuera.** El backend de perf no puede hablar con servicios reales con datos falsos. Buscá tareas programadas (`@Scheduled`) y clientes HTTP salientes, y vaciá sus variables solo para el stack de perf, con un override de Compose fuera del repo o con variables en la línea de comandos. En Study Arena, `MetricsScheduler` manda KPIs a la plataforma de KPIs todos los días a las 18:00 y a las 20:00: dejá vacías `KPIS_PLATFORM_URL` y `KPIS_PLATFORM_PUBLISHABLE_KEY`, y también las de Gemini y Azure (`GEMINI_API_KEY`, `AZURE_STORAGE_CONNECTION_STRING`). Confirmá en el log del arranque que esas integraciones quedaron desactivadas antes de cargar datos. Si alguna integración no deja arrancar el backend con la variable vacía (en Study Arena pasa con Azure Storage), usá un valor de prueba local que no apunte a ningún servicio real.
5. Anotá la máquina (CPU y RAM) y el commit: los números absolutos solo se comparan dentro de la misma máquina.

## Paso 1: elegir qué medir

1. Listá los endpoints de lectura de los controllers y priorizá los que **dependen del tamaño de los datos**: rankings, listados, búsquedas, historial, perfil con estadísticas, feeds y todo lo que agrega o cuenta.
2. Proponé entre 5 y 12 endpoints y los volúmenes. Por defecto: **1.000 → 10.000 → 100.000** filas en la tabla principal (usuarios o actividad), con las tablas relacionadas en proporción realista (por ejemplo, 30 actividades por usuario y 5 salas por cada 100 usuarios).
3. Escribí un `endpoints.txt` en un directorio temporal (formato en `medir.py`), con parámetros realistas (`page=0&size=20`, un id que exista, un texto de búsqueda que matchee).
4. Mostrá el plan y esperá el OK.

## Paso 2: generar el volumen

Escribí un script SQL por nivel, usando `generate_series` (es mucho más rápido que insertar desde Java):

```sql
INSERT INTO users (email, name, created_at)
SELECT 'perf' || g || '@perf.test', 'Perf ' || g,
       now() - (random() * interval '120 days')
FROM generate_series(1, 10000) g;
```

- Respetá FKs, `NOT NULL`, `UNIQUE` y enums **del esquema real** (leé las migraciones de Flyway o, si no hay, las entidades JPA y `\d+ <tabla>` en psql).
- Distribuciones realistas: pocos usuarios con mucha actividad y muchos con poca (`power(random(), 3)`), no todo uniforme.
- Cada nivel **suma** sobre el anterior hasta el total (1.000, después 9.000 más, después 90.000 más).
- Después de cada carga: `ANALYZE;` para que el planner tenga estadísticas actualizadas.
- Dejá un usuario conocido para autenticarte (si hay JWT, obtené el token con el endpoint de login y guardalo en una variable de entorno; **nunca** lo pegues en el chat ni en archivos).

## Paso 3: medir en cada nivel

Para cada volumen:

1. **Latencia**:
   `python3 -I <carpeta-de-la-skill>/medir.py medir --base http://localhost:8080 --endpoints endpoints.txt --volumen <N> --reps 30 --csv resultados.csv --token-env STUDY_TOKEN`
2. **Queries por request**: activá el log de SQL del backend de perf (`logging.level.org.hibernate.SQL=DEBUG`, por variable de entorno `LOGGING_LEVEL_ORG_HIBERNATE_SQL=DEBUG` en el compose de perf) o las estadísticas de Hibernate (`spring.jpa.properties.hibernate.generate_statistics=true`). Pedí cada endpoint **una vez** y contá las queries en el log. Si la cantidad **crece con el volumen** o con el tamaño de página, es un **N+1**.
3. **Tamaño de respuesta**: el CSV lo registra. Si crece con el volumen, el endpoint no pagina.

Al terminar todos los niveles: `python3 -I medir.py comparar --csv resultados.csv` arma la tabla volumen × endpoint y clasifica el crecimiento:
- 🟢 **constante**: el tiempo casi no cambia (paginado y con índice). Es lo ideal.
- 🟡 **sublineal**: crece poco.
- 🟠 **lineal**: si los datos se multiplican por 10, el tiempo también. Suele ser un full scan o la falta de paginación.
- 🔴 **superlineal**: crece más rápido que los datos. Suele ser un N+1 combinado con traer todo, o un ordenamiento en memoria.

## Paso 4: diagnosticar los 🟠 y 🔴

Para cada uno:

1. Ubicá la query: el log de SQL, el repository (`@Query`, métodos derivados) y el service.
2. Corré en psql, sobre la base de perf, `EXPLAIN (ANALYZE, BUFFERS) <query con parámetros reales>;` y buscá: `Seq Scan` sobre tablas grandes, `Sort` con `external merge` (ordenamiento en disco), `rows` estimadas muy distintas de las reales o un `Nested Loop` con muchas iteraciones.
3. Si `pg_stat_statements` está disponible, usalo para ver las queries con más tiempo total.
4. Causas típicas en Spring + JPA y su arreglo:
   - **N+1** por `@OneToMany` o `@ManyToOne` lazy recorridos en un loop o al serializar → `JOIN FETCH`, `@EntityGraph` o una proyección o DTO con una sola query.
   - **Sin paginación** (`findAll()` y después filtrar o ordenar en Java) → `Pageable` y `ORDER BY` en la base.
   - **Falta un índice** en una FK, un filtro o un `ORDER BY` (por ejemplo, el filtro por grupo y fecha del ranking semanal) → índice, idealmente compuesto según el `WHERE` + `ORDER BY`.
   - **Ranking calculado en cada request** → vista materializada, columna desnormalizada o caché con invalidación.
   - **`COUNT(*)` de `Page`** caro → `Slice` si la UI no necesita el total.
   - **`LIKE '%texto%'`** → `pg_trgm` con un índice GIN, o búsqueda por prefijo.
5. Si es posible, **probá el arreglo en el entorno de perf** (crear el índice a mano o cambiar la query en una rama local temporal) y volvé a medir ese endpoint para mostrar el antes y el después. Un índice nuevo va en una migración Flyway **propuesta**, no aplicada al repo.

## Output

1. Entorno: commit, máquina, volúmenes y tablas que se poblaron.
2. **Tabla volumen × endpoint** (p95 por nivel, crecimiento y bytes).
3. **Queries por request** de cada endpoint por nivel (marcá los N+1).
4. Por cada 🟠/🔴: causa con evidencia (fragmento del EXPLAIN y `archivo:línea`), arreglo propuesto (diff o migración Flyway propuesta) y, si se probó, el antes y el después.
5. Un umbral orientativo: qué endpoints superan los 300 ms de p95 a 10.000 filas (o el umbral que defina el equipo).
6. Limitaciones: máquina local, sin concurrencia, distribución de datos supuesta.

Ver `example-output.md` para una corrida real sobre Study Arena.

## Al terminar

Ofrecé bajar el entorno de perf: `docker compose -p studyarena-perf down -v` (borra sus volúmenes; el stack normal no se toca). Hacelo solo con un "sí".

## Qué no hacer

- No cargues datos en la base de desarrollo, en una base compartida ni en una base remota.
- No cambies código ni migraciones del repo: los arreglos son propuestas.
- No compares números entre máquinas distintas.
- No imprimas tokens, contraseñas ni la URL de conexión.

## Ejemplo de uso

**Pedido:** Quiero saber cómo se comportan el ranking semanal, el historial y el listado de sesiones si tenemos 100.000 sesiones.

**Resultado:** Levanta un stack Docker aislado con las integraciones externas desactivadas y carga 1k, 10k y 100k sesiones con actividad realista vía generate_series. Mide p50, p95 y queries por request en cada nivel y arma la tabla de crecimiento. Encuentra, por ejemplo, que el listado de sesiones no pagina y tiene un N+1 de participantes, y que el primer GET del ranking semanal calcula los puntos pendientes dentro del request; propone paginación, una sola consulta de participantes y calcular los puntos fuera del GET.
