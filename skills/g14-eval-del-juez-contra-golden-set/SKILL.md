---
name: g14-eval-del-juez-contra-golden-set
description: Construye y congela la referencia de un golden set y mide contra ella un juez LLM (por ejemplo, el que puntúa pares donación–necesidad de un motor de matching) contra un golden set cuyos niveles fijó antes un panel de tres modelos de otra familia (nivel final = mediana), con criterios de decisión escritos antes de correr. Usala cuando hay que defender un KPI de calidad del juez o decidir si un prompt nuevo mejora sin calibrarlo contra lo que ya vio. No elige modelo ni proveedor (eso es g14-benchmark-de-modelos-del-motor, de donde toma medir.py).
metadata:
  tipo: skill
  area:
  - qa
  - ia
  fase:
  - testing
  - revision
  tecnologias:
  - python
  - n8n
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - openrouter
  - vertex-ai
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

# Evaluar un juez LLM contra un golden set

El golden set es la única evidencia de que el juez funciona cuando el producto no tiene usuarios reales. Su validez depende de una sola propiedad: **los niveles de referencia se fijan antes de ver una corrida del juez y no se tocan después.**

## 1. Armar el set

- **Unidad = caso**: un ítem de un lado (una donación) con 5 o 6 candidatos del otro (necesidades). El KPI habla de «los tres primeros», y eso solo existe dentro de un grupo.
- **Tres familias, las tres necesarias**: obvios que sí (el sistema no está roto), obvios que no (no dice que sí a todo) y **difíciles**, donde está todo el valor: semántica sin palabras compartidas, misma categoría con otro uso, resuelve parte, roto, talle, tamaño, pieza faltante.
- Textos ficticios pero que suenen reales: cortados, con faltas, con el dato clave al final. Un pool prolijo no prueba nada.
- La IA puede redactar publicaciones y formar los casos, **con edición humana**. Proporción buscada antes del juicio: ~40 % en niveles altos, ~25 % medio, ~35 % «Malo».

## 2. Escala: la misma del prompt del juez

Usá **las anclas textuales del prompt** (en VaiVen, 0 a 4: sin relación · categoría vecina · resuelve parte · resuelve con salvedad menor · resuelve lo pedido). Así comparar set y juez es una resta. Definí la línea del error caro (VaiVen: **Malo = nivel ≤ 1**).

El panel ve **lo mismo que el juez** (título, descripción, categoría, cantidad, estado), nada de lo que la fórmula determinística agrega después (zona, urgencia): si no, mezclás distancia con juicio.

## 3. Panel y congelamiento

1. Tres modelos de **familias distintas a la del juez** (VaiVen: GLM-5.3, DeepSeek V4 Pro y Kimi K3 por OpenRouter; ningún Gemini), temperatura 0, una llamada por modelo y caso, con la planilla y las anclas.
2. Validá cada respuesta (ids completos, niveles en rango); reintentá hasta 3 veces.
3. **Nivel final = mediana.** Guardá columnas individuales, top 1 de cada modelo y marcá ⚠ los pares donde el panel no coincide de qué lado de la línea del Malo cae.
4. Congelá (`niveles-*.json`, anotá su hash) **antes** de la primera corrida del juez. Si vas a probar un prompt alternativo, escribilo y hasheálo también antes de ver al panel.
5. Informá el número como «coincidencia del juez con un panel de modelos», no como juicio humano.

## 4. Correr el juez

- Mismo camino que producción: el prompt se lee del workflow en `origin/main` en cada corrida, misma entrada, mismo formato de salida (en n8n, las instrucciones del Structured Output Parser dentro del prompt).
- **Tres corridas por combinación** (prompt × set). Si una llamada falla (429), repetí la corrida entera.
- Comparación por **moda de las tres corridas** contra la referencia. Métricas: nivel exacto, acuerdo en la línea del Malo, pares inestables (los que saltan la línea entre corridas, se reportan aparte).

## 5. Criterios de decisión, escritos antes de correr

Ejemplo real (spike v2 de VaiVen):

1. Prompt actual ≥ 90 % exacto en el set nuevo → no se toca.
2. Actual < 90 % y el alternativo gana ≥ 2 pares **sin perder ninguno en el set anterior** → se propone.
3. El alternativo pierde en el set anterior → no se propone; el set nuevo queda como hallazgo.

Resultado: actual 71 %, alternativo 77 % pero perdía un par del v1 → criterio 3. **No se recalibró el prompt contra el mismo set**: hacerlo es medir contra lo que ya se vio; una regla nueva se prueba con casos nuevos.

## Reglas

- Nunca uses pares del set como ejemplos en el prompt del juez.
- Informá el tamaño junto al número: con 31–35 pares, un par mueve ~3 puntos; 71 % y 77 % no se distinguen. Lo que se sostiene es el patrón por tipo de trampa.
- Declará el sesgo de diseño (quien escribió los casos conocía las trampas).
- Lista de desajustes para el dev: pares que cruzan la línea del Malo o difieren en ≥ 2 niveles, con nivel de referencia, del juez, criterio y justificación del modelo.

## Salida

Tabla por combinación (prompt, set, exacto, línea del Malo, pares que fallan `ref→juez`), pares ganados/perdidos entre prompts, veredicto contra los criterios fijados y sección «lo que esto no prueba».

## Requisitos e instalación

- **Scripts:** `correr.py` (panel por OpenRouter y corridas del juez) y `analizar.py` (exacto, línea del Malo, moda, ganados/perdidos), del spike v2 de VaiVen. `correr.py` carga `medir.py` desde la pieza **`g14-benchmark-de-modelos-del-motor`**: instalá las dos carpetas una al lado de la otra. Solo biblioteca estándar de Python 3 y `openssl` en el PATH.
- **Proveedores:** OpenRouter (panel; `OPENROUTER_API_KEY` en un `.env` local) y Vertex AI (juez; service account JSON en `~/.config/`, región `global`). Nada de eso va en el código.
- **Entradas que no viajan** (son del proyecto; armá las tuyas con el procedimiento de arriba): `planilla.md` del set nuevo y `prompt-mejorado.txt` en esta carpeta; `golden-set-v1.md` y `golden-set-v1-planilla.md` del set anterior; el workflow del motor en un clon con `origin/main`. Las rutas a esas entradas están fijadas en `medir.py` y `correr.py` con la disposición del repo de VaiVen: ajustalas antes de correr.
- **Salidas:** `panel.json`, `niveles-v2.json` (el congelado) y `corrida-<prompt>-<set>-<n>.json`.

## Ejemplo de uso

**Pedido:** Armá un set de 35 pares difíciles (roto, talle, tamaño, pieza faltante) y decime si el prompt nuevo del juez es mejor que el actual.

**Resultado:** Fija los niveles con el panel de tres modelos y los congela, corre 3 veces cada prompt en el set nuevo y en el anterior, y devuelve la tabla de acuerdo exacto por moda con el veredicto según los criterios escritos antes: en VaiVen, 71 % contra 77 %, con el alternativo descartado por perder un par en el set anterior.
