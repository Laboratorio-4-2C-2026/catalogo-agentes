# Ejemplo de output — de lecciones a reglas (Study Arena, Sprint 3)

Corrida real del 11/11/2026 sobre el Sprint 3 (desde el 15/10), commit `874dc77`.

**Fuentes:** 25 PRs mergeados, con 13 pedidos de cambios, 32 comentarios en línea, 15 reviews con texto y 5 comentarios generales; 238 corridas de CI; reglas existentes en el repo.
**Reglas existentes:** no hay `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md` ni template de PR. Hay correcciones puntuales en el código (`StrictIntegerDeserializer`, `spring.jpa.open-in-view=false`).

## Patrones encontrados (por impacto)

| # | Patrón | Ocurrencias | Costo |
|---|---|---|---|
| 1 | **Concurrencia y transacciones**: chequear y después escribir sin lock, o esperar a un servicio externo con una transacción o conexión abierta. | 6 comentarios en 5 PRs: #71 (avatar bloquea la fila mientras responde Azure), #76 (lock que puede dejar la app sin conexiones 30 s), #78 (publicar, editar y eliminar en paralelo), #84 (dos PUT simultáneos dan 500), #89 (conexión retenida durante la llamada a Gemini) | Errores 500 en producción con carga real; difíciles de reproducir. |
| 2 | **Números que aceptan decimales o texto** (coerción de Jackson): `1.7` o `"2"` se convierten sin aviso en otro valor. | 4 PRs: #75 (`correctIndex`), #76 (`selectedIndex`, `questionIndex`), #84 (`studyPeriod` numérico), #89 (`correctIndex` devuelto por la IA) | Respuestas correctas guardadas mal sin ningún error. Se corrigió **campo por campo**, por eso reaparece. |
| 3 | **Textos largos y pantallas angostas** rompen la UI. | 4 PRs: #72 (nombre largo rompe la card del perfil), #83 (pestañas con scroll horizontal a 320 px), #90 (palabra larga deja "Siguiente" fuera de vista), #91 (diálogos que desbordan) | Retrabajo en cada pantalla nueva. |
| 4 | **Foco y accesibilidad**: el foco se pierde en el `body` después de publicar o eliminar, y hay elementos sin nombre accesible. | 3 PRs: #91 y #96 (el mismo bug de foco, aunque ya estaba resuelto en `MaterialsPage`), #72 (input de archivo invisible con foco, chip de puntos ilegible para lectores de pantalla) | Un arreglo que existe no se reutiliza. |
| 5 | **Tests que faltan o no son deterministas.** | 2 PRs: #74 (faltan los tests de heartbeat y leave que pedía el ticket, y los tests dependen de la fecha real), #71 (faltan variantes de los escenarios 7, 10, 17 y 23) | La suite queda en verde aunque se rompa lo que pedía el ticket. |

## Reglas propuestas (máximo 5)

**1. Coerción estricta global (patrón 2)**
- **Destino:** código + test (lo más automático).
- **Regla:** configurar una sola vez el mapper JSON global de Spring para que rechace decimales y texto en campos enteros y números en campos de texto o enum, en lugar de anotar `@JsonDeserialize(using = StrictIntegerDeserializer.class)` campo por campo. Sumar un test de API que mande `1.5` y `"1"` a un campo entero y espere `400`.
- **Cómo se verifica:** el test falla si alguien desactiva la configuración o agrega un DTO nuevo sin ella.

**2. Nada externo dentro de una transacción; nada de chequear y después escribir sin protección (patrón 1)**
- **Destino:** `CLAUDE.md` (nuevo) + checklist del PR.
- **Texto para `CLAUDE.md`:**
  ```
  - No llames a servicios externos (Azure Storage, Gemini, HTTP) dentro de un método @Transactional: primero la llamada externa, después la escritura, o al revés con compensación. Retener la conexión deja a la API sin conexiones.
  - Todo "busco y si no existe, creo" o "leo el estado y guardo" lleva un lock sobre la fila o una constraint única con manejo de la violación (ver el patrón de PointsService.awardPoints).
  ```
- **Cómo se verifica:** item del template de PR: "¿Hay llamadas externas en métodos `@Transactional`? ¿Hay chequeos y escrituras sin lock ni constraint?".

**3. Probar textos largos y 320 px (patrón 3)**
- **Destino:** template de PR (nuevo) + `CLAUDE.md`.
- **Item del template:** `- [ ] Probé la pantalla a 320 px y con una palabra larga sin espacios (nombre, título, opción).`
- **Línea para `CLAUDE.md`:** `En diálogos y grids, los hijos de texto llevan min-w-0 y break-words: el contenido no puede definir el ancho mínimo de la columna.`

**4. Un solo helper para devolver el foco (patrón 4)**
- **Destino:** código (extraer el arreglo de `MaterialsPage` a un hook compartido) + `CLAUDE.md`.
- **Línea para `CLAUDE.md`:** `Después de eliminar o publicar desde un diálogo, usá el hook compartido para devolver el foco; no repitas el arreglo en cada pantalla.`
- **Cómo se verifica:** `g07-auditoria-accesibilidad` sobre las pantallas con diálogos.

**5. Escenarios del ticket mapeados a tests y reloj inyectado (patrón 5)**
- **Destino:** template de PR + `CLAUDE.md`.
- **Item del template:** una tabla `Escenario del ticket → test que lo cubre`.
- **Línea para `CLAUDE.md`:** `Los tests no leen la fecha real: usan el Clock inyectado (como WeekService) fijado en el test.`

## Reglas existentes que no se cumplen

- **`StrictIntegerDeserializer`** existe pero hay que acordarse de anotarlo en cada campo: por eso el patrón 2 reapareció en 4 PRs. Propuesta: la regla 1 lo vuelve global.
- **El arreglo del foco de `MaterialsPage`** existe pero no se reutilizó en #91 ni en #96. Propuesta: la regla 4.

## Candidatas para el próximo sprint

- **Un dato inválido o ausente borra información en silencio** (#84: una clave ausente en el PUT borra la meta; #88: un texto inválido en un input numérico borra la meta).
- **Mensajes de resultado calculados con el dato equivocado** (#90: "Sumaste 0 puntos" en un intento que no daba puntos; #91: "No se pudo publicar" cuando sí se publicó; #88: "100 %" y "Te faltan 0 min" sin la meta cumplida).
- **Base de los PRs apilados** (#72 y #88: apuntar el PR a la branch de la que sale y hacer rebase; #80: no mergear hasta que esté el front).

## Observaciones

- El CI no falló ninguna vez en el período (0 de 238 corridas): los problemas los encuentran las reviews y el QA, no el CI. Las reglas 1 y 3 los llevan al CI o al checklist.
- Las reviews de QA son muy completas (escenarios del ticket, pruebas E2E automatizadas y StepCI); el 52% de los PRs (13 de 25) tuvo pedido de cambios.
- No se analizaron los tickets reabiertos de Jira (requiere el historial de cambios de cada ticket).
- El reporte no nombra personas: los patrones son del equipo.
