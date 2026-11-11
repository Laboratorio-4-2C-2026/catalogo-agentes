# Ticket de frontend

Usá solo las secciones que aporten información real al requerimiento, manteniendo este orden general.

## Estructura recomendada

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

## Precisiones importantes

- Indicá la fuente de cada identificador: params, sesión, props o respuesta de API.
- En guards, definí por separado el caso sin sesión y el caso sin rol/permisos, incluyendo cada redirección.
- Para formularios editables, especificá inicialización, resincronización al cambiar datos, submit pendiente, prevención de doble envío y feedback.
- Para mutaciones de varios pasos, indicá si son secuenciales o paralelas, qué se actualiza tras cada confirmación y qué queda disponible para reintentar si falla parcialmente.
- Para responsive, describí solo diferencias funcionales o de layout relevantes; usá clases exactas únicamente si forman parte del contrato solicitado.
- No diseñes un backend alternativo. Documentá el contrato que consume el frontend y cualquier dependencia que deba existir.
