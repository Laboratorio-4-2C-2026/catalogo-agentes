---
name: g05-watchparty-pr-preparation
description: 'Prepara los cambios del checkout de WatchParty para revisión: alcance del diff, validaciones locales,
  título, descripción y evidencia de la PR. Usar antes de entregar cambios o actualizar una solicitud de revisión.'
metadata:
  tipo: skill
  area:
  - devops
  - qa
  - documentacion
  fase:
  - revision
  tecnologias:
  - git
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
  relacionados:
  - g09-pre-pr-gate
---

# Preparación de Pull Requests

## Entradas y frontera

Prepará la entrega de los cambios del checkout actual antes de solicitar revisión. Identificá objetivo, base de comparación y validaciones aplicables. Comprobá el diff y generá título, descripción y evidencia de la PR. La revisión técnica y la decisión de integración son pasos posteriores. Si la tarea incluye crear o actualizar una PR, usá el flujo y las herramientas disponibles del proyecto; un pedido de checklist o borrador no implica publicar, commitear ni hacer push.

## Procedimiento

1. Confirmá repositorio, estado de trabajo y base. En consultas Git usá operaciones de lectura; no hagas checkout, reset, rebase, stash ni limpieza. Si la base es ambigua, pedí la referencia y continuá con lo que no depende de ella. Considerá cambios sin commit si el usuario los incluye.
2. Leé el diff y archivos relevantes para explicar problema y comportamiento resultante. Separá cambio necesario, soporte técnico y modificación no relacionada. Proponé separar o justificar alcance ajeno sin ejecutar movimientos ni descartar trabajo.
3. Revisá higiene de entrega: archivos generados, datos de prueba reales, secretos aparentes, cambios de configuración global y lockfile cuando cambian dependencias. No imprimas un valor sensible encontrado; informá ubicación y tipo de dato redactado. No atribuyas problemas a personas.
4. Resolvé qué checks aplican desde package.json/workflows vigentes. El README de la raíz describe `pnpm validate` para formato, lint, tipos, tests y build. Confirmá script y efectos actuales antes de ejecutarlo. No uses `format:write` como si fuera un check de lectura. No lances smoke/scripts con usuarios o datos reales para rellenar evidencia.
5. Corré los checks locales pertinentes después de verificar sus efectos; registrá comando, revisión y resultado. Si no se ejecutan, informá pendiente. Una salida exitosa previa a cambios nuevos no demuestra el HEAD o working tree actual. No cambies tests o thresholds para que pasen.
6. Redactá título y cuerpo con problema concreto, comportamiento final, alcance y validación. Citá el issue correcto sin inventar identificadores. Para cambios visibles, incluí evidencia disponible con entorno; no afirmes capturas o pruebas de navegador que no existen.
7. Señalá riesgos materiales, compatibilidad y comprobaciones manuales restantes. No declares “listo para merge” a partir de este preflight ni apruebes una PR. Prepará el texto exacto, sin publicarlo salvo una instrucción separada y específica.

## Entrega

Resumen de alcance, checklist con pasa/falla/pendiente/no aplica y motivo, título/cuerpo listos para revisar y archivos o decisiones pendientes. Si se encuentra un problema, describí la corrección esperada sin aplicarla fuera del pedido.

## Ejemplo de uso

**Pedido:** Prepará la descripción y el checklist de mi cambio de frontend antes de pedir review.

**Resultado:** Borrador basado en el diff, checks aplicables y estado real de evidencia, sin publicar ni tocar commits.

**Otro uso:** Un cambio SQL y API necesita revisión. Documentá el orden y compatibilidad a verificar y enlazá el análisis de migración disponible sin aplicarla.


## Trabajo en el repositorio

Trabajá sobre el checkout actual de WatchParty. Leé los `AGENTS.md` aplicables, el `README.md` y los archivos del módulo antes de modificarlo. Las rutas `apps/`, `supabase/` y `docs/` se interpretan desde la raíz del monorepo. Resolvé herramientas, scripts y versiones desde `package.json`, el lockfile y la configuración vigente; seguí los ejemplos cercanos cuando el código haya evolucionado.

Cuando la tarea pida implementar, realizá los cambios de código, tests o documentación necesarios dentro de su alcance. Si pide una revisión o un diagnóstico sin cambios, entregá los hallazgos. Conservá trabajo ajeno y cambios no relacionados. No introduzcas otra arquitectura, librería o configuración para evitar entender el patrón existente.

Ejecutá las validaciones pertinentes y registrá los comandos y resultados reales. Antes de correr un script, comprobá sus dependencias y si modifica datos o llama a servicios: las pruebas aisladas usan dobles y datos ficticios; las verificaciones con efectos externos requieren un entorno y alcance previstos para ellas. No expongas secretos. Informá qué cambió, dónde, qué se verificó y qué quedó pendiente; citá archivos, líneas o evidencia concreta. Una prueba no ejecutada no cuenta como exitosa.
