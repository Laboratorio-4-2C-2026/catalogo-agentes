## Ejemplo de uso

**Pedido:** La dev abre el PR #46 (`SCRUM-75`, drawer de razonamiento) en `vaiven-app` y pide review a `@vaivendev`.

**Resultado:** El workflow del repo de producto dispara `revisar-pr.yml` en el repo del bot, que publica una review con `event=COMMENT`: criterios del ticket marcados cumple / no cumple / sin evidencia (detectó que el criterio «se agranda arrastrándolo» no se cumplía), hallazgos de lógica y seguridad, el estado de cada ítem de la DoD y la lista de documentos del kit que usó. En el dry-run, el filtro bajó de 10 a 5 comentarios con los mismos hallazgos de fondo.
