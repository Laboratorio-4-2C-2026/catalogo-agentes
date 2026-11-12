#!/usr/bin/env bash
#
# Junta la evidencia de la semana y la escribe como JSON.
#
# Mismo principio que blockers-facts.sh: la evidencia la junta este script y el
# agente solo la narra. Un reporte de progreso que el agente pueda completar por
# su cuenta es un reporte que puede inflar, y este va a la cátedra: una semana
# floja tiene que poder verse floja.
#
# Uso: progreso-facts.sh <owner/repo> > progreso.json
set -euo pipefail

REPO="${1:?falta owner/repo}"
DIAS="${DIAS_VENTANA:-7}"
AHORA=$(date -u +%s)
DESDE=$((AHORA - DIAS * 86400))

# GNU y BSD no comparten la sintaxis para formatear un epoch. El script corre en
# ubuntu-latest, pero conviene que también se pueda probar a mano en una Mac.
iso() { date -u -d "@$1" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -r "$1" +%Y-%m-%dT%H:%M:%SZ; }
DESDE_ISO=$(iso "$DESDE")
HASTA_ISO=$(iso "$AHORA")

# Las etiquetas de los reportes automáticos: sus issues no son trabajo del
# equipo y no tienen que aparecer como tal.
ETIQUETAS_DE_REPORTE='["blockers-report", "reporte-semanal", "hallazgos-pendientes"]'

# --- Pull requests ------------------------------------------------------------
# Una sola llamada trae todo lo que hace falta de los PRs; el filtro por ventana
# lo hace jq sobre esa respuesta.
todos_prs=$(gh pr list -R "$REPO" --state all --limit 100 \
  --json number,title,author,createdAt,mergedAt,closedAt,state,isDraft,additions,deletions,changedFiles,labels,url,closingIssuesReferences)

