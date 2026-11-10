---
name: g02-ticket-reminder
description: Usar los martes para avisar en Multica a los devs de Zest qué tickets que vencen el jueves todavía no terminaron, con un comentario en cada ticket pendiente.
metadata:
  tipo: skill
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
  - g02-ticket-reminder-agent
---
# Recordatorio de tickets del jueves — Zest

## Objetivo
Los martes, encontrar los tickets de los devs que **vencen el jueves de esta semana** y **todavía no están terminados**, y avisarles **en Multica** con un comentario en cada ticket. Si todos están terminados, **no hacer nada**: ni comentarios ni issues.

Devs a revisar: **Dev 1** (`usuario-dev1`) y **Dev 2** (`usuario-dev2`).

## Pasos

### 1. Buscar los tickets pendientes
```bash
multica issue list --output json > issues.json
multica workspace member list --output json > members.json
python3 pending_tickets.py issues.json --members members.json \
  --devs "usuario-dev1,usuario-dev2,Dev 1,Dev 2"
```

| Código | Significa | Qué hacer |
|---|---|---|
| `0` | No hay tickets pendientes para el jueves | **Terminar sin hacer nada.** |
| `1` | Hay tickets pendientes | Seguir con el paso 2 para cada ticket de `por_dev`. |

### 2. Comentar en cada ticket pendiente
Para cada ticket, escribir `aviso.md` y comentarlo:
```bash
multica issue comment add <id> --content-file aviso.md
```
`<id>` es el campo `id` del ticket en la salida del script.

Texto de `aviso.md`, según el estado del ticket:

- **To do / sin empezar:**
  ```markdown
  ⏰ **Recordatorio:** este ticket vence el **jueves <DD/MM>** y todavía no arrancó.
  ¿Llegás con la fecha? Si hay algo que te bloquea, comentalo acá así te ayudamos a destrabarlo.
  ```
- **In progress:**
  ```markdown
  ⏰ **Recordatorio:** este ticket vence el **jueves <DD/MM>** y sigue en progreso.
  Recordá dejar el PR abierto con tiempo para la revisión. Si algo te bloquea, comentalo acá.
  ```
- **In review:**
  ```markdown
  ⏰ **Recordatorio:** este ticket vence el **jueves <DD/MM>** y está en revisión.
  Revisá si hay cambios pedidos en el PR para que se pueda mergear antes del jueves.
  ```
- **Cualquier otro estado:** usar el texto de In progress.

### 3. Asegurar que el dev reciba la notificación
Para cada ticket comentado, suscribir a su dev (si ya estaba suscripto, no pasa nada):
```bash
multica issue subscriber add <id> --user-id <assignee_id>
```

### 4. Resumen
Terminar la ejecución con una línea de resumen, por ejemplo: "Avisé 3 tickets que vencen el 05/11: 2 de Dev 1 y 1 de Dev 2."

## Reglas
- Un solo comentario de recordatorio por ticket y por semana: si el ticket ya tiene un comentario que empieza con "⏰ **Recordatorio:**" de esta semana, no repetirlo (`multica issue comment list <id>`).
- No cambiar el estado, la fecha ni la asignación de los tickets.
- Tono amable y de ayuda, nunca de reproche.
- No avisar por WhatsApp ni por otros medios: solo Multica.

## Ejemplo de uso
**Pedido:** Recordales los tickets del jueves.
**Resultado:** Busca los tickets abiertos que vencen el jueves y comenta un recordatorio en cada uno, suscribiendo al dev.
