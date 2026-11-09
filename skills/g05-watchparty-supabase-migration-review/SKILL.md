---
name: g05-watchparty-supabase-migration-review
description: Revisa migraciones SQL y políticas de acceso de WatchParty buscando incompatibilidad con datos existentes,
  pérdida de datos y cambios de privilegios. Usar antes de aplicar cambios de schema; entrega hallazgos y un plan
  de verificación, sin ejecutar migraciones.
metadata:
  tipo: skill
  area:
  - datos
  - backend
  - seguridad
  - qa
  fase:
  - revision
  tecnologias:
  - supabase
  - postgresql
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
  - g11-revisar-migracion
---

# Revisión de migraciones y acceso a datos

## Entrada y modo fijo

Revisá el diff SQL y las migraciones relevantes de `supabase/`, junto con las consultas y consumidores en `apps/api`. Reconstruí el estado anterior y el propuesto desde los archivos del checkout. Esta revisión no aplica DDL, migraciones, backfills, seeds ni cambios de permisos. La ejecución de una migración debe seguir su tarea y el runbook del entorno correspondiente; no es un paso implícito para emitir el informe.

## Procedimiento

1. Enumerá objetos afectados: tablas, columnas, constraints, índices, funciones, vistas, triggers y políticas. Compará antes/después. Un rename expresado como drop/add puede perder información; una vista reemplazada puede romper lectores aunque las tablas no cambien.
2. Revisá precondiciones de datos para NOT NULL, UNIQUE, FK, CHECK, conversiones de tipo y defaults. No deduzcas que una tabla está vacía porque la migración inicial lo estaba. Sin datos anonimizados o evidencia, marcá el riesgo y proponé una consulta de lectura acotada para verificarlo; no la ejecutes contra producción por defecto.
3. Identificá pérdida de datos, conversiones irreversibles y operaciones que pueden bloquear o reescribir tablas. No prometas tiempo de ejecución sin tamaño y condiciones. Separá certeza de fallo por SQL de riesgos dependientes de volumen/estado.
4. Contrastá consumidores y versiones: API vieja con schema nuevo, API nueva con datos anteriores y reversión después de escrituras en el formato nuevo. Señalá orden y compatibilidad necesarios; no propongas rollback destructivo como receta universal.
5. Revisá RLS y privilegios por objeto/operación/identidad. Diferenciá filtros del código de políticas efectivas y roles que pueden omitirlas. Para vistas/funciones, leé la semántica de seguridad usada y, si hace falta, documentación oficial de PostgreSQL/Supabase de la versión relevante. Una política declarada no prueba por sí sola acceso seguro.
6. Detectá concesiones amplias, funciones con privilegios elevados y exposición de datos a roles no previstos. No solicites claves reales ni pruebes accesos con cuentas del equipo. Prepará casos positivos/negativos con identidades ficticias para un entorno aislado.
7. Verificá que el archivo encaje con el orden y convención de migraciones existente en `supabase/`. No renumeres, modifiques ni sustituyas migraciones que ya podrían haberse aplicado.

## Entrega

Tabla objeto/cambio | evidencia | precondición | impacto | hallazgo o incertidumbre | verificación propuesta. Incluí compatibilidad, revisión de permisos y límites del plan de reversión. El veredicto puede ser sin bloqueos detectados en lo inspeccionado, cambios necesarios o información insuficiente; nunca equivale a permiso para ejecutar.

## Ejemplo de uso

**Pedido:** Revisá una migración que agrega UNIQUE a una relación usuario/recurso.

**Resultado:** Evaluación de duplicados posibles, efecto sobre la API y comprobaciones de lectura propuestas, sin borrar datos ni aplicar el constraint.

**Otro uso:** Una vista expone datos propios a una nueva consulta. Revisá columnas, consumidores y contexto de privilegios/RLS antes de considerarla segura.


## Trabajo en el repositorio

Trabajá sobre el checkout actual de WatchParty. Leé los `AGENTS.md` aplicables, el `README.md` y los archivos del módulo antes de modificarlo. Las rutas `apps/`, `supabase/` y `docs/` se interpretan desde la raíz del monorepo. Resolvé herramientas, scripts y versiones desde `package.json`, el lockfile y la configuración vigente; seguí los ejemplos cercanos cuando el código haya evolucionado.

Cuando la tarea pida implementar, realizá los cambios de código, tests o documentación necesarios dentro de su alcance. Si pide una revisión o un diagnóstico sin cambios, entregá los hallazgos. Conservá trabajo ajeno y cambios no relacionados. No introduzcas otra arquitectura, librería o configuración para evitar entender el patrón existente.

Ejecutá las validaciones pertinentes y registrá los comandos y resultados reales. Antes de correr un script, comprobá sus dependencias y si modifica datos o llama a servicios: las pruebas aisladas usan dobles y datos ficticios; las verificaciones con efectos externos requieren un entorno y alcance previstos para ellas. No expongas secretos. Informá qué cambió, dónde, qué se verificó y qué quedó pendiente; citá archivos, líneas o evidencia concreta. Una prueba no ejecutada no cuenta como exitosa.
