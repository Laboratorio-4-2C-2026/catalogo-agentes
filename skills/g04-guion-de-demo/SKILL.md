---
name: g04-guion-de-demo
description: Escribe el guión paso a paso de una demo en vivo de PitStop, con datos preparados, qué mostrar y decir en cada paso y un plan B si algo falla. Usar antes de una demo, un sprint review o la presentación final.
metadata:
  tipo: skill
  area:
  - gestion
  - qa
  fase:
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: "04"
  autor:
    nombre: Tomás Serra
    github: TomasSerra
  responsables:
  - TomasSerra
  madurez: experimental
  relacionados:
  - g15-demo-recorder
---

# Guión de demo

Una demo se ensaya: esta skill deja un recorrido corto, verificado y con salida si algo falla.

## Flujo

1. **Elegir la historia:** una persona y un problema (por ejemplo, alguien que no recuerda cuándo le toca el service), no una lista de pantallas.
2. **Elegir qué se muestra:** solo funcionalidades integradas en la rama principal. Confirmarlo con `g04-team-weekly-status`.
3. **Preparar los datos:** usuario de demo, vehículos e historial que hagan la historia creíble. Nunca datos personales reales.
4. **Escribir los pasos:** acción en pantalla, frase para decir y qué se tiene que ver. Marcar el tiempo acumulado.
5. **Probar el guión** en el ambiente donde será la demo, en la resolución que se va a mostrar. Corregir lo que no coincida.
6. **Plan B:** por cada paso con riesgo (red, deploy, servicio externo), una alternativa como video grabado o capturas.

## Salida

Datos a preparar, tabla de pasos, checklist del día (deploy correcto, sesión iniciada, datos cargados, red, zoom del navegador) y plan B.

## Reglas

- No mostrar lo que no está integrado sin decir que es un prototipo.
- No dar por probado un paso que no se ejecutó: marcar lo pendiente.
- Dejar afuera lo que no entra en el tiempo.

## Ejemplo de uso
**Pedido:** Armá el guión de la demo de 5 minutos para el viernes.

**Resultado:** Los datos a preparar, una tabla de pasos con acción, frase y resultado esperado, una verificación previa en el ambiente real y un plan B para cada momento delicado.
