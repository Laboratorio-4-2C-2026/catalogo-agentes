---
name: g12-preparar-relevo-rol
description: Prepara el traspaso de una responsabilidad o rol de proyecto con estado a la fecha, decisiones vigentes, pendientes con responsable y próximos pasos sustentados en fuentes. Usar cuando una persona deja un rol y otra lo toma, por ejemplo al rotar roles entre sprints.
metadata:
  tipo: skill
  area:
  - gestion
  - documentacion
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
  - g12-registrar-decision
---

# Preparar relevo de rol

Preparar un relevo que permita a la persona entrante continuar sin reconstruir el trabajo previo.
Ejemplo: `/preparar-relevo-rol PM, cierre del sprint 2`.

## Ubicar el relevo

Identificar rol, persona saliente, entrante, período y fecha de corte. Consultar las
asignaciones y decisiones del período: comprobar quién ejerce cada responsabilidad
hoy, sin asumir que los nombres o roles de otro período siguen vigentes. Si la persona entrante no está definida, preparar el informe
sin asignarle pendientes a alguien por suposición.

Localizar el registro de decisiones y los documentos relevantes a esa responsabilidad. Reunir la
planificación vigente, tickets, PRs, incidentes, riesgos y entregables pertinentes al corte.
Resolver contradicciones dando prioridad a la decisión vigente y evidencia fechada;
mostrar las diferencias no resueltas, sin presentar un plan histórico como actual.

## Contenido según el rol

Priorizar lo que la persona necesita para tomar su próxima decisión. Adaptar estos
ejemplos a los roles reales de la organización; el relevo también puede ser de una
función, servicio o iniciativa sin un cargo formal:

- **PM:** hitos y compromisos, base aprobada, capacidad, cronograma, costos, riesgos,
  bloqueos y decisiones pendientes con sus fechas.
- **PO:** alcance acordado, historias priorizadas, criterios ambiguos, diseños y feedback
  de usuarios, validaciones de producto y compromisos pendientes.
- **TL:** arquitectura y ADR vigentes, dependencias entre PRs, contratos API/web,
  despliegues, configuración necesaria y deuda técnica que afecte al próximo trabajo.
- **QA:** gates de calidad, versión y ambiente evaluados, pruebas y evidencia,
  regresiones abiertas, cobertura pendiente y limitaciones conocidas del release.

Incluir sólo la información que afecte la continuidad. Referenciar los documentos fuente
en lugar de copiar todo el backlog. Mantener las evaluaciones de desempeño en el
proceso y audiencia correspondientes; no agregar notas personales al relevo.

## Pendientes y próximos pasos

Por cada pendiente registrar asunto, estado observado, próxima acción, responsable
confirmado, fecha comprometida si existe, dependencia y enlace de evidencia. Distinguir
responsables actuales de los propuestos. Un pendiente sin responsable queda visible como
`Por asignar`; una fecha ausente como `Sin fecha acordada`.

Separar hechos, decisiones vigentes, propuestas y preguntas abiertas. Señalar qué entradas
reemplazaron decisiones anteriores. Ordenar las primeras acciones por impacto, vencimiento
y dependencias, explicando qué debe resolverse primero. No crear compromisos nuevos.

Para accesos, listar servicio, permiso necesario y quién lo gestiona; no copiar tokens,
contraseñas ni archivos de entorno. La persona entrante confirma sus accesos; el informe
no puede darlos por obtenidos sin evidencia.

## Entrega y cierre

Entregar un informe breve con rol y corte, estado, decisiones clave, tabla de pendientes,
primeras acciones y mapa de fuentes. Adjuntar preguntas concretas que debe resolver la
conversación de relevo. Marcar evidencia faltante o desactualizada.

Verificar que cada acción urgente tenga dueño o esté visiblemente por asignar, que los
links correspondan al tema y que un ticket cerrado no oculte trabajo aún no desplegado
o validado. Presentar el documento como preparado, no como un relevo aceptado: la
recepción la confirma la persona entrante. No enviar mensajes, reasignar tickets ni
cambiar responsables en trackers salvo instrucción explícita para esas acciones.

## Ejemplo de uso

**Pedido:** /preparar-relevo-rol PM, cierre del sprint 2

**Resultado:** Entrega un informe breve con el estado al corte, las decisiones vigentes, una tabla de pendientes con responsable o "Por asignar" y las preguntas para la charla de relevo.
