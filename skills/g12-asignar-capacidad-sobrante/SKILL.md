---
name: g12-asignar-capacidad-sobrante
description: Propone qué hace un dev con las horas que le sobran en la semana, en este orden — adelantar un ticket de la semana siguiente, tomar un bug o tiempo libre — sin meter alcance que no era plan. Usar cuando un dev termina antes, cuando su semana tiene menos horas asignadas que su capacidad, o al planificar la semana.
owner: '@n-mangini'
role: pm
created: '2026-11-09'
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - linear
  grupo: '12'
  autor:
    nombre: Nicolas Mangini
    github: n-mangini
  responsables:
  - n-mangini
  madurez: experimental
  relacionados:
  - g12-armar-tickets-semanales
  - g12-cerrar-semana
---

# Asignar capacidad sobrante

Sin una regla, las horas que sobran se pierden: el valor ganado queda igual al planificado,
el CPI sale alto y parece eficiencia cuando es capacidad sin usar. Si se liberan todas,
el dev avanza sobre una base que la revisión todavía puede cambiar, y eso es retrabajo.

La regla de SplitIt está en el decision log de PM (sesión del 2026-10-22). Leerla antes de
proponer: si cambió, manda la versión escrita.

## 1. Medir lo que sobra

Para el dev: capacidad semanal (en SplitIt, 6 h) menos las horas de sus tickets de la semana.
Contar solo si sus tickets ya están **corregidos**: si hay una PR con cambios pedidos, esas
horas no sobran todavía.

## 2. Elegir, en orden

1. **2 h o más:** adelantar un ticket de la semana siguiente que entre en ese tiempo,
   solo si el ticket del que depende ya está corregido y mergeado. Revisar el bloqueo en
   Linear (blocked by), no suponerlo.
2. **1 h:** tomar un bug (se estiman en 1 h).
3. **Si no hay nada de eso:** tiempo libre.

El backlog entra muy rara vez. Si un ticket de backlog se va a trabajar, primero pasa a Todo
con su estimación: lo que está en Todo es plan, y lo que no, suma costo sin valor.

En la última semana del sprint no hay semana siguiente: lo que sobra va a bugs o a tiempo
libre.

Listo cuando cada dev con horas libres tiene una propuesta y su motivo.

## 3. Devolver

Por dev: horas sobrantes, qué se propone y por qué ese escalón. Agregar el efecto en el
valor ganado:

- adelantar sube el SPI de la semana;
- un bug baja un poco el CPI, y se explica como costo de corregir;
- el tiempo libre no mueve el plan.

Es una propuesta para el PM. No reasignar tickets en Linear sin que lo confirme.

## Ejemplo de uso

**Pedido:** Un dev terminó sus tickets y le sobran 3 horas esta semana, ¿qué hace?

**Resultado:** Propone adelantar un ticket de la semana siguiente que entre en 3 horas y cuyo bloqueo en Linear ya esté mergeado, explica el efecto en el SPI y deja la reasignación a confirmación del PM.
