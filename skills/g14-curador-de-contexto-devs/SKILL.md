---
name: g14-curador-de-contexto-devs
description: "Audita el contenido del kit de contexto de los devs (AGENTS.md, CLAUDE.md y docs) con un script que chequea la presencia de reglas prefijadas: DoD, stack, manejo de claves, migraciones y merge. Usala cuando cambia un ADR, la DoD o el stack; no compara la redacción contra las fuentes canónicas ni genera espejos, que son del curador multiherramienta."
metadata:
  tipo: skill
  area:
  - documentacion
  fase:
  - mantenimiento
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: '14'
  autor:
    nombre: Elías Ballesteros
    github: Elias85974
  colaboradores: []
  responsables:
  - Elias85974
  madurez: usado-en-proyecto
  relacionados:
  - g14-curador-de-contexto-multiherramienta
---

# Curador de contexto de los desarrolladores (Guardián de convenciones)

Audita y mantiene sincronizado el contexto de los desarrolladores (`ai-config/AGENTS.md`, `CLAUDE.md` y `docs/`) con respecto a las decisiones de arquitectura (ADRs) y reglas de gobernanza definidas en `vaiven-direccion`.

## El principio

La fuente canónica de decisiones es **`vaiven-direccion`** (ADRs en `docs/architecture/adr/` y reglas de kit en `docs/kit-devs/`).
El repositorio **`ai-config`** es el kit entregado a los desarrolladores de Lab II.

Cualquier cambio en un ADR o en la DoD debe ser inmediatamente reflejado en `ai-config`. Este agente detecta reglas prefijadas que faltan en el kit; no contrasta su redacción contra los ADRs, eso sigue siendo lectura humana.

## El protocolo

### 1. Ejecutar auditoría determinista de paridad

Correr el script de auditoría para verificar la alineación de convenciones:

```bash
python3 scripts/auditar-contexto-devs.py --out salidas/auditoria-contexto-devs.txt
```

Si el script detecta fallos (código de salida 1):
1. Identificar las reglas o criterios con estado `[FAIL]`.
2. Actualizar las secciones correspondientes en `ai-config/AGENTS.md`, `ai-config/CLAUDE.md` o `ai-config/docs/`.
3. Garantizar la paridad 100% entre `ai-config/AGENTS.md` y `ai-config/CLAUDE.md`.

### 2. Sincronizar espejos multiplataforma

Una vez validado `ai-config` y las skills de `vaiven-agentes`:

```bash
python3 scripts/sync-agentes.py --write
python3 scripts/sync-agentes.py --check
```

### 3. Reglas críticas que no pueden violarse

- **service_role key:** NUNCA en el frontend (`app/src/`), en el `.env` del frontend ni en Vercel. Únicamente en credenciales de n8n (ADR-0006, ADR-0011).
- **Semillas de BD:** Siempre en archivos de migración SQL (`supabase/migrations/`), NUNCA en `seed.sql` (ADR-0002).
- **Entorno diario:** Stack local Docker (`supabase start` / `reset`), no `vaiven-dev` (ADR-0013).
- **Sin código de producto:** Dirección y sus agentes NO escriben ni modifican código de producto en `app/`.
- **Merge:** Únicamente ejecutado por desarrolladores de Lab II (DoD Criterio 8).

## Verificación de salida

Asegurarse de que `salidas/auditoria-contexto-devs.txt` contenga `RESULTADO: 🟢 PARIDAD COMPLETA`.

## Ejemplo de uso

**Pedido:** Cambiamos la DoD, verificá que el kit de los devs esté al día.

**Resultado:** Corre el script, que chequea que las reglas prefijadas de DoD, stack, claves, migraciones y merge estén presentes en el kit, y lista las que faltan.
