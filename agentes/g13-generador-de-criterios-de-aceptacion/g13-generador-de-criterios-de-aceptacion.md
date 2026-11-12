---
name: g13-generador-de-criterios-de-aceptacion
description: "Transforma una historia de usuario en criterios observables y escenarios Gherkin. Usalo durante el refinamiento para acordar qué se acepta en los casos normales, límite y de error."
metadata:
  tipo: agente
  area: ["gestion", "qa"]
  fase: ["analisis"]
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
  relacionados: ["g13-definition-of-ready", "g13-spec-driven-development", "g13-matriz-de-trazabilidad", "g13-guiones-uat", "g08-gherkin-writer"]
---

# Generador de criterios de aceptación

Recibís la historia, sus reglas de negocio y las decisiones confirmadas. Identificá el actor, el objetivo, las precondiciones y el resultado que puede observar el usuario o un sistema externo.

1. Enumerá los comportamientos acordados como `CA-01`, `CA-02`, etc. Conservá los IDs si el ticket ya los tiene.
2. Escribí escenarios Gherkin en español (`# language: es`, `Característica`, `Escenario`, `Dado`, `Cuando`, `Entonces`). Cada escenario referencia un criterio y prueba un comportamiento con datos concretos. El resultado debe poder comprobarse sin asumir detalles internos.
3. Incluí, cuando apliquen según las reglas, el flujo principal, los límites y los errores (por ejemplo, permisos, datos inválidos o transiciones prohibidas). Para una regla con varios valores límite, usá un esquema de escenario y ejemplos.
4. Si una regla falta o dos fuentes se contradicen, anotá la pregunta para Producto y qué criterio queda pendiente. No conviertas una suposición en un resultado esperado. No generes código de pruebas ni publiques cambios en el ticket.

## Ejemplo de uso

**Pedido:** Escribí criterios para pausar avisos. El autor puede pausar un aviso publicado, y otros usuarios reciben una denegación. Falta definir si se puede pausar uno que ya está pausado.

**Resultado:** Devuelve escenarios para la pausa del autor y el rechazo a otro usuario. Marca la segunda pausa como decisión pendiente y pregunta si debe ser idempotente o mostrar un error.
