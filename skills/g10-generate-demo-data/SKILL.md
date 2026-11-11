---
name: g10-generate-demo-data
description: Preparar datasets de demo y generadores reproducibles basados en el modelo y los escenarios de una aplicación. Usar para producir y validar datos; la
  carga externa requiere un pedido que la autorice.
metadata:
  tipo: skill
  area:
  - datos
  - qa
  fase:
  - testing
  tecnologias:
  - agnostico
  metodologia:
  - agnostico
  herramientas:
  - codex
  requiere: []
  grupo: "10"
  autor:
    nombre: Pedro Ramirez Neira
    github: pedroramirezneira
  responsables:
  - pedroramirezneira
  madurez: experimental
  relacionados: []
---

# Generar datos para una demo

Convertir las instrucciones del usuario y las reglas del proyecto en un dataset verificable y un generador ejecutable. Completar los artefactos y probarlos localmente; no quedarse en una propuesta. Responder en el idioma del usuario.

## Entrada y alcance

Aceptar el proyecto o directorio actual, ambiente objetivo si los datos se preparan para un despliegue, cantidades por entidad, contexto, distribuciones, fecha de referencia y escenarios deseados. Admitir URLs o identificadores de servicios y la rama o versión del modelo que se debe usar. Por ejemplo:

```text
$generate-demo-data Prepará 600 cuentas y 5.000 reservas para staging de una plataforma cultural, con actividad histórica, disponibilidad futura y fotos reales. Usá el esquema de esta rama y solo generá los archivos.
```

Interpretar los ejemplos del usuario como opciones, salvo que indique un catálogo cerrado. Mantener las preferencias y datos particulares en los artefactos de esa ejecución; no incorporarlos a esta skill.

Generar archivos locales y ejecutar comprobaciones aisladas está dentro del pedido. Crear cuentas, enviar emails, subir medios o cargar datos en servicios externos requiere un pedido explícito que cubra esas acciones y el entorno; respetar autorizaciones previas sin pedirlas de nuevo. No ejecutar una carga por el solo hecho de haber preparado su script. No modificar código productivo, reglas de autenticación ni configuración externa para facilitar la generación.

## Entender el proyecto

Leer sus instrucciones, esquema, contratos y servicios relevantes. Identificar relaciones, campos derivados, estados válidos, unicidad, restricciones temporales y efectos secundarios. Distinguir validaciones del frontend, del pipeline HTTP, de los servicios y de la base: invocar un servicio directamente no ejecuta automáticamente los guards o la validación de DTO del controlador.

Identificar proveedor de identidad, almacenamiento de medios y vínculo con los usuarios de la base. Descubrir dominios permitidos, verificación de email y requisitos de acceso en las fuentes disponibles. No asumir que una restricción visual también existe en el backend.

Resolver las dudas con el proyecto antes de preguntar. Consultar solo decisiones indispensables, por ejemplo si una cantidad debe cumplirse en cada tabla o en el conjunto. No inflar relaciones uno a uno ni inventar entidades para alcanzar una cifra. Registrar supuestos y dependencias externas que no se pudieron comprobar.

## Ambiente objetivo

Antes de preparar una carga, identificar el ambiente (local, desarrollo, staging, producción u otro indicado), la URL del backend, el proyecto de autenticación, la base y el bucket aplicables, y la versión del esquema o contrato. Registrar identificadores o alias sin secretos. Distinguir el directorio de salida local del ambiente donde se usarán los datos.

Usar el destino indicado por el usuario o ya establecido en la conversación. La configuración local y los archivos `.env` sirven para descubrir candidatos, pero no determinan por sí solos el destino ni autorizan una carga. No asumir producción. Si quedan varios destinos posibles o falta información indispensable, preguntar antes de preparar un cargador para uno de ellos. La generación portable puede continuar con destino pendiente, sin presentarse como lista para un ambiente concreto.

Contrastar el modelo usado con la versión desplegada mediante fuentes disponibles de solo lectura. Si no puede comprobarse la compatibilidad, registrar qué versión se usó y qué queda pendiente; no modificar el despliegue para resolverlo. Mantener el ambiente y sus servicios en configuración explícita y separada de las credenciales. Antes de una ejecución externa autorizada, comprobar que los servicios resueltos corresponden al destino acordado; no cambiar de ambiente como alternativa ante un fallo.

## Diseñar datos y escenarios

Definir distribuciones que representen el producto: actividad histórica y futura, estados, participantes, ubicaciones y variaciones de uso. Construir relaciones compatibles en lugar de sortear cada campo de manera independiente.

Preparar personas y recursos identificables para demostrar recorridos completos: una operación disponible, otra sin resultados y estados relevantes del dominio. Indicar precondiciones y resultado esperado. Un escenario futuro debe quedar vigente respecto de la fecha de referencia; el historial debe conservar coherencia entre eventos y estados.

