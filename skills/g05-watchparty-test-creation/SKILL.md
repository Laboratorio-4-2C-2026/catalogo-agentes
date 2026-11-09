---
name: g05-watchparty-test-creation
description: Crea y mantiene tests unitarios, HTTP y React de WatchParty con Vitest, Supertest y Testing Library.
  Usar al implementar funcionalidades, corregir defectos o reforzar cobertura siguiendo la estructura del repositorio.
metadata:
  tipo: skill
  area:
  - qa
  - backend
  - frontend
  fase:
  - desarrollo
  - testing
  tecnologias:
  - typescript
  - vitest
  - supertest
  - react
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
  - g03-javascript-typescript-vitest
  - g03-supertest-api-testing
  - g03-express-test-builder-agent
---

# Creación y estructura de tests de WatchParty

## Entradas y frontera

Identificá el comportamiento que se agrega, corrige o necesita cobertura y localizá su implementación y tests existentes. Derivá los escenarios del requerimiento, los contratos y los riesgos del código; incorporá escenarios ya definidos cuando existan. Para una tarea de tests, creá o actualizá los archivos y helpers necesarios. Si la tarea también incluye corregir un defecto productivo, mantené separadas la prueba que lo reproduce y la corrección mínima. No cambies el comportamiento esperado ni debilites una aserción para conseguir verde. Si solo se pide un diseño de pruebas, entregá la propuesta sin implementar.

## Estructura de tests

- API: paquete `@watchparty/api`, Vitest y Supertest; `apps/api/src/app.test.ts` usa `describe`, `it`, `expect`, una app Express y dependencias inyectadas. Hay capas `domain`, `application`, `http` e `infrastructure` dentro de `apps/api/src/modules/`.
- Web: paquete `web`, Vitest, Testing Library, user-event, jest-dom y JSDOM. `apps/web/vite.config.ts` registra `src/test/setup.ts`. Existe `apps/web/src/App.test.tsx`; no crees un segundo setup si el actual sirve.
- Conservá sufijos `.test.ts` o `.test.tsx` según el archivo y los imports ESM del paquete. Para un módulo nuevo, buscá un test homólogo y seguí su ubicación; no reorganices tests existentes.

## Procedimiento

1. Leé la implementación y dos pruebas cercanas cuando estén disponibles. Elegí nivel: unidad para lógica aislable; HTTP con Supertest para contrato de ruta/middlewares; componente para interacción React. No llames E2E a un componente en JSDOM.
2. Organizá `describe` por unidad o comportamiento y `it` por resultado observable. Cada caso sigue preparar → actuar → verificar, sin necesidad de tres comentarios si el código ya es claro. Usá nombres que expliquen condición y resultado. Parametrizá variantes equivalentes; mantené separados escenarios con causas diferentes.
3. Prepará datos ficticios mínimos, con identidad y fechas explícitas. Construí dependencias nuevas por caso si tienen estado. Inyectá dobles por interfaces existentes; no conectes Supabase real ni API-Football para un test aislado. No conviertas un doble de prueba en fallback productivo.
4. Verificá resultado significativo: en API, status y forma/contenido relevante; en aplicación, regla y efectos sobre el doble; en React, elementos por rol/nombre y acciones de usuario. Evitá asserts de detalles internos, snapshots enormes o mocks de la propia función bajo prueba.
5. Esperá acciones/promesas realmente observables. No uses sleeps para tapar carreras. Controlá reloj/aleatoriedad solo cuando afecten al comportamiento y restauralos. Limpiá mocks, listeners, timers y cambios de entorno con las utilidades compatibles con el setup existente. No restaures silenciosamente una variable a un valor distinto del anterior.
6. Inspeccioná el comando antes de ejecutarlo. Los scripts de los paquetes son `pnpm --filter @watchparty/api test` y `pnpm --filter web test`; ambos llaman `vitest run`. Para un subconjunto, verificá cómo pasan argumentos en la versión de pnpm instalada. Separá los smoke/scripts de verificación: algunos crean usuarios o escriben datos y no equivalen a unit tests.
7. Si la ejecución falla, distinguí defecto del test, defecto de producto y entorno faltante. No agregues skip, reintentos, exclusiones ni reduzcas cobertura para ocultarlo.

## Entrega

Mapa escenario → archivo → aserción principal, archivos creados o propuesta, dependencias simuladas, comandos realmente ejecutados y resultado. Informá qué no se verificó. Un test escrito pero no ejecutado se marca como tal.

## Ejemplo de uso

**Pedido:** Implementá tests del caso de uso que guarda una reseña con un store en memoria.

**Resultado:** Archivo junto al patrón del módulo, casos deterministas para los escenarios acordados y validación autorizada, sin acceder a Supabase real.

**Otro uso:** Probar un formulario React. Usá JSDOM, Testing Library y user-event para sus estados e interacción; los breakpoints visuales necesitan navegador y quedan separados.


## Trabajo en el repositorio

Trabajá sobre el checkout actual de WatchParty. Leé los `AGENTS.md` aplicables, el `README.md` y los archivos del módulo antes de modificarlo. Las rutas `apps/`, `supabase/` y `docs/` se interpretan desde la raíz del monorepo. Resolvé herramientas, scripts y versiones desde `package.json`, el lockfile y la configuración vigente; seguí los ejemplos cercanos cuando el código haya evolucionado.

Cuando la tarea pida implementar, realizá los cambios de código, tests o documentación necesarios dentro de su alcance. Si pide una revisión o un diagnóstico sin cambios, entregá los hallazgos. Conservá trabajo ajeno y cambios no relacionados. No introduzcas otra arquitectura, librería o configuración para evitar entender el patrón existente.

Ejecutá las validaciones pertinentes y registrá los comandos y resultados reales. Antes de correr un script, comprobá sus dependencias y si modifica datos o llama a servicios: las pruebas aisladas usan dobles y datos ficticios; las verificaciones con efectos externos requieren un entorno y alcance previstos para ellas. No expongas secretos. Informá qué cambió, dónde, qué se verificó y qué quedó pendiente; citá archivos, líneas o evidencia concreta. Una prueba no ejecutada no cuenta como exitosa.
