---
name: g04-load-testing
description: Prueba de carga de la API NestJS con el tráfico esperado para comprobar latencia p95 y tasa de errores, en un entorno local o de prueba. Usar cuando se pregunta si la API aguanta el uso previsto o antes de un release; para buscar el límite, usar stress testing.
metadata:
  tipo: skill
  area:
  - qa
  - backend
  fase:
  - testing
  tecnologias:
  - nestjs
  - k6
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: "04"
  autor:
    nombre: Alexander Köttner
    github: Alexander-Kottner
  responsables:
  - Alexander-Kottner
  madurez: experimental
  relacionados: []
---

# Load testing

Responde: **¿la API se comporta bien con la carga que esperamos?** Se mantiene una carga realista durante un tiempo; no se busca romperla.

## Seguridad

Correr solo contra el entorno local o un ambiente de prueba propio, con autorización del equipo. Nunca contra producción ni contra servicios de terceros (Vercel, Neon, Firebase): sus condiciones de uso limitan estas pruebas y consumen cuota real.

## Flujo

1. **Definir la carga esperada:** usuarios concurrentes, requests por usuario y duración. Si no hay datos, proponer un supuesto y dejarlo escrito.
2. **Definir umbrales antes de correr**, por ejemplo p95 por debajo del objetivo acordado y menos de 1% de errores. Alinearlos con los KPIs de latencia y errores del proyecto si existen.
3. **Elegir endpoints reales:** los flujos más usados, con la mezcla habitual de lectura y escritura.
4. **Preparar datos y autenticación:** usuarios de prueba y un volumen de datos realista. No poner tokens en el repo: usar variables de entorno.
5. **Escribir el script** con k6 (o la herramienta que ya tenga el proyecto): subida gradual, meseta de al menos 5 minutos y bajada, con `thresholds`.
6. **Medir una línea base** con poca carga y después correr la prueba. Registrar p50, p95, p99, requests por segundo, errores y uso de CPU, memoria y conexiones.
7. **Analizar:** si no cumple, buscar la causa (consultas lentas, N+1, conexiones). Proponer el arreglo.

## Salida

Supuestos, entorno, script, tabla contra umbrales, cuello de botella y recomendación. Aclarar que un resultado local no equivale a producción.

## Reglas

- Si hay que instalar una herramienta, avisar antes. No agregarla al proyecto sin acuerdo.
- No inventar resultados ni extrapolarlos más allá de lo medido.

## Ejemplo de uso
**Pedido:** Hacé un load test del listado de mantenimientos con 50 usuarios.

**Resultado:** Un script de k6 reproducible, los resultados de p50, p95, errores y requests por segundo contra los umbrales, y el cuello de botella si no cumple.
