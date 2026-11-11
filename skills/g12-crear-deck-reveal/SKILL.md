---
name: g12-crear-deck-reveal
description: Crea o actualiza presentaciones HTML con Reveal.js a partir de un brief y fuentes, adaptando narrativa, identidad visual, notas y exportación a la audiencia y al proyecto. Usar al preparar un steering, una demo o una propuesta que se presenta con diapositivas.
metadata:
  tipo: skill
  area:
  - documentacion
  - gestion
  fase:
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - codex
  - otra
  requiere: []
  grupo: '12'
  autor:
    nombre: Marcos Hussey
    github: husseymarcos
  responsables:
  - husseymarcos
  madurez: usado-en-proyecto
  relacionados:
  - g12-preparar-demo
---

# Crear deck con Reveal.js

Convertir material del proyecto en un deck HTML editable, listo para exponer.
Ejemplo: `/crear-deck-reveal demo de producto, 10 minutos, identidad del sitio adjunto`.
Usar el idioma del brief o del solicitante.

## Brief y fuentes

Determinar audiencia, propósito, duración, formato de entrega, fecha de corte y si se
requiere uso offline. Consultar instrucciones del destino y fuentes aportadas. Buscar
decks previos, identidad visual y feedback cuando existan, sin exigir rutas de un
proyecto específico. Si falta una referencia, avanzar con una propuesta explícita de estilo.

Sustentar cifras, responsables y estados en fuentes vigentes. Registrar archivo o URL y
fecha en notas o un apéndice. Marcar faltantes como `Por confirmar`; un deck anterior
sirve como referencia visual, no como prueba del estado actual.

## Narrativa

Cada slide comunica una idea con título concreto y evidencia visual; trasladar el
desarrollo a las notas. Ajustar cantidad y secuencia al tiempo disponible y al objetivo.

- **Seguimiento de proyecto:** resultados, cambios, decisiones, demo, alcance,
  cronograma, costos, riesgos y próximos pasos según lo que necesite la audiencia.
- **Demo de producto:** problema, recorrido, valor comprobable y cierre; identificar
  prototipos y diferenciar capacidad implementada de planes.
- **Propuesta o decisión:** contexto, opciones, recomendación, consecuencias y pedido
  concreto. Distinguir supuestos de resultados medidos.

Estas secuencias son opciones, no secciones obligatorias. En gestión, distinguir plan,
real y proyección; separar riesgos futuros de issues ocurridos y mantener unidades
coherentes. No agregar indicadores que no estén respaldados.

## Identidad visual

Usar colores, tipografías, marca y componentes de las referencias disponibles y permitidas.
Si no hay identidad, proponer una dirección simple y consistente. No imponer la marca,
paleta ni estilo de otro equipo.

Para un deck nuevo sin restricciones, usar 16:9 como punto de partida, por ejemplo
1440 × 810; conservar el formato del deck existente al editar. Priorizar espacio en
blanco, jerarquía clara, tablas legibles y gráficos etiquetados. Definir márgenes y
tamaños según el contenido y verificar legibilidad al tamaño de exposición.
Dividir slides densas antes de reducir el texto a tamaños ilegibles.

Preferir imágenes, diagramas y tablas breves a párrafos. Usar tipografías realmente
disponibles o fallbacks; acompañar el color con texto o símbolos para expresar estados.
Reutilizar componentes pertinentes sin copiar datos ni acumular overrides históricos.

## Reveal.js

Inspeccionar la versión y forma de carga del deck existente. Conservarlas salvo pedido
de actualización; en uno nuevo, verificar la documentación y elegir una versión explícita
compatible con el entorno. Mantener CSS, JS y plugins en la misma versión.
No añadir dependencias al proyecto sin autorización.

Usar HTML con CSS propio y assets relativos, estructura `.reveal > .slides > section`,
identificadores estables y `<aside class="notes">` para el guion, las fuentes y salvedades.
Cargar el plugin de notas antes de inicializarlo. Conservar la configuración pertinente
del deck existente; para uno nuevo, considerar navegación por teclado, enlaces por hash,
progreso y transiciones discretas según el brief.

Usar fragments cuando ayuden a explicar una secuencia. Respetar movimiento reducido y
hacer visible el contenido completo en impresión. Consultar documentación de la versión
usada antes de introducir APIs o configuración nueva.

El uso por CDN requiere conexión: hacerlo explícito. Para offline, incluir recursos
locales, fuentes y licencias necesarias; comprobar que no queden dependencias remotas.

## Verificación y entrega

Abrir el deck servido por HTTP y recorrer todas las slides y fragments. Revisar capturas
en el tamaño del canvas y en una ventana de exposición: desbordes, legibilidad, assets,
consola, teclado, enlaces directos y notas. Contrastar las cifras con sus fuentes.

Si se requiere PDF, usar el flujo de impresión documentado por la versión de Reveal.js,
esperar fuentes e imágenes y comprobar paginación, gráficos y fragments. Si el objetivo
es una página por slide, verificarlo en el PDF resultante. Declarar los checks que no se
pudieron ejecutar en vez de afirmar que el deck está validado.

Entregar HTML, assets, preview, PDF si se pidió, instrucciones para abrirlo y pendientes.
Respetar repositorios de sólo lectura generando fuera de ellos. Publicar o hacer push
sólo dentro del pedido; si se solicitó revisión previa, mostrar el resultado primero.

## Ejemplo de uso

**Pedido:** /crear-deck-reveal demo de producto, 10 minutos, identidad del sitio adjunto

**Resultado:** Genera un deck HTML con Reveal.js y la identidad visual de la referencia, con notas del orador y fuentes, lo recorre servido por HTTP y entrega los archivos con los checks que no pudo hacer.
