---
name: g05-watchparty-decision-handover-brief
description: "Sintetiza decisiones técnicas vigentes para traspasos del PO al equipo. Usar cuando hay ADRs, issues y conversaciones contradictorias."
metadata:
  tipo: skill
  area: ["gestion","documentacion"]
  fase: [analisis, revision]
  tecnologias: ["agnostico"]
  herramientas: [claude-code, cursor, codex, otra]
  requiere: []
  grupo: "05"
  autor:
    nombre: Ramiro Castro Martínez
    github: rcastromartinez
  responsables: [rcastromartinez]
  madurez: experimental
---

# g05-watchparty-decision-handover-brief

## Objetivo
Producir un resumen trazable de decisiones, propuestas y dudas sin alterar documentación.

## Activación
Sintetiza decisiones técnicas vigentes para traspasos del PO al equipo. Usar cuando hay ADRs, issues y conversaciones contradictorias.

## Entradas
Fragmentos de código o documentación pertinentes, reglas esperadas y ejemplos anonimizados.
Solicitar únicamente los datos que bloqueen el análisis. Si falta evidencia, continuar con alcance parcial declarado.

## Procedimiento
1. Delimitar tema y reunir fuentes aportadas con fecha, autor o estado si constan.
2. Extraer decisiones explícitas, justificación, alternativas descartadas y consecuencias.
3. Comparar cronología y autoridad documentada; no interpretar silencio ni PR abierto como aprobación.
4. Registrar contradicciones con citas breves y separar vigente, propuesta, sustituida y pendiente.
5. Redactar siguiente acción sugerida y pregunta concreta para cada bloqueo, sin asignar personas ni crear tickets.

## Validaciones
- Leer instrucciones del repositorio y fuentes aportadas dentro del alcance autorizado.
- Asociar cada hallazgo a archivo y línea, documento o evento verificable. No inventar referencias.
- Diferenciar hechos observados, hipótesis y ejemplos. Marcar no verificable cuando falte evidencia.
- Comprobar que la salida respete las reglas vigentes sin añadir funcionalidad.
- Identificar cobertura analizada y límites antes de emitir conclusiones.
- Si se consulta documentación externa, usar la fuente oficial vigente y citarla. No requerir conexiones externas para trabajar con material suministrado.

## Salida esperada
Resumen de traspaso y tabla decisión / estado / fuente / consecuencia / duda.
Cerrar con pendientes y limitaciones. Si no hay hallazgos, indicar el alcance inspeccionado; no certificar ausencia de defectos.

## Restricciones
Trabajar en modo de solo lectura. No modificar código, tickets, PRs, datos, permisos, configuraciones o recursos existentes. No ejecutar migraciones, despliegues, peticiones de escritura o automatizaciones. No publicar comentarios ni crear tickets. Entregar propuestas para revisión humana. No copiar secretos ni datos personales; usar muestras ficticias o anonimizadas. No instalar dependencias ni ejecutar scripts del proyecto sin verificar su alcance y obtener autorización cuando excedan esta lectura.

## Autoría y estado
Autor: Ramiro Castro Martínez (GitHub: rcastromartinez). Grupo: 05 — WatchParty. Responsable: rcastromartinez. Madurez: experimental; sin ejecución funcional acreditada.

## Ejemplo de uso
**Pedido:** Resumí el contrato de chat con un ADR aprobado y un issue posterior que propone cambiarlo.

**Resultado esperado (ilustrativo, no ejecución real):** Resumen que conserva el ADR como decisión confirmada y marca el issue como propuesta hasta evidencia de aprobación.
