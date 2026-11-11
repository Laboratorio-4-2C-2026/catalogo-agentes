---
name: g14-investigador-kpi-multi-equipo
description: Investiga y compara arquitecturas para que varios equipos de la materia reporten KPIs diarios a una plataforma común, y arma una propuesta para votar (documento largo, resumen de una carilla, encuesta y banco interno de alternativas descartadas). Usala cuando la cátedra pide un estándar compartido entre equipos y hay que coordinar sin reuniones.
metadata:
  tipo: skill
  area:
  - gestion
  - datos
  fase:
  - analisis
  - diseno
  tecnologias:
  - agnostico
  metodologia:
  - agnostico
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

# Investigador de KPIs entre equipos

Llevá a varios equipos a un acuerdo técnico con una propuesta que se pueda votar en una semana. En VaiVen (escenario 2 del KPI Challenge, equipos 9 a 16) el resultado vive en `docs/challenge-kpi/`.

## 1. Leé la consigna y bajala a criterios

Copiá la consigna textual a `consigna.md`. De ahí, escribí **criterios de comparación numerados y verificables**, no preferencias. Los de VaiVen:

1. Un profesor la opera sin los autores, con los pasos de la guía.
2. Claude o ChatGPT llegan a los datos en un paso.
3. Un equipo se integra en una tarde.
4. **Cada pieza copia una práctica publicada** (OpenTelemetry, OpenMetrics, SemVer, Idempotency-Key…), no gusto de nadie.
5. Nadie puede borrar datos, tampoco quien administra.
6. Sin sobreingeniería: estimá el volumen total (VaiVen: ~10.000 filas) y sacá toda capa que no sirva a un criterio.

## 2. Investigá en cinco informes separados

En `investigacion/`, uno por pregunta, para que no se contaminen:

| Informe | Pregunta |
|---|---|
| `01-estandares` | Qué práctica publicada respalda cada campo y cada mecanismo |
| `02-arquitecturas` | Qué plataformas pueden cumplir, con límites del plan gratuito citados |
| `03-<proyecto>` | Qué KPIs reporta el propio equipo y cuánto le cuesta integrarse |
| `04-critica` | Ataque a cada opción: la objeción en 15 minutos, qué pasa si se va la cuenta del creador, si recibe datos el día uno. Resuelve las contradicciones entre informes y da un veredicto |
| `05-huecos` | Lo que falta verificar antes de presentar |

Cada afirmación lleva fuente (URL de documentación oficial) o `[asumido]`. Los límites de planes gratuitos se citan textuales: cambian.

## 3. Reducí a tres opciones comparables

Una tabla, mismas filas para todas: setup del profesor, horas de integración por equipo, consulta con IA, dónde se valida, cómo se evita el borrado. Una recomendación y una segunda. Frente a la propuesta rival, decí **dónde no ganás** antes de decir dónde sí.

## 4. Escribí cuatro piezas

| Pieza | Para quién | Regla |
|---|---|---|
| `propuesta-<escenario>.md` | Quien quiere objetar | Criterios, opciones, recomendación, comparación con la rival, esfuerzo por equipo, cómo seguimos; anexos con el contrato de datos y la governance |
| `resumen-una-carilla.md` | Quien vota | Fecha límite arriba, tabla de opciones, recomendación, contrato en una figura, governance en cinco líneas, qué hace cada equipo gane quien gane |
| `mensaje-y-encuesta.md` | El grupo de los equipos | Mensaje corto con los dos links, una encuesta nativa (un voto por equipo), fecha y hora de cierre, «si nadie vota, va la recomendación», opción «Otra» |
| `alternativas-descartadas.md` | **Sólo interno** | Banco de «¿y por qué no X?»: alternativa · por qué no · hecho que la cierra · fuente. Lo `[asumido]` no se dice en voz alta |

Los PDF se generan desde los markdown con un script (`scripts/generar-pdf-challenge-kpi.py` en VaiVen); el PDF entregado es un snapshot y las correcciones posteriores se marcan `[corregido <fecha>]` en el markdown.

## 5. Contrato y governance

- **El contrato es uno solo**: si la base valida con claves foráneas y `CHECK`, no agregues un JSON Schema paralelo que se desvíe al segundo cambio.
- Clave natural de idempotencia (proyecto, KPI, fecha, ambiente) antes que un id de corrida.
- La nota se cuenta por la fecha de recepción del servidor, no la declarada.
- Governance en reglas cortas: repo público del contrato, SemVer, aprobaciones por tipo de cambio, plazo para objetar.

## Reglas

- Nada está pactado: la propuesta se ofrece para ahorrar reuniones, y cualquier equipo puede sumar una opción.
- Ofrecé presentar y preparar la demo; invitá a sumarse.
- Después de adoptada, auditá la propuesta contra lo construido y anotá lo que quedó viejo.

## Ejemplo de uso

**Pedido:** La cátedra pide que los equipos 9 a 16 acuerden una plataforma de KPIs diarios distinta de Dataverse; armá la propuesta para votar antes del lunes.

**Resultado:** Produce los cinco informes de investigación, la propuesta larga con tres opciones y anexos de contrato y governance, el resumen de una carilla, el mensaje con la encuesta y el banco interno de alternativas descartadas con su fuente.
