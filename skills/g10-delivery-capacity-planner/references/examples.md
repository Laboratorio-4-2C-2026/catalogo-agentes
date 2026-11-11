# Ejemplo de planificación con 12 horas

Caso hipotético; las cifras son datos de entrada, no valores por defecto.

## Entrada

"Objetivo: que el usuario consulte sus solicitudes activas. Ana (backend) y Bruno (frontend) tienen 6 h netas cada uno para esta iteración. Usamos horas. No hay fechas ni línea base de roadmap disponibles.

Backlog aportado y revisado por el equipo:
- Ajustar consulta y contrato: 3 h restantes de Ana.
- Pruebas del servicio: 1 h restante de Ana.
- Integrar pantalla existente: 3 h restantes de Bruno, requiere contrato estable.
- Validación end-to-end: 2 h restantes de Bruno, después de pruebas del servicio e integración.
- Ajuste cosmético opcional: 3 h de Bruno.
Las pruebas están desglosadas y no incluidas de nuevo en implementación. Solo solicito una propuesta".

## Salida

**Objetivo:** consulta de solicitudes activas funcionando de extremo a extremo.

**Estado inicial:** estimaciones restantes aportadas por el equipo; consulta necesita ajuste e integración pendiente. No se cuenta con evidencia de entrega funcional terminada.

| Persona | Trabajo | Prioridad | Horas restantes | Dependencia |
|---|---|---|---:|---|
| Ana | Consulta y contrato | Obligatoria | 3 | Inicio |
| Ana | Pruebas del servicio | Obligatoria | 1 | Consulta |
| Bruno | Integración de pantalla | Obligatoria | 3 | Contrato estable |
| Bruno | Validación end-to-end | Obligatoria | 2 | Integración y pruebas del servicio |

| Persona | Capacidad neta | Carga propuesta | Saldo |
|---|---:|---:|---:|
| Ana | 6 h | 4 h | 2 h |
| Bruno | 6 h | 5 h | 1 h |
| Equipo | 12 h | 9 h | 3 h |

**Dependencias y riesgo:** hay 9 horas-persona, pero la ruta secuencial contrato → integración → validación requiere al menos 8 h transcurridas si se libera el contrato al finalizar sus 3 h y las personas están disponibles en momentos compatibles. Las pruebas del servicio pueden avanzar junto con la integración. Si ambos solo tienen una ventana simultánea de 6 h, el objetivo completo no cabe en esa ventana. Sin agenda no se puede prometer la entrega aunque las cargas individuales entren. Confirmar secuencia de disponibilidad antes de comprometer la fecha; no convertir las 12 h de capacidad total en duración.

**Diferido:** cosmética, 3 h de Bruno. Sumada a sus 5 h obligatorias produciría 8 h frente a 6 h disponibles. Las 2 h libres de Ana no se transfieren automáticamente a Bruno. No agregar tareas para agotar el saldo.

**Cronograma:** no es posible calcular atraso ni variación de fecha sin compromiso y línea base. No inventar fechas.

**Retrabajo:** no consta corrección de entrega previa; el ajuste no se clasifica automáticamente como retrabajo.

**Recomendación del PM:** priorizar el objetivo funcional, diferir cosmética y resolver disponibilidad secuencial antes de aprobar el compromiso. No se modificó Jira.

## Cuando faltan estimaciones

**Entrada:** "Dos personas tienen 12 h totales; planificá todo el backlog", sin capacidad por persona, desglose ni estimaciones.

**Salida:** priorización preliminar y dependencias conocidas; pedir reparto de capacidad y base de esfuerzo antes de afirmar que el alcance cabe. No asignar 6 h a cada persona por deducción ni inventar horas para completar una tabla.
