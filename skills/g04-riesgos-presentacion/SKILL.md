---
name: g04-riesgos-presentacion
description: 'Prepara la lámina de riesgos e incidentes de PitStop a partir de risks.yaml: matriz de probabilidad e impacto, principales riesgos, planes e incidentes ocurridos. Usar al presentar o reportar el estado de los riesgos del proyecto.'
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
  requiere: []
  grupo: "04"
  autor:
    nombre: Tomás Serra
    github: TomasSerra
  responsables:
  - TomasSerra
  madurez: experimental
  relacionados: []
---

# Riesgos para presentación

Resume el registro de riesgos en algo que se entienda en un minuto. Fuentes en `pitstop-management/project-plan/`.

## Flujo

1. Leer `risks.yaml` y separar riesgos abiertos, cerrados e incidentes.
2. Calcular la exposición de cada abierto: `probability` × `impact`. Si `notes` trae un VME, mostrarlo tal cual.
3. Armar la matriz de probabilidad contra impacto, con el `id` corto de cada riesgo.
4. Elegir los tres de mayor exposición. Por cada uno: qué podría pasar, responsable (`owner_id`, resuelto con `team.yaml`), mitigación y contingencia.
5. Incidentes: qué pasó, efecto en el cronograma y cómo se resolvió. Cruzar con los desvíos de `g04-earned-value-presentacion`.
6. Controlar y avisar: riesgos con `review_date` vencida y sin cambios. Esto se reporta; no se cambia la fecha para disimularlo.

## Salida

Mensaje de la lámina en una frase, matriz, tabla de los tres principales, incidentes y una lista de riesgos que necesitan revisión.

## Reglas

- No cambiar `risks.yaml` para que la lámina se vea mejor. Si hay que actualizarlo, proponerlo aparte.
- No inventar probabilidades, impactos ni montos.

## Ejemplo de uso
**Pedido:** Preparame los riesgos para la presentación.

**Resultado:** La matriz de riesgos abiertos, los tres principales con responsable y plan, los incidentes ocurridos, los riesgos sin revisar y el mensaje de la lámina.
