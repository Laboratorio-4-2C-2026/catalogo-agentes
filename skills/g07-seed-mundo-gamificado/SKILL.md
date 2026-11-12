---
name: g07-seed-mundo-gamificado
description: "Genera y carga en la base Postgres local de Study Arena un mundo de datos realista y coherente con las reglas reales del backend (usuarios, grupos, sesiones de estudio con presencia, quizzes con intentos, puntos y ranking semanal por grupo, metas y tiempo de estudio diario), leyendo el esquema de las entidades JPA. Usar antes de una demo o un steering, o para cumplir la carga masiva realista que pide la cátedra; solo escribe en una base local y no sirve para medir performance."
metadata:
  tipo: skill
  area:
  - datos
  - backend
  fase:
  - desarrollo
  - testing
  tecnologias:
  - postgresql
  - spring-boot
  - docker
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
  madurez: experimental
  relacionados:
  - g07-balance-gamificacion
  - g07-performance-con-volumen
  - g07-preguntas-de-la-catedra
---

# Seed de mundo gamificado

Una app de estudio vacía no demuestra nada: un ranking con un solo usuario, un perfil sin horas de estudio y un grupo sin sesiones no muestran el producto. Esta skill genera un **mundo creíble**: datos que cuentan una historia y que respetan las mismas reglas que aplica el backend.

La diferencia con un generador de datos cualquiera es la **coherencia**: los puntos de cada usuario salen de las sesiones y quizzes que hizo, calculados con la fórmula real; el tiempo de estudio diario coincide con la presencia en sesiones; y el ranking semanal de cada grupo se puede explicar fila por fila.

## Cuándo usar esta skill

- "Datos para la demo", "poblar la base", "que el ranking no se vea vacío", "usuarios de prueba con historial".
- Antes de un steering, una entrega o una prueba con usuarios.
- Para la **carga masiva realista** que pide la cátedra (por ejemplo, más de 500 usuarios y al menos 5.000 registros en las tablas principales, sin nombres como "Usuario_001").

Si lo que se quiere es ver cómo se comportan los endpoints con mucho volumen, usar `g07-performance-con-volumen`: esta skill prioriza que los datos sean realistas, no medir.

## Paso 0: solo base local

1. La carga va **únicamente** a la base local del `docker compose` de desarrollo (en Study Arena, el servicio `database`, Postgres 16, base `study-arena-db`). Si `.env` o la configuración apuntan a un host que no es local, frená y preguntá.
2. Si el stack de `g07-performance-con-volumen` está levantado, no cargues ahí: son bases distintas a propósito.
3. No toques las tablas de KPIs y métricas (`kpi_snapshots`, `metric_events`).
4. Recomendá hacer un backup antes de cargar: `docker compose exec -T database pg_dump -U postgres study-arena-db > /tmp/backup-antes-del-seed.sql`.

## Paso 1: entender el esquema y las reglas reales (no inventarlos)

1. **Esquema.** Study Arena no usa Flyway: Hibernate arma las tablas desde las entidades (`spring.jpa.hibernate.ddl-auto`). Leé las entidades JPA (`@Entity`, `@Table`, `@Column`, relaciones, enums, constraints únicas) y confirmá contra la base con `docker compose exec database psql -U postgres -d study-arena-db -c '\d+ <tabla>'` antes de escribir SQL. Levantá el backend al menos una vez para que existan las tablas.
2. **Reglas que el seed tiene que respetar**, cada una con `archivo:línea` (verificalas: el código manda):
   - **Puntos**: una fila en `point_transactions` por recompensa, única por `(user_id, source_type, source_id, reason)`. Los motivos son solo `SESSION_PARTICIPATION` y `QUIZ_COMPLETION`.
   - **Sesión** (`SessionPointsCalculator`): `participación = total_seconds / (duración planificada × 60)`. Con `≥ 0,85` se multiplica por 1,5, con `≥ 0,50` por 1,0, con `≥ 0,20` por 0,5 y por debajo da 0. `puntos = round(duración × multiplicador)`. La duración es `(focus + break) × ciclos`, y `earned_at` es el fin planificado de la sesión.
   - **Quiz** (`QuizService`): `puntos = round(correctas / total × 50)`, solo por el primer intento completado.
   - **Ranking**: semanal por grupo, de lunes a lunes en hora de Buenos Aires, según `earned_at`.
   - **Tiempo de estudio diario**: lo que se acumula en `total_seconds` también se registra por día (`DailyStudyTimeRecorder`). El seed tiene que cargar las dos cosas de forma consistente.
   - **Estados**: sesiones `SCHEDULED`, `ACTIVE` y `FINISHED`; quizzes en borrador y publicados; intentos abiertos y completados; miembros con rol `OWNER` o `MEMBER`.
3. Si una regla no está clara en el código, **preguntala**. No la completes por tu cuenta.
4. Mostrale al usuario las tablas que vas a poblar y las reglas que vas a respetar. Esperá el OK.

## Paso 2: diseñar el mundo (antes de escribir SQL)

Proponé el elenco y la historia en una tabla corta. Por defecto, para una demo chica:

