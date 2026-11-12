---
name: g05-watchparty-release-demo-preflight
description: "Prepara un guion de demo verificable para una entrega académica. Usar antes de mostrar WatchParty al profesor."
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

# g05-watchparty-release-demo-preflight

## Objetivo
Preparar una demostración reproducible con alternativas seguras y evidencia vigente.

## Activación
Prepara un guion de demo verificable para una entrega académica. Usar antes de mostrar WatchParty al profesor.

## Entradas
Fragmentos de código o documentación pertinentes, reglas esperadas y ejemplos anonimizados.
Solicitar únicamente los datos que bloqueen el análisis. Si falta evidencia, continuar con alcance parcial declarado.

## Procedimiento
1. Identificar objetivo, audiencia, duración y funcionalidades efectivamente confirmadas.
2. Ordenar recorridos por valor observable y dependencias, con presupuesto de tiempo.
3. Para cada paso definir precondición, acción, señal visible de éxito y evidencia disponible.
4. Preparar alternativa con evidencia existente si falla un servicio; marcarla como grabación o captura.
5. Separar limitaciones conocidas y pendientes; no afirmar que una funcionalidad funciona sin evidencia.

## Validaciones
- Leer instrucciones del repositorio y fuentes aportadas dentro del alcance autorizado.
- Asociar cada hallazgo a archivo y línea, documento o evento verificable. No inventar referencias.
- Diferenciar hechos observados, hipótesis y ejemplos. Marcar no verificable cuando falte evidencia.
- Comprobar que la salida respete las reglas vigentes sin añadir funcionalidad.
- Identificar cobertura analizada y límites antes de emitir conclusiones.
- Si se consulta documentación externa, usar la fuente oficial vigente y citarla. No requerir conexiones externas para trabajar con material suministrado.

## Salida esperada
Guion temporizado, checklist de preparación y contingencias por recorrido.
Cerrar con pendientes y limitaciones. Si no hay hallazgos, indicar el alcance inspeccionado; no certificar ausencia de defectos.

## Restricciones
Trabajar en modo de solo lectura. No modificar código, tickets, PRs, datos, permisos, configuraciones o recursos existentes. No ejecutar migraciones, despliegues, peticiones de escritura o automatizaciones. No publicar comentarios ni crear tickets. Entregar propuestas para revisión humana. No copiar secretos ni datos personales; usar muestras ficticias o anonimizadas. No instalar dependencias ni ejecutar scripts del proyecto sin verificar su alcance y obtener autorización cuando excedan esta lectura.

## Autoría y estado
Autor: Ramiro Castro Martínez (GitHub: rcastromartinez). Grupo: 05 — WatchParty. Responsable: rcastromartinez. Madurez: experimental; sin ejecución funcional acreditada.

## Ejemplo de uso
**Pedido:** Armá una demo de seis minutos de login, partidos y chat con alternativa si no hay conexión.

**Resultado esperado (ilustrativo, no ejecución real):** Guion ilustrativo que reserva tiempos y usa capturas identificadas como tales, sin crear cuentas o datos.
