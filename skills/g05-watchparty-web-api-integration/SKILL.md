---
name: g05-watchparty-web-api-integration
description: 'Integra o revisa pantallas React de WatchParty con su API Node: cliente tipado, sesión, carga, errores
  y ciclo de vida asíncrono. Usar al conectar datos; la apariencia, los tokens y los componentes visuales corresponden
  a watchparty-ui.'
metadata:
  tipo: skill
  area:
  - frontend
  - backend
  fase:
  - desarrollo
  - revision
  tecnologias:
  - react
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
  - g11-revisar-react-query
  - g05-watchparty-ui
  - g05-watchparty-bug-diagnosis
---

# Integración de la web con la API

## Entradas y fronteras

Localizá la pantalla o feature, el endpoint del backend y el mecanismo de sesión en el checkout. Leé el contrato desde sus rutas, validadores y tests; no inventes campos ni rutas. Implementá la conexión de datos y errores siguiendo los clientes existentes. Para apariencia y componentes, consultá [WatchParty UI](../g05-watchparty-ui/SKILL.md). No presupongas TanStack Query ni otra librería que el proyecto no use.

## Estructura de la web

La web está en `apps/web`, con React, TypeScript, Vite y React Router. Existen áreas `src/app`, `src/auth`, `src/lib`, `src/features`, `src/components` y `src/layouts`; inspeccioná sus responsabilidades vigentes. La guía de UI establece Supabase para Auth y la API Node para datos de la aplicación: no agregues `supabase.from(...)` a las pantallas.

## Procedimiento

1. Seguí un consumo ya existente desde pantalla hasta función HTTP y manejo de sesión. Reutilizá cliente/base URL/configuración del proyecto antes de crear otro fetch helper, provider o almacén. Identificá el contrato real de respuestas y errores del endpoint.
2. Definí tipos de entrada/salida según ese contrato; distinguí null, ausente, vacío y cero. TypeScript no valida una respuesta externa en runtime: usá la estrategia de validación/mapeo existente en el límite y reportá cualquier gap que necesite decisión.
3. Obtené la sesión con el mecanismo de `auth` del proyecto y enviá credenciales únicamente al destino previsto. Diferenciá 401, 403, validación, recurso ausente y falla temporal según el contrato. No copies tokens a mensajes o logs y no crees un segundo sistema de sesión.
4. Explicitá carga inicial, datos, vacío, error y operación pendiente. Conservá la intención del usuario al fallar; no conviertas una petición iniciada en confirmación de éxito. Dejá el diseño visual a los patrones de UI existentes.
5. Analizá cambios de parámetros, desmontaje y respuestas tardías. Una respuesta de una pantalla, usuario o filtro anterior no debe imponerse sobre el contexto actual. Si existe caché, inspeccioná claves, dueño y limpieza; si no existe, no introduzcas una por costumbre.
6. Las escrituras solo ocurren como resultado de una acción definida. Tratá doble envío, timeout con resultado desconocido y reintento de acuerdo con la semántica del backend: no reenvíes mutaciones ciegamente. No presupongas que cancelar la espera cancela el efecto remoto.
7. Conectá los archivos necesarios y agregá pruebas con dobles del límite HTTP/sesión. No llames a servicios reales como efecto de un test de componente. No cambies rutas, providers o arquitectura fuera del alcance.

## Entrega

Mapa pantalla → cliente → endpoint → estado, contrato usado, comportamiento por error y validaciones. En revisión, tabla de discrepancias con evidencia. En implementación, archivos modificados y qué se ejecutó realmente.

## Ejemplo de uso

**Pedido:** Conectá una pantalla de historial al endpoint existente con filtros y estado vacío.

**Resultado:** Consumo tipado, estados y control de solicitudes del contexto anterior, sin cambiar el diseño ni consultar la base desde React.

**Otro uso:** Revisar un formulario que muestra éxito antes de recibir confirmación. Documentá la secuencia, el estado correcto y la comprobación mínima pendiente.


## Trabajo en el repositorio

Trabajá sobre el checkout actual de WatchParty. Leé los `AGENTS.md` aplicables, el `README.md` y los archivos del módulo antes de modificarlo. Las rutas `apps/`, `supabase/` y `docs/` se interpretan desde la raíz del monorepo. Resolvé herramientas, scripts y versiones desde `package.json`, el lockfile y la configuración vigente; seguí los ejemplos cercanos cuando el código haya evolucionado.

Cuando la tarea pida implementar, realizá los cambios de código, tests o documentación necesarios dentro de su alcance. Si pide una revisión o un diagnóstico sin cambios, entregá los hallazgos. Conservá trabajo ajeno y cambios no relacionados. No introduzcas otra arquitectura, librería o configuración para evitar entender el patrón existente.

Ejecutá las validaciones pertinentes y registrá los comandos y resultados reales. Antes de correr un script, comprobá sus dependencias y si modifica datos o llama a servicios: las pruebas aisladas usan dobles y datos ficticios; las verificaciones con efectos externos requieren un entorno y alcance previstos para ellas. No expongas secretos. Informá qué cambió, dónde, qué se verificó y qué quedó pendiente; citá archivos, líneas o evidencia concreta. Una prueba no ejecutada no cuenta como exitosa.
