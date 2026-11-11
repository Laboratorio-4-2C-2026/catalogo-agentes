---
name: g09-kotlin-springboot
description: Orienta el desarrollo de aplicaciones Kotlin con Spring Boot; usar al implementar o revisar servicios con ese stack.
metadata:
  tipo: skill
  area:
  - backend
  fase:
  - desarrollo
  tecnologias:
  - kotlin
  - spring-boot
  metodologia:
  - agnostico
  herramientas:
  - codex
  requiere: []
  grupo: 09
  autor: null
  responsables:
  - Agustin5421
  madurez: experimental
  relacionados: []
  autor_original: No identificado; publicado en GitHub Awesome Copilot
---

# Spring Boot with Kotlin Best Practices

Your goal is to help me write high-quality, idiomatic Spring Boot applications using Kotlin.

## Project Setup & Structure

- **Build Tool:** Use Maven (`pom.xml`) or Gradle (`build.gradle`) with the Kotlin plugins (`kotlin-maven-plugin` or `org.jetbrains.kotlin.jvm`).
- **Kotlin Plugins:** For JPA, enable the `kotlin-jpa` plugin to automatically make entity classes `open` without boilerplate.
- **Starters:** Use Spring Boot starters (e.g., `spring-boot-starter-web`, `spring-boot-starter-data-jpa`) as usual.
- **Package Structure:** Organize code by feature/domain (e.g., `com.example.app.order`, `com.example.app.user`) rather than by layer.

## Dependency Injection & Components

- **Primary Constructors:** Always use the primary constructor for required dependency injection. It's the most idiomatic and concise approach in Kotlin.
- **Immutability:** Declare dependencies as `private val` in the primary constructor. Prefer `val` over `var` everywhere to promote immutability.
- **Component Stereotypes:** Use `@Service`, `@Repository`, and `@RestController` annotations just as you would in Java.

## Configuration

- **Externalized Configuration:** Use `application.yml` for its readability and hierarchical structure.
- **Type-Safe Properties:** Use `@ConfigurationProperties` with `data class` to create immutable, type-safe configuration objects.
- **Profiles:** Use Spring Profiles (`application-dev.yml`, `application-prod.yml`) to manage environment-specific configurations.
- **Secrets Management:** Never hardcode secrets. Use environment variables or a dedicated secret management tool like HashiCorp Vault or AWS Secrets Manager.

## Web Layer (Controllers)

- **RESTful APIs:** Design clear and consistent RESTful endpoints.
- **Data Classes for DTOs:** Use Kotlin `data class` for all DTOs. This provides `equals()`, `hashCode()`, `toString()`, and `copy()` for free and promotes immutability.
- **Validation:** Use Java Bean Validation (JSR 380) with annotations (`@Valid`, `@NotNull`, `@Size`) on your DTO data classes.
- **Error Handling:** Implement a global exception handler using `@ControllerAdvice` and `@ExceptionHandler` for consistent error responses.

## Service Layer

- **Business Logic:** Encapsulate business logic within `@Service` classes.
- **Statelessness:** Services should be stateless.
- **Transaction Management:** Use `@Transactional` on service methods. In Kotlin, this can be applied to class or function level.

## Data Layer (Repositories)

- **JPA Entities:** Define entities as classes. Remember they must be `open`. It's highly recommended to use the `kotlin-jpa` compiler plugin to handle this automatically.
- **Null Safety:** Leverage Kotlin's null-safety (`?`) to clearly define which entity fields are optional or required at the type level.
- **Spring Data JPA:** Use Spring Data JPA repositories by extending `JpaRepository` or `CrudRepository`.
- **Coroutines:** For reactive applications, leverage Spring Boot's support for Kotlin Coroutines in the data layer.

## Logging

- **Companion Object Logger:** The idiomatic way to declare a logger is in a companion object.
  ```kotlin
  companion object {
      private val logger = LoggerFactory.getLogger(MyClass::class.java)
  }
  ```
- **Parameterized Logging:** Use parameterized messages (`logger.info("Processing user {}...", userId)`) for performance and clarity.

## Testing

- **JUnit 5:** JUnit 5 is the default and works seamlessly with Kotlin.
- **Idiomatic Testing Libraries:** For more fluent and idiomatic tests, consider using **Kotest** for assertions and **MockK** for mocking. They are designed for Kotlin and offer a more expressive syntax.
- **Test Slices:** Use test slice annotations like `@WebMvcTest` or `@DataJpaTest` to test specific parts of the application.
- **Testcontainers:** Use Testcontainers for reliable integration tests with real databases, message brokers, etc.

## Coroutines & Asynchronous Programming

- **`suspend` functions:** For non-blocking asynchronous code, use `suspend` functions in your controllers and services. Spring Boot has excellent support for coroutines.
- **Structured Concurrency:** Use `coroutineScope` or `supervisorScope` to manage the lifecycle of coroutines.

## Ejemplo de uso

**Pedido:** Ayudame a implementar un endpoint Kotlin con Spring Boot.

**Resultado:** Aplica las convenciones y recomendaciones de la skill al servicio.


## Licencia original

MIT License

Copyright GitHub, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
