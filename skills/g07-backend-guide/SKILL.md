---
name: g07-backend-guide
description: "Guía de reglas para backends Spring Boot 3 + JPA/Hibernate + PostgreSQL, salidas de reviews de PR: normalización en el compact constructor de los records, @ExceptionHandler por excepción, asociaciones y constraints en JPA con soft delete, JPQL antes que SQL nativo, orden alfabético con Collator, LIKE con ESCAPE, zonas horarias, variables de entorno en Compose y tests de API. Usar al implementar un ticket de backend y como checklist antes de abrir la PR; si el repo tiene su propia guía, gana la del repo."
metadata:
  tipo: skill
  area:
  - backend
  - qa
  fase:
  - desarrollo
  - revision
  tecnologias:
  - spring-boot
  - postgresql
  - docker
  metodologia:
  - agnostico
  herramientas:
  - claude-code
  requiere: []
  grupo: "07"
  autor:
    nombre: Julieta Garberoglio
    github: JulietaG13
  responsables:
  - JulietaG13
  madurez: usado-en-proyecto
  relacionados: []
---

# Guía de backend — Spring Boot + JPA + PostgreSQL

Reglas que salieron de reviews de PR de un proyecto real. Documento vivo: cuando una review encuentra algo nuevo y general, se agrega.

Pensada para: Spring Boot 3 / Java 21 / JPA + Hibernate / PostgreSQL en prod, H2 en tests.

## Cómo usarla

- **Si el repo tiene su propia guía de backend, gana la del repo.** Esta se usa como base para lo que la del repo no dice.
- La sección **Convenciones del equipo** son decisiones de estilo de un equipo, no errores: se aplican solo si el repo las adopta. El resto son reglas del stack, que valen siempre.
- Los nombres de clases y tablas que aparecen (`RegisterRequest`, `SecurityConfig`, `group_members`, `TextNormalizer`…) son ejemplos: se reemplazan por los equivalentes del repo.
- Antes de usar los comandos, pedile al usuario lo que no esté en el `CLAUDE.md` / `AGENTS.md` del repo: la carpeta del backend, el comando para levantar el entorno sobre base limpia y el comando para consultar la base.

---

## Antes de abrir la PR

- [ ] `main` mergeado y la suite completa en verde **después** de resolver los conflictos, no solo compilando.
- [ ] El entorno levanta sobre base limpia con el comando del proyecto (por ejemplo `docker compose down -v && docker compose up -d --build`) y con el repo tal como queda en la rama, sin variables inyectadas a mano.
- [ ] Cada escenario del ticket tiene un test de API, no solo de service.
- [ ] Los nombres de campos de request y response son literalmente los del contrato del ticket.
- [ ] `git status` limpio: nada de archivos sueltos fuera de la carpeta del backend.

---

## Convenciones del equipo

Opcionales: se aplican si el repo las adopta.

- Paquetes por capa y subpaquete por dominio: `controller/`, `service/`, `repository/` (+ `projection/`), `dto/<dominio>/`, `entity/<dominio>/`, `exception/runtime/`. Un archivo nuevo va donde ya viven sus pares.
- Inyección por constructor, con los campos `private final`. Nada de `@Autowired` sobre el campo ni de Lombok.
- Los DTOs son `record`, sin más lógica que el compact constructor de normalización.
- Una excepción de dominio por caso, en `exception/runtime/`, con su `public static final String CODE`.
- El controller no tiene lógica: `@Valid`, delegar al service y envolver en `ApiResponse`. El usuario actual entra por `@AuthenticationPrincipal UUID`, no se saca del token a mano.
- `@Transactional` en el service, nunca en el controller.
- Las constantes van `private static final` al tope de la clase; nada de literales repetidos dentro de los métodos.
- Imports explícitos, sin comodines. Indentación de 4 espacios.
- Los tests nuevos se nombran `método_condición_resultado`: `search_missingQuery_returns400`.

