# Ejemplos de entrada y salida

Casos ilustrativos; no fijan proveedores, arquitectura ni condiciones comerciales universales.

## Proveedor de geolocalización y restricción de acceso

**Entrada:** "Evaluamos Google Maps y Geoapify. El equipo eligió el nivel gratuito de Geoapify porque quería evitar registrar tarjeta. Observamos coordenadas distintas para un texto igual. Separamos el proveedor con una abstracción de geolocalización y Strategy; no implementamos el proveedor Maps. Reconstruí la decisión sin consultar servicios".

**Salida esperada:** reconstrucción con fecha actual, selección y restricción atribuidas al relato, no afirmaciones sobre condiciones comerciales vigentes. Comparación con datos desconocidos explícitos, tradeoff operativo/calidad y variabilidad reportada sin diagnóstico causal. Contrato común e implementación existente como evidencia actual si se inspeccionaron. Sustitución prevista por diseño, con adaptación y comprobaciones pendientes para el proveedor no implementado.

No afirmar que Maps fue probado, que ambos son equivalentes o que la variación ocurre siempre. Una prueba futura debería controlar request completo, parámetros y contexto; no inventar resultados. Si se pide elegir hoy, verificar condiciones oficiales actuales antes de basar la recomendación en acceso o precio.

## Restricciones excluyentes antes de puntuar

**Entrada:** "Necesitamos un motor de búsqueda local sin enviar documentos a terceros. Opción A se ejecuta localmente y hay una prueba aportada con los filtros requeridos. Opción B solo ofrece API remota según documentación aportada. Trabajá offline con estas fuentes fechadas".

**Salida esperada:** B no cumple el requisito excluyente con la evidencia disponible, aunque pudiera tener ventajas en otros criterios. A es recomendación condicionada al alcance de la prueba y requisitos restantes. No inventar benchmarks, costos ni una matriz de puntajes; indicar antigüedad y límites de los extractos. No exigir abrir una cuenta para completar una comparación documental.

## Conservar la solución actual

**Entrada:** "El proveedor actual cumple las pruebas de precisión y el volumen acordado. No hay problemas observados. ¿Conviene cambiar porque apareció una librería nueva?".

**Salida esperada:** no hay un beneficio demostrado que justifique el costo y riesgo del cambio. Recomendar conservar la solución actual dentro del alcance probado, identificar qué necesidad futura podría reabrir la decisión y dejar costos de migración sin cifra si no fueron estimados. No inventar un requisito para justificar el reemplazo.
