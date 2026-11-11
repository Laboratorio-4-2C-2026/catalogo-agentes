"""Firma el token del rol motor_matching para la nube. Lo corre el dev de datos, en su laptop, apenas crea el proyecto.

Uso: python3 -I firmar-token-motor.py <archivo-con-legacy-jwt-secret> <vencimiento ISO, ej. 2026-11-15T23:59-03:00> > token-motor
El secreto se lee de un archivo (nunca por argumento: quedaría en el historial) y no se guarda en ningún lado.
El vencimiento se pasa en cada corrida, con zona horaria; si ya pasó, no se firma nada.
"""
import base64, hashlib, hmac, json, sys
from datetime import datetime, timezone

if len(sys.argv) != 3:
    sys.exit(__doc__)
vence = datetime.fromisoformat(sys.argv[2])
if vence.tzinfo is None:
    sys.exit("El vencimiento necesita zona horaria (ej. -03:00).")
if vence <= datetime.now(timezone.utc):
    sys.exit(f"El vencimiento {vence.isoformat()} ya pasó.")
print(f"El token vence el {vence.isoformat()}.", file=sys.stderr)

b = lambda x: base64.urlsafe_b64encode(x).rstrip(b"=")
secreto = open(sys.argv[1]).read().strip().encode()
h = b(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())
p = b(json.dumps({"role": "motor_matching", "exp": int(vence.timestamp())}, separators=(",", ":")).encode())
print((h + b"." + p + b"." + b(hmac.new(secreto, h + b"." + p, hashlib.sha256).digest())).decode())
