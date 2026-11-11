---
name: g10-nestjs-endpoint-doc-generator
description: Generar documentación en Markdown de los endpoints de un módulo NestJS a partir de su controller y DTOs reales, sin inventar comportamiento. Usar al terminar un módulo backend o antes de documentar la API para el resto del equipo.
metadata:
  tipo: skill
  area:
  - documentacion
  - backend
  fase:
  - mantenimiento
  tecnologias:
  - nestjs
  - typescript
  metodologia:
  - agnostico
  herramientas:
  - claude-code
  requiere: []
  grupo: "10"
  autor:
    nombre: Victoria Martin Botter
    github: vmartinbotter
  responsables:
  - vmartinbotter
  madurez: experimental
  relacionados:
  - g10-dto-validation-checker
  - g10-adr-writer
  - g05-watchparty-api-documentation
---
# NestJS Endpoint Doc Generator

Generar documentación de los endpoints de un módulo del backend de Conexia (ej. `trips`, `travel-intents`, `travel-matches`, `subjects`, `profile`) leyendo el controller y los DTOs reales, no suponiendo cómo "debería" funcionar.

## Qué leer

1. El `*.controller.ts` del módulo: método HTTP, ruta, guards (`@UseGuards`), y si usa `@CurrentUser()`.
2. Los DTOs de `dto/` referenciados en cada método, para documentar el body/query real (campos, tipo, opcionalidad según `@IsOptional`).
3. El `*.service.ts` solo para entender qué devuelve cada método (forma de la respuesta), sin copiar su lógica interna.

## Qué generar

Un archivo Markdown (o la sección que el usuario indique) con, por endpoint:
- Método y ruta (ej. `POST /trips/:id/passengers`).
- Si requiere autenticación (según el guard detectado).
- Parámetros de ruta, query y body, con su tipo y si son opcionales.
- Códigos de respuesta relevantes (incluyendo los que lanza explícitamente el controller/service, como `ForbiddenException` o `NotFoundException`).
- Un ejemplo de request/response armado a partir de los tipos reales, marcado como ejemplo (no como valor garantizado por el backend).

## Reglas

- No documentar comportamiento que no esté en el código leído. Si algo no se puede confirmar (ej. un rate limit), decir "no confirmado en código" en vez de omitirlo o inventarlo.
- Si el controller cambia después, esta documentación queda desactualizada: no asumir que sigue vigente sin volver a generarla.

## Ejemplo de uso

**Pedido:** Documentá los endpoints del módulo de trips para que el resto del equipo los pueda consumir desde el frontend.
**Resultado:** Un Markdown con cada endpoint de `trips.controller.ts`, sus parámetros según los DTOs reales, autenticación requerida y un ejemplo de request/response.
