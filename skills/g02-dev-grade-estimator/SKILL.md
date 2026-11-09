---
name: g02-dev-grade-estimator
description: Usar para estimar una nota orientativa de cada desarrollador de Zest según el cumplimiento de sus tickets en Multica y la dificultad de lo que terminó, con el desglose y acciones para mejorar.
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
  relacionados: []
---
# Estimador de nota para devs — Zest

## Objetivo
Calcular para cada dev una **nota orientativa** con la rúbrica de `rubrica.md`:
**50% cumplimiento de los tickets de Multica + 50% dificultad de lo terminado.**
Se informa con el desglose, los tickets que la respaldan y 2 o 3 acciones para mejorar. Es una herramienta de seguimiento para los líderes, no la nota oficial.

## Pasos

### 1. Definir el período
Por defecto, desde el inicio del sprint actual hasta hoy. Si el issue indica otro período ("todo el cuatrimestre", "sprint 2"), usar ese. El cuatrimestre empezó el 10/08/26.

### 2. Juntar datos
```bash
multica issue list --output json > issues.json
multica workspace member list --output json > members.json
python3 dev_grades.py issues.json --members members.json --desde <YYYY-MM-DD> --hasta <YYYY-MM-DD> \
  --solo "usuario-dev1,usuario-dev2,Dev 1,Dev 2"
```

### 3. Clasificar la dificultad (si hace falta)
Si el script termina con código **3**, devuelve la lista `sin_clasificar`: tickets terminados que todavía no tienen dificultad. Para cada uno:
1. Leer el ticket completo en Multica: descripción, criterios de aceptación, labels y comentarios (`multica issue get <id> --output json` y `multica issue comment list <id>`).
2. Asignar el nivel según la tabla de `rubrica.md`: **1 = Baja, 2 = Media, 3 = Alta**. Ante la duda entre dos niveles, elegir el más bajo y explicarlo.
3. Agregarlo al archivo de dificultad (`~/.config/zest/dificultad.json`; crearlo si no existe), **sin modificar los tickets ya clasificados**:
   ```json
   {"ZEST-12": {"nivel": 2, "motivo": "Endpoint + pantalla de edición con validaciones"}}
   ```

Después, volver a correr el script hasta que termine con código **0**.

Este archivo hace que un ticket mantenga siempre la misma dificultad entre una estimación y la siguiente. Si alguien del equipo pide corregir una clasificación, cambiarla ahí y aclararlo en el informe.

### 4. Informar
Comentar en el issue que pidió la estimación:
```bash
multica issue comment add <id-del-issue> --content-file notas.md
```
Una sección por dev, en orden alfabético:
```markdown
## Estimación de nota — <período>

### <Nombre> — **7,5** (orientativa)
| Criterio | Detalle | Puntaje | Peso |
|---|---|---|---|
| Cumplimiento | 6 a tiempo, 1 tarde (ZEST-41, 2 días), 1 vencido (ZEST-44) | 6,9 | 50% |
| Dificultad | 2 Alta, 3 Media, 1 Baja → 13 puntos (110% del promedio) | 8,5 | 50% |

**Tickets de mayor dificultad:** ZEST-30 (Alta: <motivo>), ZEST-33 (Alta: <motivo>)

**Para mejorar:**
- <acción concreta ligada al criterio más bajo, con un ticket de ejemplo>
- <otra acción>

---
_Nota orientativa calculada con los tickets de Multica según la rúbrica del equipo. No incluye comunicación, asistencia ni calidad del código. La fecha de cierre es aproximada (última modificación del ticket)._
```

## Reglas
- Basarse solo en los tickets: cada puntaje lleva sus tickets de respaldo.
- La dificultad se juzga por el alcance del trabajo, no por quién lo hizo ni por cuánto tardó.
- No hacer rankings ni comparar devs entre sí en el informe. La comparación con el promedio solo se usa para calcular el puntaje.
- No publicar las notas en el grupo de WhatsApp ni en lugares públicos: solo en el issue que lo pidió.
- Tono constructivo: acciones concretas y alcanzables.

## Ejemplo de uso
**Pedido:** Dame la nota orientativa de cada dev.
**Resultado:** Aplica una rúbrica sobre cumplimiento de tickets y dificultad y devuelve la nota con el desglose y acciones para mejorar.