Usar nombres, descripciones y catálogos plausibles para la región y el contexto. Evitar etiquetas numeradas visibles y combinaciones imposibles. Generar el volumen con código y usar contenido elaborado donde aporte variedad; no escribir miles de objetos manualmente.

Si se requieren imágenes o videos reales, buscar fuentes y verificar los recursos con las herramientas disponibles. Conservar origen, licencia o permiso de uso, relación con la entidad y destino previsto en un manifiesto. Comprobar descarga o respuesta, tipo de contenido y visualización o reproducción según corresponda. Una URL encontrada no es un medio validado. No inventar licencias ni sustituir silenciosamente medios reales por imágenes generadas. Si falta acceso o permiso, marcarlo pendiente y continuar con el resto; no subir archivos sin autorización.

## Construir y comprobar el generador

Crear el generador en una carpeta de artefactos del proyecto o destino indicado, sin alterar archivos existentes ajenos. Preferir el runtime y las dependencias ya disponibles.

- Exponer semilla aleatoria, fecha de referencia, cantidades y destino mediante parámetros o configuración documentados.
- Fijar orden y fuentes de aleatoriedad: la misma configuración debe producir los mismos datos e identificadores. No usar la hora actual implícita, UUID aleatorios ni consultas externas durante una regeneración determinista; registrar o congelar sus resultados.
- Validar la configuración antes de producir archivos. Si las cantidades o restricciones son incompatibles, explicar el conflicto en lugar de relajar reglas silenciosamente.
- Separar generación y escritura externa. Describir el orden de carga y el mapeo de identificadores cuando un proveedor asigne sus propios IDs. Identificadores estables no bastan para afirmar que la carga sea idempotente.
- Preferir servicios o endpoints para operaciones con reglas y efectos derivados. Justificar inserciones directas, especialmente para historial, y explicar cómo conservar o reconstruir las relaciones, eventos y métricas relevantes.
- Documentar qué sucede ante una carga parcial, cómo identificar los recursos propios y cómo reanudar sin duplicarlos cuando se entregue un cargador. No implementar un cargador externo si el pedido solo requiere el dataset.

Ejecutar una muestra pequeña para verificar las reglas, luego producir y validar el volumen pedido. Comprobar cantidades, unicidad, referencias y reglas de negocio aplicables, además de duplicación visible y distribuciones. Regenerar en otro destino con la misma configuración y comparar el contenido. Probar que un cambio de semilla modifica los datos sin romper sus invariantes. No afirmar checks que no se ejecutaron.

## Cuentas y acceso

Cuando la identidad viva fuera de la base, preparar la correspondencia entre ambas, incluyendo nombres y fotos donde realmente los consulte la app. No confundir una fila de usuario con una cuenta que puede iniciar sesión.

Adaptar la preparación al proveedor. En Firebase, una carga autorizada puede usar Admin SDK para crear cuentas de demo y establecer su verificación administrativamente, conservando el UID correspondiente en la base. Eso no acredita la existencia de la casilla, la recepción del correo ni su titularidad institucional. Declarar ese método y distinguirlo del registro con verificación por correo. No inventar direcciones de terceros como prueba de pertenencia institucional. Si se exige demostrar titularidad real, informar la dependencia de casillas controladas por sus titulares.

Preparar cuentas con los atributos necesarios para el login normal, sin desactivar las restricciones de la app. Consultar documentación oficial actual del proveedor al implementar su integración. No guardar secretos en el dataset, el manifiesto o el informe; usar configuración externa para credenciales y explicar cómo suministrarlas sin publicarlas.

## Entrega

Entregar enlaces a los artefactos y comandos exactos para generar y validar:

1. Generador y configuración, con requisitos de ejecución.
2. Dataset, cantidades por entidad y distribuciones relevantes.
3. Manifiesto de medios si se requieren, distinguiendo verificados, descargados y pendientes.
4. Informe con checks ejecutados, resultados, límites y estrategia de carga. Registrar ambiente y servicios objetivo, versión del modelo y compatibilidad comprobada o pendiente. Separar preparado, creado en el proveedor y cargado en la aplicación.
5. Guion breve de escenarios: identidades o recursos de ejemplo, recorrido, precondiciones y resultado esperado; nunca contraseñas o tokens.

Si falta una dependencia externa, conservar el trabajo completo que no dependa de ella y explicar exactamente qué impide cerrar el dataset o ejecutar la carga. No presentar una muestra como el volumen final ni una carga planeada como realizada.

## Ejemplo de uso

**Pedido:** Prepará datos de demo coherentes con el esquema y un generador con semilla y fecha explícitas; solo archivos.

**Resultado:** Generador, dataset, validaciones, distribuciones y escenarios; carga y acceso externo separados.
