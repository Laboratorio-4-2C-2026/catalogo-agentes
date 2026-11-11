---
name: g09-planificacion-tickets-jira
description: Redacta, divide y secuencia tickets de Jira con dependencias, criterios verificables y pruebas, adaptados a la capacidad del equipo.
metadata:
  tipo: skill
  area:
  - gestion
  - qa
  fase:
  - planificacion
  - analisis
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - codex
  requiere:
  - jira
  grupo: 09
  autor:
    nombre: Agustín Martínez
    github: Agustin5421
  responsables:
  - Agustin5421
  madurez: experimental
  relacionados: []
---

# Planificación de tickets Jira

Transformar la intención del producto en trabajo implementable para las personas desarrolladoras del proyecto.

## Contexto permanente

- El repositorio del prototipo expresa la intención funcional y visual de los directores de proyecto. No representa necesariamente el estado de la aplicación oficial ni código que deba copiarse.
- La aplicación oficial es desarrollada por otro equipo y puede estar atrasada respecto del prototipo.
- Obtener del usuario la capacidad semanal disponible por persona y el uso previsto de asistencia de inteligencia artificial; declarar cualquier supuesto.
- Acordar el tamaño y la cantidad de unidades de trabajo según la capacidad y las condiciones reales del equipo.

## Antes de redactar

1. Identificar el comportamiento esperado en el prototipo y las decisiones explícitas del usuario.
2. Verificar el estado relevante de la aplicación oficial cuando esté disponible. No inferir que ya coincide con el prototipo.
3. Revisar tickets relacionados y contratos existentes si afectan dependencias o evitan duplicación.
4. Construir el grafo de dependencias del conjunto solicitado, no solo de cada ticket aislado.
5. Declarar los supuestos que no puedan verificarse. Preguntar solamente cuando una decisión cambie materialmente el alcance, el contrato o la secuencia.

Priorizar las fuentes en este orden: instrucciones actuales del usuario, decisiones aprobadas, aplicación oficial, prototipo y supuestos declarados.

## Conexión a Jira y uso eficiente del contexto

- Para consultar o modificar Jira, usar siempre una conexión autenticada: preferir las herramientas MCP nativas de Atlassian disponibles en la sesión.
- Usar la terminal únicamente como alternativa cuando el MCP no esté disponible o no exponga la operación necesaria, y solo si ya existe una CLI/API configurada y autenticada. No iniciar otra sesión de Codex para que actúe como proxy del MCP: añade transcripciones y salidas de herramientas al contexto y puede multiplicar mucho el consumo de tokens.
- Al comenzar, verificar que Jira esté accesible y resolver el proyecto/sitio una sola vez por sesión. Reutilizar el `cloudId` y los identificadores devueltos; no volver a descubrirlos sin necesidad.
- Consultar con JQL acotado al proyecto, estados y sprint pertinentes. Pedir solo los campos que cambian la decisión (`key`, `summary`, `status`, `parent`, `labels`, `assignee`, sprint, estimación y enlaces). Empezar con vista compacta; traer descripciones completas solo para candidatos concretos que haya que desglosar o evitar duplicar.
- Agrupar lecturas de issues conocidos en una sola operación cuando la herramienta lo permita. No consultar issue por issue si una búsqueda o lectura por lote cubre el mismo análisis.
- Para escrituras, descubrir metadatos únicamente de los campos/operaciones requeridos, crear o editar en Jira y verificar los resultados con una lectura acotada. No repetir búsquedas generales ni devolver payloads completos al usuario.
- Antes de crear tickets planificados, verificar y completar su metadata de planificación: sprint correcto para el ciclo acordado, fecha de inicio y fecha límite/fin en los campos disponibles, persona asignada (confirmada como asignable), estimación de tiempo, tipo, prioridad cuando corresponda, etiquetas/componentes relevantes y dependencias/enlaces. No asumir que la fecha final del sprint coincide con la fecha límite del ticket. Tras crear, volver a leer cada ticket y confirmar que los campos quedaron guardados; corregir cualquier campo omitido o mal resuelto. Si Jira no ofrece un campo solicitado, declararlo y registrar la mejor alternativa sin alterar las fechas del sprint sin autorización explícita.
- Si MCP y terminal están disponibles, elegir MCP: su contrato tipado, filtros de campos y respuestas directas permiten una integración más clara y normalmente consumen menos tokens que una sesión de terminal que devuelve logs o transcripciones. La eficiencia depende de acotar los campos y resultados; MCP no ahorra tokens si se solicita contenido completo innecesario.
- Nunca mostrar credenciales, tokens de acceso ni secretos de configuración en salidas o tickets.

## División obligatoria

