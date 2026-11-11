# Handoff de despliegue

Plantilla adaptable. Completar con fuentes; marcar lo desconocido o no aplicable. Eliminar instrucciones de plantilla del documento final. No incluir credenciales.

## Identificación y estado

- Proyecto y versión/commit:
- Fecha de elaboración:
- Entorno objetivo y destinos confirmados:
- Estado de la guía y pendientes:
- Estado del despliegue, fuente y alcance de comprobación:
- Naturaleza del documento: guía nueva / revisión / reconstrucción actual de un caso histórico.
- Fuentes actuales y testimonios históricos, separados:

## Arquitectura y responsables

Describir componentes, conexiones y servicios externos aplicables.

| Componente o acción | Destino | Responsable de ejecución | Acceso requerido, sin secretos | Fuente |
|---|---|---|---|---|

Indicar por separado quién controla dominio/DNS y quién puede cambiarlo.

## Precondiciones y configuración

- Repositorio, rama/commit y requisitos de runtime:
- Build, artefactos y comandos sustentados por archivos/documentación:
- Accesos que debe resolver el equipo:
- Respaldo, migraciones y compatibilidad de datos, cuando apliquen:

| Variable o referencia | Componente | Build o runtime | Secreta o pública | Origen/gestor, sin valor secreto |
|---|---|---|---|---|

## Procedimiento por dependencias

Para cada paso: responsable, precondición, ubicación, acción/comando confirmado, resultado esperado, comprobación y condición para detenerse. Separar comandos listos de acciones pendientes de datos. Evitar instrucciones destructivas genéricas.

| Paso | Responsable | Precondición | Acción y lugar | Resultado esperado | Verificación / detener si |
|---|---|---|---|---|---|

## Verificación posterior

| Escenario | Tipo de operación y autorización necesaria | Esperado | Ejecutado/no ejecutado | Observado y evidencia |
|---|---|---|---|---|

Distinguir página accesible, integración y recorrido funcional persistido. No presentar resultados esperados como observados.

## Recuperación y problemas conocidos

- Fallos observados, diagnóstico y pasos respaldados:
- Versión/configuración recuperable y responsable:
- Compatibilidad del rollback con datos y migraciones:
- Backup/restauración, ventana y riesgos pendientes:
- Criterio para detener ejecución y escalar al equipo:

## Límites y transferencia

- Validaciones locales realmente realizadas:
- Acciones externas realmente realizadas, si fueron autorizadas:
- Pendientes con impacto y responsable por confirmar si no se conoce:
- Recursos o procesos propios retenidos y limpieza, si existieron:
- Revisión/aceptación del equipo: no afirmar aceptación sin confirmación.
