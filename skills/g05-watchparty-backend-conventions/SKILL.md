---
name: g05-watchparty-backend-conventions
description: Implementa y revisa módulos y endpoints Express de WatchParty siguiendo sus capas, contratos, errores
  e inyección de dependencias. Usar al crear o modificar el backend del repositorio.
metadata:
  tipo: skill
  area:
  - backend
  fase:
  - desarrollo
  - revision
  tecnologias:
  - express
  - typescript
  - supabase
  herramientas:
  - codex
  requiere: []
  grupo: '05'
  autor:
    nombre: Pedro de Foronda
    github: Pedrodeforonda
  responsables:
  - Pedrodeforonda
  madurez: experimental
  relacionados:
  - g03-express-project-structure-guidelines
---

# Convenciones de backend de WatchParty

## Entradas y alcance

Aplicá estas convenciones al crear, modificar o revisar módulos y endpoints del backend. Partí del requerimiento y del código del módulo, identificá la regla y el contrato afectados e implementá el cambio siguiendo el patrón local. Para un pedido de revisión, describí los hallazgos sin aplicar correcciones que no se hayan solicitado.

## Estructura del backend

El backend vive en `apps/api`, paquete `@watchparty/api`, con Express y TypeScript ESM. Los módulos, por ejemplo `reviews`, separan `domain`, `application`, `http` e `infrastructure`. `src/app.ts` compone la app y `src/server.ts` cumple la función de arranque local. Hay errores compartidos en `src/errors` y middleware en `src/middleware`. Verificá sus APIs reales antes de escribir un import.

## Procedimiento

1. Encontrá un módulo homólogo por comportamiento, no solo por nombre. Leé ruta, caso de uso, interfaz de store, implementación y punto de composición. Registrá dónde vive la regla y evitá una nueva arquitectura paralela.
2. Definí la entrada y salida del caso de uso con el vocabulario existente. El dominio representa reglas y contratos propios; infraestructura adapta Supabase u otro servicio. No hagas que un detalle HTTP o un cliente de proveedor se convierta en una dependencia obligatoria del dominio sin un precedente aprobado.
3. En `http`, seguí los mecanismos existentes para parseo, validación y obtención de identidad. Usá la identidad validada por el servidor; un userId enviado por el navegador no demuestra pertenencia. No uses una validación solo visual como control backend.
4. Conservá status, códigos y estructura de errores mediante las clases y middleware vigentes. `app.test.ts` verifica un sobre `error` con `code` y `message` y ausencia de detalles internos para errores inesperados. No serialices objetos del proveedor, stack traces o tokens en respuestas.
5. Inyectá dependencias mediante los puntos de composición existentes. Una implementación de prueba no debe elegirse automáticamente en producción al fallar configuración. Revisá el default export de `app.ts` y el contrato de despliegue antes de mover composición: Vercel puede cargar la app sin ejecutar `server.ts`.
6. Concentrá el acceso a datos en infraestructura. Usá campos explícitos y filtros por recurso/identidad donde corresponda. No amplíes privilegios ni introduzcas claves de servicio en la web. Cambios de schema se revisan aparte; esta skill no los ejecuta.
7. Implementá el módulo, su composición y la cobertura pertinente. Para las convenciones de pruebas, consultá [Creación de tests](../g05-watchparty-test-creation/SKILL.md). Ejecutá los checks del paquete y mantené acotado el diff; no cambies dependencias globales ni convenciones ajenas al requerimiento.

## Entrega

Mapa de archivos/capas y flujo request → validación/identidad → caso de uso → store → respuesta. En revisión, hallazgos con impacto y ubicación; en implementación, resumen de cambios y validaciones reales. Separá reglas pendientes de detalles ya resueltos por el patrón existente.

## Ejemplo de uso

**Pedido:** Agregá un endpoint de consulta de una entidad propia siguiendo el backend actual.

**Resultado:** Plan o implementación según autorización, reutilizando identidad, errores y store, con el cambio de composición mínimo.

**Otro uso:** Revisar un endpoint que consulta Supabase desde un handler extenso. Identificá responsabilidades mezcladas y propuesta compatible con el módulo existente, sin refactorizar por iniciativa propia.


## Trabajo en el repositorio

Trabajá sobre el checkout actual de WatchParty. Leé los `AGENTS.md` aplicables, el `README.md` y los archivos del módulo antes de modificarlo. Las rutas `apps/`, `supabase/` y `docs/` se interpretan desde la raíz del monorepo. Resolvé herramientas, scripts y versiones desde `package.json`, el lockfile y la configuración vigente; seguí los ejemplos cercanos cuando el código haya evolucionado.

Cuando la tarea pida implementar, realizá los cambios de código, tests o documentación necesarios dentro de su alcance. Si pide una revisión o un diagnóstico sin cambios, entregá los hallazgos. Conservá trabajo ajeno y cambios no relacionados. No introduzcas otra arquitectura, librería o configuración para evitar entender el patrón existente.

Ejecutá las validaciones pertinentes y registrá los comandos y resultados reales. Antes de correr un script, comprobá sus dependencias y si modifica datos o llama a servicios: las pruebas aisladas usan dobles y datos ficticios; las verificaciones con efectos externos requieren un entorno y alcance previstos para ellas. No expongas secretos. Informá qué cambió, dónde, qué se verificó y qué quedó pendiente; citá archivos, líneas o evidencia concreta. Una prueba no ejecutada no cuenta como exitosa.
