---
name: g13-matriz-de-trazabilidad
description: "Relaciona cada criterio de aceptación con su PR y la prueba que lo verifica. Usalo para detectar historias sin implementación vinculada y criterios sin evidencia de cobertura."
metadata:
  tipo: agente
  area: ["gestion", "qa", "documentacion"]
  fase: ["revision", "testing"]
  tecnologias: [agnostico]
  metodologia: [agnostico]
  herramientas: [codex]
  requiere: []
  grupo: "13"
  autor:
    nombre: Jeronimo Engelhard
    github: JeroEngel
  responsables: [JeroEngel]
  madurez: experimental
  relacionados: ["g13-definition-of-done", "g13-spec-driven-development", "g13-pr-review-contra-ticket", "g14-chequeo-trazabilidad-pr-ticket", "g13-generador-de-criterios-de-aceptacion"]
---

# Matriz de trazabilidad

Recibís historias y criterios de aceptación, PR candidatas y pruebas o resultados de verificación. Usá evidencia adjunta y, si tenés acceso, inspeccioná los enlaces y sus cambios. Marcá los enlaces inaccesibles como no verificados.

1. Conservá los IDs de criterios. Si no los hay, numerá las filas por historia y citá el texto correspondiente. Incluí las historias sin criterios como un hueco aparte.
2. Para cada criterio, identificá las PR que lo implementan y el cambio concreto que lo demuestra. Un ID de ticket en el título de una PR es una pista, no prueba del vínculo. Indicá si la PR sigue abierta o ya se integró.
3. Buscá un test identificable por nombre o ruta, o un caso manual documentado. Comprobá que su aserción o resultado esperado corresponda al criterio. Si hay resultados, separá la existencia de una prueba de la evidencia de su ejecución.
4. Devolvé una fila por criterio: **historia | criterio | PR y evidencia | test y evidencia | estado**. Usá **trazado**, **sin PR verificada**, **sin prueba verificada** o **sin ambas**. Al final, agrupá historias huérfanas y criterios con vínculos pendientes. No inventes enlaces y no actualices el ticket.

## Ejemplo de uso

**Pedido:** Armá la matriz para pausar avisos. La PR adjunta modifica el endpoint. Un test comprueba que el autor puede pausar, pero solo encontré una mención al caso de otro usuario.

**Resultado:** Vincula el criterio del autor a la PR y a su test, y marca que falta verificar una prueba de denegación para terceros.
