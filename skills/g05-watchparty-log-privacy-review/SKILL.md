---
name: g05-watchparty-log-privacy-review
description: "Revisa fragmentos de logs de autenticación y chat para minimizar datos sensibles. Usar antes de compartir trazas o instrumentar eventos."
metadata:
  tipo: skill
  area: ["seguridad","devops"]
  fase: [analisis, revision]
  tecnologias: ["typescript","nodejs"]
  herramientas: [claude-code, cursor, codex, otra]
  requiere: []
  grupo: "05"
  autor:
    nombre: Ramiro Castro Martínez
    github: rcastromartinez
  responsables: [rcastromartinez]
  madurez: experimental
---

# g05-watchparty-log-privacy-review

## Objetivo
Proponer observabilidad útil sin exponer contenido de mensajes ni credenciales.

## Activación
Revisa fragmentos de logs de autenticación y chat para minimizar datos sensibles. Usar antes de compartir trazas o instrumentar eventos.

## Entradas
Fragmentos de código o documentación pertinentes, reglas esperadas y ejemplos anonimizados.
Solicitar únicamente los datos que bloqueen el análisis. Si falta evidencia, continuar con alcance parcial declarado.

## Procedimiento
1. Identificar campos de logs, destino, propósito y retención conocida; trabajar con muestras anonimizadas.
2. Clasificar tokens, cookies, passwords, email, IDs y texto de chat según necesidad diagnóstica.
3. Rastrear serialización de request, response y error para detectar filtraciones indirectas.
4. Proponer redacción por campo y correlación con identificadores de operación, sin copiar valores sensibles.
5. Comparar muestra antes/después mediante marcadores ficticios y señalar capacidad diagnóstica preservada.

## Validaciones
- Leer instrucciones del repositorio y fuentes aportadas dentro del alcance autorizado.
- Asociar cada hallazgo a archivo y línea, documento o evento verificable. No inventar referencias.
- Diferenciar hechos observados, hipótesis y ejemplos. Marcar no verificable cuando falte evidencia.
- Comprobar que la salida respete las reglas vigentes sin añadir funcionalidad.
- Identificar cobertura analizada y límites antes de emitir conclusiones.
- Si se consulta documentación externa, usar la fuente oficial vigente y citarla. No requerir conexiones externas para trabajar con material suministrado.

## Salida esperada
Tabla campo / finalidad / riesgo / tratamiento y ejemplo redactado con datos ficticios.
Cerrar con pendientes y limitaciones. Si no hay hallazgos, indicar el alcance inspeccionado; no certificar ausencia de defectos.

## Restricciones
Trabajar en modo de solo lectura. No modificar código, tickets, PRs, datos, permisos, configuraciones o recursos existentes. No ejecutar migraciones, despliegues, peticiones de escritura o automatizaciones. No publicar comentarios ni crear tickets. Entregar propuestas para revisión humana. No copiar secretos ni datos personales; usar muestras ficticias o anonimizadas. No instalar dependencias ni ejecutar scripts del proyecto sin verificar su alcance y obtener autorización cuando excedan esta lectura.

## Autoría y estado
Autor: Ramiro Castro Martínez (GitHub: rcastromartinez). Grupo: 05 — WatchParty. Responsable: rcastromartinez. Madurez: experimental; sin ejecución funcional acreditada.

## Ejemplo de uso
**Pedido:** Revisá un logger que serializa headers de login y body de mensajes.

**Resultado esperado (ilustrativo, no ejecución real):** Propuesta ilustrativa que omite Authorization y contenido, conservando request_id, estado y duración.
