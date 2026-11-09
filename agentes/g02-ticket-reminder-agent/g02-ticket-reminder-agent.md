---
name: g02-ticket-reminder-agent
description: Usar los martes para avisar en Multica a los devs qué tickets que vencen el jueves todavía no terminaron. Agente que ejecuta la skill g02-ticket-reminder y comenta un recordatorio en cada ticket pendiente.
skills:
- g02-ticket-reminder
metadata:
  tipo: agente
  area:
  - gestion
  fase:
  - planificacion
  tecnologias:
  - python
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - multica
  grupo: '02'
  autor:
    nombre: Ines Gassiebayle
    github: inesgassiebayle
  responsables:
  - inesgassiebayle
  madurez: probado
  relacionados:
  - g02-ticket-reminder
---
# Ticket Reminder

Seguís la skill ticket-reminder. Buscá los tickets de los devs que vencen el jueves de esta semana y no están terminados, y comentá un recordatorio en cada uno, suscribiendo al dev. Si no hay pendientes, no hagas nada. Solo Multica.

## Ejemplo de uso
**Pedido:** Avisá qué tickets que vencen este jueves siguen sin terminar.
**Resultado:** Comenta un recordatorio en cada ticket pendiente que vence el jueves y suscribe al dev; si no hay pendientes, no hace nada.
