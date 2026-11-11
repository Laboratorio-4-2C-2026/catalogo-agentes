---
name: g12-armar-linktree
description: Arma una página de links del proyecto con la estructura de Linktree y la identidad visual de la app — producción, prototipo, catálogo, KPIs, repo y equipo — en un único HTML estático. Usar al preparar una entrega, una presentación o cualquier lugar donde haya que mostrar el proyecto con un solo link.
metadata:
  tipo: skill
  area:
  - documentacion
  - diseno
  fase:
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: '12'
  autor:
    nombre: Nicolas Mangini
    github: n-mangini
  responsables:
  - n-mangini
  madurez: usado-en-proyecto
  relacionados: []
---

# Armar linktree

La página es la puerta de entrada al proyecto para alguien de afuera: cátedra, jurado,
directores. Lo que más importa es la mezcla: **Linktree define cómo se ordena la página y
la app define cómo se ve.** Así se reconoce de un vistazo qué es, y a la vez se siente parte
del mismo producto. Si chocan, gana la app.

En SplitIt quedó en `SplitItLab/splitit-linktree`: un `index.html` y `assets/` con los
fondos. Usarlo como referencia.

## 1. Tomar la identidad de la app

Leer del front del proyecto, sin inventar nada:

- los tokens de color (primario, hover, texto, secundario, bordes, fondos) y la tipografía;
- el componente del logo, para rearmarlo igual en versión mini;
- el fondo de la landing, en su versión mobile y desktop;
- sombras, radios y cómo se ven las tarjetas y los íconos sobre el color suave.

Pasar todo a variables CSS en `:root`. Listo cuando no queda un color, tipografía o sombra
en la página que no salga de la app.

## 2. Armar la estructura de Linktree

- **Barra superior:** logo mini a un lado, botón de compartir al otro (usa `navigator.share`
  y, si no existe, copia el link).
- **Perfil centrado:** avatar redondo grande con la marca, nombre, una línea de bio y una de
  datos (materia, cuatrimestre).
- **Botones de ancho completo** apilados: ícono a la izquierda sobre el color suave, título y
  descripción centrados, flecha a la derecha. Al pasar el mouse se agrandan apenas.
- **Etiquetas chicas** para separar secciones (proyecto, equipo).
- **Celular:** la página ocupa toda la pantalla sobre el fondo mobile.
  **Desktop:** tarjeta flotante centrada sobre el fondo desktop, desenfocado y apenas oscurecido.

## 3. Elegir los links

1. La app en producción, como botón principal en el color de marca.
2. El prototipo o canvas, el catálogo de skills, los KPIs (a la plataforma, no al motor) y el repo.
3. El equipo: una fila por persona con GitHub y LinkedIn.

Cada link va a lo que ve el usuario, no al código interno de una herramienta. Lo que todavía
no existe (por ejemplo, el video de la demo) va como "Próximamente", sin link y con
`aria-disabled`, para que no quede escondido ni roto. Lo que no está listo para mostrar
no entra.

## 4. Entregar

Un solo HTML estático con los estilos dentro y los fondos en `assets/`, sin build ni
dependencias. Revisarlo a 375 px y a 1280 px antes de publicar, y confirmar que todos los
links abren.

## Ejemplo de uso

**Pedido:** Armame la página de links de SplitIt para la entrega final, con producción, canvas, KPIs, repo y el equipo.

**Resultado:** Entrega un único HTML estático con la estructura de Linktree y los colores, tipografía y logo de la app, con lo que todavía no existe marcado como "Próximamente".
