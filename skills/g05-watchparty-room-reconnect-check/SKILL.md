---
name: g05-watchparty-room-reconnect-check
description: "Ejecuta y documenta una comprobación repetible de reconexión en salas de WatchParty con dos sesiones de navegador y una interrupción controlada."
metadata:
  tipo: skill
  area: ["qa"]
  fase: ["testing"]
  tecnologias: ["react","playwright"]
  metodologia: [scrum]
  herramientas: [codex]
  requiere: []
  grupo: '05'
  autor:
    nombre: Manuel Salas Seeber
    github: Manuelsalasseeber
  responsables: [Manuelsalasseeber]
  madurez: experimental
  relacionados: ["g06-qa-playwright-evidence","g05-watchparty-qa-handoff"]
---

# Verificación de reconexión en salas

## Procedimiento

1. Identificá versión, entorno de prueba autorizado, sala, dos cuentas de prueba y comportamiento esperado al reconectar. Confirmá qué eventos deben recuperarse o qué estado debe volver a consultarse. Si la regla es ambigua, registrá lo observado y dejá pendiente el veredicto de ese criterio.
2. Usá dos contextos de navegador independientes, con Playwright si está disponible. Registrá el estado inicial de ambos. Interrumpí la red solo en el contexto A y confirmá que B siga operativo.
3. Desde B generá un comentario y, cuando corresponda, una reacción identificables. Restaurá la red en A sin recargar manualmente, salvo que ese sea el comportamiento definido. Esperá una señal observable de reconexión y verificá si el estado coincide con lo esperado, incluyendo recuentos y duplicados. Generá un evento posterior para comprobar que siguen llegando novedades.
4. Guardá la secuencia con marcas de tiempo, el resultado por sesión y la evidencia disponible sin credenciales. Marcá cada criterio como aprobado, fallido o bloqueado. Diferenciá el resultado de una reconexión automática del obtenido después de recargar.

## Ejemplo de uso

**Pedido:** En staging, desconectá una sesión mientras otra comenta y verificá qué pasa al volver la red.

**Resultado:** Entrega la secuencia de ambas sesiones y evidencia de si el comentario aparece una sola vez y si se reciben eventos posteriores.
