#!/usr/bin/env bash
#
# Junta los hallazgos [Crítico] y [Alto] que dejaron nuestros revisores en un PR
# mergeado y, para cada uno, las señales de si alguien lo atendió: si el hilo se
# resolvió, quién contestó y cómo cambió ese archivo después del comentario.
#
# Mismo principio que blockers-facts.sh: qué hallazgos existen y qué pasó con
# ellos lo mide este script. El agente solo lee los diffs y decide si el cambio
# responde al hallazgo; no puede sumar ni sacar hallazgos.
#
# Uso: hallazgos-facts.sh <owner/repo> <número de PR>
# Escribe hallazgos.json y, por cada hallazgo cuyo archivo cambió después del
# comentario, seguimiento/<id>.diff.
set -euo pipefail

REPO="${1:?falta owner/repo}"
PR="${2:?falta el número de PR}"
[[ "$PR" =~ ^[0-9]+$ ]] || { echo "el número de PR tiene que ser un entero: $PR" >&2; exit 1; }
OWNER="${REPO%/*}"
NOMBRE="${REPO#*/}"

# Topes en bytes. Un archivo reescrito entero no entra en contexto, y tampoco
# hace falta entero para ver si se tocó lo que señalaba el hallazgo.
TOPE_DIFF=20000
# El diff completo después del comentario hace falta porque el arreglo no
# siempre está en el archivo del hallazgo: en la PR #33 el [Alto] sobre la ruta
# de release se arregló con una guarda en SQL y en el servicio, y la ruta quedó
# igual.
TOPE_DIFF_COMPLETO=80000

# Lo intermedio va a archivos y no a argumentos de jq: Linux corta un argumento
# en 128 KB, y un PR con muchos hilos o una comparación grande lo pasan.
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir -p seguimiento

# --- El PR y sus hilos de review ----------------------------------------------
# GraphQL y no REST porque solo GraphQL dice si un hilo se marcó como resuelto.
# Un hallazgo es el primer comentario de un hilo, escrito por un bot, que abre
# con [Crítico] o [Alto]; el resto del hilo son sus respuestas.
gh api graphql -F owner="$OWNER" -F nombre="$NOMBRE" -F pr="$PR" -f query='
  query($owner: String!, $nombre: String!, $pr: Int!) {
    repository(owner: $owner, name: $nombre) {
      pullRequest(number: $pr) {
        number title url mergedAt headRefOid
        author { login }
        reviewThreads(first: 100) {
          nodes {
            isResolved isOutdated path originalLine
            resolvedBy { login }
            comments(first: 50) {
              nodes {
                databaseId url createdAt body
                author { login __typename }
                originalCommit { oid }
              }
            }
          }
        }
      }
    }
  }' --jq '.data.repository.pullRequest' > "$TMP/pr.json"

