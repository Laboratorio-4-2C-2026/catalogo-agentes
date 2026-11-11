---
name: g14-tablero-semanal-de-la-catedra
description: Arma la entrada semanal del tablero que pide la cátedra a partir de Jira y GitHub, y propone con Gemini el color de estado de cada frente para que el equipo lo confirme. Corre como GitHub Action o a mano.
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  - jira
  - google-sheets
  - gemini
  grupo: '14'
  autor:
    nombre: Martina de Jesus
    github: mardejesus
  colaboradores: []
  responsables:
  - mardejesus
  madurez: usado-en-proyecto
  relacionados: []
---

# Tablero semanal de la cátedra

Prepara lo que el PM carga cada jueves antes de las 9 en la planilla de la cátedra. Los datos los junta un script; la skill pone el criterio: un color por área, con evidencia.

## Reglas fijas

1. **Nunca se escribe en la planilla.** Se sugiere; carga el PM.
2. **Fecha real = el día en que se abrió el último PR de la tarea.** Si no hay PR, el paso a revisión en Jira. Cuando las dos difieren, se muestran las dos.
3. **F. Fin L. Base no se mueve.** Fila existente: la de la planilla. Fila nueva: el fin del sprint de Jira, marcado «confirmar».
4. **F. Fin Estimado = L. Base**, salvo que haya un cambio de pronóstico con evidencia.
5. **Desvío = L. Base − Real**, en días. Positivo es antes de tiempo.
6. **General no se elige, se calcula:** Rojo si hay ≥1 rojo o ≥3 amarillos; Amarillo si hay ≥1 amarillo; Verde en el resto (`--general`).
7. **Cada color lleva su evidencia**: `SCRUM-n`, `PR #n`, una entrada de bitácora o una sesión. Sin evidencia, el área queda «a confirmar», no Verde por defecto.
8. Motivo y acción con el formato de la planilla: «Sem-NN: …», en pasado, una o dos frases. Sólo si el área no es Verde.

## Protocolo

1. Correr `python3 scripts/tablero-semanal.py` (con `--semana Sem-NN` para forzar una). Detecta solo las semanas vacías hasta hoy.
2. **Estado semanal**, por semana y por área (Alcance, Cronograma, Incidentes, Calidad, Riesgos):
   - **Alcance**: ¿entró trabajo que no estaba planificado? Mirar tickets creados en la semana y lo que traiga dirección.
   - **Cronograma**: los desvíos de la tabla. Alguno negativo, o una tarea sin empezar a un día del cierre → Amarillo.
   - **Incidentes**: algo que frenó a alguien o rompió algo. Fuente: bitácora y novedades de `vaiven-direccion`.
   - **Calidad**: veredictos del reviewer de PRs (`salidas/code-reviewer-de-prs.txt`) y checks de build.
   - **Riesgos**: algo que todavía no pasó pero puede pasar. Fuente: spikes, bitácora, `PLANNING-STATE`.
3. Calcular el General con la regla 6. Si da Rojo por tres amarillos, decirlo explícitamente.
4. **Cronograma**: completar las diez columnas (Actividad, Estado, Avance, L. Base, Estimado, Real, Desvío, Comentarios) y el encabezado (Avance Global, Fecha de Fin Prevista).
5. **Incidentes**: una fila por incidente nuevo, con las ocho columnas (Descripción, Estado, Criticidad, F. Alta, F. Límite, F. Cierre, Vencido, Resolución). Si empezó en una semana ya cargada, avisarlo.
6. Entregar todo listo para copiar, con lo que decide el PM marcado como tal.

## Disparo

- 🟢 `cron`: el workflow viene en esta carpeta, en `.github/workflows/tablero-semanal.yml`; copialo al `.github/workflows/` de tu repo junto con `scripts/`. Corre los jueves 8:30. Abre un issue con los datos, una propuesta de colores de Gemini (`scripts/tablero-ia.py`, con estas mismas reglas) y menciona a los cuatro. Decide el PM.
- 🟡 `humano`: esta skill, cuando además se quiere la propuesta de colores con evidencia.

## Instalación

- **Secrets del repo:** `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, `GEMINI_API_KEY` (AI Studio) y un token de lectura de GitHub (`VAIVEN_APP_TOKEN` en el workflow) que vea los repos que se miden.
- **Planilla:** se lee como CSV exportado, sin credenciales; tiene que ser visible por enlace. Cambiá `PLANILLA` y `GID_EQUIPO_14` en `scripts/tablero-semanal.py`, los repos del paso de comprobación y la lista de `--mencionar` del workflow.
- A mano: exportá las mismas variables y corré los dos scripts; el resultado sale por consola, no se guarda en archivos.

## Ejemplo de uso

**Pedido:** Armá la entrada del tablero de la cátedra para las semanas 9 y 10.

**Resultado:** Junta el avance de Jira y GitHub, abre la propuesta en un issue con los colores sugeridos por la IA y su motivo (también en el resumen de la corrida), listo para que el PM lo copie a la planilla.
