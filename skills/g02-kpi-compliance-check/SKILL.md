---
name: g02-kpi-compliance-check
description: Usar para chequear a diario en el panel público de Lab4 KPIs si el Equipo 2 (Zest) reportó el día COMPLETO, y crear un issue con los suscriptores del autopilot solo cuando no lo está.
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - revision
  tecnologias:
  - python
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - multica
  grupo: '02'
  autor:
    nombre: Ines Gassiebayle
    github: inesgassiebayle
  responsables:
  - inesgassiebayle
  madurez: probado
  relacionados:
  - g11-explicar-kpi
  - g02-kpi-compliance-checker
---
# Chequeo diario de cumplimiento de KPIs — Zest (Equipo 2)

## Objetivo
Verificar que la fila **2. Zest** del [panel de cumplimiento](https://lab4-kpis.github.io/kpis/#/cumplimiento) esté en **Completo** para el último día evaluado. **Si está completo, no se hace nada**: no hay issue ni comentario. Si no lo está, se crea un issue y se suscribe a las personas configuradas en el autopilot.

Un día es Completo cuando llegan, en `prod`, todos los KPIs activos del catálogo (entre 5 y 10). Cuenta la **fecha de recepción**, no la fecha declarada.

## Pasos

### 1. Chequear
```bash
python3 check_kpis.py
```
El script imprime un JSON y termina con un código:

| Código | Significa | Qué hacer |
|---|---|---|
| `0` | COMPLETO | **Terminar sin hacer nada.** No crear issue ni comentar. |
| `1` | INCOMPLETO o SIN REPORTE | Seguir con el paso 2. |
| `2` | No se pudo chequear (red, sitio caído, sin datos) | No crear issue. Terminar la ejecución informando el error del JSON. |

### 2. Evitar duplicados
```bash
multica issue list --output json --fields id,title,status
```
Si ya existe un issue con el título `KPIs incompletos — Zest — <fecha>` para la misma fecha, **terminar sin crear otro**.

### 3. Crear el issue
Escribir `issue.md` en el directorio actual con esta plantilla (fecha en formato DD/MM/AA):

```markdown
El panel de cumplimiento de Lab4 KPIs muestra a **Zest (Equipo 2)** en **<status_label>** el **<fecha>**: llegaron **<valid_kpis> de <expected_kpis>** KPIs.

**KPIs que no llegaron:** <missing_kpis, si el JSON los trae; si no, "ver el detalle en Mi equipo con la PROJECT_KEY">

Panel: https://lab4-kpis.github.io/kpis/#/cumplimiento

### Qué revisar
- [ ] Que el reporter haya corrido ese día en producción (logs del job o cron).
- [ ] Que el backend no se haya desplegado o reiniciado justo antes del envío.
- [ ] Que el reporte use la clave **prod** (dev y qa no cuentan).
- [ ] Que el envío de hoy salga completo.

> Ese día ya no se puede corregir, porque cuenta la fecha de recepción. Lo importante es que no se repita.
```

Después crearlo:
```bash
multica issue create --title "KPIs incompletos — Zest — <fecha>" --description-file issue.md --output json
```
Guardar el `id` del issue creado.

### 4. Suscribir a las personas del autopilot
El autopilot corre en modo *Run only*, así que Multica no suscribe a nadie automáticamente: hay que copiar sus suscriptores al issue.
```bash
multica autopilot get "$MULTICA_AUTOPILOT_ID" --output json
```
Para cada elemento de `subscribers`, ejecutar:
```bash
multica issue subscriber add <id-del-issue> --user-id <user_id>
```
Si `MULTICA_AUTOPILOT_ID` está vacío (corrida manual), suscribir solo a quien pidió la ejecución y decirlo en la respuesta.

## Reglas
- Crear el issue **solo** cuando el código de salida es `1`.
- No modificar el código ni el reporter: solo avisar.
- No crear más de un issue por fecha.
- No mostrar claves (`LAB4_PROJECT_KEY`) en el issue ni en los logs.

## Ejemplo de uso
**Pedido:** ¿Zest reportó hoy en el panel de KPIs?
**Resultado:** Corre el chequeo diario contra el panel público de Lab4 KPIs y define cuándo crear el issue y a quién suscribir, según el código de salida.
