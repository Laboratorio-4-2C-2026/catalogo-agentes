---
name: g04-imagenes-para-ticket
description: Saca capturas de referencia de la pantalla correcta del prototipo en mobile y desktop y las adjunta al ticket de Linear sin tocar la descripción. Usar cuando un ticket de UI necesita su referencia visual o hay que agregarle imágenes.
metadata:
  tipo: skill
  area:
  - gestion
  - diseno
  fase:
  - analisis
  - planificacion
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - linear
  grupo: "04"
  autor:
    nombre: Tomás Serra
    github: TomasSerra
  responsables:
  - TomasSerra
  madurez: experimental
  relacionados: []
---

# Imágenes para ticket

Deja el aspecto esperado a la vista del dev: es la forma más rápida de que un junior entienda qué está construyendo.

## Flujo

1. Leer el ticket y su `Referencia visual`: qué pantalla y cómo se llega. Si es `no aplica`, no hacer nada.
2. Levantar el prototipo y navegar hasta esa pantalla, en el estado que importa para el ticket (con datos, vacío, modal abierto).
3. Capturar en dos resoluciones: desktop (1440 px) y mobile (390 px). Capturar la pantalla completa si es larga.
4. Nombrar y guardar: `project-plan/ticket-drafts/<slug>-desktop.jpg` y `<slug>-mobile.jpg`.
5. Mirar cada imagen antes de subirla: que sea la pantalla correcta, sin errores en pantalla, sin datos personales reales.
6. Adjuntarlas al issue con las herramientas de adjuntos de Linear, con título claro ("Referencia desktop").
7. Comprobar que aparecen en el issue y devolver el link.

## Reglas

- Subir como **adjunto o comentario, nunca pegada dentro de la descripción**: una edición posterior del cuerpo se la puede llevar y Linear no permite recuperarla.
- No editar la descripción para agregar la imagen.
- Si la pantalla no existe en el prototipo, decirlo. No generar una imagen inventada como si fuera la referencia.

## Ejemplo de uso
**Pedido:** Agregale las capturas del prototipo al ticket de la landing.

**Resultado:** Saca las capturas de desktop y mobile, las adjunta al ticket como adjuntos y confirma que aparecen en Linear.
