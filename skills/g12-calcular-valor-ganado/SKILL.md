---
name: g12-calcular-valor-ganado
description: Calcula el valor ganado de un proyecto a una fecha de corte, con PV, EV, AC, indicadores y proyección trazables a la línea base aprobada y a la evidencia de ejecución. Usar en cada corte de seguimiento o antes de un steering, cuando hay que medir avance y costo contra la línea base.
owner: '@husseymarcos'
role: pm
created: '2026-11-05'
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - codex
  - otra
  requiere: []
  grupo: '12'
  autor:
    nombre: Marcos Hussey
    github: husseymarcos
  responsables:
  - husseymarcos
  madurez: usado-en-proyecto
  relacionados:
  - g12-cerrar-semana
  - g02-valor-ganado-evm
  - g15-evm-calculator
---

# Calcular valor ganado

Convertir el seguimiento del proyecto en un corte reproducible de valor ganado.
Ejemplo: `/calcular-valor-ganado sprint 3, corte al 5 de noviembre de 2026`.

## Fijar el corte

Resolver período, fecha de corte, alcance (sprint o proyecto) y unidad. Consultar el
plan aprobado y las decisiones vigentes del proyecto; identificar la versión
aprobada del presupuesto, su BAC y la regla de reconocimiento de valor. Un ADR propuesto
no reemplaza una línea base aprobada. Si hay dos bases incompatibles sin resolución,
mostrar la diferencia y pedir cuál usar antes de presentar un indicador definitivo.

Localizar presupuesto, seguimiento, reglas de aceptación y fuentes de costo en los
archivos, planillas o servicios que use el proyecto. Registrar la autoridad y vigencia
de cada fuente; no exigir una estructura de carpetas ni un proveedor. Si faltan reglas
de reconocimiento de valor o reparto de partidas, pedirlas y avanzar con la tabla de
evidencia; dejar los cálculos afectados pendientes.

## Reconstruir PV, EV y AC

Construir una tabla por unidad de trabajo: ID, partida, valor presupuestado, período
planificado, evidencia y fecha de aceptación, costo real, fuente y datos faltantes.

- **PV:** valor presupuestado del trabajo previsto hasta el corte según la línea base.
  Un atraso o reasignación no desplaza su PV a la semana nueva.
- **EV:** valor presupuestado del trabajo que satisface la regla de aceptación al corte.
  Aplicar 0/100 o avance parcial sólo según la regla documentada; el porcentaje de horas
  consumidas no demuestra avance ganado.
- **AC:** esfuerzo o costo real incurrido hasta el corte, incluido el trabajo fuera de
  presupuesto. Un gasto no presupuestado suma AC, pero no gana EV automáticamente.

Usar la regla de reparto aprobada cuando una partida cubra varias unidades de trabajo.
El hito de aceptación puede ser entrega, aprobación, merge u otro definido por el
proyecto: no elegir uno por defecto. Revisar también el costo del trabajo en curso;
se puede incurrir en costo antes de ganar valor. Si el dato no está disponible, señalar
AC incompleto. Distinguir mediciones, declaraciones e imputaciones aproximadas.

Evitar doble conteo entre épicas y tareas, PRs y time entries, sprints anteriores y el
actual. Relacionar PRs con tickets y repartir sólo con una regla sustentada. Mantener
precisión interna y redondear al presentar. Registrar qué datos se excluyeron y por qué.
Una hora y un punto sólo equivalen si la fuente define esa conversión. No convertir
horas en moneda sin tarifas documentadas.

## Indicadores y proyección

Usar acumulados del mismo alcance, unidad y corte:

| Indicador | Cálculo | Lectura |
|---|---|---|
| CV | EV − AC | Desvío de costo, en la unidad de la base |
| SV | EV − PV | Desvío de trabajo valorizado; no son días de atraso |
| CPI | EV / AC | Eficiencia de costo |
| SPI | EV / PV | Avance contra el plan valorizado |
| EAC | AC + (BAC − EV) / CPI | Escenario que mantiene la eficiencia de costo |
| ETC | EAC − AC | Costo proyectado restante |
| VAC | BAC − EAC | Margen proyectado contra el presupuesto |

Ante denominador cero, dato faltante o base incoherente, indicar `No calculable` con
motivo; no sustituirlo por cero. Presentar EAC como escenario y explicitar su supuesto.
Si se proyecta el remanente a costo presupuestado, usar AC + (BAC − EV) y nombrar ese
supuesto. No deducir una fecha final de SPI sin analizar el cronograma y dependencias.

## Entrega y comprobación

Entregar base y corte, tabla de trazabilidad, acumulados, indicadores, interpretación,
proyección y faltantes. Explicar contradicciones entre dedicación, productividad y CPI.
Separar capacidad disponible de trabajo presupuestado. Si hay serie temporal, incluir
una tabla por período con plan hasta el final y una proyección diferenciada de los reales.

Reconciliar la suma de partidas con BAC, EV con las unidades aceptadas y AC con las
fuentes sin duplicados. Verificar que fechas posteriores al corte no sumen como reales.
Si sólo hay datos parciales, etiquetar el resultado como provisional. Generar archivos
fuera de repositorios de sólo lectura; no alterar presupuestos ni cargar indicadores en
servicios externos salvo que el pedido lo incluya.

## Ejemplo de uso

**Pedido:** /calcular-valor-ganado sprint 3, corte al 5 de noviembre de 2026

**Resultado:** Arma la tabla de trazabilidad por ticket con PV, EV y AC acumulados, calcula CV, SV, CPI, SPI y EAC (o "No calculable" con el motivo) y lista los datos faltantes.
