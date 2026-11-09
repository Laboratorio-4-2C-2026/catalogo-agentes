---
name: g05-watchparty-regression-selection
description: Selecciona y ejecuta los tests existentes de WatchParty pertinentes al impacto de un cambio. Usar al
  validar una tarea o planificar regresión; distingue cobertura existente y brechas que requieren pruebas nuevas.
metadata:
  tipo: skill
  area:
  - qa
  - backend
  - frontend
  fase:
  - planificacion
  - testing
  tecnologias:
  - typescript
  - vitest
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
  - g15-regression-matrix-keeper
---

# Selección de regresión por impacto

## Entradas y diferencia de responsabilidad

Leé el diff de la tarea y el inventario de tests del checkout para decidir qué pruebas existentes volver a ejecutar. Usá la base/revisión acordada y el presupuesto de validación si lo hay. Esta skill selecciona regresión existente; para implementar cobertura faltante, consultá [Creación de tests](../g05-watchparty-test-creation/SKILL.md).

## Procedimiento

1. Enumerá comportamientos y contratos afectados por el cambio real. Seguí consumidores: caso de uso → HTTP → cliente → pantalla, y dependencias compartidas como autenticación, errores, schema o componentes base. No limites impacto a tests cuyo nombre coincide con el archivo editado.
2. Inspeccioná los tests candidatos para saber qué asertan. Un nombre o porcentaje de cobertura no demuestra protección de una regla. Registrá archivo, nivel, comportamiento y dependencias externas. No ejecutes automáticamente un script por llamarse verify o smoke.
3. Mapeá cambio → flujo afectado → test existente → razón de selección. Incluí regresiones directas y efectos cruzados sustentados. Identificá tests irrelevantes y casos que no puede demostrar una prueba JSDOM, como visibilidad real por media queries.
4. Ordená por criticidad, proximidad al cambio y costo conocido. Si hay presupuesto, conservá checks obligatorios del repositorio y mostrá lo que queda fuera; no autorices saltarlos. Si faltan duraciones, usá cantidades y no inventes minutos ni una cobertura porcentual sin denominador.
5. Separá el plan por nivel/paquete y por entorno: unitarios/componentes aislados, HTTP con dobles y smoke con servicios reales. Los scripts de los paquetes incluyen `pnpm --filter @watchparty/api test` y `pnpm --filter web test`; verificá comandos y argumentos actuales antes de proponer una selección ejecutable.
6. Si se pide validar el cambio, ejecutá la selección local después de verificar efectos y destinos; si se pide únicamente planificar, entregá el plan. Presentá por test/paquete revisión, comando y resultado: pasa, falla, no ejecutado o bloqueado. No extrapoles un subconjunto verde a toda la entrega ni actualices estados de tickets.
7. Si un comportamiento importante no tiene una prueba existente, registrá la brecha con su razón. Cuando la tarea incluya cubrirla, aplicá las convenciones de creación de tests y distinguí las pruebas nuevas de las que ya existían. Si el pedido era solo seleccionar regresión, dejá la implementación propuesta. Conservá la trazabilidad para recalcular la selección ante cambios posteriores.

## Entrega

Matriz cambio | flujo/contrato | test existente | motivo/prioridad | entorno | ejecución/evidencia. Añadí excluidos con motivo, brechas de cobertura y límites por presupuesto. Un plan de regresión no equivale a aceptación de funcionalidad o autorización de release.

## Ejemplo de uso

**Pedido:** Cambió el middleware de autenticación; elegí la regresión existente que conviene correr.

**Resultado:** Selección sustentada de pruebas de rutas protegidas y sesión dependiente, con comandos y límites, sin escribir tests nuevos.

**Otro uso:** Un componente compartido de formulario cambió. Localizá sus pruebas y consumidores relevantes; separá interacciones automatizadas de responsive visual pendiente.


## Trabajo en el repositorio

Trabajá sobre el checkout actual de WatchParty. Leé los `AGENTS.md` aplicables, el `README.md` y los archivos del módulo antes de modificarlo. Las rutas `apps/`, `supabase/` y `docs/` se interpretan desde la raíz del monorepo. Resolvé herramientas, scripts y versiones desde `package.json`, el lockfile y la configuración vigente; seguí los ejemplos cercanos cuando el código haya evolucionado.

Cuando la tarea pida implementar, realizá los cambios de código, tests o documentación necesarios dentro de su alcance. Si pide una revisión o un diagnóstico sin cambios, entregá los hallazgos. Conservá trabajo ajeno y cambios no relacionados. No introduzcas otra arquitectura, librería o configuración para evitar entender el patrón existente.

Ejecutá las validaciones pertinentes y registrá los comandos y resultados reales. Antes de correr un script, comprobá sus dependencias y si modifica datos o llama a servicios: las pruebas aisladas usan dobles y datos ficticios; las verificaciones con efectos externos requieren un entorno y alcance previstos para ellas. No expongas secretos. Informá qué cambió, dónde, qué se verificó y qué quedó pendiente; citá archivos, líneas o evidencia concreta. Una prueba no ejecutada no cuenta como exitosa.
