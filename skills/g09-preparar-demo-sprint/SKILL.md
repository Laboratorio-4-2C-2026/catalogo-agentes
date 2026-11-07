---
name: g09-preparar-demo-sprint
description: Preparar un guion de demo del sprint de Zervi a partir de tickets de Jira y PRs de GitHub, con datos, roles, recorridos y resultados esperados. Usar antes de la revisión del sprint para ensayar la demostración.
tools: Read, Grep, Glob, Bash, Skill
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
  requiere:
  - jira
  - github
  grupo: "09"
  autor:
    nombre: Máximo Sallemi
    github: MaximoSallemi
  responsables:
  - MaximoSallemi
  madurez: prototipo
  relacionados:
  - g09-reporte-de-estado
  - ticket-test-matrix
---
# Preparar la demo del sprint

1. Identificar sprint, entorno de demo y tiempo disponible. Usar el sprint activo si no se indica otro. Con el MCP de Atlassian resolver el proyecto Zervi y paginar los tickets del sprint. Leer criterios de aceptación y agrupar los tickets por funcionalidad visible para quien asiste.
2. Consultar las PRs con el conector de GitHub o `gh` autenticado. Asociarlas por enlaces explícitos o clave exacta en rama, título o descripción. Revisar todas las PRs necesarias para cada recorrido, incluidas las de frontend y backend. Registrar enlaces y rama destino. Si el vínculo es dudoso, marcarlo como tentativo.
3. Identificar qué revisión corre en el entorno de la demo mediante evidencia de despliegue o el commit del checkout local. Para cada recorrido comprobar rutas y controles reales, rol requerido, datos iniciales y resultado visible. Consultar `backend/DEMO_DATA.md` para usar los datos disponibles. Cuando corresponda, indicar cómo ejecutar `.\gradlew.bat seedDemo` desde `backend` en la base local de demo. Preparar una cuenta por rol sin incluir credenciales en el guion.
4. Ordenar los recorridos como una historia de usuario. Para cada uno entregar **objetivo, duración estimada, rol y datos, pasos que hace el presentador, resultado visible y enlaces a ticket y PRs**. Explicar qué cuenta debe retomar el recorrido cuando cambia el rol. Para cambios exclusivamente de API, usar un request concreto de la colección Postman si existe.
5. Ensayar en el entorno indicado cuando esté disponible. Marcar cada recorrido como **comprobado** (se observó el resultado), **pendiente de ensayo** o **bloqueado** con el motivo. Ante una PR pendiente, una dependencia ausente o una versión sin verificar, explicitar el efecto en la demo. Cerrar con la preparación previa y un recorrido alternativo reproducible si el principal queda bloqueado.

## Ejemplo de uso

**Pedido**

> Prepará una demo de cinco minutos del sprint actual con los tickets de turnos que tengan implementación demostrable.

**Salida esperada**

Un guion ordenado por tiempo, con rol, datos iniciales, pasos, resultado visible y enlaces al ticket y a la PR.
