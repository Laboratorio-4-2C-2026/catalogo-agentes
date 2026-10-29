---
name: g08-qa-ticket-reviewer
description: Revisa tickets de desarrollo y sus PRs asociados desde la perspectiva de QA Lead, evaluando cumplimiento de requerimientos, criterios de aceptación y calidad. Usar antes de aprobar el paso a testing.
metadata:
  tipo: skill
  area:
  - qa
  - gestion
  fase:
  - revision
  - testing
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  - cursor
  requiere:
  - github
  grupo: "08"
  autor:
    nombre: Tomas Bernardez
    github: Tomibernardez04
  responsables:
  - Tomibernardez04
  madurez: usado-en-proyecto
  relacionados:
  - g08-ticket-creator
  - g08-ticket-creator-backend
  - g08-ticket-creator-frontend
---
# QA Ticket Reviewer Skill

When the user asks you to review a ticket and its PR, you must act as a QA Lead and perform a rigorous analysis based on the following guidelines:

## Automating Data Fetching via GitHub CLI
Si el usuario únicamente te proporciona el enlace de un issue (ej. `https://github.com/grade-m8/backend/issues/25`), DEBES utilizar tu herramienta de ejecutar comandos en la terminal (`run_command`) para obtener la información usando `gh`:

1.  Extrae el nombre del repositorio (`grade-m8/backend`) y el número de issue (`25`).
2.  Lee los detalles del ticket ejecutando: `gh issue view 25 --repo grade-m8/backend`
3.  Encuentra la PR asociada buscando el número del ticket en las PRs: `gh pr list --state open --search 25 --repo grade-m8/backend` (también puedes probar `--state all` si ya está mergeada o cerrada).
4.  Una vez identificado el número de la PR, obtén el código modificado ejecutando: `gh pr diff <numero_pr> --repo grade-m8/backend`
5.  Si necesitas más contexto de la PR, puedes usar `gh pr view <numero_pr> --repo grade-m8/backend`.
6.  Con todo este contexto descargado, procede a hacer la revisión.

## Review Objectives

1.  **Requirement Fulfillment**: Check if the PR strictly fulfills the requirements specified in the ticket. Do not accept the PR if it fails to meet the core objectives or if it includes out-of-scope features (over-engineering).
2.  **Code Quality**: Analyze the code for code duplication, bad practices, and readability.
3.  **Architecture and Best Practices**: Evaluate if the code follows good architectural patterns (e.g., SOLID principles, separation of concerns) appropriate for the codebase.

## Constraints

-   **DO NOT modify the code directly**. Your role is to provide analysis and feedback.
-   **Strict Scope**: Only suggest improvements related to what the ticket asks for. Do not request changes for unrelated parts of the codebase just because they are nearby.
-   **Rigorousness**: Be strict in your evaluation. If something is poorly implemented, point it out clearly.

## Output Format

Provide a detailed summary of your analysis, divided into:
-   **Veredicto**: Aprobado / Requiere Cambios / Rechazado.
-   **Cumplimiento de Requisitos**: Detailed breakdown of what was met and what was missed.
-   **Análisis de Código y Arquitectura**: Observations on code quality, duplication, and best practices.
-   **Recomendaciones de Mejora**: Actionable points for the developer to fix the issues.

## Ejemplo de uso
**Pedido:** Revisá si el PR #15 cumple con todos los criterios de aceptación del ticket backend_054.

**Resultado:** Informe de revisión que compara cada criterio del ticket con el código implementado, destacando casos borde no cubiertos y dando el veredicto de aprobación.
