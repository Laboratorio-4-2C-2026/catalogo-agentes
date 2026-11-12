#!/usr/bin/env bash
#
# Junta las vulnerabilidades conocidas de las dependencias de Eureka y las
# escribe como JSON.
#
# Dos fuentes, las dos deterministas:
# - npm: `npm audit` sobre package-lock.json, sin instalar nada. Corre dos
#   veces, con y sin las dependencias de desarrollo, para saber cuáles llegan a
#   producción.
# - Solidity: las librerías de contracts/lib son submódulos, no paquetes de
#   npm, y `npm audit` no las ve. Se lee la versión de OpenZeppelin de cada
#   submódulo y se consulta la base de advisories de GitHub para esa versión.
#
# El agente que lee esta salida prioriza y explica, pero no decide qué
# vulnerabilidades existen: si las buscara por su cuenta, una inventada sería
# indistinguible de una real.
#
# Uso: dependencias-facts.sh > facts.json  (necesita GH_TOKEN para la API)
set -euo pipefail

AHORA=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Los JSON intermedios van a archivos y no a variables: la salida de
# `npm audit` pesa cientos de KB, y pasada con `--argjson` supera el límite de
# tamaño de un argumento (128 KB en Linux) y el script se cae.
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# --- npm ----------------------------------------------------------------------
# `npm audit` sale con código distinto de cero cuando encuentra algo: eso no es
# un error. Un error de verdad (sin red, lockfile roto) deja un JSON con `error`
# o directamente no deja JSON.
npm_audit() {
  local destino="$1"; shift
  npm audit --package-lock-only --json "$@" > "$destino" 2>/dev/null || true
  if ! jq -e 'has("vulnerabilities")' "$destino" > /dev/null 2>&1; then
    echo '{"error": true}' > "$destino"
  fi
}

npm_audit "$TMP/todo.json"
npm_audit "$TMP/prod.json" --omit=dev

jq -n --slurpfile todo "$TMP/todo.json" --slurpfile prod "$TMP/prod.json" '
  $todo[0] as $todo | $prod[0] as $prod |
  if ($todo.error // false) then {ok: false}
  else {
    ok: true,
    por_severidad: ($todo.metadata.vulnerabilities // {}),
    vulnerabilidades: ([
      $todo.vulnerabilities | to_entries[] | .value as $v | {
        paquete: .key,
        severidad: $v.severity,
        directa: $v.isDirect,
        en_produccion: (($prod.vulnerabilities // {}) | has($v.name)),
        rango_afectado: $v.range,
        arreglo: (
          if ($v.fixAvailable | type) == "object"
          then {paquete: $v.fixAvailable.name, version: $v.fixAvailable.version, cambio_mayor: $v.fixAvailable.isSemVerMajor}
          else $v.fixAvailable end
        ),
        # `via` mezcla avisos (objetos) con nombres de otros paquetes
        # vulnerables (strings): los strings dicen por qué dependencia llega.
        avisos: [$v.via[] | objects | {titulo: .title, url: .url, severidad: .severity}],
        llega_por: [$v.via[] | strings]
      }
    ] | sort_by({"critical":0,"high":1,"moderate":2,"low":3,"info":4}[.severidad]))
  } end' > "$TMP/npm.json"

# --- Solidity -----------------------------------------------------------------
# El package.json publicable de OpenZeppelin está en contracts/ dentro de cada
# repo; el de la raíz es el del monorepo y no tiene el nombre del paquete.
echo '[]' > "$TMP/solidity.json"
for pkg in contracts/lib/openzeppelin-contracts/contracts/package.json \
           contracts/lib/openzeppelin-contracts-upgradeable/contracts/package.json; do
  if [ ! -f "$pkg" ]; then
    jq --arg p "$pkg" '. + [{archivo: $p, ok: false}]' "$TMP/solidity.json" > "$TMP/sol.tmp"
    mv "$TMP/sol.tmp" "$TMP/solidity.json"
    continue
  fi
  nombre=$(jq -r .name "$pkg")
  version=$(jq -r .version "$pkg")
  gh api "advisories?ecosystem=npm&affects=${nombre}@${version}&per_page=100" > "$TMP/avisos.json" 2>/dev/null \
    || echo 'null' > "$TMP/avisos.json"
  jq --arg n "$nombre" --arg v "$version" --slurpfile a "$TMP/avisos.json" '$a[0] as $a | . + [
    if $a == null then {paquete: $n, version: $v, ok: false}
    else {
      paquete: $n, version: $v, ok: true,
      avisos: [$a[] | {
        id: .ghsa_id, severidad: .severity, titulo: .summary, url: .html_url,
        # Una versión arreglada por cada rama afectada (4.9.6 y 5.0.2, por
        # ejemplo): se guardan todas y el agente elige la de la rama en uso.
        arreglado_en: ([.vulnerabilities[]? | select(.package.name == $n) | .first_patched_version] | map(select(. != null)))
      }]
    } end]' "$TMP/solidity.json" > "$TMP/sol.tmp"
  mv "$TMP/sol.tmp" "$TMP/solidity.json"
done

jq -n --arg generado "$AHORA" --slurpfile npm "$TMP/npm.json" --slurpfile sol "$TMP/solidity.json" '
  $npm[0] as $npm | $sol[0] as $sol | {
  generado: $generado,
  npm: $npm,
  solidity: $sol,
  resumen: {
    npm_ok: $npm.ok,
    solidity_ok: ($sol | all(.ok)),
    criticas: ([$npm.vulnerabilidades[]? | select(.severidad == "critical")] | length),
    altas: ([$npm.vulnerabilidades[]? | select(.severidad == "high")] | length),
    moderadas: ([$npm.vulnerabilidades[]? | select(.severidad == "moderate")] | length),
    bajas: ([$npm.vulnerabilidades[]? | select(.severidad == "low")] | length),
    en_produccion: ([$npm.vulnerabilidades[]? | select(.en_produccion)] | length),
    avisos_solidity: ([$sol[].avisos[]?] | length)
  }
}'
