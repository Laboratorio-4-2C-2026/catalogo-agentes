---
name: g05-watchparty-acceptance-evidence-map
description: "Mapea criterios de aceptación a evidencia de una entrega. Usar cuando el PO debe distinguir cumplimiento demostrado y pendientes."
metadata:
  tipo: skill
  area: ["gestion","qa"]
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

# g05-watchparty-acceptance-evidence-map

## Objetivo
Evaluar cobertura de una entrega sin aprobar PRs ni cambiar estados.

## Activación
Mapea criterios de aceptación a evidencia de una entrega. Usar cuando el PO debe distinguir cumplimiento demostrado y pendientes.

## Entradas
Fragmentos de código o documentación pertinentes, reglas esperadas y ejemplos anonimizados.
Solicitar únicamente los datos que bloqueen el análisis. Si falta evidencia, continuar con alcance parcial declarado.

## Procedimiento
1. Descomponer criterios compuestos en resultados observables conservando texto e identificador originales.
2. Vincular cada resultado con demo, captura, prueba, código o registro suministrado y su versión.
3. Clasificar demostrado, contradicho o no verificable según fuerza y alcance de la evidencia.
4. Distinguir existencia de una prueba, ejecución exitosa y validez para el criterio.
5. Presentar brechas y comprobación mínima pendiente sin añadir requisitos al alcance.

## Validaciones
- Leer instrucciones del repositorio y fuentes aportadas dentro del alcance autorizado.
- Asociar cada hallazgo a archivo y línea, documento o evento verificable. No inventar referencias.
- Diferenciar hechos observados, hipótesis y ejemplos. Marcar no verificable cuando falte evidencia.
- Comprobar que la salida respete las reglas vigentes sin añadir funcionalidad.
- Identificar cobertura analizada y límites antes de emitir conclusiones.
- Si se consulta documentación externa, usar la fuente oficial vigente y citarla. No requerir conexiones externas para trabajar con material suministrado.

## Salida esperada
Tabla criterio / evidencia / versión / estado / limitación / comprobación pendiente.
Cerrar con pendientes y limitaciones. Si no hay hallazgos, indicar el alcance inspeccionado; no certificar ausencia de defectos.

## Restricciones
Trabajar en modo de solo lectura. No modificar código, tickets, PRs, datos, permisos, configuraciones o recursos existentes. No ejecutar migraciones, despliegues, peticiones de escritura o automatizaciones. No publicar comentarios ni crear tickets. Entregar propuestas para revisión humana. No copiar secretos ni datos personales; usar muestras ficticias o anonimizadas. No instalar dependencias ni ejecutar scripts del proyecto sin verificar su alcance y obtener autorización cuando excedan esta lectura.

## Autoría y estado
Autor: Ramiro Castro Martínez (GitHub: rcastromartinez). Grupo: 05 — WatchParty. Responsable: rcastromartinez. Madurez: experimental; sin ejecución funcional acreditada.

## Ejemplo de uso
**Pedido:** Mapeá estos cinco criterios a las capturas y resultados de tests de la entrega.

**Resultado esperado (ilustrativo, no ejecución real):** Mapa ilustrativo con estados justificados; una captura de login no demuestra autorización de endpoints.
