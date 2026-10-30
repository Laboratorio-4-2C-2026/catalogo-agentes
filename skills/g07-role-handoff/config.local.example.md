# Configuración local — no se versiona

Copiá este archivo como `config.local.md` en esta misma carpeta y pegá la URL. `config.local.md` tiene que estar en el `.gitignore`: la URL de un webhook es un secreto (quien la tenga puede postear en el canal).

- **Discord webhook URL**: `<pegar acá la URL del webhook>`

## Cómo conseguir la URL

Discord → configuración del canal → Integraciones → Webhooks → Nuevo webhook → Copiar URL del webhook.

Si preferís no tener el archivo, exportá la URL en la variable de entorno que indica `config.md`: tiene prioridad sobre este archivo.
