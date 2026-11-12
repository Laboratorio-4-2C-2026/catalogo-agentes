---
name: g05-watchparty-optimistic-action-recovery
description: "Evalúa recuperación de likes y ratings optimistas en React. Usar cuando fallos o respuestas fuera de orden dejan estados incorrectos."
metadata:
  tipo: skill
  area: ["frontend","qa"]
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

# g05-watchparty-optimistic-action-recovery

## Objetivo
Verificar coherencia entre intención del usuario, estado visual y estado confirmado.

## Activación
Evalúa recuperación de likes y ratings optimistas en React. Usar cuando fallos o respuestas fuera de orden dejan estados incorrectos.

## Entradas
Fragmentos de código o documentación pertinentes, reglas esperadas y ejemplos anonimizados.
Solicitar únicamente los datos que bloqueen el análisis. Si falta evidencia, continuar con alcance parcial declarado.

## Procedimiento
1. Identificar estado confirmado, estado optimista, operación pendiente y política de reintento.
2. Trazar click, actualización local, request, respuesta y reconciliación.
3. Evaluar doble click, error, timeout con resultado desconocido, respuesta tardía y desmontaje.
4. Comprobar si rollback restaura una versión vieja y pisa una intención más reciente.
5. Proponer criterios verificables para cancelar, serializar o versionar operaciones según contrato existente.

## Validaciones
- Leer instrucciones del repositorio y fuentes aportadas dentro del alcance autorizado.
- Asociar cada hallazgo a archivo y línea, documento o evento verificable. No inventar referencias.
- Diferenciar hechos observados, hipótesis y ejemplos. Marcar no verificable cuando falte evidencia.
- Comprobar que la salida respete las reglas vigentes sin añadir funcionalidad.
- Identificar cobertura analizada y límites antes de emitir conclusiones.
- Si se consulta documentación externa, usar la fuente oficial vigente y citarla. No requerir conexiones externas para trabajar con material suministrado.

## Salida esperada
Matriz de secuencias / estado final esperado / riesgo / evidencia y estrategia de recuperación.
Cerrar con pendientes y limitaciones. Si no hay hallazgos, indicar el alcance inspeccionado; no certificar ausencia de defectos.

## Restricciones
Trabajar en modo de solo lectura. No modificar código, tickets, PRs, datos, permisos, configuraciones o recursos existentes. No ejecutar migraciones, despliegues, peticiones de escritura o automatizaciones. No publicar comentarios ni crear tickets. Entregar propuestas para revisión humana. No copiar secretos ni datos personales; usar muestras ficticias o anonimizadas. No instalar dependencias ni ejecutar scripts del proyecto sin verificar su alcance y obtener autorización cuando excedan esta lectura.

## Autoría y estado
Autor: Ramiro Castro Martínez (GitHub: rcastromartinez). Grupo: 05 — WatchParty. Responsable: rcastromartinez. Madurez: experimental; sin ejecución funcional acreditada.

## Ejemplo de uso
**Pedido:** Revisá dos likes seguidos cuando la primera petición falla después de completarse la segunda.

**Resultado esperado (ilustrativo, no ejecución real):** Secuencia ilustrativa que distingue rollback obsoleto de fallo actual y explica cómo preservar la intención más reciente.
