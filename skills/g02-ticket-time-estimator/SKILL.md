---
name: g02-ticket-time-estimator
description: Usar cuando piden estimar cuánto va a durar un ticket de Zest. Estima en días hábiles, solo con el historial de tickets terminados en Multica, para cada persona del equipo y para el equipo en promedio.
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
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
  madurez: experimental
  relacionados:
  - g11-estimar-ticket
---
# Estimador de duración de tickets — Zest

## Objetivo
Te pasan un ticket (su ID, o te mencionan o asignan en él) y tenés que estimar **cuántos días hábiles va a durar**:
- **para cada persona del equipo**, y
- **para el equipo en promedio**.

Si piden una persona en particular ("¿cuánto tardaría Liz?"), destacarla primero. Si el ticket ya tiene asignado a alguien, destacar a esa persona.

**Fuente única: Multica.** La duración de un ticket terminado se calcula desde su fecha de inicio (o de creación, si no tiene) hasta su cierre. No modificar el ticket: solo comentar.

## Pasos

### 1. Leer el ticket a estimar
```bash
multica issue get <id> --output json
```
Mirar título, descripción, criterios de aceptación y labels: qué capas toca (front, back, base de datos, integración) y cuánta incertidumbre tiene. Si es demasiado ambiguo para comparar, decirlo y pedir lo que falta.

### 2. Traer el historial de Multica
```bash
multica issue list --output json > issues.json
multica workspace member list --output json > members.json
python3 durations.py issues.json            # tickets terminados y cuántos días hábiles tardaron
```
Con `members.json`, traducir cada `assignee_id` a su nombre.

### 3. Elegir tickets parecidos
Entre **3 y 6 tickets terminados** parecidos: mismas labels o capas, alcance comparable, títulos o descripciones similares.

### 4. Calcular
```bash
python3 durations.py issues.json --ids ZEST-12,ZEST-18,ZEST-21
```
Devuelve:
- `equipo`: la **mediana** de los tickets parecidos (la estimación del equipo) y su **rango probable**.
- `por_persona`: para cada persona, `estimacion_dias` = mediana del equipo × su **ritmo habitual** (`ritmo_vs_equipo`: 1,3 significa que suele tardar un 30% más que el promedio). Si la persona ya hizo tickets parecidos, también trae `mediana_parecidos_propios`.

Para cada persona, si tiene 2 o más tickets parecidos propios, usar su `mediana_parecidos_propios`; si no, usar `estimacion_dias`. Si una persona tiene menos de 3 tickets terminados en total, marcar su estimación como poco confiable.

Si el ticket tiene más incertidumbre o dependencias que las referencias, ajustar hacia arriba y explicarlo.

### 5. Comentar en el ticket
```bash
multica issue comment add <id-del-ticket> --content-file estimacion.md
```
Si te mencionaron desde un comentario, responder con `--parent <id-del-comentario>`.

Formato de `estimacion.md`:
```markdown
## ⏱️ Duración estimada

**Equipo (promedio): 3 días hábiles** — rango probable: 2 a 4

| Persona | Estimación | Base |
|---|---|---|
| <Persona> | 2,5 días | 3 tickets parecidos propios |
| <Persona> | 4 días | ritmo habitual × promedio del equipo |
| <Persona> | ~3 días ⚠️ | pocos tickets terminados: poco confiable |

**Si arranca el <DD/MM>, el equipo lo terminaría alrededor del <DD/MM>.**

**Por qué:** <2 o 3 líneas: capas, incertidumbre, dependencias>

**Tickets de referencia:** ZEST-12 (3 días), ZEST-18 (2 días), ZEST-21 (4 días)

_Estimación calculada con el historial de tickets terminados en Multica. El cierre se toma de la última modificación del ticket y, si no tenía fecha de inicio, de su creación._
```

## Reglas
- Usar solo datos de Multica y citar tickets reales del historial.
- Con menos de 3 tickets parecidos, avisar que la estimación es poco confiable.
- No ordenar a las personas de más rápida a más lenta ni hacer comentarios sobre su ritmo: mostrar la tabla en orden alfabético, salvo la persona destacada, que va primero.

## Ejemplo de uso
**Pedido:** ¿Cuánto va a tardar este ticket?
**Resultado:** Calcula días hábiles por persona y para el equipo con tickets terminados de Multica y deja la estimación comentada.
