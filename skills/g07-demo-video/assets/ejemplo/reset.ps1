# Base nueva + datos de la demo. El backend crea las tablas al arrancar (ddl-auto=update).
$repo = Resolve-Path "$PSScriptRoot\..\..\..\.."
$compose = @('compose', '-p', 'mi-app-demo', '--env-file', "$repo\.env",
  '-f', "$PSScriptRoot\app\docker-compose.yml", '-f', "$PSScriptRoot\compose.demo.yml")

docker @compose down -v
docker @compose up -d --build
for ($i = 0; $i -lt 60; $i++) {
  try { Invoke-RestMethod http://localhost:8080/api/v1/health -TimeoutSec 3 | Out-Null; break } catch { Start-Sleep 2 }
}
node "$PSScriptRoot\seed.mjs"
