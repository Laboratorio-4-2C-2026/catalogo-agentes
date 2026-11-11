#!/usr/bin/env bash
# Se corre EN LA VM, en ~/n8n, con creds.json y wf.json (los arma importar.sh) en la carpeta personal.
# Importa las credenciales y el workflow, lo publica, reinicia n8n y borra los archivos pase lo que pase.
set -euo pipefail
# La limpieza se arma antes de cualquier paso: cubre también los fallos tempranos. No tapa el error (el exit code se conserva).
limpiar() {
  rm -f ~/creds.json ~/wf.json
  (cd ~/n8n && docker compose exec -T n8n rm -f /tmp/creds.json /tmp/wf.json) >/dev/null 2>&1 || true
}
trap limpiar EXIT
cd ~/n8n
WF_ID=$(python3 -c 'import json,os; print(json.load(open(os.path.expanduser("~/wf.json")))["id"])')
# Por stdin, para que el archivo quede del usuario de n8n (docker cp lo deja de root y n8n no lo lee).
docker compose exec -T n8n sh -c 'umask 077; cat > /tmp/creds.json' < ~/creds.json
docker compose exec -T n8n sh -c 'cat > /tmp/wf.json' < ~/wf.json
docker compose exec -T n8n sh -c "n8n import:credentials --input=/tmp/creds.json && n8n import:workflow --input=/tmp/wf.json && n8n publish:workflow --id=$WF_ID"
docker compose restart n8n
echo "Listo. En un minuto: https://<host>/webhook/motor-juicio por POST tiene que dar 403."
