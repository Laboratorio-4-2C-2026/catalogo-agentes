---
name: g05-watchparty-room-accessibility
description: "Audita en el navegador el recorrido accesible de una sala de WatchParty. Usar para validar teclado, foco y anuncios durante la interacción en vivo."
metadata:
  tipo: skill
  area: ["qa","frontend"]
  fase: ["testing"]
  tecnologias: ["react"]
  metodologia: [scrum]
  herramientas: [codex]
  requiere: []
  grupo: '05'
  autor:
    nombre: Manuel Salas Seeber
    github: Manuelsalasseeber
  responsables: [Manuelsalasseeber]
  madurez: experimental
  relacionados: ["g07-auditoria-accesibilidad","g05-watchparty-ui", "g05-watchparty-room-reconnect-check"]
---

# Accesibilidad de una sala en vivo

## Procedimiento

1. Registrá versión, navegador y tecnología de asistencia disponible. Usá una sala de prueba con contenido controlado y una segunda sesión para disparar cambios en vivo.
2. Recorré la sala con teclado. Verificá que se pueda entrar, leer, comentar, reaccionar y salir según el alcance del producto. Observá orden y visibilidad del foco y su restauración al cerrar menús o diálogos.
3. Con lector de pantalla, comprobá el nombre y estado de los controles y qué se anuncia cuando llega un comentario, cambia una reacción o se pierde la conexión. Verificá que los cambios pertinentes se comuniquen sin interrumpir la escritura ni mover el foco. Si solo inspeccionaste el árbol de accesibilidad, dejá pendiente la comprobación del anuncio real.
4. Entregá por hallazgo el paso de reproducción, lo observado, el impacto, severidad y criterio aplicable cuando puedas identificarlo. Registrá las combinaciones verificadas y las pendientes.

## Ejemplo de uso

**Pedido:** Probá si se puede reaccionar con teclado y si un comentario nuevo se anuncia mientras escribo.

**Resultado:** Entrega los pasos y observaciones sobre activación, foco y anuncios, con el estado de cada comprobación.
