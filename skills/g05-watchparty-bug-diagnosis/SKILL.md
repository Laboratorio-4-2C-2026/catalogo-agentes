---
name: g05-watchparty-bug-diagnosis
description: Diagnostica fallas de WatchParty desde el código, los tests y las evidencias del entorno. Usar ante
  errores nuevos o intermitentes; cuando la tarea incluye resolverlos, guía la corrección y su prueba de regresión.
metadata:
  tipo: skill
  area:
  - qa
  - frontend
  - backend
  fase:
  - analisis
  - testing
  tecnologias:
  - react
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
  - g15-bug-investigator
  - g05-watchparty-web-api-integration
---

# Diagnóstico de errores de WatchParty

## Entradas y alcance

Investigá el síntoma en el código y los tests del checkout actual. Establecé resultado esperado, entorno y versión desde la tarea y las evidencias disponibles. Si se pide solo investigar, entregá el diagnóstico. Si el pedido incluye resolver la falla, reproducila con un caso mínimo, implementá la corrección acotada y verificá una prueba de regresión. No conviertas un error de entorno en una excusa para cambiar configuración o servicios sin relación con el defecto.

## Procedimiento

1. Separá lo observado de la explicación del reportante. Registrá precondiciones, frecuencia y secuencia mínima. Un “a veces” sin repeticiones comparables no demuestra intermitencia del mismo artefacto.
2. Fijá alcance por capas: documento/asset, router/estado React, cliente HTTP, middleware/handler Express, caso de uso, infraestructura o proveedor. Ubicá la primera señal que diferencia capas; un 500 visible en UI no identifica la causa raíz.
3. Usá código, resultados existentes y logs redactados. Conservá tiempos y correlación necesarios con IDs ficticios, sin tokens ni texto privado. Un error posterior puede ser consecuencia: buscá la primera causa útil sin inventar una cronología ausente.
4. Formulá hipótesis rivales con predicciones concretas y evidencia a favor/en contra. Considerá código, contrato, datos, identidad, entorno y método de prueba. Relacioná diferencias de versión antes de culpar a red o proveedor.
5. Diseñá la comprobación de menor efecto que distinga dos hipótesis: estado o payload anonimizado, inspección de una rama, simulación aislada o acción acotada en entorno de prueba. Marcá lo que requiere escribir, enviar mensajes, login o red. No ejecutes scripts de verificación sin inspeccionar destino y efectos.
6. Reproducí con tests y datos ficticios en el entorno local apropiado. Registrá pasos y resultados reales y clasificá reproducido, no reproducido o bloqueado. Cuando la tarea incluya corregir, agregá una prueba que exponga la causa, aplicá el arreglo mínimo y volvé a ejecutar las pruebas afectadas. No uses pruebas de carga, barridos de endpoints ni reintentos indefinidos como diagnóstico por defecto.
7. Al recibir nueva evidencia, descartá o ajustá hipótesis y proponé el siguiente paso. Solo llamá causa confirmada a una explicación respaldada por evidencia que discrimine alternativas relevantes. Una mitigación no demuestra corrección definitiva.

## Entrega

Resumen, entorno/revisión, pasos mínimos con esperado/observado, evidencia, hipótesis y causa sustentada o pendiente. En modo diagnóstico, incluí la corrección propuesta y el siguiente experimento. Si se pidió resolver, añadí archivos modificados, prueba de regresión y comandos/resultados de validación. No presentes una sugerencia como un arreglo aplicado.

## Ejemplo de uso

**Pedido:** Una pantalla muestra error al consultar una ruta protegida; investigá sin cambiar nada.

**Resultado:** Separación de estado de sesión, respuesta HTTP y error de infraestructura, con hipótesis y una comprobación discriminante.

**Otro uso:** Un test pasa aislado pero falla en suite. Compará orden, reloj y estado compartido; no lo desactives ni lo repitas hasta obtener verde.


## Trabajo en el repositorio

Trabajá sobre el checkout actual de WatchParty. Leé los `AGENTS.md` aplicables, el `README.md` y los archivos del módulo antes de modificarlo. Las rutas `apps/`, `supabase/` y `docs/` se interpretan desde la raíz del monorepo. Resolvé herramientas, scripts y versiones desde `package.json`, el lockfile y la configuración vigente; seguí los ejemplos cercanos cuando el código haya evolucionado.

Cuando la tarea pida implementar, realizá los cambios de código, tests o documentación necesarios dentro de su alcance. Si pide una revisión o un diagnóstico sin cambios, entregá los hallazgos. Conservá trabajo ajeno y cambios no relacionados. No introduzcas otra arquitectura, librería o configuración para evitar entender el patrón existente.

Ejecutá las validaciones pertinentes y registrá los comandos y resultados reales. Antes de correr un script, comprobá sus dependencias y si modifica datos o llama a servicios: las pruebas aisladas usan dobles y datos ficticios; las verificaciones con efectos externos requieren un entorno y alcance previstos para ellas. No expongas secretos. Informá qué cambió, dónde, qué se verificó y qué quedó pendiente; citá archivos, líneas o evidencia concreta. Una prueba no ejecutada no cuenta como exitosa.