| Perfil | Cantidad | Para qué sirve en la demo |
|---|---|---|
| Usuario de la demo (el que se loguea) | 1 | Tiene historial, metas cargadas y está **a pocos puntos de pasar a alguien** en el ranking semanal de su grupo, así la demo muestra ese momento. |
| Compañeros activos del grupo de la demo | 4–7 | Llenan el ranking con diferencias chicas entre posiciones. |
| Usuarios constantes | varios | Muchas sesiones con buena presencia y algunos quizzes. |
| Usuarios ocasionales | varios | Poca presencia, ninguna actividad esta semana. |
| Usuarios nuevos | 2–3 | Recién registrados, sin historial (muestran el estado vacío). |

Para la **carga masiva** escalá las proporciones (por ejemplo, 500 o más usuarios en 60 a 100 grupos de 3 a 8 personas) y repartí la actividad para superar el mínimo de registros que pida la cátedra en las tablas principales.

Además:
- **Nombres y contenido realistas**: personas con nombres y apellidos argentinos variados (con tildes y ñ), y grupos, sesiones y quizzes con nombres de materias reales de la facultad ("Análisis Matemático II", "Física I", "Base de Datos", "Laboratorio IV"). Preguntas de quiz con sentido, sobre esas materias. Nunca uses datos de personas reales del curso.
- **Tiempo**: repartí la actividad en las últimas 4 a 6 semanas, con más carga antes de fechas de parcial y menos los fines de semana. Usá fechas **relativas a `now()`** para que el seed siga funcionando la semana siguiente, y dejá actividad en la **semana actual** para que el ranking no aparezca vacío.
- **Estados para mostrar**: al menos una sesión programada, una activa y varias terminadas por grupo de la demo; un quiz en borrador, uno publicado sin jugar y uno con tabla de posiciones; un intento a medio responder.
- **Bordes visibles**: un empate en el ranking, un nombre largo y uno con acentos y ñ.
- **Archivos**: los materiales viven en Azure Storage. No subas archivos a un storage real desde el seed; si la demo necesita archivos, avisale al usuario qué hay que cargar a mano o con qué storage local.

Esperá el OK (o cambios) antes de generar.

## Paso 3: generar el seed

1. Escribí un único archivo `seed/demo-mundo.sql` (o donde el repo guarde seeds; si hay una convención, seguila). No lo agregues al arranque del backend.
2. Estructura del archivo:
   - comentario de cabecera con qué genera, la fecha y el commit sobre el que se escribió;
   - `BEGIN;` … `COMMIT;`;
   - limpieza **solo de los datos del seed** (marcalos, por ejemplo con emails `@demo.studyarena.test`), nunca `TRUNCATE` de tablas enteras;
   - inserts en orden de dependencias, con `generate_series` para la carga masiva;
   - **puntos calculados en SQL con la fórmula real** a partir de la duración y los segundos de presencia de cada participación, y de las correctas de cada intento. Nunca pongas números de puntos sueltos que no salgan de la actividad.
3. **Contraseñas**: generá el hash con el mismo algoritmo que usa el backend (BCrypt del `PasswordEncoder` de Spring; en SQL, `crypt('<clave>', gen_salt('bf'))` de `pgcrypto` si es compatible) y dejá la contraseña de demo en un README al lado del seed, nunca en Discord ni en un ticket.
4. Que sea **idempotente**: correrlo dos veces deja el mismo resultado.

## Paso 4: cargar y verificar

1. Cargalo: `docker compose exec -T database psql -U postgres -d study-arena-db < seed/demo-mundo.sql`.
2. Verificá la coherencia con consultas de control y mostrá el resultado:
   - para cada participación terminada, los puntos guardados coinciden con la fórmula real;
   - el tiempo de estudio diario coincide con la suma de presencia de las sesiones;
   - top 5 del ranking semanal del grupo de la demo;
   - cantidad de filas por tabla (para la carga masiva, contra el mínimo pedido).
3. Logueate con el usuario de la demo y pedí por API el perfil, las métricas y el ranking semanal de su grupo (`curl` contra el backend local). Compará con la base: una diferencia significa que el seed no respeta alguna regla, y hay que corregirlo.
4. Recomendá abrir el front y revisar el perfil, el grupo y el ranking.

## Output

1. Resumen del mundo generado: usuarios, grupos, sesiones, quizzes e intentos, rango de fechas y estados cubiertos.
2. Ruta del archivo `.sql` y los comandos para cargarlo y para limpiarlo.
3. Usuario y contraseña de la demo, y **el momento de demo preparado** (por ejemplo: "si `demo@…` completa el quiz de Física I, pasa a Martina en el ranking semanal").
4. Resultado de las consultas de control.
5. Reglas que asumiste o que no encontraste en el código.

## Qué no hacer

- No cargues datos en una base que no sea local ni en la del stack de performance.
- No borres datos que no sean del seed.
- No insertes en las tablas de KPIs y métricas (en Study Arena, `kpi_snapshots` y `metric_events`): los datos de demo no deben mezclarse con lo que se reporta a la plataforma de KPIs.
- No modifiques entidades ni código del backend.
- No inventes reglas de puntos que no estén en el código.
- No subas archivos a un storage real.

## Ejemplo de uso

**Pedido:** El jueves tenemos steering. Poblame la base local para que el ranking y el perfil se vean vivos, con al menos 500 usuarios realistas.

**Resultado:** Lee las entidades JPA y las reglas de puntos del backend y propone 550 usuarios en 80 grupos de materias reales, con 5 semanas de sesiones y quizzes. Genera `seed/demo-mundo.sql` idempotente con los puntos calculados con la fórmula real y lo carga en el Postgres local. Muestra las consultas de control y deja un usuario de demo a un quiz de pasar a una compañera en el ranking semanal.
