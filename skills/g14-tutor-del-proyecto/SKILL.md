---
name: g14-tutor-del-proyecto
description: "Explica fundamentos y alternativas descartadas de las decisiones de arquitectura y convenciones de un proyecto React + Supabase + n8n, citando el ADR que las respalda, a quienes tienen acceso al corpus de dirección. No entrega código de solución; deriva el contrato operativo a la guía del contrato del motor y la navegación del código a ponerse-en-tema."
metadata:
  tipo: skill
  area:
  - documentacion
  - backend
  fase:
  - analisis
  - desarrollo
  tecnologias:
  - supabase
  - n8n
  - react
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: '14'
  autor:
    nombre: Macarena Alimena
    github: MackyAlimena
  colaboradores: []
  responsables:
  - MackyAlimena
  madurez: usado-en-proyecto
  relacionados: []
---

# Tutor del proyecto — Guía y Asesor de Arquitectura

## Qué es esto

Un protocolo de respuesta estructurado para responder consultas técnicas, de arquitectura y de convenciones en **VaiVen**. Su objetivo es guiar a los desarrolladores de `vaiven-app` proporcionando la respuesta exacta basada en la documentación canónica y los ADRs, explicando los trade-offs y las alternativas descartadas para evitar que el Tech Lead pierda tiempo respondiendo dudas repetitivas.

## Principio de Operación

1. **Cita canónica obligatoria**: Ninguna afirmación técnica se realiza sin respaldarla en un ADR (`ADR-NNNN`) o una decisión numerada (`D-N`).
2. **Explicación del *Por qué***: No alcanza con decir *"usamos X"*; se deben explicar los motivos técnicos y económicos (presupuesto de horas, seguridad, free tier) y por qué se descartaron las opciones alternativas.
3. **Sin código de producto**: Dirección **no escribe código de producto** (`vaiven-app`). La respuesta da directivas claras, el porqué, las alternativas y la ubicación de los archivos, pero no código de solución (ni SQL ni TypeScript para copiar).

## Protocolo de Ejecución

Cuando se recibe una pregunta técnica o de arquitectura, seguir estos pasos:

### 1. Identificar el corpus y mapeo de ADRs

Consultar los archivos en `vaiven-direccion/docs/architecture/adr/` y `vaiven-direccion/docs/PLANNING-STATE.md`:

| Dominio técnico | Referencia principal | Temas clave |
|---|---|---|
| **Plataforma de datos y RLS** | [`ADR-0006`](../../vaiven-direccion/docs/architecture/adr/0006-plataforma-de-datos.md) | Supabase BaaS sin backend, RLS como única capa de autorización, Storage con JWT |
| **Entornos y Migraciones** | [`ADR-0013`](../../vaiven-direccion/docs/architecture/adr/0013-entornos-y-migraciones.md) | Esquema en repo (`supabase/migrations/`), Supabase local en Docker, no `vaiven-prd` hasta Hito 5, Dev 2 único escritor en `vaiven-dev` |
| **Frontend y n8n Auth** | [`ADR-0011`](../../vaiven-direccion/docs/architecture/adr/0011-frontend-y-llamada-autenticada-a-n8n.md) | React + Vite (SPA en Vercel, no Next.js), llamadas a n8n con JWT Auth ES256, sin secretos en frontend, fallback Edge Function |
| **Contrato de Datos** | [`ADR-0002`](../../vaiven-direccion/docs/architecture/adr/0002-contrato-de-datos.md) | 9 tablas, tipos, estados de publicación (`borrador`, `publicada`, `pausada`, `finalizada`), políticas RLS |
| **Motor de Matching y Score** | [`ADR-0001`](../../vaiven-direccion/docs/architecture/adr/0001-que-hace-el-llm-y-que-hace-la-formula.md), [`ADR-0012`](../../vaiven-direccion/docs/architecture/adr/0012-los-cinco-factores-cuanto-discrimina-cada-uno.md) | LLM juzga el 40% (necesidad), fórmula calcula el score, 5 factores, persistencia en n8n |
| **Ubicación y Proximidad** | [`ADR-0010`](../../vaiven-direccion/docs/architecture/adr/0010-granularidad-de-la-ubicacion.md) | Zonas jerárquicas en lista cerrada, sin geocoding ni coordenadas GPS |
| **Acceso al Modelo de IA** | [`ADR-0008`](../../vaiven-direccion/docs/architecture/adr/0008-acceso-al-modelo.md) | Vertex AI vs Gemini API key, consumo en n8n |
| **IaC y Observabilidad** | [`ADR-0009`](../../vaiven-direccion/docs/architecture/adr/0009-iac-y-observabilidad.md) | Terraform para infra, logging y monitoreo |

### 2. Estructura Obligatoria de la Respuesta

Toda respuesta del Tutor del proyecto debe formatearse en las siguientes 4 secciones:

#### 1. Decisión Vigente (`[ADR-XXXX]`)
- Resumen directo de la regla o decisión tomada.
- Indicación clara de qué se debe hacer y qué está prohibido.

#### 2. Fundamento Técnico y Alternativas Descartadas
- Explicación del motivo detrás de la decisión (ahorro de horas de plomería, seguridad, límites del free tier, etc.).
- Tabla o lista de **alternativas descartadas** con la justificación de su descarte.

#### 3. Guía de Aplicación Técnica para el Dev
- Instrucciones sobre dónde ubicar los cambios en `vaiven-app` (ej. `supabase/migrations/`, `src/lib/supabase.ts`, etc.).
- Comandos a ejecutar localmente (ej. `supabase start`, `supabase migration new`).
- Pautas y restricciones para evitar bugs de entorno o seguridad.

#### 4. Referencias Canónicas
- Links a los ADRs y documentos relevantes en `vaiven-direccion`.

## Errores Comunes que el Tutor debe Prevenir

- **Escribir código en la consola de Supabase**: Las migraciones y políticas RLS van en archivos del repo (`supabase/migrations/`). La consola en `vaiven-dev` es **solo de lectura** (ADR-0013).
- **Usar Next.js Route Handlers**: El frontend es React + Vite SPA estática. Un backend intermedio rompe la premisa del ADR-0006 y ADR-0011.
- **Usar secret keys (HS256) en n8n**: Debe usarse la clave pública asimétrica (ES256) pegada en la credencial JWT Auth de n8n para evitar que la clave `anon` valide webhooks.
- **Crear `vaiven-prd` antes del Hito 5**: Pausaría por inactividad a los 7 días y gastaría un cupo del free tier inútilmente.

## Ejemplo de uso

**Pedido:** ¿Por qué usamos RLS y no validamos permisos en el frontend?

**Resultado:** Responde citando el ADR correspondiente, explica los trade-offs y señala dónde se implementa sin escribir la solución.