jq '
  [ .reviewThreads.nodes[]
    | . as $hilo
    | .comments.nodes[0] as $c
    | select($c != null and $c.author.__typename == "Bot")
    | select($c.body | test("^\\s*\\[(Cr[ií]tico|Alto)\\]"; "i"))
    | {
        id: $c.databaseId,
        url: $c.url,
        severidad: ($c.body | capture("^\\s*\\[(?<s>[^\\]]+)\\]").s),
        revisor: $c.author.login,
        archivo: $hilo.path,
        linea: $hilo.originalLine,
        creado: $c.createdAt,
        commit_revisado: ($c.originalCommit.oid // null),
        texto: ($c.body | .[0:2000]),
        hilo: {
          resuelto: $hilo.isResolved,
          resuelto_por: ($hilo.resolvedBy.login // null),
          desactualizado: $hilo.isOutdated
        },
        respuestas: [
          $hilo.comments.nodes[1:][]
          | {
              autor: (.author.login // "ghost"),
              es_bot: (.author.__typename == "Bot"),
              creado: .createdAt,
              texto: (.body | .[0:800])
            }
        ]
      }
  ]' "$TMP/pr.json" > "$TMP/hallazgos.json"

head_sha=$(jq -r '.headRefOid' "$TMP/pr.json")
total=$(jq 'length' "$TMP/hallazgos.json")

# --- Qué cambió en cada archivo después del comentario ------------------------
# Se compara el commit que vio el revisor contra el último del PR. Si la rama se
# rebaseó, el commit revisado puede no existir más: el hallazgo queda con
# `cambios.disponible: false` y el agente lo tiene que decir.
: > "$TMP/enriquecidos.jsonl"
for ((i = 0; i < total; i++)); do
  jq ".[$i]" "$TMP/hallazgos.json" > "$TMP/h.json"
  id=$(jq -r '.id' "$TMP/h.json")
  archivo=$(jq -r '.archivo' "$TMP/h.json")
  base=$(jq -r '.commit_revisado // ""' "$TMP/h.json")

  cambios='{"disponible": false, "commits": [], "estado_archivo": null, "archivo_cambiado": false, "diff_truncado": false, "archivos": [], "diff_completo": null, "diff_completo_truncado": false}'
  if [ -n "$base" ] && gh api "repos/$REPO/compare/$base...$head_sha" > "$TMP/cmp.json" 2>/dev/null; then
    jq --arg p "$archivo" \
      '[.files[]? | select(.filename == $p or .previous_filename == $p)] | first // null' \
      "$TMP/cmp.json" > "$TMP/archivo.json"

    truncado=false
    jq -j '.patch // ""' "$TMP/archivo.json" > "$TMP/patch"
    if [ -s "$TMP/patch" ]; then
      if [ "$(wc -c < "$TMP/patch")" -gt "$TOPE_DIFF" ]; then
        truncado=true
        head -c "$TOPE_DIFF" "$TMP/patch" > "seguimiento/$id.diff"
      else
        cp "$TMP/patch" "seguimiento/$id.diff"
      fi
    fi

    # Uno por commit revisado: los hallazgos de una misma pasada lo comparten.
    # El código va primero y los tests al final, así lo que se corta por el
    # tope son tests.
    completo="seguimiento/despues-${base:0:7}.diff"
    if [ ! -f "$completo" ]; then
      jq -r '
        [.files[]? | select(.patch != null)]
        | sort_by(.filename | test("^(test|cypress)/|\\.(test|spec)\\.[jt]sx?$"))
        | .[]
        | "### \(.filename) (\(.status), +\(.additions) -\(.deletions))\n\(.patch)\n"' \
        "$TMP/cmp.json" > "$TMP/completo-${base:0:7}"
      head -c "$TOPE_DIFF_COMPLETO" "$TMP/completo-${base:0:7}" > "$completo"
    fi
    completo_truncado=$([ "$(wc -c < "$TMP/completo-${base:0:7}")" -gt "$TOPE_DIFF_COMPLETO" ] && echo true || echo false)

    cambios=$(jq \
      --slurpfile archivo "$TMP/archivo.json" \
      --argjson truncado "$truncado" \
      --arg completo "$completo" \
      --argjson completo_truncado "$completo_truncado" '{
        disponible: true,
        commits: [.commits[]? | {sha: .sha[0:7], mensaje: (.commit.message | split("\n")[0]), fecha: .commit.committer.date}],
        estado_archivo: ($archivo[0].status // null),
        archivo_cambiado: ($archivo[0] != null),
        diff_truncado: $truncado,
        archivos: [.files[]? | {archivo: .filename, estado: .status, agregadas: .additions, borradas: .deletions}],
        diff_completo: $completo,
        diff_completo_truncado: $completo_truncado
      }' "$TMP/cmp.json")
  fi

  jq -c --argjson c "$cambios" '. + {cambios: $c}' "$TMP/h.json" >> "$TMP/enriquecidos.jsonl"
done

jq -n \
  --arg repo "$REPO" \
  --arg generado "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --slurpfile pr "$TMP/pr.json" \
  --slurpfile hallazgos "$TMP/enriquecidos.jsonl" '
  $pr[0] as $p
  | {
    repo: $repo,
    generado: $generado,
    pr: {
      numero: $p.number,
      titulo: $p.title,
      url: $p.url,
      autor: ($p.author.login // "ghost"),
      mergeado: $p.mergedAt
    },
    hallazgos: $hallazgos,
    resumen: {
      total: ($hallazgos | length),
      hilos_resueltos: ([$hallazgos[] | select(.hilo.resuelto)] | length),
      con_respuesta_humana: ([$hallazgos[] | select([.respuestas[] | select(.es_bot | not)] | length > 0)] | length),
      archivo_cambiado_despues: ([$hallazgos[] | select(.cambios.archivo_cambiado)] | length),
      sin_ninguna_senal: ([$hallazgos[]
        | select((.hilo.resuelto | not)
                 and ([.respuestas[] | select(.es_bot | not)] | length == 0)
                 and (.cambios.archivo_cambiado | not))] | length)
    }
  }' > hallazgos.json
