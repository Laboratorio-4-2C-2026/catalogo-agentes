---
name: g12-revisar-pr
description: Revisa un PR contra las convenciones del repositorio y los criterios de la historia. Devuelve hallazgos en español, líneas exactas y comentarios listos para copiar. Usar cuando un PR está listo para revisión técnica.
metadata:
  tipo: skill
  area:
  - qa
  fase:
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - codex
  - otra
  requiere:
  - github
  grupo: '12'
  autor:
    nombre: Marcos Hussey
    github: husseymarcos
  responsables:
  - husseymarcos
  madurez: usado-en-proyecto
  relacionados:
  - g12-validar-pr-de-producto
---

# Revisar PR

Revisar el cambio solicitado sin modificar código. Ejemplo: `/revisar-pr <URL del PR>`.

## Evidencia y alcance

Leer el PR, su descripción, la historia vinculada, los comentarios existentes y los
`AGENTS.md` aplicables a cada archivo. Identificar base y head SHA; revisar todos los
archivos del diff y el código circundante necesario para seguir el flujo afectado.
Si no se puede acceder a la historia, continuar la revisión técnica e indicar que falta
verificar la especificación. Una discusión resuelta sólo se reabre con evidencia nueva.

Distinguir cambios del PR de problemas anteriores. Para cada posible hallazgo, seguir
sus llamadas y consumidores y comprobar que exista un caso alcanzable que lo produzca.
Si cambia un contrato entre módulos, servicios o clientes, inspeccionar ambos lados
y sus tests.

## Dos lecturas

- **Standards:** contrastar con las instrucciones del proyecto y los patrones existentes.
  Descubrir la arquitectura, lenguajes y herramientas en la documentación y el código;
  evaluar contra esas decisiones, sin imponer una arquitectura o stack distintos.
  Revisar validación, autorización, manejo de errores y cobertura donde correspondan.
  En interfaces de usuario, revisar estados de carga, vacío, error y éxito,
  accesibilidad y contratos con sus servicios.
- **Spec:** recorrer cada criterio de aceptación y relacionarlo con evidencia del diff,
  código o pruebas. Separar un incumplimiento demostrado de una ambigüedad de producto.
  No inventar requisitos que la historia no establece.

Priorizar errores observables y simplificaciones concretas que reduzcan complejidad
innecesaria. Una preferencia personal de estilo no es un bloqueo. No solicitar nuevas
abstracciones si el código existente resuelve el caso con claridad.

## Verificación

Usar checks existentes sólo si las instrucciones y permisos permiten sus efectos.
En repositorios de sólo lectura, no ejecutar tests, builds ni formateadores que
escriban en ellos. Como alternativa, consultar
resultados de CI, aclarando qué SHA verificaron. No afirmar que se reprodujo un error
cuando sólo se confirmó mediante lectura de código.

## Entrega

Responder en español bajo **Standards** y **Spec**, con hallazgos ordenados por impacto.
Por cada hallazgo incluir:

- **Bloqueante** cuando impide cumplir el contrato, rompe un flujo o viola una regla
  explícita relevante; **Sugerencia** para una mejora no necesaria para aceptar el PR.
- Archivo y rango mínimo de líneas, enlazado al diff del SHA revisado cuando sea posible.
- Condición que dispara el problema, consecuencia para el usuario y corrección esperada.
- Un comentario breve listo para copiar y una forma concreta de verificar la corrección.

Cerrar con cobertura revisada, verificaciones realizadas y límites. Si no hay hallazgos,
decirlo sin convertirlo en garantía de ausencia de bugs. No publicar comentarios,
aprobar ni mergear salvo pedido explícito. Si se pide publicar, comprobar primero que
el head siga siendo el revisado; ante cambios, revisar los hunks nuevos antes de enviar.

## Ejemplo de uso

**Pedido:** /revisar-pr https://github.com/<org>/<repo>/pull/<n>

**Resultado:** Devuelve hallazgos en español bajo Standards y Spec, ordenados por impacto, con archivo y líneas, si es bloqueante o sugerencia y un comentario listo para copiar; no publica nada sin pedido.
