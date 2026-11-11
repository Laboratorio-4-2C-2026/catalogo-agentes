---
name: g10-deployment-handoff
description: Preparar instrucciones de despliegue con arquitectura, configuración, responsables, verificaciones y recuperación para que el equipo las ejecute. Usar
  para transferir el procedimiento conservando el ownership y el entorno elegidos.
metadata:
  tipo: skill
  area:
  - devops
  - documentacion
  fase:
  - despliegue
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
  relacionados:
  - g08-release-checklist
  - g11-revisar-despliegue
---

# Deployment Handoff

Convertir la arquitectura y las restricciones de un proyecto en un procedimiento verificable para quienes operan el despliegue. Completar la guía solicitada, con comandos sustentados y pendientes explícitos. Responder en el idioma del usuario.

## Contexto y límites

Funciona de forma independiente. Usar documentación, instrucciones del repositorio y `PROJECT_CONTEXT.md` si existe; no requiere otras skills ni proveedores determinados. Recuperar la información disponible antes de preguntar, y consultar solo datos esenciales ausentes. Conservar el entorno, arquitectura y ownership elegidos: preparar instrucciones no transfiere cuentas, dominio ni responsabilidad operativa al agente.

El pedido autoriza inspección, redacción y comprobaciones locales aisladas necesarias; no implica crear servicios, desplegar, migrar una base compartida, cambiar DNS, subir secretos ni contratar planes. Si el usuario solicita además ejecución, tratarla como un alcance adicional con acciones y destino concretos; respetar autorizaciones ya otorgadas. No escribir en Jira, hacer commits ni publicar documentación por el solo pedido de handoff.

Separar hechos comprobados, inferencias, testimonios y pendientes. No inventar accesos, configuración, comandos, fechas, resultados ni evidencia histórica. Si se reconstruye un caso sin documentos originales, identificarlo como reconstrucción actual basada en fuentes y relato; no atribuirle ejecuciones pasadas.

## Preparar el procedimiento

1. Identificar aplicación, versión/rama, entorno objetivo y ejecutores. Inventariar componentes y conexiones: base, backend, frontend, identidad, almacenamiento, servicios externos y dominio cuando correspondan. No deducir producción del archivo de configuración local. Con un destino ambiguo, preparar el material portable y dejar pendientes los pasos dependientes de ese destino.
2. Inspeccionar manifests, lockfiles, scripts, rutas de build, arranque, migraciones y configuración de ejemplo. Registrar rutas y fuentes sin exponer valores secretos. Distinguir variables de build del frontend de configuración de runtime del servidor; valores incluidos en el cliente no son secretos protegidos.
3. Verificar documentación oficial actual al indicar pasos específicos de un proveedor, comandos/versiones dudosos o condiciones de servicio. Usar conectores o navegación disponibles; para trabajo offline, usar extractos aportados con fecha y procedencia. Si no se puede verificar un dato, marcarlo pendiente y evitar presentarlo como instrucción confirmada. No copiar precios, requisitos de tarjeta, planes ni opciones de panel de memoria.
4. Ordenar el trabajo por dependencias reales. Para cada paso incluir responsable, precondición, acción o comando, ubicación de ejecución, resultado esperado, comprobación y condición para detenerse. No imponer una secuencia universal: distinguir URL temporal de URL definitiva y resolver dependencias circulares de configuración.
5. Detallar únicamente los recursos aplicables: conexión a base y SSL/pooling cuando procedan, generación de cliente/migraciones, build y arranque, puertos, CORS, URLs públicas, redirects de autenticación, TLS, DNS y rutas de SPA según el proyecto. Derivar comandos del código y documentación; si no existe endpoint de salud, elegir una comprobación real disponible, sin inventar `/health`.
6. Documentar configuración con nombres y referencias seguras al gestor de secretos, nunca valores de credenciales. Para DNS, usar registros y destinos verificados del despliegue/proveedor: no adivinar IPs ni reemplazar registros ajenos. Registrar quién controla DNS y quién ejecuta cada cambio.
7. Proponer verificación posterior mínima: servicio accesible, conexión entre componentes y recorrido funcional pertinente con persistencia cuando sea necesario. Una carga de página o un HTTP 200 cubren solo ese alcance. Las comprobaciones que escriban datos compartidos requieren autorización; la guía puede describirlas sin ejecutarlas.
8. Incluir recuperación proporcional: qué versión volver a desplegar, qué configuración restaurar y cómo comprobar recuperación. Separar rollback de aplicación y recuperación de datos: una migración puede ser irreversible o incompatible con la versión anterior. No recomendar resets ni prometer rollback sin respaldo. Registrar decisiones de backup, ventana y responsable cuando hagan falta.

## Validación y entrega

Usar [assets/DEPLOYMENT_HANDOFF.md](assets/DEPLOYMENT_HANDOFF.md) como estructura adaptable; omitir secciones no aplicables y no crear documentación extra sin utilidad. Consultar [references/examples.md](references/examples.md) para ejemplos de distintos entornos y reconstrucción.

Comprobar rutas, scripts, consistencia de variables, dependencias y pasos de la guía. Ejecutar verificaciones locales solo cuando sean pertinentes y aisladas, sin modificar código productivo ni llamar inadvertidamente servicios compartidos. No ejecutar un comando de migración o deploy para validar su sintaxis.

Entregar el documento en el destino pedido, o en el chat si no se indicó archivo, con:

- Arquitectura, entorno/versión y matriz de responsabilidades.
- Precondiciones, configuración sin secretos y procedimiento ordenado.
- Comprobaciones, recuperación y resolución de problemas basada en fallos conocidos.
- Fuentes y fecha de consulta; lista de validaciones realmente ejecutadas, no ejecutadas y pendientes.
- Estado de la guía: preparada, preparada con pendientes o bloqueada en pasos concretos. Separar ese estado del estado del despliegue.

No declarar una aplicación desplegada o validada porque existe una guía. Un handoff puede estar completo como documento y conservar pasos de ejecución a cargo del equipo.

## Responsabilidad e invocación

No sustituye la selección de proveedores, la revisión de una PR ni la auditoría integral de una demo. Si una decisión técnica pendiente impide cerrar un paso, explicitarla y avanzar con el resto; no cambiar de proveedor automáticamente.

Ejemplo: `$deployment-handoff Prepará la guía de despliegue con el repositorio y PROJECT_CONTEXT.md. Los devs ejecutarán los pasos; incluí responsables, validaciones y recuperación.`


## Ejemplo de uso

**Pedido:** Prepará el handoff de despliegue para los devs con responsables, precondiciones y recuperación; no ejecutes cambios.

**Resultado:** Guía verificable con pasos sustentados, comprobaciones propuestas y pendientes de destino.
