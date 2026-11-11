---
name: g12-auditar-kpis-reportados
description: Revisa qué métricas o KPIs llegaron de verdad a su destino (plataforma, dashboard, base) en un rango de días y devuelve los huecos — días sin dato, KPIs faltantes, valores fuera de rango, ambiente equivocado, diferencias entre lo calculado y lo enviado — con causa probable y si corresponde abrir incidente. Usar antes de una entrega o reunión de seguimiento, o cuando se sospecha un día incompleto; no reenvía nada.
owner: '@lucasmonteverdi1'
role: pm
created: '2026-11-09'
metadata:
  tipo: skill
  area:
  - gestion
  - datos
  fase:
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  - codex
  requiere: []
  grupo: '12'
  autor:
    nombre: Lucas Monteverdi
    github: lucasmonteverdi1
  responsables:
  - lucasmonteverdi1
  madurez: usado-en-proyecto
  relacionados:
  - g12-reportar-incidente
  - g04-chequeo-de-kpis
---

# Auditar los KPIs reportados

## Para qué

Un KPI que se reporta todos los días se rompe en silencio: un deploy que reinicia el proceso,
una credencial vencida, un job que no corrió. Si el destino no deja corregir el pasado, el
hueco queda para siempre. Mirar seguido es lo único que achica el daño.

## Entrada

Rango de fechas (default: los últimos 7 días) y ambiente (default: producción).

## Descubrir las fuentes

Buscar en el repo y su documentación (ADRs, README, código del exportador o del job):

- **Qué se esperaba:** la lista de KPIs, su unidad, rango válido y frecuencia, y en qué zona
  horaria se define "el día".
- **Qué se calculó:** dónde guarda el sistema sus propias corridas (tabla, endpoint, logs).
- **Qué se envió:** el destino final y cómo consultarlo.
- **Si el destino permite corregir:** si conserva el primer valor o el último, o si reenviar
  duplica.

Consultar con las credenciales que el usuario ya tenga configuradas; nunca pedirlas en el
chat ni escribirlas en archivos. Si no queda claro cuál es la fuente de verdad, preguntar.

## Checks por día

1. **¿Hubo dato?** Día sin ningún registro en el destino → hueco.
2. **¿Están todos los KPIs?** Si falta uno, mirar lo calculado: si allí también está vacío por
   diseño (sin actividad, sin muestras), es esperado; si tiene valor, se perdió en el envío.
3. **¿El valor tiene sentido?** Porcentajes entre 0 y 100, fracciones entre 0 y 1, health
   checks en sus valores posibles, timestamps dentro del día. Un salto de un orden de magnitud
   se marca aunque esté "bien enviado".
4. **¿Ambiente correcto?** Datos de desarrollo o staging donde debería haber producción, o al
   revés.
5. **Calculado vs enviado.** Si difieren, gana lo enviado (es lo que ve quien consume el
   reporte); se anota la diferencia.

Cruzar cada hueco contra el historial de deploys, reinicios e incidentes: un hueco el mismo
día que un deploy suele ser estado en memoria perdido.

## Salida

```
KPIs <ambiente> del <desde> al <hasta>: N de M días completos

| Día | Faltan | Fuera de rango | Causa probable | ¿Incidente? |
```

Solo filas con algo que decir. Al final: para cada hueco nuevo que no esté en el registro de
incidentes del proyecto, un borrador de incidente (qué pasó, impacto, fecha, si es
corregible). Si el patrón se repite (mismos KPIs, mismo horario), decirlo en una línea.

## Qué no hace

No reenvía ni corrige mediciones, no toca la configuración del envío. Si no tiene acceso a una
fuente, lo dice y audita con las otras.

## Ejemplo de uso

**Pedido:** Revisá si los KPIs de producción de los últimos 7 días llegaron completos a la plataforma.

**Resultado:** Devuelve cuántos días quedaron completos y una tabla con los días con faltantes o valores fuera de rango, su causa probable y un borrador de incidente para cada hueco nuevo; no reenvía nada.
