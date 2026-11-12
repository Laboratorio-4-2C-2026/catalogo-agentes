---
name: g05-watchparty-room-concurrency
description: "Mide el rendimiento de salas de WatchParty con niveles acordados de concurrencia en un entorno de prueba, desde la entrada a sala hasta la propagación de eventos."
metadata:
  tipo: skill
  area: ["qa","backend"]
  fase: ["testing"]
  tecnologias: ["agnostico"]
  metodologia: [scrum]
  herramientas: [codex]
  requiere: []
  grupo: '05'
  autor:
    nombre: Manuel Salas Seeber
    github: Manuelsalasseeber
  responsables: [Manuelsalasseeber]
  madurez: experimental
  relacionados: ["g07-performance-con-volumen"]
---

# Rendimiento de salas con concurrencia

## Procedimiento

1. Confirmá entorno aislado, versión, cuentas sintéticas, niveles de concurrencia, duración y condiciones de parada. Definí con el equipo los umbrales y el patrón de entrada, lectura y emisión de eventos. Si faltan condiciones de ejecución, entregá el plan de medición.
2. Medí una línea base con pocos clientes y repetí el mismo patrón por escalones. Mantené estables el dataset, la duración de la ventana y la proporción de acciones. Distinguí concurrencia sostenida de entradas simultáneas a una misma sala.
3. Registrá latencia de entrada y de propagación, volumen completado, errores y eventos perdidos. Para medir propagación, correlacioná cada evento y usá un reloj común o registrá el margen de error de la sincronización. Conservá tamaño de muestra y percentiles cuando sean representativos.
4. Entregá una tabla por escalón con concurrencia efectiva, latencias, errores, pérdidas y comparación con los umbrales. Indicá cuándo se detuvo el ensayo y qué limitaciones del entorno afectan la lectura.

## Ejemplo de uso

**Pedido:** Medí cuánto demora en verse un comentario al subir gradualmente la cantidad de usuarios conectados a una sala de prueba.

**Resultado:** Entrega latencia de propagación, tamaño de muestra y tasa de errores por nivel acordado, con el umbral y la condición de parada.
