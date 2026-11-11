---
name: g09-redactar-tickets-tecnicos
description: Redacta, completa o revisa tickets técnicos de frontend y backend como especificaciones listas para implementar y probar. Úsalo cuando el usuario pida crear un ticket, convertir requerimientos en tickets, separar trabajo frontend/backend o validar que un ticket sea inequívoco y verificable.
metadata:
  tipo: skill
  area:
  - gestion
  - frontend
  - backend
  fase:
  - analisis
  - planificacion
  tecnologias:
  - agnostico
  metodologia:
  - agnostico
  herramientas:
  - codex
  requiere: []
  grupo: "09"
  autor:
    nombre: Xoaquin Sanchez Varsallona
    github: XoaquinSanchezVarsallona
  responsables:
  - XoaquinSanchezVarsallona
  madurez: experimental
  relacionados:
  - g09-review-ticket-pr
---
# Redactar tickets técnicos

Convertí el requerimiento en una especificación ejecutable, no en una historia de usuario genérica. El equipo debe poder implementar y probar el ticket sin adivinar contratos, estados, reglas ni límites.

## Elegir el tipo de ticket

- Si el trabajo es solo frontend, leé [references/frontend.md](#referencia-de-frontend).
- Si el trabajo es solo backend, leé [references/backend.md](#referencia-de-backend).
- Si abarca ambos, redactá dos tickets independientes —frontend y backend— y leé ambas referencias. No mezcles responsabilidades en un único ticket salvo que el usuario lo pida expresamente.
- Si el usuario entrega un ticket como ejemplo, extraé su nivel de precisión y convenciones; no copies requisitos funcionales que no correspondan al nuevo trabajo.

## Reglas de redacción

1. Preservá literalmente nombres de rutas, endpoints, componentes, clases, métodos, campos, query keys, roles, status codes, mensajes visibles y mensajes de error proporcionados.
2. Hacé explícitas las diferencias con impacto observable: autenticado/no autenticado, dueño/tercero, vacío/no vacío, `null`/ausente/cero, mobile/desktop, éxito/error y orden de operaciones.
3. Identificá qué artefactos existentes deben reutilizarse y qué no debe crearse de nuevo. Si hay acceso al repositorio y el ticket debe alinearse con él, inspeccioná primero las convenciones pertinentes.
4. No inventes endpoints, campos, componentes ni reglas. Cuando falte una decisión imprescindible, agregá una sección breve `Definiciones pendientes`; si puede resolverse con una suposición conservadora, declarala como `Supuesto`.
5. Incluí estados de carga, error, vacío, reintento y éxito cuando apliquen. Describí la secuencia exacta de efectos asíncronos si el orden importa.
6. Cerrá siempre con `Fuera de alcance` y `Criterios de aceptación`. Los criterios deben ser concretos, observables y cubrir las reglas críticas, no repetir vagamente el objetivo.
7. Incluí pruebas o casos de prueba cuando el ticket defina lógica, validaciones, permisos o contratos. Diferenciá claramente requisitos obligatorios de recomendaciones.
8. Escribí en español claro, directo y técnico. Usá tablas cuando compacten rutas, endpoints, permisos o respuestas. Evitá introducciones ceremoniales, estimaciones y detalles genéricos que no cambien la implementación.

## Control de calidad

Antes de entregar, comprobá que:

- alcance, implementación, pruebas y criterios de aceptación sean consistentes entre sí;
- cada comportamiento condicional indique condición y resultado;
- cada operación protegida defina autenticación/autorización y comportamiento ante incumplimiento;
- cada validación indique restricción y mensaje/status esperado si fueron definidos;
- la persistencia, invalidación o actualización de caché y manejo de errores estén especificados cuando correspondan;
- ninguna funcionalidad fuera de alcance aparezca implícitamente como obligatoria;
- dependencias, inconsistencias o migraciones faltantes estén señaladas sin ampliar el alcance por cuenta propia.

## Ejemplo de uso

**Pedido:** Separá este requerimiento de edición de perfil en tickets frontend y backend, conservando los endpoints y permisos del contrato adjunto.

**Resultado:** Dos especificaciones con contratos, estados, pruebas, fuera de alcance y criterios de aceptación; las decisiones faltantes quedan explícitas.


## Referencia de frontend

### Ticket de frontend

Usá solo las secciones que aporten información real al requerimiento, manteniendo este orden general.

#### Estructura recomendada

1. **Título y objetivo:** qué experiencia se incorpora y para quién.
2. **Alcance:** pantallas, flujos y piezas compartidas incluidas.
3. **Rutas:** tabla con ruta, componente y guard/acceso.
4. **Pantallas o flujos:** una sección por pantalla con layout, contenido, comportamiento responsive, condiciones de renderizado, navegación e interacción.
5. **Datos y estado:** queries, query keys, mutations, parámetros, caché, estado local y secuencia de efectos.
6. **Estados de UI:** carga, error, vacío, reintento y éxito, conservando los textos exactos.
7. **Formularios:** librerías, schema, coerciones, defaults, reset, campos, restricciones y mensajes exactos.
8. **Media y recursos:** previews, persistencia, limpieza/revocación y límites cuando haya archivos o imágenes.
9. **Componentes compartidos:** qué reutilizar y la responsabilidad específica de cada componente nuevo inevitable.
10. **Cliente API y tipos:** firmas, payloads, responses e interfaces necesarias para implementar el ticket.
11. **Pruebas:** permisos, renderizado condicional, validaciones, interacciones, fallos y efectos de caché relevantes.
12. **Fuera de alcance.**
13. **Criterios de aceptación.**

#### Precisiones importantes

- Indicá la fuente de cada identificador: params, sesión, props o respuesta de API.
- En guards, definí por separado el caso sin sesión y el caso sin rol/permisos, incluyendo cada redirección.
- Para formularios editables, especificá inicialización, resincronización al cambiar datos, submit pendiente, prevención de doble envío y feedback.
- Para mutaciones de varios pasos, indicá si son secuenciales o paralelas, qué se actualiza tras cada confirmación y qué queda disponible para reintentar si falla parcialmente.
- Para responsive, describí solo diferencias funcionales o de layout relevantes; usá clases exactas únicamente si forman parte del contrato solicitado.
- No diseñes un backend alternativo. Documentá el contrato que consume el frontend y cualquier dependencia que deba existir.


## Referencia de backend

### Ticket de backend

Usá solo las secciones que aporten información real al requerimiento, manteniendo este orden general.

#### Estructura recomendada

1. **Título y objetivo:** capacidad de negocio y recurso administrado.
2. **Alcance:** casos de uso y capas afectadas.
3. **Modelo de datos:** tablas, columnas, tipos, nulabilidad, defaults, índices, constraints, claves foráneas, cascadas y migraciones.
4. **Entidades y relaciones:** anotaciones relevantes, ownership, colecciones, orden y auditoría.
5. **Endpoints:** tabla con método, path, autenticación/autorización, request, response y status exitoso.
6. **DTOs y validación:** firmas o esquemas, campos requeridos/opcionales, Bean Validation y semántica de `null` o ausencia.
7. **Lógica de negocio:** una sección por método con búsqueda, errores, cambios de estado, orden de operaciones, persistencia y respuesta.
8. **Transacciones:** escritura frente a `readOnly`, dirty checking, cascadas y atomicidad cuando sean relevantes.
9. **Errores esperados:** excepción, status y mensaje exacto si fue definido.
10. **Repositorio:** interfaz, queries o métodos nuevos necesarios.
11. **Casos de prueba:** happy paths, conflictos, no encontrado, permisos, validación, ordenamiento y semánticas de actualización parcial.
12. **Fuera de alcance.**
13. **Criterios de aceptación.**

#### Precisiones importantes

- Para rutas equivalentes a `/me`, el identificador debe provenir del principal autenticado; no aceptes un identificador del body o query salvo requisito explícito.
- Distinguí con exactitud creación, reemplazo y actualización parcial. Documentá por campo qué ocurre con valor, `null` y ausencia.
- Indicá quién mantiene campos derivados y si el feature solo los expone.
- Si una migración o contrato existente está incompleto, señalá el cambio necesario y su relación con las entidades; no ocultes la inconsistencia.
- Especificá orden estable de colecciones cuando el consumidor dependa de él.
- Reutilizá las excepciones y el manejo global existentes si el proyecto ya los define.
- No agregues endpoints auxiliares, almacenamiento real, búsquedas u operaciones administrativas salvo que estén dentro del alcance solicitado.
