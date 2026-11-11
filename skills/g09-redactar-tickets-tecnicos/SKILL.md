---
name: g09-redactar-tickets-tecnicos
description: Redacta, completa o revisa tickets técnicos de frontend y backend como especificaciones listas para implementar y probar. Úsalo cuando el usuario pida crear un ticket, convertir requerimientos en tickets, separar trabajo frontend/backend o validar que un ticket sea inequívoco y verificable.
metadata:
  tipo: skill
  area:
  - gestion
  - frontend
  - backend
  fase:
  - analisis
  - planificacion
  tecnologias:
  - agnostico
  metodologia:
  - agnostico
  herramientas:
  - codex
  requiere: []
  grupo: "09"
  autor:
    nombre: Xoaquin Sanchez Varsallona
    github: XoaquinSanchezVarsallona
  responsables:
  - XoaquinSanchezVarsallona
  madurez: experimental
  relacionados:
  - g09-review-ticket-pr
---
# Redactar tickets técnicos

Convertí el requerimiento en una especificación ejecutable, no en una historia de usuario genérica. El equipo debe poder implementar y probar el ticket sin adivinar contratos, estados, reglas ni límites.

## Elegir el tipo de ticket

- Si el trabajo es solo frontend, leé [references/frontend.md](references/frontend.md).
- Si el trabajo es solo backend, leé [references/backend.md](references/backend.md).
- Si abarca ambos, redactá dos tickets independientes —frontend y backend— y leé ambas referencias. No mezcles responsabilidades en un único ticket salvo que el usuario lo pida expresamente.
- Si el usuario entrega un ticket como ejemplo, extraé su nivel de precisión y convenciones; no copies requisitos funcionales que no correspondan al nuevo trabajo.

## Reglas de redacción

1. Preservá literalmente nombres de rutas, endpoints, componentes, clases, métodos, campos, query keys, roles, status codes, mensajes visibles y mensajes de error proporcionados.
2. Hacé explícitas las diferencias con impacto observable: autenticado/no autenticado, dueño/tercero, vacío/no vacío, `null`/ausente/cero, mobile/desktop, éxito/error y orden de operaciones.
3. Identificá qué artefactos existentes deben reutilizarse y qué no debe crearse de nuevo. Si hay acceso al repositorio y el ticket debe alinearse con él, inspeccioná primero las convenciones pertinentes.
4. No inventes endpoints, campos, componentes ni reglas. Cuando falte una decisión imprescindible, agregá una sección breve `Definiciones pendientes`; si puede resolverse con una suposición conservadora, declarala como `Supuesto`.
5. Incluí estados de carga, error, vacío, reintento y éxito cuando apliquen. Describí la secuencia exacta de efectos asíncronos si el orden importa.
6. Cerrá siempre con `Fuera de alcance` y `Criterios de aceptación`. Los criterios deben ser concretos, observables y cubrir las reglas críticas, no repetir vagamente el objetivo.
7. Incluí pruebas o casos de prueba cuando el ticket defina lógica, validaciones, permisos o contratos. Diferenciá claramente requisitos obligatorios de recomendaciones.
8. Escribí en español claro, directo y técnico. Usá tablas cuando compacten rutas, endpoints, permisos o respuestas. Evitá introducciones ceremoniales, estimaciones y detalles genéricos que no cambien la implementación.

## Control de calidad

Antes de entregar, comprobá que:

- alcance, implementación, pruebas y criterios de aceptación sean consistentes entre sí;
- cada comportamiento condicional indique condición y resultado;
- cada operación protegida defina autenticación/autorización y comportamiento ante incumplimiento;
- cada validación indique restricción y mensaje/status esperado si fueron definidos;
- la persistencia, invalidación o actualización de caché y manejo de errores estén especificados cuando correspondan;
- ninguna funcionalidad fuera de alcance aparezca implícitamente como obligatoria;
- dependencias, inconsistencias o migraciones faltantes estén señaladas sin ampliar el alcance por cuenta propia.

## Ejemplo de uso

**Pedido:** Separá este requerimiento de edición de perfil en tickets frontend y backend, conservando los endpoints y permisos del contrato adjunto.

**Resultado:** Dos especificaciones con contratos, estados, pruebas, fuera de alcance y criterios de aceptación; las decisiones faltantes quedan explícitas.
