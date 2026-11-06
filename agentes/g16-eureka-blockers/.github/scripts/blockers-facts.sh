#!/usr/bin/env bash
#
# Junta los hechos que necesita el detector de blockers y los escribe como JSON.
#
# La detección es determinista a propósito: el agente que lee esta salida
# tríagea y prioriza, pero no decide qué existe. Si le dejáramos consultar la
# API por su cuenta, un blocker inventado sería indistinguible de uno real.
#
# Uso: blockers-facts.sh <owner/repo> > facts.json
set -euo pipefail

REPO="${1:?falta owner/repo}"
HORAS_SIN_REVIEW="${HORAS_SIN_REVIEW:-48}"
DIAS_SIN_CODIGO="${DIAS_SIN_CODIGO:-7}"
AHORA=$(date -u +%s)

# Trae un endpoint de lista de la API como un único arreglo JSON.
# `gh api --paginate` escribe un arreglo por página, uno pegado al otro, y si la
# llamada falla igual imprime el cuerpo del error por stdout. Ninguna de las dos
# cosas la acepta `jq --argjson`, así que si falla se descarta la salida, y si
# no, se juntan las páginas.
api_lista() {
  local salida
  salida=$(gh api "$1" --paginate 2>/dev/null) || salida='[]'
  jq -s 'add // []' <<<"$salida"
}

# --- PRs abiertos -------------------------------------------------------------
# Solo cuentan las reviews HUMANAS. Las de Slither, Claude y Copilot no: si
# contaran, todo PR que revisan nuestros propios agentes quedaría marcado como
# atendido, que es exactamente lo contrario de lo que este detector busca.
# La API distingue unas de otras con `user.type == "Bot"`.
#
# Los borradores no cuentan: todavía no piden atención de nadie.
ESTADO_PR="${ESTADO_PR:-open}"   # "all" sirve para probar el script a mano
prs="[]"
for n in $(gh pr list -R "$REPO" --state "$ESTADO_PR" --limit 100 --json number --jq '.[].number'); do
  meta=$(gh pr view "$n" -R "$REPO" \
    --json number,title,author,createdAt,updatedAt,isDraft,reviewRequests,url)
  revs=$(api_lista "repos/$REPO/pulls/$n/reviews")

  prs=$(jq -n \
    --argjson acc "$prs" \
    --argjson meta "$meta" \
    --argjson revs "$revs" \
    --argjson ahora "$AHORA" \
    --argjson limite "$HORAS_SIN_REVIEW" '
      ($revs | map(select(.user.type != "Bot")) | length) as $humanas
      | ($revs | map(select(.user.type == "Bot")) | length) as $de_agente
      | (($ahora - ($meta.createdAt | fromdateiso8601)) / 3600 | floor) as $horas_abierto
      | (($ahora - ($meta.updatedAt | fromdateiso8601)) / 3600 | floor) as $horas_quieto
      | $acc + [{
          numero: $meta.number,
          titulo: $meta.title,
          autor: $meta.author.login,
          borrador: $meta.isDraft,
          horas_abierto: $horas_abierto,
          horas_sin_actividad: $horas_quieto,
          reviews_humanas: $humanas,
          reviews_de_agente: $de_agente,
          reviewers_pedidos: [$meta.reviewRequests[]?.login, $meta.reviewRequests[]?.name] | map(select(. != null)),
          url: $meta.url,
          sin_review_humana_pasado_el_limite:
            ($humanas == 0 and $meta.isDraft == false and $horas_abierto >= $limite)
        }]')
done

# --- Issues abiertos ----------------------------------------------------------
# Se excluyen los issues de los reportes automáticos: el de este mismo detector,
# que si no se encuentra a sí mismo, el semanal de progreso, que queda abierto
# a propósito y a los siete días figuraría como un ticket sin código, y el de
# post-deploy, que no se arregla con código sino con configuración.
ETIQUETAS_DE_REPORTE='["blockers-report", "reporte-semanal", "post-deploy"]'
numeros=$(gh issue list -R "$REPO" --state open --limit 100 \
  --json number,labels \
  | jq -r --argjson excluir "$ETIQUETAS_DE_REPORTE" \
      '[.[] | select([.labels[].name] | any(. as $l | $excluir | index($l)) | not) | .number] | .[]')

issues="[]"
for n in $numeros; do
  # El timeline dice si el ticket tocó código alguna vez y cuántas veces rebotó.
  tl=$(api_lista "repos/$REPO/issues/$n/timeline")
  meta=$(gh api "repos/$REPO/issues/$n" --jq '{titulo: .title, creado: .created_at, actualizado: .updated_at, asignados: [.assignees[].login], url: .html_url}')

  issues=$(jq -n \
    --argjson acc "$issues" \
    --argjson tl "$tl" \
    --argjson meta "$meta" \
    --argjson n "$n" \
    --argjson ahora "$AHORA" \
    --argjson dias "$DIAS_SIN_CODIGO" '
      ($tl | map(select(.event == "cross-referenced" or .event == "connected" or .event == "referenced" or .event == "committed")) | length) as $refs_codigo
      | ($tl | map(select(.event == "reopened")) | length) as $reaperturas
      | ($tl | map(select(.event == "labeled" or .event == "unlabeled")) | length) as $cambios_label
      | ($tl | map(select(.event == "moved_columns_in_project")) | length) as $movidas_tablero
      | (($ahora - ($meta.creado | fromdateiso8601)) / 86400 | floor) as $dias_abierto
      | $acc + [{
          numero: $n,
          titulo: $meta.titulo,
          asignados: $meta.asignados,
          dias_abierto: $dias_abierto,
          referencias_a_codigo: $refs_codigo,
          reaperturas: $reaperturas,
          cambios_de_etiqueta: $cambios_label,
          movidas_de_columna: $movidas_tablero,
          url: $meta.url,
          sin_codigo_pasado_el_limite: ($refs_codigo == 0 and $dias_abierto >= $dias),
          rebota_de_estado: ($reaperturas >= 2 or $cambios_label >= 6 or $movidas_tablero >= 4)
        }]')
done

jq -n \
  --argjson prs "$prs" \
  --argjson issues "$issues" \
  --arg repo "$REPO" \
  --arg generado "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --argjson horas "$HORAS_SIN_REVIEW" \
  --argjson dias "$DIAS_SIN_CODIGO" '{
    repo: $repo,
    generado: $generado,
    umbrales: { horas_sin_review: $horas, dias_sin_codigo: $dias },
    prs_abiertos: $prs,
    issues_abiertos: $issues,
    resumen: {
      prs_abiertos: ($prs | length),
      prs_sin_review_humana: ([$prs[] | select(.sin_review_humana_pasado_el_limite)] | length),
      issues_abiertos: ($issues | length),
      issues_sin_codigo: ([$issues[] | select(.sin_codigo_pasado_el_limite)] | length),
      issues_que_rebotan: ([$issues[] | select(.rebota_de_estado)] | length)
    }
  }'
