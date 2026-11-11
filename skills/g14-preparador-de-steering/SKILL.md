---
name: g14-preparador-de-steering
description: Arma el contenido, el guion y el respaldo de un steering o sprint review (estado, cronograma, valor ganado, riesgos, próximos pasos y demo) en tres niveles —slide, notas y respaldo— sobre la plantilla de la cátedra, y lo pasa a Canva respetando los límites de su MCP. Usala la semana previa a un steering, cuando hay que convertir el estado del proyecto en 15 minutos defendibles.
metadata:
  tipo: skill
  area:
  - gestion
  - documentacion
  fase:
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - canva
  - jira
  grupo: '14'
  autor:
    nombre: Macarena Alimena
    github: MackyAlimena
  colaboradores: []
  responsables:
  - MackyAlimena
  madurez: usado-en-proyecto
  relacionados:
  - g14-valor-ganado-desde-jira
---

# Preparador de steering

Convertí el estado del proyecto en una presentación de tiempo fijo donde cada número tiene fuente y cada pregunta probable tiene respuesta. Primero el texto, después el diseño.

## 1. Fijá los criterios antes del contenido

Escribí una tabla de criterios y hacela aprobar por el equipo antes de redactar slides:

| Tema | Qué fijar (ejemplo VaiVen, Steering 1) |
|---|---|
| Duración | 15 min: 8:30 de slides, 4:30 de demo, 2:00 de margen |
| Quién presenta | Por slide, según el rol vigente en ese hito |
| Fecha real | La del tablero: la tarea quedó lista para revisión |
| Desvío | Línea base − real; negativo = atraso |
| Valor ganado | En horas de desarrollo, capacitación incluida |
| Riesgos | Los del tablero compartido con la cátedra + los del charter que siguen abiertos |
| Fuera de la presentación | Lo que no se proyecta aunque exista (horas de dirección, agente de review) |

**Fuentes, nombradas con su versión:** tablero compartido con la cátedra (fechas, semáforos, riesgos), Jira por API (horas), la rama `main` del producto con su SHA (PRs y demo), charter (alcance y presupuesto).

## 2. Recortá la plantilla

Partí de la plantilla oficial y decidí qué páginas quedan. Fusionar o borrar una página es válido si se anota y se prepara la respuesta (VaiVen fusionó Presupuesto en Valor ganado y preparó la defensa en dólares por si la pedían).

## 3. Escribí cada slide en tres niveles

| Nivel | Qué entra | Regla de corte |
|---|---|---|
| **En la slide** | El mensaje y lo que pide el campo de la plantilla | Se lee en menos de un tercio del tiempo de la slide. Sustantivos y números. Subtítulo de ~60 caracteres. Sin códigos internos ni etiquetas |
| **Notas** | Lo que dice quien presenta: por qué, qué acción, pase a la siguiente | ~130 palabras por minuto de slide |
| **Respaldo** | Fuentes, cálculos, tablas completas, contingencias y preguntas con respuesta | Si nadie pregunta, no se dice |

Menos texto proyectado = menos cosas que defender. Densidad de referencia: una idea por slide, menos de 30 palabras.

## 4. Bloques típicos y de dónde salen

1. **Portada, proyecto, equipo y roles.** Roles del hito que se rinde.
2. **Alcance.** Qué cambió desde el steering anterior y por qué; un cambio de alcance presentado se escribe después en el charter.
3. **Cronograma.** Gantt por módulo con estado en rangos de avance funcional, no lineal en horas.
4. **Valor ganado.** Con `g14-valor-ganado-desde-jira`. Curva, recuadro de índices y una frase.
5. **Riesgos foco.** Pocos (cuatro o cinco), priorizados con probabilidad × impacto, cada uno con respuesta y responsable.
6. **Próximos pasos.** Sólo lo planificado; sugerencias de los profesores sin horas van a las notas.
7. **Demo.** Pasos numerados para los devs y plan B (demo local con la semilla).

## 5. Entregables

- `docs/presentaciones/steering-N-<fecha>.md`: contenido en tres niveles, tabla de tiempos y «Pendiente antes del jueves».
- `docs/presentaciones/steering-N-<fecha>-guion.md`: lo que se dice por slide, con rol y tiempo, más una tabla «Si preguntan» (pregunta · respuesta corta · quién responde).
- Si un tema es flanco (presupuesto, valor ganado), un documento de defensa aparte que no se proyecta.

## 6. Pasar a Canva

- Leé antes la bitácora del MCP de Canva del repo. La API **no lista todos los elementos** (formas y gráficos quedan fuera), **no crea elementos** y formatea el elemento entero: `find_and_replace_text` hereda el formato del tramo donde arranca la coincidencia.
- Antes de reacomodar una slide, contá los elementos del thumbnail contra los que devuelve la API; la diferencia es la lista de tareas manuales, que se entrega junta al final.
- Trabajá sobre una copia del deck; pasá al original lo aprobado.
- El thumbnail lo ve el agente, no la persona: **commiteá la edición y pedí la revisión sobre el diseño real.** Si una edición fue rechazada, releé antes de commitear: puede haber quedado aplicada.
- Medí las fuentes: mínimo legible ~22 en texto, 26–30 en tablas.

## Reglas

- Lo `[asumido]` no se afirma en voz alta como hecho; si entra, va al respaldo con su etiqueta.
- Un desvío conocido que no se corrige antes de presentar (VaiVen: la tabla de costos del charter descuadraba $3) se prepara en una frase y no se discute.
- Ofrecé el punto débil antes de que lo pregunten (el SPI de 0,69 a mitad del hito).
- Tiempos sumados: el total tiene que dar la duración pactada.

## Ejemplo de uso

**Pedido:** Prepará el Steering 2 del cierre del Hito 4: guion de 15 minutos, valor ganado al 15/10 y los riesgos para lo que queda.

**Resultado:** Entrega la tabla de criterios para aprobar, el contenido de cada slide en tres niveles, el guion con rol y tiempo por slide, la tabla «Si preguntan» y la lista de tareas manuales para terminar el deck en Canva.
