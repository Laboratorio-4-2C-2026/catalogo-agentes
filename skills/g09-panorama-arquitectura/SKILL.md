---
name: g09-panorama-arquitectura
description: Explica la arquitectura y las decisiones técnicas de Zervi o Conexia para obtener un panorama general del proyecto, siguiendo código, contratos, configuración y decisiones documentadas. Usar para onboarding o exposición técnica; no realiza una refactorización ni una auditoría integral.
metadata:
  tipo: skill
  area:
  - documentacion
  - frontend
  - backend
  - devops
  fase:
  - analisis
  - diseno
  tecnologias:
  - react
  - typescript
  - kotlin
  - spring-boot
  - nestjs
  - prisma
  - flyway
  - postgresql
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
  relacionados: []
---
# Panorama de arquitectura y decisiones técnicas

Construí una explicación que le permita a alguien nuevo entender cómo funciona el proyecto, dónde viven sus responsabilidades y qué decisiones condicionan su evolución.

## Entrada y fuentes

Recibí proyecto, rama/SHA si interesa una versión concreta y nivel de detalle. Usá por defecto el checkout local `zervi/Zervi` o `conexia`, registrando rama, SHA y presencia de cambios locales relevantes. `zervi/zervi-lab4` es otro checkout: no mezcles su código con el de `zervi/Zervi` como si fueran una sola versión.

Leé las instrucciones aplicables y empezá por manifiestos de dependencias, estructura de código, entrada de la aplicación, composición de módulos, esquema/migraciones y configuración de integraciones. Los README locales pueden ser breves o conservar plantillas; contrastalos con código antes de describir la aplicación. Las copias en `agentes/fuentes` son antecedentes fechados: preferí el repositorio original actual.

Pistas de lectura, no hechos inmutables:

- Zervi: `backend/` Kotlin/Spring, `frontend/` React/Vite, `docs/`, migraciones Flyway y `zervi/infrastructure-updated/` si el alcance incluye despliegue. Confirmá versiones y estructura en el checkout elegido. Leé el [runbook](references/runbook-despliegue.md) antes de describir su infraestructura.
- Conexia: `backend/` NestJS, `backend/prisma/`, `frontend/`, `e2e/`, `.github/workflows/` y [documentación de notificaciones](references/notificaciones.md). Confirmá su autenticación e integraciones desde módulos y configuración.

No accedas a `.env`, state ni archivos de credenciales para explicar la arquitectura; los nombres de variables y ejemplos públicos suelen bastar.

## Análisis

1. Identificá el propósito del producto, actores y capacidades principales que estén implementadas en la revisión elegida.
2. Mapeá frontend, backend, persistencia, autenticación, integraciones externas, tareas asíncronas y runtime. Marcá qué componente pertenece a cada proceso o servicio. Tener carpetas por dominio no prueba una arquitectura de microservicios.
3. Seguí uno o dos flujos representativos desde una acción de UI hasta API, autorización, servicio, persistencia y efectos externos. Elegí flujos que existan en el código; no inventes endpoints para completar un esquema ideal.
4. Explicá límites de responsabilidad, contratos, manejo de errores, estado de cliente, migraciones y estrategia de pruebas/CI en lo que afecte esos flujos.
5. Relevá decisiones técnicas en ADR, tickets/comentarios aportados o accesibles, PR y documentación específica. El uso de una biblioteca demuestra su adopción, no el motivo por el que el equipo la eligió.
6. Clasificá cada decisión: **documentada** (hay una razón expresada), **observada** (se ve en el código, motivo no documentado) o **inferencia** (interpretación razonada y explícita). No atribuyas al equipo alternativas evaluadas, ventajas buscadas ni acuerdos que no estén registrados.
7. Separá arquitectura implementada, código incompleto o mocks, planes documentados y mejoras sugeridas por vos. Describí contradicciones entre documentos y código con sus fuentes.

## Entrega

Empezá con un panorama breve en lenguaje accesible. Incluí un diagrama Mermaid pequeño si aclara las relaciones; usá nombres de componentes realmente encontrados y distinguí fronteras externas. Después presentá:

- Componentes y responsabilidades, con archivos concretos para ubicarlos.
- Recorrido de los flujos elegidos y contratos relevantes.
- Decisiones, motivo conocido, efecto/contrapartida y grado de evidencia.
- Deuda y limitaciones verificadas, planes ya documentados y preguntas sin respuesta.
- Cinco puntos de entrada de lectura como máximo para seguir explorando.

Para decisiones usá:

| Decisión | Documentada / observada / inferencia | Fundamento conocido | Consecuencia o contrapartida | Fuente |
| --- | --- | --- | --- | --- |

Indicá versión analizada y citá archivos/líneas o enlaces a decisiones. Si el usuario pide ambos proyectos, mostrálos por separado y compará solo después, sin trasladar autenticación, entidades o despliegue de uno al otro.

## Límites y aceptación

Es una tarea de lectura y explicación: no cambia dependencias, código, infraestructura ni crea decisiones a nombre del equipo. Está completa cuando permite entender el mapa, seguir un flujo real y distinguir hechos de razones documentadas e inferencias.

## Ejemplo de uso

**Pedido:** Explicame la arquitectura del checkout indicado y seguí un flujo real desde la interfaz hasta la persistencia.

**Resultado:** Un mapa de componentes y flujos, con archivos de entrada y decisiones diferenciadas como documentadas, observadas o inferidas.
