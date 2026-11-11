---
name: g14-benchmark-de-modelos-del-motor
description: Compara modelos y puertas de acceso (Gemini por AI Studio, por OpenRouter o por Vertex) para el juez de un motor con LLM, midiendo sobre el golden set nivel, latencia p50/p95, costo por corrida y validez del JSON, y opcionalmente el efecto de mandarle imágenes. Usala antes de cambiar el modelo, el proveedor o la entrada del motor (por ejemplo, sumar la foto de la donación). No construye la referencia ni optimiza prompts (eso es g14-eval-del-juez-contra-golden-set).
metadata:
  tipo: skill
  area:
  - ia
  - qa
  fase:
  - testing
  - diseno
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

# Benchmark de modelos del motor

La pregunta «¿qué modelo?» suele ser la menos importante. En VaiVen, cinco modelos fallaron exactamente los mismos dos pares del golden set; lo que decidía era **por qué puerta entra la llamada, con qué medio de pago y con qué crédito**. Este benchmark mide las tres cosas a la vez.

## Antes de medir

1. **Contá cuántas llamadas hace el caso de uso real** y ponelo contra el cupo del proveedor (una carga del golden set de VaiVen = 90 juicios; el free tier no alcanzaba).
2. **Probá el medio de pago contra el proveedor** antes de elegirlo: Google no aceptó tarjetas prepagas. Mirá también qué crédito ya hay y qué puerta lo consume (el crédito de prueba paga Vertex, no AI Studio).
3. Fijá el golden set y sus niveles **antes** (ver `g14-eval-del-juez-contra-golden-set`).

## Cómo se mide

- **Mismo prompt y mismo esquema que producción**, leídos del workflow en `origin/main` (en VaiVen, `matching-v2.json`: nodo `chainLlm` y `outputParserStructured`).
- **Formato como lo hace el orquestador**: instrucciones de formato dentro del prompt, igual que el Structured Output Parser de n8n. **No uses `response_format: json_schema` estricto con Gemini vía OpenRouter**: devolvió JSON relleno de espacios hasta el tope, 31/31 inválidos y cobrados.
- Temperatura 0, thinking apagado o con presupuesto explícito, concurrencia 4.
- Por modelo: válidos/total, nivel exacto, acuerdo en la línea del error caro, top 1 por caso, **p50 y p95** de latencia, costo (OpenRouter lo devuelve por llamada; en Vertex se reportan tokens de entrada/salida/pensamiento y el costo sale de facturación) y la versión de modelo que respondió.

```bash
SSL_CERT_FILE=/etc/ssl/cert.pem python3 medir.py google/gemini-3.1-flash-lite '{"reasoning":{"effort":"none"}}'
SSL_CERT_FILE=/etc/ssl/cert.pem python3 medir.py vertex:gemini-3.1-flash-lite '{"thinkingConfig":{"thinkingBudget":0}}'
```

Guardá la salida como `resultados-<fecha>[-<puerta>].json`. Ejemplo real (04–05/10, 31 pares): Gemini 3.1 Flash-Lite 26/31, p50 2,1 s, US$0,012 por corrida; Gemini 2.5 Flash 19/31; DeepSeek V4 Flash 22/31 con p50 5,1 s; Vertex 3.1 Flash-Lite igual que por OpenRouter.

## Variante: ¿mejora si ve la imagen?

Diseño fijado antes de la primera corrida, dos brazos:

| Brazo | Entrada |
|---|---|
| A | Prompt actual, solo texto |
| B | Mismo prompt + la foto como parte `inlineData` antes del texto + una instrucción mínima para usarla |

- 2 brazos × 2 sets × 3 corridas, misma concurrencia. Fotos con licencia libre, fijadas antes de correr, con URL, licencia y autor en un CSV.
- **Criterio de «B no empeora»**: en cada set, B pierde como mucho 1 par de acuerdo exacto (por moda) y ningún par cruza la línea del Malo solo en B.
- Reportá tokens extra por llamada, % de costo y latencia agregada.
- **Extra adversarial** (no cuenta para el criterio): pares donde la foto contradice el texto. B «detecta» si su moda baja y la narrativa nombra la discrepancia en 2 de 3 corridas.

Resultado real: B detectó 6/6 contradicciones pero **no pasó** (perdió 4 pares por set y provocó falsos positivos: la foto hace al juez indulgente con objetos de otra categoría), con +80 % de costo y +0,36 s.

## Gotchas verificados

- Los Gemini 3.x en Vertex responden solo en la región `global`; en otra región dan 404 como un modelo inexistente.
- En zsh, `$m:generateContent` rompe la URL (modificador de variable): usá `${m}:generateContent`.
- Un rechazo de «formato» con pocos tokens de salida es truncación: el thinking consume `maxOutputTokens`.

## Reglas

- Llamada directa no es el workflow: informalo. Precio de Vertex igual al de la Gemini API es un supuesto hasta verificarlo.
- Con ~31 pares un par mueve ~3 puntos: se sostiene el patrón, no la cifra.
- No toques el workflow de producción: el benchmark lee, no escribe. El cambio lo hace el dev con un ticket.

## Requisitos e instalación

- **Scripts:** `medir.py` (benchmark por OpenRouter o Vertex; esta es su única copia en el catálogo, la usa también `g14-eval-del-juez-contra-golden-set`), `correr-imagenes.py` y `analizar-imagenes.py` (variante con imagen). La variante con imagen reusa `correr.py` de **`g14-eval-del-juez-contra-golden-set`**: instalá las dos carpetas una al lado de la otra. Solo biblioteca estándar de Python 3 y `openssl` en el PATH.
- **Proveedores:** OpenRouter (`OPENROUTER_API_KEY` en un `.env` local) y Vertex AI (service account JSON en `~/.config/`, región `global`). Nunca en el código.
- **Entradas que no viajan** (son del proyecto): el golden set congelado (`golden-set-v1.md`, `golden-set-v1-planilla.md`, planilla y `niveles-v2.json` del set nuevo), el workflow del motor en un clon con `origin/main`, y para la variante con imagen `fotos/<caso>.jpg` con su CSV de URL, licencia y autor. Las rutas están fijadas con la disposición del repo de VaiVen al principio de cada script: ajustalas antes de correr.
- **Salidas:** el JSON de `medir.py` por consola (guardalo como se indica arriba) y `corridas/<brazo>-<set>-<n>.json`.

## Ejemplo de uso

**Pedido:** Compará Gemini 3.1 Flash-Lite por OpenRouter y por Vertex contra el golden set, y decime si conviene mandarle la foto de la donación al juez.

**Resultado:** Devuelve una tabla por modelo y puerta (exacto, línea del Malo, p50/p95, costo o tokens, válidos) y el veredicto del brazo con imagen contra el criterio fijado antes, con costo y latencia agregados y la lectura de los pares que cambian.