---

## Contrato de API

- Si el proyecto tiene un wrapper de respuesta común (por ejemplo `ApiResponse` con `{result, data, errors}`), toda respuesta va envuelta en él, incluidas las que no pasan por un controller: el `authenticationEntryPoint()` (401) y el `accessDeniedHandler()` (403) de la configuración de seguridad lo serializan con `ObjectMapper`, no arman el JSON a mano.
- Los nombres de campos son los del ticket, incluido el `field` de los errores de conflicto. Compararlos uno por uno antes de mergear.
- No poblar un campo `@CreationTimestamp` desde el objeto que devuelve `repository.save()`: se resuelve en el flush y llega `null`. Releer la entidad o dejar el campo fuera de la response.

---

## Validación y normalización

- Normalizar en el compact constructor del record, nunca en el service: Jackson deserializa por el constructor canónico, así que corre antes de `@Valid`.

  ```java
  public record RegisterRequest(...) {
      public RegisterRequest {
          if (name != null) name = name.trim();
          if (email != null) email = email.trim().toLowerCase();
      }
  }
  ```

- Los DTOs que comparten un campo lo normalizan igual (`email` en `RegisterRequest` y en `LoginRequest`).
- No normalizar valores de enum de entrada: un `toUpperCase()` vuelve válido lo que el ticket manda rechazar con 400.

---

## Excepciones y códigos de estado

- Cada excepción de framework alcanzable lleva su `@ExceptionHandler`. Sin él, el `@ExceptionHandler(Exception.class)` la devuelve como 500 — es lo que pasa con `MissingServletRequestParameterException`.
- Probar en cada endpoint nuevo los caminos degenerados: parámetro ausente, tipo incorrecto, JSON malformado, `Content-Type` faltante, método HTTP incorrecto.
- Una excepción por status, no por nombre: si "no existe" es 401 en un flujo y 404 en otro, son dos clases distintas.
- Cada conflicto que el front tenga que distinguir lleva su propio código de máquina.

---

## Persistencia (JPA)

- Mapear las columnas `*_id` como asociación, no como `@Column` de UUID: sin `@ManyToOne` Hibernate no genera la FK y la integridad queda en manos de un `existsById`.

  ```java
  @ManyToOne(fetch = FetchType.LAZY, optional = false)
  @JoinColumn(name = "owner_id", nullable = false)
  private User owner;
  ```

- `fetch = LAZY` explícito: el default de `@ManyToOne` es `EAGER`.
- Declarar la unicidad aparte de la FK, que no la cubre.

  ```java
  @Table(name = "group_members",
         uniqueConstraints = @UniqueConstraint(columnNames = {"group_id", "user_id"}))
  ```

- Con soft delete, reutilizar la fila dada de baja en vez de insertar otra: `@SQLRestriction` la esconde de JPQL pero no de la constraint única, y el `INSERT` sale `23505` → 500.
- Verificar todo cambio de esquema con volumen limpio. `ddl-auto=update` solo agrega lo que falta: no borra, no modifica columnas y, si los datos existentes violarían la constraint nueva, no la crea y sigue sin avisar.

  ```bash
  docker compose down -v && docker compose up -d
  docker exec <contenedor-de-la-base> psql -U <usuario> -d <base> \
    -c "SELECT conrelid::regclass, pg_get_constraintdef(oid) FROM pg_constraint WHERE contype='f';"
  ```

---

## Consultas

