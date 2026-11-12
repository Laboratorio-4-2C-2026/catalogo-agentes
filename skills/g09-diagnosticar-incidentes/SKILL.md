---
name: g09-diagnosticar-incidentes
description: Investiga fallas de Zervi o Conexia correlacionando síntomas, logs, requests, configuración y cambios recientes para reconstruir la secuencia del incidente y contrastar hipótesis de causa. Usar cuando hay errores, degradación o un comportamiento intermitente que necesita diagnóstico; entrega evidencias, comprobaciones pendientes y acciones propuestas para recuperación y prevención.
metadata:
  tipo: skill
  area:
  - backend
  - frontend
  - devops
  - qa
  fase:
  - mantenimiento
  tecnologias:
  - agnostico
  metodologia:
  - agnostico
  herramientas:
  - codex
  requiere: []
  grupo: "09"
  autor:
    nombre: Xoaquin Sanchez Varsallona
    github: XoaquinSanchezVarsallona
  responsables:
  - XoaquinSanchezVarsallona
  madurez: experimental
  relacionados:
  - g09-verificar-despliegue
  - g09-qa-funcional-navegador
  - g09-analista-impacto-cambios
  - g09-redactar-tickets-tecnicos
  - g09-debug-local-integration
  - g12-reportar-incidente
---
# Diagnóstico de incidentes

Investigá por qué falla un comportamiento y qué evidencia permite distinguir las causas posibles. Entregá un diagnóstico que otro integrante pueda continuar, incluso si faltan logs o acceso al ambiente.

## Delimitar el incidente

Identificá proyecto, ambiente, síntoma observado, resultado esperado, primera y última ocurrencia conocidas y alcance reportado. Recuperá del contexto disponible URL o endpoint, método, status code, rol, pasos de reproducción y request/correlation ID cuando existan. Pedí solo los datos imprescindibles que no puedas obtener de las fuentes disponibles; mientras tanto, analizá lo que sí esté confirmado.

Registrá la revisión del código inspeccionado y la versión desplegada si se conoce. No atribuyas el código local al ambiente afectado sin evidencia. Por defecto consultá los originales actuales en `zervi/Zervi` o `conexia`; las copias de `agentes/fuentes/` son antecedentes. Leé las instrucciones del proyecto y, para despliegues de Zervi, el runbook actual si está disponible.

## Reconstruir lo ocurrido

1. Armá una línea de tiempo con fuente, timestamp y zona horaria. Conservá la incertidumbre cuando los relojes difieran o los logs no tengan zona. Distinguí el momento del evento del momento en que fue reportado.
2. Seguí la operación fallida desde navegador/cliente hasta API, servicio, persistencia e integración externa según corresponda. Usá IDs de correlación; si solo coinciden ruta y hora, describí el vínculo como probable. Un 502 del proxy no identifica por sí solo qué componente falló.
3. Compará una ejecución fallida con una exitosa equivalente cuando exista. Buscá diferencias concretas de versión, instancia, payload, rol, datos, configuración o dependencia; un health check exitoso no prueba que el recorrido afectado funcione.
4. Revisá cambios cercanos al inicio: commits, despliegues, migraciones, variables y dependencias. La cercanía temporal habilita una hipótesis, pero no demuestra causalidad. Separá síntomas posteriores de la falla inicial y de condiciones que amplificaron el impacto.
5. Conservá referencias a archivos y líneas, fragmentos de logs o consultas usadas. Mostrá solo los campos necesarios y ocultá tokens, cookies, credenciales y datos personales en los ejemplos del informe.

Si no hay acceso remoto, trabajá con los logs o exportaciones proporcionados y el código disponible. Declaralo: la ausencia de un error en una muestra parcial no demuestra que no haya ocurrido.

## Contrastar hipótesis

Para cada hipótesis relevante indicá el mecanismo que explicaría el síntoma, la evidencia a favor, la evidencia en contra y una comprobación que permita distinguirla de las alternativas. Priorizá las comprobaciones según su poder para resolver la duda y su costo; evitá listas genéricas de causas sin conexión con el caso.

Podés ejecutar lecturas y reproducciones locales acordes con el pedido. Usá datos sintéticos y un entorno aislado para reproducciones con escrituras; una configuración que apunta a producción no sirve como entorno de prueba. No reinicies servicios, cambies variables, ejecutes migraciones, publiques correcciones ni generes tráfico de carga como parte del diagnóstico. Si una acción operativa resulta necesaria, describí la acción concreta, su efecto y cómo se verificaría para que el usuario pueda autorizarla.

Marcá cada hipótesis como confirmada, probable, descartada o pendiente. Para confirmar una causa, mostrá una reproducción controlada o evidencia directa del mecanismo de falla; un mensaje genérico o la desaparición del síntoma tras reiniciar no bastan. Si los datos no alcanzan, entregá las hipótesis abiertas y el siguiente dato discriminante sin inventar una causa raíz.

## Recuperación y prevención

Separá acciones de contención, corrección del mecanismo y prevención de recurrencia. Para cada propuesta indicá qué evidencia la justifica, riesgos relevantes y cómo verificar el resultado en el recorrido afectado. Una mitigación puede recuperar el servicio sin resolver la causa.

Si proponés rollback, verificá primero qué versión se recuperaría y qué se sabe de la compatibilidad del esquema y los datos. No lo presentes como seguro cuando esa compatibilidad sea desconocida. No marques una acción como ejecutada ni una recuperación como comprobada si solo fueron propuestas.

Derivá el trabajo según el resultado: el redactor de tickets puede convertir una corrección identificada en una tarea; el analista de impacto puede evaluar sus consumidores; QA puede verificar la corrección y regresiones; el verificador de despliegue puede comprobar la versión publicada. `g09-debug-local-integration` se concentra en la integración local y `g12-reportar-incidente` en registrar el incidente: esta pieza produce el diagnóstico técnico. Preparar esos insumos no crea tickets ni publica reportes automáticamente.

## Entrega

Abrí con el síntoma, el impacto conocido y el estado del diagnóstico. Incluí:

- Ambiente, versiones verificadas, ventana temporal y fuentes consultadas.
- Línea de tiempo de eventos con sus evidencias y huecos.
- Hipótesis, estado de cada una, evidencia y comprobación discriminante.
- Causa confirmada o probable, condiciones contribuyentes y limitaciones.
- Acciones propuestas de contención, corrección y prevención, con su validación.

Distinguí el impacto observado del reportado y del todavía desconocido. El diagnóstico queda listo para continuar cuando cada conclusión material tiene una fuente y cada incertidumbre que condiciona la recuperación tiene un próximo paso concreto.

## Ejemplo de uso

**Pedido:** Desde el despliegue de Zervi de las 14:10 aparecen 502 intermitentes al consultar turnos. Revisá estos logs del proxy y de la API, junto con los dos SHA, y decime qué comprobar antes de decidir un rollback.

**Resultado:** Una línea de tiempo con zona horaria y requests correlacionados, una comparación de casos exitosos y fallidos y las hipótesis respaldadas por los logs. Si la muestra no identifica la causa, la deja pendiente y precisa qué dato de instancia, versión o conexión falta. Propone contención y verificaciones del recorrido de turnos, e indica qué compatibilidad de migraciones habría que comprobar antes de un rollback, sin ejecutarlo.
