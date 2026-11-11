# Ticket de backend

Usá solo las secciones que aporten información real al requerimiento, manteniendo este orden general.

## Estructura recomendada

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

## Precisiones importantes

- Para rutas equivalentes a `/me`, el identificador debe provenir del principal autenticado; no aceptes un identificador del body o query salvo requisito explícito.
- Distinguí con exactitud creación, reemplazo y actualización parcial. Documentá por campo qué ocurre con valor, `null` y ausencia.
- Indicá quién mantiene campos derivados y si el feature solo los expone.
- Si una migración o contrato existente está incompleto, señalá el cambio necesario y su relación con las entidades; no ocultes la inconsistencia.
- Especificá orden estable de colecciones cuando el consumidor dependa de él.
- Reutilizá las excepciones y el manejo global existentes si el proyecto ya los define.
- No agregues endpoints auxiliares, almacenamiento real, búsquedas u operaciones administrativas salvo que estén dentro del alcance solicitado.