- Las consultas se escriben con Spring Data: método derivado del nombre, y `@Query` en JPQL cuando el nombre no alcanza. JPQL valida los campos contra las entidades al arrancar y es portable entre H2 y PostgreSQL.
- El SQL nativo y `JdbcTemplate` quedan solo para lo que JPQL no puede expresar —por ejemplo saltear el `@SQLRestriction` de una entidad con soft delete—, y ahí el porqué va comentado. (En los tests, `JdbcTemplate` para armar datos y verificar filas está bien.)
- Ordenar alfabéticamente en Java, no en la base: una imagen como `postgres:16-alpine` compara por bytes (`Ana, Bandera, andes, zanahoria, Ángela, Ñandú`). Sacar el `ORDER BY` de la query.

  ```java
  // El locale es el idioma de la interfaz.
  private static final Locale ES = Locale.forLanguageTag("es");
  ...
  // Collator no es thread-safe: se instancia por llamada.
  Collator collator = Collator.getInstance(ES);
  return ...stream().sorted(Comparator.comparing(UserBrief::name, collator)).toList();
  ```

- Escapar los comodines de todo `LIKE` que reciba un término del usuario, o un `q=%%` devuelve la tabla entera. En el ejemplo, `TextNormalizer` es el normalizador de texto del proyecto.

  ```java
  String normalized = TextNormalizer.normalize(trimmed)
      .replace("!", "!!").replace("%", "!%").replace("_", "!_");
  ```
  ```sql
  AND u.nameNormalized LIKE CONCAT('%', :normalizedQuery, '%') ESCAPE '!'
  ```

---

## Fechas

- Zona explícita siempre: `LocalDateTime.now()` toma la del JVM y, etiquetada después como UTC, deja el instante corrido.

  ```java
  LocalDateTime deletedAt = LocalDateTime.now(ZoneOffset.UTC);
  ```

---

## Configuración

- Toda propiedad nueva resuelta por placeholder sin default (`jwt.secret=${JWT_SECRET}`) va en dos lugares o el contenedor no arranca. El `.env` solo interpola el compose: no puebla el entorno del contenedor.

  ```yaml
  # docker-compose.yml
    backend:
      environment:
        JWT_SECRET: ${JWT_SECRET}
        JWT_EXPIRATION_MS: ${JWT_EXPIRATION_MS:-3600000}
  ```
  ```dotenv
  # .env.example  (versionado: el .gitignore lo permite con !.env.example)
  # Mínimo 32 caracteres: jjwt exige 256 bits para HMAC-SHA
  JWT_SECRET=change-me-to-a-random-secret-of-at-least-32-characters
  ```

- Los filtros de la cadena de seguridad no llevan `@Component`: Spring Boot auto-registra cualquier bean que sea `Filter` y con `addFilterBefore` queda registrado dos veces. Declararlos como `@Bean` en `SecurityConfig`.

---

## Tests

- Todo escenario que dependa del status HTTP, o del orden entre validación y lógica, va en un `*ApiTest`: un test de service instancia el DTO a mano y saltea `@Valid` entero.
- Los tests de error afirman el cuerpo, no solo el status.
- Lo que dependa del motor —orden alfabético, collation, tipos— se verifica a mano contra el container: la suite corre en H2 y prod es PostgreSQL.
- Los datos de prueba distinguen el caso que se está probando: `Ana`/`Beto` ordenan igual por bytes que por locale, así que no prueban un orden locale-aware. Usar `andes`, `Ángela`, `Ñandú`, `zanahoria`.

---

## Comentarios

- Comentar solo la decisión que el código no muestra: por qué query nativa, por qué la normalización ocurre en Java, por qué `Collator` se instancia por llamada.
- Borrar el `@param` que repite el nombre del componente y el comentario que repite el nombre del método o de la anotación.
- Una regla se explica en un solo lugar, no en el repositorio, las proyecciones y cada DTO que la atraviesa.

## Ejemplo de uso

**Pedido:** "Revisá mi rama del endpoint de búsqueda de usuarios con la guía de backend antes de abrir la PR."
**Resultado:** recorre el checklist y las reglas contra el diff, y marca lo que no cumple con archivo, línea y el cambio que lo resuelve. Por ejemplo, un `LIKE` sin `ESCAPE`, un `ORDER BY` alfabético en la base o un escenario cubierto solo por un test de service.
