---
name: g10-uat-planner
description: Preparar guiones de pruebas de aceptación de usuario (UAT) desde requisitos y criterios acordados, con roles, datos, pasos y resultados esperados. Usar para planificar validación funcional, pruebas manuales o demos de aceptación de una entrega.
metadata:
  tipo: skill
  area:
  - qa
  fase:
  - planificacion
  - testing
  tecnologias:
  - agnostico
  metodologia:
  - agnostico
  herramientas:
  - codex
  requiere: []
  grupo: "10"
  autor:
    nombre: Marcos Carrizo Aslanian
    github: MarcosCarrizoA
  responsables:
  - MarcosCarrizoA
  madurez: experimental
  relacionados: []
---
# UAT Planner

Transformar el alcance acordado en un recorrido que una persona pueda ejecutar y evaluar. Responder en el idioma del usuario, con el detalle necesario para reproducir la prueba.

## Contexto y alcance

Usar los requisitos, tickets, diseños y fuentes indicados por el usuario. Si proporciona `context_path`, leerlo; en su defecto, consultar `pm/sprint-context.json` únicamente si existe en el proyecto actual. Tomar de esa tarea o proyecto sus repositorios, ambientes, roles, herramientas y rutas de salida. Evitar heredar datos de otros proyectos.

Trabajar con texto pegado o documentos suficientes sin exigir Jira, GitHub, un sprint ni acceso a una aplicación. Cuando las fuentes estén conectadas, consultarlas mediante sus herramientas y enlazar la evidencia relevante. Si falta información, avanzar con lo independiente y preguntar solo lo que cambia el recorrido o el resultado esperado.

Identificar qué entrega se valida, para quién y con qué criterios. Respetar el alcance: una entrega de API o un proceso sin interfaz puede aceptarse mediante operaciones y resultados observables, sin inventar pantallas.

## Diseñar los casos

- Asociar cada caso con el criterio o requisito que verifica. Conservar sus identificadores; si no existen, usar referencias locales claras. Una sugerencia adicional debe quedar identificada como propuesta.
- Cubrir el recorrido principal y los errores, alternativas o límites que realmente puedan cambiar la aceptación. Elegir casos representativos; evitar multiplicar combinaciones sin un motivo concreto.
- Precisar estado inicial, rol que ejecuta cada acción y datos necesarios. En flujos con varias personas, indicar quién hace qué y en qué orden, incluyendo cambios de sesión cuando correspondan.
- Dar pasos ejecutables y un resultado observable en el paso donde se comprueba el criterio. Evitar expresiones como «funciona correctamente». Indicar qué pantalla, respuesta, estado o dato permite decidir.
- Para límites numéricos o transiciones de estado, incluir ejemplos que permitan distinguir el comportamiento esperado, siempre que la regla esté definida.
- Obtener reglas, rutas, campos y permisos de las fuentes. El código puede aclarar cómo observar una operación, pero una diferencia con el requisito debe señalarse; no redefinir la aceptación para que coincida con lo implementado.
- Si un criterio es ambiguo o contradictorio, explicitar la decisión pendiente y su efecto sobre los casos. Las hipótesis de trabajo deben quedar visibles y los casos dependientes, pendientes de esa decisión.
- Usar datos ficticios identificados como ejemplos o cuentas de prueba provistas. Si hace falta crear datos, describir su preparación sin afirmar que ya existen. Aclarar cómo restablecer el estado cuando una repetición lo requiera.

## Entregar un guion ejecutable

Por defecto, entregar contexto breve y los casos priorizados. Cada caso debe permitir identificar:

- ID y criterio cubierto.
- Roles, precondiciones y datos.
- Pasos en orden y resultados esperados.
- Evidencia útil y preparación o limpieza necesarias, cuando aporten a la prueba.

Usar tabla o pasos numerados según la longitud del flujo. Mantener juntos los pasos de un caso para que pueda ejecutarse sin reconstruir información dispersa. Incluir ambiente y versión si se conocen o son necesarios para interpretar el resultado.

Cerrar con criterios sin cubrir y decisiones pendientes solo cuando existan. Diferenciar cobertura planificada, evidencia de pruebas previas y ejecución actual: redactar un caso no demuestra que haya pasado.

## Ejecución y registro

Preparar el plan no ejecuta acciones sobre una aplicación ni publica cambios externos. Si el usuario también pide probar, actuar dentro del alcance autorizado y registrar el ambiente, la versión y los resultados realmente observados.

Usar «pasó», «falló», «bloqueado» o «no ejecutado» según la evidencia. Un entorno inaccesible o datos faltantes bloquean la comprobación; no demuestran un defecto funcional. Registrar pasos de reproducción y evidencia de los fallos. El resultado esperado debe permanecer separado del resultado real.

Guardar un archivo cuando se solicite o el contexto indique una ruta de salida; en otro caso, entregar el guion en el chat. Crear tickets, comentar, publicar o compartir resultados requiere autorización para esa acción y destino; reutilizar la ya dada.

## Ejemplo de uso

**Pedido:** A partir de este ticket y sus criterios, prepará el UAT para cancelar una reserva: quién prueba, qué datos necesita, los pasos y qué debe observar.
**Resultado:** Un guion trazable a los criterios, con roles, datos de prueba, recorrido principal y alternativas relevantes. Las reglas que el ticket no define quedan como decisiones pendientes, y los casos conservan el estado de no ejecutados.