- No combinar implementación de frontend y backend en un mismo ticket.
- Para una funcionalidad transversal, crear tickets separados titulados `Frontend — ...` y `Backend — ...`.
- Explicitar la dependencia y el contrato compartido en ambos tickets. Evitar duplicar detalle que pertenezca exclusivamente a la otra capa.
- Backend cubre reglas de negocio, persistencia, migraciones, contratos HTTP, autorización y pruebas backend.
- Frontend cubre interacción, estados de UI, cliente API, tipos, responsive, accesibilidad y pruebas frontend.
- Crear un ticket adicional de integración solo si existe trabajo real que no pertenece claramente a ninguna de las dos capas.

## Planificación en pipeline

Antes de entregar una familia de tickets, analizarla como carriles paralelos de frontend y backend, adaptados a las personas disponibles.

- Preferir que backend esté una feature por delante cuando exista una dependencia real de API o persistencia.
- El escenario ideal es que, durante una semana, frontend integre una feature cuyo backend ya quedó terminado, mientras backend prepara la siguiente feature.
- No asignar por defecto en la misma semana un frontend que dependa de un backend todavía no implementado.
- Definir primero el contrato mínimo compartido y mantenerlo estable para que el ticket frontend pueda comenzar sin rediseño.
- Cuando sea seguro, permitir que frontend adelante estructura visual o cliente contra un contrato acordado, pero no considerar terminado el ticket hasta validarlo contra el backend real.
- Evitar adelantar varios backends que frontend no podrá consumir pronto: limitar trabajo en curso y priorizar el próximo desbloqueo útil.
- Usar features solo frontend o solo backend para equilibrar semanas donde el pipeline normal no sea posible.
- Tratar este pipeline como preferencia de planificación, no como regla absoluta. Romperlo cuando haya una razón concreta, y explicarla.

Para una planificación de varias semanas, presentar una tabla con `Semana`, `Carril frontend`, `Carril backend`, `Dependencia lista` y `Riesgo o excepción`. Comprobar que cada carril respeta la capacidad semanal acordada.

Cada ticket debe indicar:

- qué necesita terminado para comenzar;
- qué ticket o trabajo posterior habilita;
- si puede ejecutarse en paralelo de forma real, con contrato estable, o si debe esperar.

## Tamaño

- Diseñar cada ticket para que una persona pueda implementarlo y probarlo normalmente en el tiempo acordado con asistencia de IA.
- Si excede el tiempo acordado, contiene más de un resultado funcional independiente o requiere varias migraciones, contratos o pantallas, dividirlo antes de entregarlo.
- Mantener como máximo una responsabilidad principal por ticket.
- No reducir calidad, seguridad ni pruebas para cumplir el tiempo: reducir alcance.
- Señalar dependencias externas o decisiones pendientes que puedan impedir terminarlo dentro de la semana.

## Formato

Cada ticket debe incluir título con resultado observable, objetivo, contexto verificado, dependencias, alcance, pruebas y validación, criterios de aceptación y fuera de alcance. Adaptar el detalle al tamaño del trabajo; no omitir alcance, pruebas, criterios de aceptación ni fuera de alcance.

Redactar en español claro y normativo. Preferir “debe”, “no debe”, “mantener”, “conservar” y “eliminar”. Los criterios deben describir resultados observables, incluyendo condiciones negativas relevantes.

## Pruebas como parte del trabajo

La validación no es opcional ni una tarea posterior. Cada ticket debe indicar cómo la IA del desarrollador debe:

- levantar o reutilizar el entorno necesario;
- ejecutar las pruebas automáticas más específicas durante el desarrollo;
- recorrer el flujo terminado en una instancia ejecutándose;
- comprobar al menos el caso feliz, un error o borde relevante y permisos cuando correspondan;
- ejecutar los checks completos de la capa afectada antes de cerrar;
- informar el comando exacto que falló y la limitación ambiental si algo no pudo verificarse.

Obtener los comandos reales desde el repositorio oficial, su README, scripts y CI. No copiar comandos del prototipo si la aplicación oficial usa otros.

## Entrega y Jira

- Entregar primero borradores revisables salvo que el usuario haya pedido explícitamente crear o actualizar tickets en Jira.
- No realizar cambios en Jira sin autorización para esa acción.
- Al crear una familia de tickets, presentar el orden sugerido, el pipeline entre carriles, las dependencias y una comprobación de que la carga total cabe en la capacidad semanal indicada.
- No afirmar que un ticket está listo si faltan contrato, criterio verificable, prueba ejecutable o una decisión bloqueante.

## Ejemplo de uso

**Pedido:** Prepará tickets de frontend y backend para implementar una nueva funcionalidad, considerando la capacidad semanal del equipo.

**Resultado:** Entrega borradores con alcance, dependencias, pruebas y criterios de aceptación, y propone una secuencia de trabajo.
