---
name: g02-branch-cleanup
description: 'Usar una vez por semana para listar las branches del repo de Zest (mergeadas, abandonadas y activas) en la planilla de limpieza de branches. Solo reporta: nunca borra branches ni hace push.'
metadata:
  tipo: skill
  area:
  - devops
  fase:
  - mantenimiento
  tecnologias:
  - git
  - python
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  - google-sheets
  grupo: '02'
  autor:
    nombre: Ines Gassiebayle
    github: inesgassiebayle
  responsables:
  - inesgassiebayle
  madurez: experimental
  relacionados:
  - g13-validar-branch
---
# Limpieza de branches — Zest

## Objetivo
Cada semana, actualizar la planilla [Zest — Limpieza de branches](https://docs.google.com/spreadsheets/d/1auaI7xH8hF4QNlxotKb28uYayFI7ColpcZATPMm7OTo) con todas las branches remotas de `proyecto-zest/zest`, clasificadas en:

| Estado | Significa | Recomendación |
|---|---|---|
| **Mergeada** | Todos sus commits están en `main`, o su PR figura como mergeado | Se puede borrar |
| **Abandonada** | Tiene commits fuera de `main` y 14 días o más sin actividad | Preguntar al autor |
| **Activa** | Tuvo commits en los últimos 14 días | Seguir |

Siempre se edita **esa misma planilla**: no crear planillas nuevas.

## Pasos

### 1. Tener el repo actualizado
El clon de trabajo vive en `~/zest-agentes/zest`. Si no existe, clonarlo:
```bash
mkdir -p ~/zest-agentes && git clone https://github.com/proyecto-zest/zest ~/zest-agentes/zest
```
No hace falta hacer checkout de ninguna branch: el script trae las referencias remotas con `git fetch --prune`.

### 2. Probar sin escribir
```bash
python3 branch_report.py --repo ~/zest-agentes/zest --dry-run
```
Revisar que el resumen tenga sentido (total de branches, cuántas mergeadas, abandonadas y activas).

### 3. Actualizar la planilla
```bash
python3 branch_report.py --repo ~/zest-agentes/zest
```
Reescribe la pestaña **Branches** y agrega una fila en **Historial** con los totales y cuántas branches se borraron desde la semana anterior.

### 4. Informar
Terminar con un resumen corto, por ejemplo:
> Planilla actualizada: 69 branches. 55 mergeadas (se pueden borrar), 3 abandonadas (ZEST-80, ZEST-95, ZEST-101) y 11 activas.

Si la corrida creó un issue (modo *Create issue*), comentar ese resumen en el issue con el link a la planilla.

## Reglas
- **Nunca borrar branches** ni hacer push: solo listar.
- No modificar las pestañas "Cómo leerla" ni el formato de la planilla.
- Si el script falla por permisos de Google (403), avisar que hay que compartir la planilla con la cuenta de servicio como Editor.
- El estado de los PRs sale de `gh`. Si `gh` no está logueado, la columna "Estado del PR" dice "(sin datos de PRs)" y las branches con squash merge pueden figurar como Abandonadas: mencionarlo en el resumen.

## Ejemplo de uso
**Pedido:** Actualizá la planilla de branches.
**Resultado:** Genera el reporte de branches mergeadas, abandonadas y activas con branch_report.py y actualiza la planilla, sin borrar nada.
