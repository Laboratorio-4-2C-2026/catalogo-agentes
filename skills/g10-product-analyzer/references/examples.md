# Ejemplos de entrada y salida

Son casos hipotéticos de criterio, no datos del proyecto actual. Los nombres de entidades son ilustrativos. No afirmar que se inspeccionaron o probaron fuera de estos ejemplos.

## Creación existente; listado ausente

**Entrada:** "Analizá qué falta en intenciones de viaje". Evidencia aportada: formulario de TravelIntent conectado a un endpoint de creación, prueba de creación exitosa; no se aportó evidencia de listado.

**Salida:** "Hecho: la creación funciona según la prueba aportada. Incertidumbre: no se verificó cómo se consultan o administran las intenciones. Recomiendo comprobar listado y usos antes de decidir un cambio. No conviene reimplementar la creación. Prioridad del posible listado: pendiente de conocer su impacto y verificar la ausencia".

La misma conclusión requiere más cautela si solo hay código: integración aparente, funcionamiento no ejecutado. No convertir "no se aportó evidencia de listado" en "no existe listado".

## Conservación de información histórica

**Entrada:** TripPassenger vincula usuario y viaje; al aceptar un match no copia el origen y destino acordados. El recorrido del viaje se puede editar después. Se aporta el esquema y el flujo de aceptación, pero no una prueba de pérdida histórica.

**Salida:** "Hecho: el modelo y el flujo inspeccionados no conservan una instantánea del acuerdo. Inferencia/riesgo: una edición posterior podría impedir reconstruir el acuerdo original. Impacto: disputas o visualización histórica incorrecta. Recomiendo comprobar si el historial existe en otra entidad y, si no, persistir el acuerdo reutilizando el modelo actual cuando resulte compatible. Prioridad sugerida: alta si el acuerdo histórico es requisito de negocio; confirmar ese requisito. Esfuerzo: no estimado".

No afirmar que ya se perdió información ni exigir una tabla nueva antes de inspeccionar las alternativas.

## Pantalla con mocks

**Entrada:** pantalla Matches renderizada con un arreglo local; endpoints de consulta documentados, sin evidencia de uso desde la pantalla.

**Salida:** "Hecho: existe UI visual y datos locales; la pantalla inspeccionada no consume los endpoints. Incertidumbre: vigencia, permisos y comportamiento real de esa API. Gap de integración en esta pantalla: demostrado por su fuente de datos. Recomiendo verificar el contrato y conectar la UI existente si la API cubre el flujo. Preservar la pantalla y el backend aprovechables. La documentación del endpoint por sí sola no demuestra que esté operativo".

## Producto correcto

**Entrada:** flujo de reserva con permisos, persistencia, confirmación y cancelación probados en el entorno indicado; no hay desvíos del objetivo acordado.

**Salida:** "No se identifican gaps en el alcance evaluado. Conservar el flujo actual. Las posibles extensiones no justifican cambios sin un objetivo nuevo". No generar mejoras ni tickets para llenar el informe.
