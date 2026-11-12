---
name: g05-watchparty-room-permission-matrix
description: "Construye una matriz de permisos por sala para endpoints y eventos. Usar al definir acceso de visitante, miembro y moderador."
metadata:
  tipo: skill
  area: ["seguridad","backend"]
  fase: [analisis, revision]
  tecnologias: ["typescript","supabase"]
  herramientas: [claude-code, cursor, codex, otra]
  requiere: []
  grupo: "05"
  autor:
    nombre: Ramiro Castro Martínez
    github: rcastromartinez
  responsables: [rcastromartinez]
  madurez: experimental
---

# g05-watchparty-room-permission-matrix

## Objetivo
Contrastar acciones permitidas con controles de servidor observables.

## Activación
Construye una matriz de permisos por sala para endpoints y eventos. Usar al definir acceso de visitante, miembro y moderador.

## Entradas
Fragmentos de código o documentación pertinentes, reglas esperadas y ejemplos anonimizados.
Solicitar únicamente los datos que bloqueen el análisis. Si falta evidencia, continuar con alcance parcial declarado.

## Procedimiento
1. Extraer roles y reglas de las fuentes aportadas; no inventar moderadores ni salas privadas.
2. Enumerar acciones reales: leer, ingresar, publicar, borrar o moderar solo cuando existan.
3. Cruzar rol, pertenencia, recurso y estado de sesión en una matriz permitir/denegar/pendiente.
4. Ubicar control efectivo en middleware, handler o política; una ocultación de UI no prueba autorización.
5. Diseñar casos de usuario A contra recurso de B y sesión revocada sin ejecutarlos ni solicitar tokens.

## Validaciones
- Leer instrucciones del repositorio y fuentes aportadas dentro del alcance autorizado.
- Asociar cada hallazgo a archivo y línea, documento o evento verificable. No inventar referencias.
- Diferenciar hechos observados, hipótesis y ejemplos. Marcar no verificable cuando falte evidencia.
- Comprobar que la salida respete las reglas vigentes sin añadir funcionalidad.
- Identificar cobertura analizada y límites antes de emitir conclusiones.
- Si se consulta documentación externa, usar la fuente oficial vigente y citarla. No requerir conexiones externas para trabajar con material suministrado.

## Salida esperada
Matriz rol / acción / condición / decisión / control / evidencia y casos negativos propuestos.
Cerrar con pendientes y limitaciones. Si no hay hallazgos, indicar el alcance inspeccionado; no certificar ausencia de defectos.

## Restricciones
Trabajar en modo de solo lectura. No modificar código, tickets, PRs, datos, permisos, configuraciones o recursos existentes. No ejecutar migraciones, despliegues, peticiones de escritura o automatizaciones. No publicar comentarios ni crear tickets. Entregar propuestas para revisión humana. No copiar secretos ni datos personales; usar muestras ficticias o anonimizadas. No instalar dependencias ni ejecutar scripts del proyecto sin verificar su alcance y obtener autorización cuando excedan esta lectura.

## Autoría y estado
Autor: Ramiro Castro Martínez (GitHub: rcastromartinez). Grupo: 05 — WatchParty. Responsable: rcastromartinez. Madurez: experimental; sin ejecución funcional acreditada.

## Ejemplo de uso
**Pedido:** Armá una matriz para borrar comentarios propios y ajenos según estas reglas.

**Resultado esperado (ilustrativo, no ejecución real):** Matriz basada en reglas suministradas; permisos no documentados quedan pendientes, sin inferir acceso.
