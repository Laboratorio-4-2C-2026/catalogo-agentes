---
name: g05-watchparty-cursor-pagination-consistency
description: "Analiza continuidad y duplicados de paginación por cursor en feeds y comentarios. Usar al revisar cursores, orden estable o carga incremental."
metadata:
  tipo: skill
  area: ["backend","datos"]
  fase: [analisis, revision]
  tecnologias: ["typescript","postgresql"]
  herramientas: [claude-code, cursor, codex, otra]
  requiere: []
  grupo: "05"
  autor:
    nombre: Ramiro Castro Martínez
    github: rcastromartinez
  responsables: [rcastromartinez]
  madurez: experimental
---

# g05-watchparty-cursor-pagination-consistency

## Objetivo
Determinar si páginas consecutivas conservan identidad y continuidad bajo inserciones.

## Activación
Analiza continuidad y duplicados de paginación por cursor en feeds y comentarios. Usar al revisar cursores, orden estable o carga incremental.

## Entradas
Fragmentos de código o documentación pertinentes, reglas esperadas y ejemplos anonimizados.
Solicitar únicamente los datos que bloqueen el análisis. Si falta evidencia, continuar con alcance parcial declarado.

## Procedimiento
1. Identificar filtros, orden completo, tamaño de página y formato de cursor.
2. Comprobar desempate por clave única y coherencia entre comparación del cursor y orden ascendente o descendente.
3. Construir conjunto mínimo con timestamps iguales e inserción entre páginas.
4. Simular página inicial, siguiente, final, cursor inválido y cambio de filtros.
5. Distinguir semántica live de snapshot; documentar qué consistencia garantiza realmente el contrato.

## Validaciones
- Leer instrucciones del repositorio y fuentes aportadas dentro del alcance autorizado.
- Asociar cada hallazgo a archivo y línea, documento o evento verificable. No inventar referencias.
- Diferenciar hechos observados, hipótesis y ejemplos. Marcar no verificable cuando falte evidencia.
- Comprobar que la salida respete las reglas vigentes sin añadir funcionalidad.
- Identificar cobertura analizada y límites antes de emitir conclusiones.
- Si se consulta documentación externa, usar la fuente oficial vigente y citarla. No requerir conexiones externas para trabajar con material suministrado.

## Salida esperada
Dataset mínimo, páginas esperadas y tabla duplicados / omisiones / causa / corrección propuesta.
Cerrar con pendientes y limitaciones. Si no hay hallazgos, indicar el alcance inspeccionado; no certificar ausencia de defectos.

## Restricciones
Trabajar en modo de solo lectura. No modificar código, tickets, PRs, datos, permisos, configuraciones o recursos existentes. No ejecutar migraciones, despliegues, peticiones de escritura o automatizaciones. No publicar comentarios ni crear tickets. Entregar propuestas para revisión humana. No copiar secretos ni datos personales; usar muestras ficticias o anonimizadas. No instalar dependencias ni ejecutar scripts del proyecto sin verificar su alcance y obtener autorización cuando excedan esta lectura.

## Autoría y estado
Autor: Ramiro Castro Martínez (GitHub: rcastromartinez). Grupo: 05 — WatchParty. Responsable: rcastromartinez. Madurez: experimental; sin ejecución funcional acreditada.

## Ejemplo de uso
**Pedido:** Revisá un cursor que solo guarda created_at cuando dos comentarios tienen la misma fecha.

**Resultado esperado (ilustrativo, no ejecución real):** Contraejemplo ilustrativo con empate temporal y propuesta de cursor compuesto, sin consultas a producción.
