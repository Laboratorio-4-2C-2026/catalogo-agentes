#!/usr/bin/env bash
#
# Junta la evidencia que necesita el chequeo de Definition of Done de un PR.
#
# Mismo principio que blockers y progreso: lo que se puede medir lo mide este
# script, y el agente solo cruza cada casilla del template contra estos números.
# Si el agente pudiera leer la API por su cuenta, podría "encontrar" evidencia
# que no existe para una casilla tildada.
#
# Uso: dod-facts.sh <owner/repo> <número de PR>
# Escribe dod.json y, si el PR toca supabase/, dod-supabase.diff.
set -euo pipefail

REPO="${1:?falta owner/repo}"
PR="${2:?falta el número de PR}"

meta=$(gh pr view "$PR" -R "$REPO" --json number,title,body,isDraft,url,files)
gh pr diff "$PR" -R "$REPO" > pr.diff

# --- Casillas del template ----------------------------------------------------
# Cada `- [ ]` / `- [x]` del body, con la sección (## …) en la que está. La
# sección importa: "Tablas nuevas con RLS" no significa lo mismo si el PR no
# toca datos.
casillas=$(jq '
  [ (.body // "") | split("\n")
    | foreach .[] as $l ({seccion: null, item: null};
        if ($l | test("^#{1,6}\\s")) then
          .seccion = ($l | sub("^#+\\s*"; "")) | .item = null
        elif ($l | test("^\\s*[-*]\\s+\\[[ xX]\\]\\s")) then
          .item = {
            seccion: .seccion,
            marcada: ($l | test("^\\s*[-*]\\s+\\[[xX]\\]")),
            texto: ($l | sub("^\\s*[-*]\\s+\\[[ xX]\\]\\s+"; ""))
          }
        else .item = null end;
        .item)
    | select(. != null) ]' <<<"$meta")

# --- Archivos por categoría ---------------------------------------------------
# Las rutas son las de este repo (ver la tabla de .github/copilot-instructions.md):
# el front vive en la raíz, la UI en visual_pages/ y Foundry en contracts/.
archivos=$(jq '[.files[] | {ruta: .path, agregadas: .additions, borradas: .deletions}]' <<<"$meta")
categorias=$(jq '
  def cuenta(f): map(select(.ruta | f)) | length;
  {
    codigo:          cuenta(test("^(app|lib|visual_pages|supabase|scripts)/") or test("^contracts/(src|script)/")),
    tests:           cuenta(test("^(test|cypress)/") or test("^contracts/test/")),
    docs:            cuenta(test("\\.md$")),
    supabase:        (cuenta(test("^supabase/")) > 0),
    contratos:       (cuenta(test("^contracts/src/")) > 0),
    tests_contratos: (cuenta(test("^contracts/test/")) > 0),
    webhooks:        (cuenta(test("webhook")) > 0),
    setup: [ .[].ruta | select(
               test("(^|/)\\.env\\.example$") or test("^package(-lock)?\\.json$")
               or test("^\\.github/workflows/") or test("^scripts/")
               or test("^contracts/(foundry\\.toml|remappings\\.txt)$")) ],
    rutas_de_api_tocadas: [ .[] | select(.ruta | test("^app/api/.*/route\\.ts$")) | .ruta ]
  }' <<<"$archivos")

# --- Evidencia en las líneas agregadas ----------------------------------------
# Solo cuentan las líneas que agrega el PR: lo que ya estaba en master no es
# evidencia de que este PR haya cumplido nada.
agregadas_en() {  # $1: regex de ruta
  awk -v pat="$1" '
    /^diff --git / { f = $4; sub(/^b\//, "", f); next }
    /^\+\+\+ /     { next }
    /^\+/          { if (f ~ pat) print substr($0, 2) }
  ' pr.diff
}
contar() { grep -ciE "$1" || true; }

sql=$(agregadas_en '^supabase/')
tests_sol=$(agregadas_en '^contracts/test/')

tablas_nuevas=$({ grep -oiE 'create table( if not exists)? [a-z0-9_."]+' <<<"$sql" || true; } \
  | awk '{print $NF}' | jq -R . | jq -s .)

evidencia=$(jq -n \
  --argjson tablas "$tablas_nuevas" \
  --argjson rls "$(contar 'enable row level security' <<<"$sql")" \
  --argjson policies "$(contar 'create policy' <<<"$sql")" \
  --argjson definer "$(contar 'security definer' <<<"$sql")" \
  --argjson search_path "$(contar 'set search_path' <<<"$sql")" \
  --argjson expect_revert "$(contar 'expectRevert' <<<"$tests_sol")" '{
    tablas_nuevas: $tablas,
    rls_habilitado_agregado: $rls,
    policies_agregadas: $policies,
    security_definer_agregadas: $definer,
    search_path_agregados: $search_path,
    expect_revert_agregados: $expect_revert
  }')

if [ -n "$sql" ]; then
  awk '
    /^diff --git / { dentro = ($3 ~ /^a\/supabase\//) }
    dentro
  ' pr.diff | head -c 100000 > dod-supabase.diff
fi

# Hoy ningún workflow corre los tests de la app ni forge test: "Tests pasando"
# no se puede verificar en CI y depende de lo que el autor pegue en el body. Se
# mide en vez de asumirlo, para que el día que exista el workflow el agente lo
# sepa solo.
ci_de_tests=$(grep -lE 'test:unit|vitest|forge test' .github/workflows/*.yml >/dev/null 2>&1 && echo true || echo false)

jq -n \
  --argjson meta "$meta" \
  --argjson casillas "$casillas" \
  --argjson archivos "$archivos" \
  --argjson categorias "$categorias" \
  --argjson evidencia "$evidencia" \
  --argjson ci_de_tests "$ci_de_tests" '{
    pr: {numero: $meta.number, titulo: $meta.title, url: $meta.url, borrador: $meta.isDraft},
    casillas: $casillas,
    archivos: $archivos,
    categorias: $categorias,
    evidencia: ($evidencia + {ci_de_tests: $ci_de_tests}),
    hay_diff_supabase: ($categorias.supabase)
  }' > dod.json

rm pr.diff
