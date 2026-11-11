---
name: g12-preparar-demo
description: Prepara un guion verificable de demo de un producto con recorrido, datos de prueba, tiempos, evidencia y alternativa ante fallas, ajustado al estado del producto. Usar antes de mostrar el producto en una demo ante la cátedra, un cliente o un steering.
owner: '@husseymarcos'
role: po
created: '2026-11-05'
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
  - codex
  - otra
  requiere: []
  grupo: '12'
  autor:
    nombre: Marcos Hussey
    github: husseymarcos
  responsables:
  - husseymarcos
  madurez: experimental
  relacionados:
  - g12-crear-deck-reveal
  - g04-guion-de-demo
  - g09-preparar-demo-sprint
  - g02-storytelling-de-demo
---

# Preparar demo

Preparar una demostración que el equipo pueda repetir en el tiempo disponible.
Ejemplo: `/preparar-demo cliente nuevo, 5 minutos, flujo de alta y primera operación`.

## Elegir el recorrido

Resolver audiencia, objetivo, duración y ambiente a partir del pedido. Leer las historias
y criterios involucrados, el estado de release y los incidentes o limitaciones conocidas.
Comprobar qué versión está desplegada: un ticket cerrado o PR mergeado no garantiza
que el comportamiento esté disponible en ese ambiente.

Seleccionar el recorrido mínimo que muestre el valor pedido. Consultar el feedback
anterior y los compromisos relevantes para esa audiencia, si existen.
No fijar todas las demos a los mismos módulos ni recorrer pantallas sin un propósito.

Identificar actores, permisos, sesiones separadas cuando hagan falta y entidades de
prueba propias del producto. Definir datos ficticios y resultados esperados antes del
ensayo. Para cálculos o transformaciones, comprobar el resultado según las reglas
documentadas del producto, sin inventar una política nueva.

## Guion y ensayo

Armar una tabla con paso, acción, mensaje oral, resultado observable, dato requerido y
tiempo. Sumar los tiempos incluyendo cambios de sesión y dejar margen para preguntas o
latencia. Distinguir lo implementado, lo verificado y lo que se mostrará como prototipo.

Si hay acceso y herramientas, ensayar en el ambiente indicado y registrar fecha, URL,
versión y resultado por paso. Preparar datos sólo en un ambiente de prueba autorizado:
crear o modificar registros cambia datos y requiere estar dentro del pedido.
No enviar invitaciones reales ni alterar producción para preparar una demo. Si esas
acciones no están autorizadas, entregar instrucciones de preparación y marcar el ensayo
como pendiente en vez de simular que ocurrió.

Comprobar acceso, permisos de los actores, carga de datos y persistencia del resultado.
Un ensayo fallido debe producir un bloqueo o una adaptación explícita del guion, no una
promesa de que funcionará. Evitar arreglos de código fuera del pedido.

## Alternativa y entrega

Para los pasos frágiles, definir una alternativa concreta: captura o grabación del mismo
flujo y versión, o un recorrido más corto ya verificado. Identificar material grabado y
mockups cuando se usen. Si no existe ese respaldo, dejar su captura como pendiente.

Entregar objetivo, guion cronometrado, instrucciones de preparación y reinicio, resultados
del ensayo, limitaciones y alternativa. Incluir enlaces a historias y evidencia sin
credenciales. Proponer limpieza sólo de los datos de prueba creados para el ensayo y
aplicarla únicamente dentro de la autorización recibida.

Esta skill produce el guion y las condiciones de ejecución. Si se piden diapositivas,
entregar el guion y el estado real al flujo de presentaciones elegido por el usuario;
no requiere instalar otra skill.

## Ejemplo de uso

**Pedido:** /preparar-demo cliente nuevo, 5 minutos, flujo de alta y primera operación

**Resultado:** Entrega un guion cronometrado con acción, mensaje y resultado esperado por paso, los datos de prueba, el resultado del ensayo y una alternativa para los pasos frágiles.
