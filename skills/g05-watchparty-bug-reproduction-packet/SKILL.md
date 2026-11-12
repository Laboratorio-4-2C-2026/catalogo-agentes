---
name: g05-watchparty-bug-reproduction-packet
description: "Transforma reportes ambiguos de errores en paquetes mínimos de reproducción. Usar antes de derivar un bug difícil de reproducir."
metadata:
  tipo: skill
  area: ["qa","gestion"]
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

# g05-watchparty-bug-reproduction-packet

## Objetivo
Entregar pasos observables y evidencia suficiente para investigar sin editar tickets.

## Activación
Transforma reportes ambiguos de errores en paquetes mínimos de reproducción. Usar antes de derivar un bug difícil de reproducir.

## Entradas
Fragmentos de código o documentación pertinentes, reglas esperadas y ejemplos anonimizados.
Solicitar únicamente los datos que bloqueen el análisis. Si falta evidencia, continuar con alcance parcial declarado.

## Procedimiento
1. Separar observación, expectativa y explicación hipotética del reportante.
2. Registrar versión, entorno, navegador, precondiciones y datos anonimizados disponibles.
3. Reducir a pasos deterministas numerados con resultado esperado y observado.
4. Identificar variables de control y proponer una reducción por vez; no afirmar reproducción si no ocurrió.
5. Listar evidencia faltante, frecuencia y alcance; redactar paquete listo para copiar.

## Validaciones
- Leer instrucciones del repositorio y fuentes aportadas dentro del alcance autorizado.
- Asociar cada hallazgo a archivo y línea, documento o evento verificable. No inventar referencias.
- Diferenciar hechos observados, hipótesis y ejemplos. Marcar no verificable cuando falte evidencia.
- Comprobar que la salida respete las reglas vigentes sin añadir funcionalidad.
- Identificar cobertura analizada y límites antes de emitir conclusiones.
- Si se consulta documentación externa, usar la fuente oficial vigente y citarla. No requerir conexiones externas para trabajar con material suministrado.

## Salida esperada
Título, entorno, precondiciones, pasos, esperado/observado, evidencia, hipótesis y dudas.
Cerrar con pendientes y limitaciones. Si no hay hallazgos, indicar el alcance inspeccionado; no certificar ausencia de defectos.

## Restricciones
Trabajar en modo de solo lectura. No modificar código, tickets, PRs, datos, permisos, configuraciones o recursos existentes. No ejecutar migraciones, despliegues, peticiones de escritura o automatizaciones. No publicar comentarios ni crear tickets. Entregar propuestas para revisión humana. No copiar secretos ni datos personales; usar muestras ficticias o anonimizadas. No instalar dependencias ni ejecutar scripts del proyecto sin verificar su alcance y obtener autorización cuando excedan esta lectura.

## Autoría y estado
Autor: Ramiro Castro Martínez (GitHub: rcastromartinez). Grupo: 05 — WatchParty. Responsable: rcastromartinez. Madurez: experimental; sin ejecución funcional acreditada.

## Ejemplo de uso
**Pedido:** Convertí 'el chat a veces queda cargando después de volver' en un reporte reproducible.

**Resultado esperado (ilustrativo, no ejecución real):** Paquete que solicita duración, secuencia de navegación y estado de conexión; declara reproducción no realizada.
