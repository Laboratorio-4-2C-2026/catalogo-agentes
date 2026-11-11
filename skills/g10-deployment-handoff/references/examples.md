# Ejemplos de entrada y salida

Los casos son ilustrativos. Proveedores y responsabilidades deben adaptarse a cada proyecto. Ningún ejemplo prueba un despliegue realizado.

## Aplicación con tres servicios y ejecución del equipo

**Entrada:** "Prepará instrucciones para base en Neon, backend en Render y frontend en Vercel. Los devs administran los despliegues; otra persona del equipo controla DNS. No ejecutes cambios. Hay repositorio pero faltan los proyectos de destino".

**Salida esperada:** guía con arquitectura y responsables separados, comandos extraídos del repo y configuración por componente. Identificar como pendientes los destinos, registros DNS y accesos desconocidos; no adivinar IP, nombre de base ni dominio. Consultar documentación oficial al especificar configuración actual de esos servicios, o marcar lo no verificado. Documentar orden y comprobaciones por paso, manteniendo la ejecución a cargo del equipo.

Estado: "guía preparada con pendientes de destino"; no "desplegado". Los destinos provisionales y definitivos deben coordinarse cuando CORS o autenticación dependan del dominio. No crear cuentas ni exigir datos secretos en el chat.

## Infraestructura existente de otro tipo

**Entrada:** "Tenemos una aplicación Python y PostgreSQL en una VM administrada por operaciones, sin frontend separado ni dominio nuevo. Documentá una actualización; no queremos migrar a proveedores cloud".

**Salida esperada:** conservar VM y responsable de operaciones. Revisar el proceso real de actualización, migraciones, supervisor y comprobaciones existentes; no introducir Neon, Render, Vercel, DNS o comandos de Node. Si falta el método de arranque, dejar ese paso pendiente en lugar de adivinarlo. Separar recuperación de aplicación y datos.

## Reconstrucción sin originales

**Entrada:** "En el primer sprint preparamos con IA una guía que ejecutaron los devs. Perdí el archivo; reconstruí un ejemplo con mi relato y el repo actual".

**Salida esperada:** documento con fecha actual y etiqueta de reconstrucción; arquitectura histórica atribuida al relato y comandos actuales identificados por versión. Sin acta de aceptación, logs ni screenshots inventados. Las comprobaciones quedan propuestas salvo que se ejecuten ahora dentro del alcance, y esas ejecuciones se registran con su fecha real. El funcionamiento actual de un sitio no demuestra que se siguiera el procedimiento reconstruido en aquel sprint.
