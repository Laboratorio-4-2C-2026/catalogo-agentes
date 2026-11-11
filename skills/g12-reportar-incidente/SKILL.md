---
name: g12-reportar-incidente
description: Convierte el relato de un incidente en un registro factual con impacto, estado, criticidad, fechas y resolución. Adapta el formato al proyecto; no diagnostica ni corrige la falla. Usar cuando una falla ya ocurrió y hay que dejarla registrada en el log de incidentes.
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - mantenimiento
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
  - g12-registrar-riesgo
  - g11-triage-incidente
  - g03-status-incidents
---

# Reportar incidente

Convertir el relato recibido en un registro breve y listo para revisar.
Invocar como `/reportar-incidente <descripción del incidente>`.

## Convenciones y evidencia

Usar la plantilla, estados, escala de severidad y SLA del proyecto cuando estén disponibles.
Resolverlos desde el material aportado o la documentación accesible; no exigir una
herramienta específica. Si no existen, usar el formato y los criterios de respaldo de abajo,
indicándolos como provisionales.

Separar hechos observados, hipótesis y resolución. No diagnosticar causas ni inventar
impacto, acciones o resultados. Registrar entorno y alcance afectados cuando se conozcan,
sin incluir credenciales ni datos personales innecesarios.

## Criterios de respaldo

- **Descripción:** qué ocurrió, a quién o qué afectó y qué impacto se observó. Una hipótesis
  de causa se identifica como tal, separada de los hechos.
- **Estado:** `Cerrado` sólo si se informa una resolución y una validación del funcionamiento;
  de lo contrario, `Abierto`. Si el proyecto distingue mitigado, monitoreo o resuelto,
  respetar sus definiciones.
- **Criticidad provisional:** `Alta` si bloquea un flujo esencial, compromete datos o impide
  operar; `Media` si degrada o bloquea parcialmente un flujo con alternativa; `Baja` si el
  impacto es menor. Usar `Por definir` cuando no alcance la evidencia. El número de personas
  afectadas aporta contexto, pero por sí solo no determina la severidad.
- **Fechas:** distinguir ocurrencia, registro y cierre. Usar fecha de registro actual si se
  pide registrar hoy; dejar ocurrencia desconocida sin completar. No usar hoy como fecha
  del incidente por falta de información. Aplicar formato y zona del proyecto; en su
  ausencia, ISO 8601 y zona explícita cuando haya horas.
- **Límite:** completar sólo con plazo acordado o SLA aplicable cuya base esté documentada.
- **Resolución:** acción realizada y evidencia de validación. Una mitigación temporal se
  identifica como tal; no se transforma en una corrección definitiva.
- **Responsable:** usar el informado o `Por asignar`, sin atribuirlo al autor de la skill.

## Salida

Usar la plantilla existente. En ausencia de una, entregar:

| Descripción e impacto | Estado | Criticidad | Ocurrencia | Registro | Límite | Cierre | Responsable | Resolución y evidencia |
|---|---|---|---|---|---|---|---|---|

Completar una fila por incidente, dejando visibles los datos no informados. Debajo,
señalar contradicciones o datos necesarios para clasificarlo. Entregar un borrador útil
antes de pedir información adicional.

La skill prepara el registro. Escribir en un tracker, enviar alertas o comunicar el
incidente a otras personas requiere que esas acciones estén incluidas en el pedido.

## Ejemplo de uso

**Pedido:** /reportar-incidente ayer a la tarde el login con Google dejó de andar en producción durante dos horas

**Resultado:** Devuelve una fila de incidente con descripción e impacto, estado, criticidad provisional y fechas, separando hechos de hipótesis y dejando visibles los datos no informados.
