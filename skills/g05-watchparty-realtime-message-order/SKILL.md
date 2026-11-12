---
name: g05-watchparty-realtime-message-order
description: "Analiza duplicados, orden y reconexión de mensajes de chat en tiempo real. Usar ante mensajes repetidos, perdidos o desordenados."
metadata:
  tipo: skill
  area: ["frontend","backend"]
  fase: [analisis, revision]
  tecnologias: ["react","typescript"]
  herramientas: [claude-code, cursor, codex, otra]
  requiere: []
  grupo: "05"
  autor:
    nombre: Ramiro Castro Martínez
    github: rcastromartinez
  responsables: [rcastromartinez]
  madurez: experimental
---

# g05-watchparty-realtime-message-order

## Objetivo
Reconstruir entrega y reconciliación de mensajes sin ejecutar tráfico real.

## Activación
Analiza duplicados, orden y reconexión de mensajes de chat en tiempo real. Usar ante mensajes repetidos, perdidos o desordenados.

## Entradas
Código de suscripción y envío, esquema de mensajes, trazas anonimizadas y comportamiento esperado.
Solicitar únicamente los datos que bloqueen el análisis. Si falta evidencia, continuar con alcance parcial declarado.

## Procedimiento
1. Identificar transporte real y garantías documentadas; no asumir exactly-once.
2. Distinguir id persistente, id temporal, autor, sala, created_at y secuencia. Reconstruir envío, confirmación y eco.
3. Simular en papel eco antes de ACK, ACK antes de eco, duplicado, reconexión con replay y cambio de sala.
4. Comprobar deduplicación por identidad estable, orden determinista con desempate y limpieza de suscripciones.
5. Separar fallas demostrables de escenarios no verificables y proponer reconciliación mínima.

## Validaciones
- Leer instrucciones del repositorio y fuentes aportadas dentro del alcance autorizado.
- Asociar cada hallazgo a archivo y línea, documento o evento verificable. No inventar referencias.
- Diferenciar hechos observados, hipótesis y ejemplos. Marcar no verificable cuando falte evidencia.
- Comprobar que la salida respete las reglas vigentes sin añadir funcionalidad.
- Identificar cobertura analizada y límites antes de emitir conclusiones.
- Si se consulta documentación externa, usar la fuente oficial vigente y citarla. No requerir conexiones externas para trabajar con material suministrado.

## Salida esperada
Cronología por evento y tabla escenario / estado esperado / estado observado / evidencia / propuesta.
Cerrar con pendientes y limitaciones. Si no hay hallazgos, indicar el alcance inspeccionado; no certificar ausencia de defectos.

## Restricciones
Trabajar en modo de solo lectura. No modificar código, tickets, PRs, datos, permisos, configuraciones o recursos existentes. No ejecutar migraciones, despliegues, peticiones de escritura o automatizaciones. No publicar comentarios ni crear tickets. Entregar propuestas para revisión humana. No copiar secretos ni datos personales; usar muestras ficticias o anonimizadas. No instalar dependencias ni ejecutar scripts del proyecto sin verificar su alcance y obtener autorización cuando excedan esta lectura.

## Autoría y estado
Autor: Ramiro Castro Martínez (GitHub: rcastromartinez). Grupo: 05 — WatchParty. Responsable: rcastromartinez. Madurez: experimental; sin ejecución funcional acreditada.

## Ejemplo de uso
**Pedido:** Revisá un chat cuyo mensaje aparece dos veces cuando llega el eco antes de la confirmación.

**Resultado esperado (ilustrativo, no ejecución real):** Una cronología ilustrativa y una propuesta de reconciliación por identificador; indicar si el código aportado demuestra el duplicado.
