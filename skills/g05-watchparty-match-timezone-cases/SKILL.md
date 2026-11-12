---
name: g05-watchparty-match-timezone-cases
description: "Diseña casos de fechas y zonas horarias para listados de partidos. Usar ante horarios incorrectos o agrupaciones por día inconsistentes."
metadata:
  tipo: skill
  area: ["frontend","qa"]
  fase: [analisis, revision]
  tecnologias: ["typescript"]
  herramientas: [claude-code, cursor, codex, otra]
  requiere: []
  grupo: "05"
  autor:
    nombre: Ramiro Castro Martínez
    github: rcastromartinez
  responsables: [rcastromartinez]
  madurez: experimental
---

# g05-watchparty-match-timezone-cases

## Objetivo
Definir cómo verificar instantes, presentación local y filtros de fecha.

## Activación
Diseña casos de fechas y zonas horarias para listados de partidos. Usar ante horarios incorrectos o agrupaciones por día inconsistentes.

## Entradas
Fragmentos de código o documentación pertinentes, reglas esperadas y ejemplos anonimizados.
Solicitar únicamente los datos que bloqueen el análisis. Si falta evidencia, continuar con alcance parcial declarado.

## Procedimiento
1. Identificar formato recibido, zona del proveedor, zona de usuario y regla de agrupación vigente.
2. Seguir el dato desde parseo hasta formato y filtro; distinguir instante UTC de fecha civil.
3. Construir casos en cruce de medianoche, offset positivo/negativo, cambio horario y fecha sin zona.
4. Para cada caso fijar instante ISO con offset, zona IANA y fecha/hora esperada; calcular sin depender de zona de la máquina.
5. Detectar parseos ambiguos y definir preguntas bloqueantes antes de sugerir cambios.

## Validaciones
- Leer instrucciones del repositorio y fuentes aportadas dentro del alcance autorizado.
- Asociar cada hallazgo a archivo y línea, documento o evento verificable. No inventar referencias.
- Diferenciar hechos observados, hipótesis y ejemplos. Marcar no verificable cuando falte evidencia.
- Comprobar que la salida respete las reglas vigentes sin añadir funcionalidad.
- Identificar cobertura analizada y límites antes de emitir conclusiones.
- Si se consulta documentación externa, usar la fuente oficial vigente y citarla. No requerir conexiones externas para trabajar con material suministrado.

## Salida esperada
Tabla entrada ISO / zona / día esperado / hora esperada / capa revisada y vacíos de especificación.
Cerrar con pendientes y limitaciones. Si no hay hallazgos, indicar el alcance inspeccionado; no certificar ausencia de defectos.

## Restricciones
Trabajar en modo de solo lectura. No modificar código, tickets, PRs, datos, permisos, configuraciones o recursos existentes. No ejecutar migraciones, despliegues, peticiones de escritura o automatizaciones. No publicar comentarios ni crear tickets. Entregar propuestas para revisión humana. No copiar secretos ni datos personales; usar muestras ficticias o anonimizadas. No instalar dependencias ni ejecutar scripts del proyecto sin verificar su alcance y obtener autorización cuando excedan esta lectura.

## Autoría y estado
Autor: Ramiro Castro Martínez (GitHub: rcastromartinez). Grupo: 05 — WatchParty. Responsable: rcastromartinez. Madurez: experimental; sin ejecución funcional acreditada.

## Ejemplo de uso
**Pedido:** Diseñá casos para un partido a las 00:30Z visto desde Buenos Aires.

**Resultado esperado (ilustrativo, no ejecución real):** Caso ilustrativo: 2026-11-06T00:30:00Z corresponde al 5 de noviembre a las 21:30 en America/Argentina/Buenos_Aires.
