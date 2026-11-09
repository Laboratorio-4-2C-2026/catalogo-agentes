---
name: g10-acceptance-criteria
description: "Definir y mejorar criterios de aceptación de funcionalidades, bugs y tickets a partir de requisitos, diseños y arquitectura existente. Usar al preparar o aclarar trabajo; no para dictaminar el cierre de un PR."
metadata:
  tipo: skill
  area: [gestion]
  fase: [analisis]
  tecnologias: [agnostico]
  metodologia: agnostico
  herramientas: [codex]
  requiere: []
  grupo: "10"
  autor:
    nombre: Marcos Carrizo Aslanian
    github: MarcosCarrizoA
  responsables: [MarcosCarrizoA]
  madurez: experimental
  relacionados: []
---

# Criterios de aceptación

Convertir lo que necesita el usuario en condiciones breves, observables y suficientes para implementar y aceptar una entrega. Mantener el alcance y el nivel de detalle pedidos; no convertir cada ticket en una especificación exhaustiva.

## Contexto y fuentes

- Usar primero los requisitos del usuario y las fuentes proporcionadas. Si existe `context_path`, leerlo; en su defecto, buscar `pm/sprint-context.json` en el proyecto actual. Usar únicamente configuraciones vinculadas a esa tarea o proyecto, sin recurrir por defecto a perfiles fijos ni heredar decisiones de otros proyectos. Las instrucciones actuales del usuario prevalecen sobre el contexto guardado.
- Leer el ticket y sus criterios antes de modificarlos. Cuando el comportamiento dependa de lo implementado, consultar el repositorio y la rama pertinentes, los contratos de API o el diseño necesario. Preferir los conectores disponibles y enlazar las fuentes que fundamentan decisiones importantes.
- Distinguir comportamiento existente, entrega solicitada y propuesta. Que un dato aparezca en un formulario no demuestra que se envíe o persista; que exista un endpoint no demuestra que la UI esté integrada. No inventar endpoints, campos, reglas o capacidades para completar una plantilla.
- Consultar solo lo necesario. No exigir un sprint, una auditoría del repositorio ni acceso a Jira para redactar criterios a partir de requisitos suficientes. Si falta un dato que cambia el comportamiento, plantear esa decisión; continuar con lo independiente sin presentar una suposición como acuerdo.

## Definir la entrega

Antes de redactar, identificar para quién es la funcionalidad, qué acción o evento la inicia, qué resultado debe obtener y cuáles son sus límites.

- Precisar el trabajo de **frontend** y **backend** cuando corresponda. Un ticket solo backend debe poder aceptarse mediante su contrato y resultados, sin esperar una pantalla.
- En frontend, decir si se debe **crear/completar UI**, **integrar UI existente** o **dejar preparado con datos de ejemplo**. No dar una integración real por terminada con mocks. Los estados visuales deben corresponder al flujo solicitado, sin exigir rediseñar pantallas ya resueltas.
- Identificar quién ejecuta cada paso y qué entrega previa permite empezar la integración. Si hay trabajo en paralelo, acordar un contrato mínimo y separar lo verificable con ejemplos de lo que requiere el backend real.
- Conservar responsable, fechas y estimación aprobados. Si los criterios revelan trabajo adicional, señalarlo y proponer un ajuste; no sumar horas, fragmentar tareas ni ampliar el alcance silenciosamente. Si el usuario agrupa una funcionalidad en un ticket, respetar esa agrupación.

## Redactar criterios útiles

- Describir **condición o evento → resultado observable**, usando términos del producto y valores concretos. Usar listas directas por defecto; Given/When/Then solo cuando aclare un flujo complejo o se solicite.
- Cubrir el recorrido principal y los casos alternativos o límites que realmente cambian la aceptación. Cuando exista un umbral, aclarar el comportamiento en el límite y a cada lado. Evitar catálogos de riesgos hipotéticos.
- Expresar por separado resultados que puedan fallar de manera independiente. Eliminar repeticiones, explicaciones largas y frases que no permiten comprobar nada, como «funciona correctamente» o «hacer toda la lógica».
- Si el flujo lo requiere, precisar campos obligatorios/opcionales, procedencia del dato, persistencia y lectura posterior, estados y transiciones, errores y resultado de reintentar. No convertir esas categorías en una checklist obligatoria para todos los tickets.
- En flujos que generan eventos o avisos, especificar **evento, destinatarios y exclusiones**. Aclarar quién no recibe el aviso y qué cuenta como evento nuevo cuando hay recálculos o reintentos. No dejar «los eventos acordados» sin enumerar los ya definidos; separar explícitamente los que aún requieren decisión.
- En operaciones que afectan varios elementos, aclarar qué se guarda junto y qué conserva estado independiente. En porcentajes o cálculos, indicar fórmula, entradas y tratamiento de datos faltantes cuando sean parte del alcance. Un ejemplo pequeño suele bastar.
- Mantener reglas y vocabulario consistentes entre contexto, descripción, criterios y dependencias. Cuando el usuario amplíe una regla, reemplazar la restricción anterior que quede obsoleta, conservando el contenido no relacionado.

## Criterios funcionales y evidencia

Los criterios describen lo que debe entregar el producto. La Definition of Done del equipo, si existe, puede agregar condiciones de cierre; no confundir ambas cosas.

- Proponer, cuando ayude, una forma breve de comprobar los criterios: petición/respuesta para backend, recorrido reproducible para UI o comprobación enfocada de una regla de negocio. No imponer suites, cobertura fija, despliegue a producción ni cantidad de revisores.
- No rellenar criterios funcionales con obligaciones genéricas como «crear PR», «todos los tests pasan» o «documentar todo». Mantener requisitos de entrega ya acordados en una sección separada si hace falta.
- Al redactar trabajo futuro, no marcar criterios como cumplidos ni agregar una auditoría de cierre por defecto. Si se pide verificar una implementación, contrastar evidencia y distinguir cumplimiento, incumplimiento y falta de evidencia; un PR fusionado por sí solo no prueba el comportamiento.

## Entrega y aplicación

Para un borrador completo, usar solo las secciones necesarias: contexto breve, alcance de frontend/backend/UI, criterios de aceptación y dependencias. Respetar formatos más cortos que pida el usuario. Mostrar decisiones pendientes o exclusiones solo si afectan la implementación; evitar repetir el historial de decisiones.

Los borradores y las consultas no autorizan cambios externos. Crear o actualizar Jira únicamente dentro de la autorización del usuario, reutilizando la aprobación ya dada para ese alcance sin pedirla otra vez. Antes de escribir, comprobar proyecto, jerarquía, campos y responsables; buscar duplicados cuando se creen tickets y preservar medios y cambios ajenos al editar. Verificar lo aplicado y devolver enlaces, sin declarar completa una actualización parcial. Esta skill no implica modificar código, cerrar tickets ni contactar al equipo.

## Ejemplo de uso

**Pedido:** Redactá los criterios de aceptación de este requisito y separá qué se comprueba en backend y qué en la interfaz.
**Resultado:** Condiciones observables, con alcance y dependencias si hacen falta. No los marca como cumplidos ni los escribe en Jira hasta que autorices esa actualización.