prs_mergeados=$(jq --argjson desde "$DESDE" '
  [ .[]
    | select(.mergedAt != null and (.mergedAt | fromdateiso8601) >= $desde)
    | {
        numero: .number,
        titulo: .title,
        autor: .author.login,
        mergeado: .mergedAt,
        horas_hasta_merge: (((.mergedAt | fromdateiso8601) - (.createdAt | fromdateiso8601)) / 3600 | floor),
        lineas_agregadas: .additions,
        lineas_borradas: .deletions,
        archivos: .changedFiles,
        etiquetas: [.labels[].name],
        cierra_issues: [.closingIssuesReferences[]?.number],
        url: .url
      }
  ] | sort_by(.mergeado)' <<<"$todos_prs")

prs_abiertos_en_la_ventana=$(jq --argjson desde "$DESDE" '
  [ .[]
    | select((.createdAt | fromdateiso8601) >= $desde)
    | {
        numero: .number,
        titulo: .title,
        autor: .author.login,
        creado: .createdAt,
        estado: .state,
        borrador: .isDraft,
        url: .url
      }
  ] | sort_by(.creado)' <<<"$todos_prs")

# Los PRs que tuvieron actividad en la ventana son los únicos donde tiene
# sentido buscar hallazgos de los agentes.
numeros_activos=$(jq -r --argjson desde "$DESDE" '
  [ .[]
    | select(((.mergedAt // "1970-01-01T00:00:00Z") | fromdateiso8601) >= $desde
             or (.createdAt | fromdateiso8601) >= $desde)
    | .number
  ] | unique | .[]' <<<"$todos_prs")

# --- Issues -------------------------------------------------------------------
todos_issues=$(gh issue list -R "$REPO" --state all --limit 100 \
  --json number,title,author,createdAt,closedAt,state,labels,assignees,url)

# Se excluyen los issues de los propios reportes automáticos.
todos_issues=$(jq --argjson excluir "$ETIQUETAS_DE_REPORTE" '
  [ .[] | select([.labels[].name] | any(. as $l | $excluir | index($l)) | not) ]' <<<"$todos_issues")

issues_cerrados=$(jq --argjson desde "$DESDE" '
  [ .[]
    | select(.closedAt != null and (.closedAt | fromdateiso8601) >= $desde)
    | {
        numero: .number,
        titulo: .title,
        cerrado: .closedAt,
        dias_abierto: (((.closedAt | fromdateiso8601) - (.createdAt | fromdateiso8601)) / 86400 | floor),
        asignados: [.assignees[].login],
        etiquetas: [.labels[].name],
        url: .url
      }
  ] | sort_by(.cerrado)' <<<"$todos_issues")

issues_abiertos_en_la_ventana=$(jq --argjson desde "$DESDE" '
  [ .[]
    | select((.createdAt | fromdateiso8601) >= $desde)
    | {
        numero: .number,
        titulo: .title,
        autor: .author.login,
        creado: .createdAt,
        estado: .state,
        url: .url
      }
  ] | sort_by(.creado)' <<<"$todos_issues")

# Arrastre: lo que sigue abierto y ya venía de antes de la ventana. Es la cifra
# que dice si el equipo está cerrando trabajo o solo acumulándolo.
arrastre=$(jq --argjson desde "$DESDE" --argjson ahora "$AHORA" '
  [ .[]
    | select(.state == "OPEN" and (.createdAt | fromdateiso8601) < $desde)
    | {
        numero: .number,
        titulo: .title,
        dias_abierto: (($ahora - (.createdAt | fromdateiso8601)) / 86400 | floor),
        asignados: [.assignees[].login],
        url: .url
      }
  ] | sort_by(-.dias_abierto)' <<<"$todos_issues")

# --- Commits en la rama por defecto -------------------------------------------
rama=$(gh repo view "$REPO" --json defaultBranchRef --jq .defaultBranchRef.name)
commits=$(gh api "repos/$REPO/commits?sha=$rama&since=$DESDE_ISO&per_page=100" --paginate 2>/dev/null || echo '[]')
commits_resumen=$(jq '{
    cantidad: length,
    autores: [.[].author.login // .[].commit.author.name] | unique
  }' <<<"$commits")

# --- Hallazgos de nuestros propios agentes ------------------------------------
# Cuenta los comentarios de bot que arrancan con una severidad. Es la evidencia
# de que el pipeline de review efectivamente corrió, y con qué resultado.
#
# Si un agente comentó sin prefijo de severidad no se cuenta como hallazgo: el
# formato es parte del contrato de los revisores y sin severidad no se puede
# priorizar. Queda en `sin_severidad` para que se note.
#
# Los reportes fijos —el de Slither, el de blockers— no son hallazgos: son un
# comentario que se reescribe en cada corrida. Se los reconoce porque abren con
# un marcador HTML, y se descuentan antes de contar. Sin esto, el reporte le
# decía a la cátedra que nuestros revisores comentan sin severidad cuando en
# realidad estaba contando la tabla de Slither.
hallazgos='{"critico":0,"alto":0,"medio":0,"bajo":0,"sin_severidad":0,"total":0}'
for n in $numeros_activos; do
  inline=$(gh api "repos/$REPO/pulls/$n/comments" --paginate 2>/dev/null || echo '[]')
  sueltos=$(gh api "repos/$REPO/issues/$n/comments" --paginate 2>/dev/null || echo '[]')

  hallazgos=$(jq -n \
    --argjson acc "$hallazgos" \
    --argjson a "$inline" \
    --argjson b "$sueltos" '
      (($a + $b)
        | map(select(.user.type == "Bot"))
        | map(select(.body | test("^\\s*<!--") | not))) as $bot
      | ($bot | map(select(.body | test("^\\s*\\[Cr[ií]tico\\]"; "i"))) | length) as $c
      | ($bot | map(select(.body | test("^\\s*\\[Alto\\]";        "i"))) | length) as $al
      | ($bot | map(select(.body | test("^\\s*\\[Medio\\]";       "i"))) | length) as $m
      | ($bot | map(select(.body | test("^\\s*\\[Bajo\\]";        "i"))) | length) as $ba
      | {
          critico:       ($acc.critico       + $c),
          alto:          ($acc.alto          + $al),
          medio:         ($acc.medio         + $m),
          bajo:          ($acc.bajo          + $ba),
          sin_severidad: ($acc.sin_severidad + (($bot | length) - $c - $al - $m - $ba)),
          total:         ($acc.total         + ($bot | length))
        }')
done

# --- Salida -------------------------------------------------------------------
jq -n \
  --arg repo "$REPO" \
  --arg generado "$HASTA_ISO" \
  --arg desde "$DESDE_ISO" \
  --arg hasta "$HASTA_ISO" \
  --arg rama "$rama" \
  --argjson dias "$DIAS" \
  --argjson prs_mergeados "$prs_mergeados" \
  --argjson prs_nuevos "$prs_abiertos_en_la_ventana" \
  --argjson issues_cerrados "$issues_cerrados" \
  --argjson issues_nuevos "$issues_abiertos_en_la_ventana" \
  --argjson arrastre "$arrastre" \
  --argjson commits "$commits_resumen" \
  --argjson hallazgos "$hallazgos" '{
    repo: $repo,
    generado: $generado,
    ventana: { dias: $dias, desde: $desde, hasta: $hasta, rama: $rama },
    prs_mergeados: $prs_mergeados,
    prs_nuevos: $prs_nuevos,
    issues_cerrados: $issues_cerrados,
    issues_nuevos: $issues_nuevos,
    arrastre: $arrastre,
    commits: $commits,
    hallazgos_de_agentes: $hallazgos,
    resumen: {
      prs_mergeados: ($prs_mergeados | length),
      prs_nuevos: ($prs_nuevos | length),
      issues_cerrados: ($issues_cerrados | length),
      issues_nuevos: ($issues_nuevos | length),
      arrastre: ($arrastre | length),
      commits: $commits.cantidad,
      lineas_agregadas: ([$prs_mergeados[].lineas_agregadas] | add // 0),
      lineas_borradas: ([$prs_mergeados[].lineas_borradas] | add // 0),
      hallazgos_de_agentes: $hallazgos.total,
      hubo_actividad: ((
        ($prs_mergeados | length) + ($prs_nuevos | length)
        + ($issues_cerrados | length) + ($issues_nuevos | length)
        + $commits.cantidad
      ) > 0)
    }
  }'
