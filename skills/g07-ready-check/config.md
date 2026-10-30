# Configuración — g07-ready-check

Datos del proyecto y Definition of Ready del equipo. No hay secretos acá.

- **Proyecto**: `<nombre del proyecto>`
- **Site de Jira**: `<tuequipo>.atlassian.net`
- **Project key**: `<KEY>`
- **Día de entrega**: `jueves` (ciclo semanal, por el campo Due date)

## Definition of Ready

Marcá cada criterio como `obligatorio`, `opcional` o `no aplica`. La skill solo exige lo que está acá.

| # | Criterio | Nivel |
|---|---|---|
| 1 | Objetivo claro (user story o objetivo explícito) | obligatorio |
| 2 | Criterios de aceptación verificables | obligatorio |
| 3 | Alcance acotado (qué entra y qué no) | opcional |
| 4 | Contrato de API definido (si cruza front y back) | obligatorio |
| 5 | Dueño asignado | obligatorio |
| 6 | Fecha de entrega (due date en día de entrega) | obligatorio |
| 7 | Épica (parent) | opcional |
| 8 | Dependencias resueltas a tiempo | obligatorio |
| 9 | Estimación (story points) | no aplica |
| 10 | Tamaño razonable | opcional |

- **Campo de story points** (solo si el criterio 9 aplica): `<customfield_NNNNN>`
- **Umbral de tamaño**: más de `20` escenarios o criterios de aceptación sugiere partir el ticket. Calibrado con los tickets del equipo: de 9 a 20 escenarios en Gherkin es lo normal acá.
- **Back y front**: el equipo los separa en tickets distintos (un ticket que mezcla los dos es señal de tamaño).
