---
name: g14-diagnostico-de-incidente
description: Lleva un incidente del síntoma a la causa raíz verificada (bot que falla, nodo de LLM que rechaza formato, proveedor que bloquea al motor) separando lo observado de lo supuesto, y deja el aprendizaje en una entrada de bitácora con «Qué pasó / Por qué pasó / Qué hacemos ahora». Usala cuando algo falla lejos de su causa o cuando la explicación obvia todavía no se comprobó.
metadata:
  tipo: skill
  area:
  - qa
  - devops
  - documentacion
  fase:
  - mantenimiento
  - testing
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: "14"
  autor:
    nombre: Martina de Jesus
    github: mardejesus
  colaboradores: []
  responsables:
  - mardejesus
  madurez: probado
  relacionados: []
---

# Diagnóstico de incidente

Los incidentes caros de VaiVen tuvieron algo en común: **el error apareció lejos de su causa** y la primera explicación era la obvia y falsa. «El schema está mal» era truncación por tokens de razonamiento; «el modelo razona mal» era el texto del ticket llegando sin saltos de línea; «la migración de la API rompió Jira» era una clave truncada en otro `.env`; «necesitamos otro modelo» era un medio de pago rechazado.

## Pasos

1. **Escribí el síntoma literal**: mensaje de error, dónde aparece, desde cuándo, con qué frecuencia (3 de 5, 31 de 31). Sin interpretar.
2. **Listá las hipótesis**, incluida la obvia, y para cada una **la observación que la descartaría**. La obvia no se acepta sin esa prueba.
3. **Mirá la entrada real, no la configuración declarada.** Leé el prompt que efectivamente recibe el modelo, el payload que llega al nodo, el valor que gana entre dos `.env` (longitud de la clave, orden de carga). Dry-run antes que razonamiento.
4. **Buscá el número que no cierra** al costado del error: tokens de salida imposibles para la respuesta (80 tokens con un JSON largo = truncación), longitudes que difieren en un carácter, una cifra de consumo que nadie midió.
5. **Aislá con una prueba mínima y discriminante**: el mismo endpoint con una y otra credencial (`/myself` → 401 vs. 200), el mismo prompt con otro `maxOutputTokens`, el mismo modelo por otra puerta o región. Una variable por vez.
6. **Contrastá las cifras heredadas** (de la memoria de sesión, de un ADR, de un chat) contra su fuente antes de repetirlas: una proyección no es un consumo.
7. **Declará la causa raíz solo con la prueba que la confirma** en esta sesión. Si quedan dudas, van como `[por-verificar]` con el comando que las cerraría.
8. **Arreglá en el lugar donde pasan todos los caminos**, no en el síntoma. Si el arreglo es código de producto, se entrega como ticket o propuesta al dev; dirección no lo escribe.

## Entrada de bitácora

Un archivo por aprendizaje: `docs/bitacora/AAAA-MM-DD-<la-lección-en-una-frase>.md`. El título es la lección, no el incidente («El nodo de LLM falla lejos de su causa», no «Error en n8n»).

```markdown
# <Lección en una frase>

**DD/MM/AAAA · sesión N**

## Qué pasó
Síntoma, hipótesis descartadas y causa, con las cifras que lo probaron.

## Por qué pasó
La causa de fondo: qué no se miró o qué se dio por supuesto.

## Qué hacemos ahora
Reglas operativas en presente, verificables, que evitan repetirlo. Si afecta a otra pieza (bot, motor, kit), se nombra.
```

Agregala al índice de documentos y, si cambia una decisión, propagala al documento que la contiene.

## Reglas

- No publicar resultados parciales de un sistema que falló: si el modelo no respondió, el bot no comenta nada (un comentario de error ocultaría el PR al cron de respaldo).
- Una bitácora no repite el incidente completo de otro documento: lo enlaza.
- Sin secretos en la bitácora: se informa la longitud o el último carácter de una clave, nunca la clave.

Evidencia en VaiVen: `docs/bitacora/2026-08-10-el-nodo-de-llm-falla-lejos-de-su-causa.md`, `2026-09-23-el-bot-fallaba-por-cosas-que-no-eran-el-modelo.md` y `2026-10-04-el-cuello-del-modelo-era-el-medio-de-pago.md`.

## Ejemplo de uso

**Pedido:** El Structured Output Parser de n8n rechaza 3 de cada 5 respuestas del modelo por formato; encontrá por qué.

**Resultado:** Descarta el schema mirando el texto crudo y el conteo de tokens de salida, identifica la truncación porque el razonamiento consume `maxOutputTokens`, lo confirma subiendo el tope (5 de 5) y deja la entrada de bitácora con la regla para dimensionar ese parámetro.
