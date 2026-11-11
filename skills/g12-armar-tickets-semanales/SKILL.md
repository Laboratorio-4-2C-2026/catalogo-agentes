---
name: g12-armar-tickets-semanales
description: Planifica y redacta tickets semanales según las prioridades, capacidad real, especialidades y convenciones de un equipo. Usar al elegir alcance, estimar, dividir o cargar trabajo; no para implementarlo.
owner: '@husseymarcos'
role: pm
created: '2026-09-08'
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - codex
  - otra
  requiere: []
  grupo: '12'
  autor:
    nombre: Marcos Hussey
    github: husseymarcos
  responsables:
  - husseymarcos
  madurez: usado-en-proyecto
  relacionados:
  - g12-orientar-sprint
  - g12-asignar-capacidad-sobrante
---

# Armar tickets semanales

Convertir las prioridades del período en incrementos realizables y verificables.
Ejemplo: `/armar-tickets-semanales próxima semana, priorizar el flujo de alta`.

## Contexto de planificación

Consultar el roadmap o backlog que el equipo use como autoridad, sus criterios de
aceptación, decisiones, trabajo en curso, PRs y dependencias. Usar las herramientas y
documentos disponibles; no exigir un tracker, prefijo de issues ni estructura de carpetas.

Determinar período, fecha de entrega, personas disponibles, especialidades, capacidad y
unidad de estimación. Descontar ausencias, soporte, reuniones y trabajo arrastrado que
consuman esa capacidad. Usar valores confirmados: no asumir horas por persona, cantidad
de developers, perfiles full-stack ni una equivalencia entre puntos y horas.

Si falta capacidad o prioridad, avanzar con un desglose provisional y preguntar por lo
que impide comprometer alcance. Un resultado provisional no es un compromiso del equipo.
Ante fuentes contradictorias, señalar la diferencia y seguir la decisión vigente.

## Reparto y alcance

- Planificar dentro de la capacidad neta de cada persona, incluyendo pruebas, integración,
  documentación necesaria y revisión. Reservar correcciones según trabajo pendiente y
  datos históricos; no fijar una reserva universal.
- Preferir incrementos que produzcan un recorrido observable. Agrupar trabajo relacionado
  cuando separarlo sólo agregue coordinación; dividir cuando reduzca tamaño o dependencia.
- Repartir según especialidades y disponibilidad reales. Si se separan capas o servicios,
  explicitar contrato, orden de integración y responsables. Si se reparte por feature,
  comprobar que quien la toma tenga acceso y capacidad para entregarla.
- Usar las convenciones del equipo para responsable, branch, PR y asignaciones. No imponer
  una PR por ticket si el repositorio tiene otro flujo documentado.
- Explicitar dependencias de API, datos, diseños y terceros. Mocks o contratos temporales
  sólo son una alternativa si el equipo los admite; incluir su validación e integración.
- Recortar extras antes que validación, autorización, manejo de errores, accesibilidad
  básica o pruebas esenciales. Si una historia no entra, nombrar el incremento y dejar
  visibles los criterios pendientes.
- Mostrar el impacto del trabajo arrastrado sobre el plan. No sustituir prioridades ni
  desplazar entregas comprometidas sin explicitar la decisión necesaria.

## Redacción

Adaptar cada ticket al formato del equipo. Elegir el nivel de detalle según el pedido y
la incertidumbre; si importa y no está definido, presentar la opción recomendada:

- **Detallado:** resultado, alcance y referencias a patrones existentes cuando la solución
  ya está acordada. Comprobar archivos y contratos antes de citarlos.
- **Diseño abierto:** resultado, restricciones, criterios de decisión y evidencia esperada;
  reservar tiempo para explorar opciones sin imponer una implementación prematura.

Estimar con la unidad y técnica del equipo, explicitando supuestos e incertidumbre.
El diseño abierto incluye exploración; no aplicar un multiplicador fijo. Si se requieren
horas para capacidad pero las estimaciones están en puntos, pedir una base de planificación
compatible en vez de inventar una conversión.

Cada ticket incluye objetivo, resultado observable, criterios de aceptación, alcance y
exclusiones, dependencias, estimación y verificaciones necesarias. Enlazar diseños y
documentación que sus destinatarios puedan consultar; mantener referencias restringidas
en el resumen interno cuando la política del proyecto lo requiera.

## Entrega y carga

Presentar una tabla con responsable propuesto, ticket, estimación, resultado y dependencias,
más el total por persona y la capacidad remanente. Mostrar el flujo que quedará funcionando,
supuestos, riesgos y alcance que no entra.

Crear o actualizar tickets sólo si el pedido lo incluye. Antes de escribir, revisar posibles
duplicados y el contenido actual; preservar campos ajenos al cambio. Asignar personas,
ciclos y vencimientos sólo dentro del alcance autorizado y según los acuerdos existentes.
Después, releer lo guardado y devolver enlaces y cambios aplicados. Si falta acceso o el
destino es de sólo lectura, entregar los tickets listos para copiar y señalar lo pendiente.

## Ejemplo de uso

**Pedido:** /armar-tickets-semanales próxima semana, priorizar el flujo de alta

**Resultado:** Propone una tabla de tickets con responsable, estimación, resultado y dependencias, el total por persona contra su capacidad y lo que queda afuera; los carga en el tracker solo si se le pide.
