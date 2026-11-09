# Rúbrica para estimar la nota de los devs — Zest

> ⚠️ Revisar entre los cuatro antes de usar el agente. Si cambian los pesos o las fórmulas,
> actualizar también las constantes al principio de `dev_grades.py`.

## Devs del equipo
Solo se evalúa a las personas de esta tabla. Se acepta el nombre, el usuario o el email de Multica.

| Dev | Usuario en Multica |
|---|---|
| Dev 1 | usuario-dev1 |
| Dev 2 | usuario-dev2 |

## Nota (1 a 10)
**Nota = 50% Cumplimiento + 50% Dificultad**, redondeada a medio punto.

### 1. Cumplimiento de los tickets (50%)
Se evalúan los tickets asignados al dev con **fecha de vencimiento dentro del período**:

| Situación | Cuenta como |
|---|---|
| Terminado a tiempo (cerrado hasta su vencimiento) | 1 |
| Terminado tarde | 0,5 |
| Vencido y sin terminar | 0 |
| En curso y todavía no vencido | No se evalúa |

**Puntaje = 10 × (suma de lo anterior ÷ tickets evaluados)**, con mínimo 1.

### 2. Dificultad de lo hecho (50%)
Cada ticket **terminado** en el período suma puntos según su dificultad:

| Nivel | Puntos | Cuándo |
|---|---|---|
| **Alta** | 3 | Varias capas (front + back + base de datos o integración externa), lógica compleja, tecnología nueva para el equipo, o mucha incertidumbre al empezar |
| **Media** | 2 | Una funcionalidad completa en una o dos capas, con algo de lógica o validaciones: un endpoint con su pantalla, un formulario con validación |
| **Baja** | 1 | Cambios acotados y conocidos: estilos, textos, un componente simple, un ajuste chico, un fix de una línea |

Se suman los puntos del dev y se comparan con el **promedio del equipo**:
**Puntaje = 8 + 5 × (puntos del dev ÷ promedio del equipo − 1)**, entre 1 y 10.

| Puntos frente al promedio | Puntaje |
|---|---|
| 140% o más | 10 |
| 100% (igual al promedio) | 8 |
| 60% | 6 |
| 20% | 4 |

## Qué no mide esta nota
Comunicación, asistencia, participación en clase y calidad del código en las revisiones. Se nombran en el informe para que los evalúe el equipo.
