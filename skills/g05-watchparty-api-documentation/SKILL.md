---
name: g05-watchparty-api-documentation
description: Crea y actualiza la documentación de endpoints Express de WatchParty a partir de las rutas, validadores,
  casos de uso y tests del repositorio. Usar cuando se agrega o cambia un contrato de API.
metadata:
  tipo: skill
  area:
  - documentacion
  - backend
  fase:
  - desarrollo
  - revision
  tecnologias:
  - express
  - typescript
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
  relacionados: []
---

# Documentación de endpoints de WatchParty

## Entradas y resultado

Partí del endpoint, módulo o diff de la tarea. Localizá sus rutas, validadores, casos de uso y tests, y encontrá la documentación que ya describe ese contrato. Al pedir documentar o actualizar la API, editá la sección del README o archivo de `docs/` correspondiente; si hace falta uno nuevo, seguí la organización existente. Si se pide solo una propuesta, entregá el borrador. Conservá el formato de documentación del repositorio; no introduzcas un generador, servidor de docs ni OpenAPI como parte implícita de la tarea.

## Procedimiento

1. Reconstruí método y ruta completa desde el montaje de routers hasta el handler. Incluí prefijos, parámetros y middleware aplicables; el nombre de un archivo no demuestra la URL pública.
2. Leé validadores, caso de uso e interfaz de datos para definir entradas: ruta, query, headers y body, con tipo, presencia, rango y default confirmados. Distinguí obligatorio, opcional y nullable. No documentes como garantizada una regla que solo aparece en un comentario desactualizado.
3. Describí autenticación/autorización según controles reales: identidad requerida, relación con el recurso y posibles respuestas 401/403. En la web, Supabase Auth y API Node cumplen funciones distintas; no sugieras enviar claves de servicio desde el navegador.
4. Extraé respuestas exitosas y errores del contrato actual. Los tests HTTP sirven como evidencia del comportamiento que realmente asertan, no como garantía de todos los casos. Indicá campos, unidades, null, paginación y estabilidad de orden cuando estén definidos. Un cursor opaco se documenta como opaco; no reveles ni inventes su contenido interno.
5. Prepará ejemplos sintéticos válidos de request/response y un error relevante. Usá marcadores como `<ACCESS_TOKEN>` y dominios ficticios; nunca pegues credenciales reales. Los ejemplos de métodos de escritura son documentación, no comandos que debas ejecutar.
6. Contrastá con docs anteriores para listar diferencias y contradicciones. Actualizá los ejemplos y secciones afectados y conservá el resto del documento. No cambies código para que coincida con una descripción deseada ni generes un contrato aspiracional como si estuviera implementado.
7. En una comprobación de ejemplo, diferenciá validación sintáctica/local de ejecución real del endpoint. No hagas requests a producción por iniciativa propia ni crees recursos para completar una captura.

## Entrega

Por endpoint: propósito, método/ruta, acceso, entradas, respuesta, errores, ejemplos y fuentes por sección. Añadí versión/revisión inspeccionada, incompatibilidades conocidas y preguntas abiertas. Si una respuesta no pudo inferirse de las fuentes, marcala no verificada en lugar de completarla por convención.

## Ejemplo de uso

**Pedido:** Documentá el listado paginado de opiniones usando su ruta y tests actuales.

**Resultado:** Contrato completo con parámetros, cursor opaco, respuestas y ejemplos ficticios trazados al código.

**Otro uso:** Tras cambiar una regla de validación, generá el delta de documentación y los errores afectados sin reescribir los endpoints ajenos al cambio.


## Trabajo en el repositorio

Trabajá sobre el checkout actual de WatchParty. Leé los `AGENTS.md` aplicables, el `README.md` y los archivos del módulo antes de modificarlo. Las rutas `apps/`, `supabase/` y `docs/` se interpretan desde la raíz del monorepo. Resolvé herramientas, scripts y versiones desde `package.json`, el lockfile y la configuración vigente; seguí los ejemplos cercanos cuando el código haya evolucionado.

Cuando la tarea pida implementar, realizá los cambios de código, tests o documentación necesarios dentro de su alcance. Si pide una revisión o un diagnóstico sin cambios, entregá los hallazgos. Conservá trabajo ajeno y cambios no relacionados. No introduzcas otra arquitectura, librería o configuración para evitar entender el patrón existente.

Ejecutá las validaciones pertinentes y registrá los comandos y resultados reales. Antes de correr un script, comprobá sus dependencias y si modifica datos o llama a servicios: las pruebas aisladas usan dobles y datos ficticios; las verificaciones con efectos externos requieren un entorno y alcance previstos para ellas. No expongas secretos. Informá qué cambió, dónde, qué se verificó y qué quedó pendiente; citá archivos, líneas o evidencia concreta. Una prueba no ejecutada no cuenta como exitosa.
