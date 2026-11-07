---
name: g09-generar-coleccion-postman
description: Generar una colección Postman ejecutable para un ticket de Zervi con requests, aserciones y fixtures locales. Usar al entregar o verificar un endpoint.
tools: Read, Write, Edit, Grep, Glob, Bash, Skill
metadata:
  tipo: skill
  area:
  - backend
  - qa
  fase:
  - desarrollo
  - revision
  tecnologias:
  - postman
  - kotlin
  - spring-boot
  - postgresql
  metodologia:
  - scrum
  herramientas:
  - codex
  requiere: []
  grupo: "09"
  autor:
    nombre: Máximo Sallemi
    github: MaximoSallemi
  responsables:
  - MaximoSallemi
  madurez: prototipo
  relacionados:
  - ticket-test-matrix
  - check-front-back-contract
---
# Generar una colección Postman

1. Leer el ticket o contrato recibido. Si solo se recibe una clave, recuperar el ticket con el MCP de Atlassian. Contrastar cada criterio con las rutas, DTOs, permisos y migraciones vigentes. Señalar cualquier discrepancia y conservar la expectativa del contrato en la prueba.
2. Inspeccionar `backend/postman/README.md`, el environment **Zervi local** y la colección más parecida. Actualizar la colección del ticket si existe. Para una nueva, crear en `backend/postman/<clave> - <funcionalidad>/` su definición bajo `.resources/` y un archivo numerado `*.request.yaml` por caso. Seguir la estructura y el registro de recursos del workspace existente, con identificadores propios.
3. Usar `{{baseUrl}}`, el orden de ejecución explícito y scripts `afterResponse` con `pm.test`. Cubrir éxito y errores relevantes al ticket. Verificar valores y efectos observables además del código HTTP. Para probar permisos, mantener válido el resto del request. Para escrituras, verificar el resultado mediante una lectura posterior cuando corresponda.
4. Descubrir IDs por API y guardarlos en variables de colección cuando sea posible. Si hacen falta datos específicos, crear un fixture SQL idempotente para la base local con IDs reservados y limpieza acotada. Para JWT usar variables locales vacías en el repo. Identificar cada caso que dependa de credenciales o datos opcionales.
5. Documentar preparación, roles, variables y orden para **Run collection**. Validar que Postman reconozca los recursos y ejecutar contra una instancia local de prueba cuando esté disponible. Entregar rutas, criterios cubiertos, resultados y casos omitidos con el motivo. Si solo se pudo validar la estructura, dejar pendiente la ejecución HTTP.

## Ejemplo de uso

**Pedido**

> Generá una colección para probar el alta de turnos en local, con un caso válido y otro sin fecha.

**Salida esperada**

Una colección importable en Postman con variables de entorno, cuerpos de ejemplo y aserciones sobre los códigos y campos definidos por el endpoint.
