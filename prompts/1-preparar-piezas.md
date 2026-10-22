Vas a preparar skills, agentes y comandos para subirlos al Catálogo Común de Agentes de la materia.

REGLA PRINCIPAL: no cambies las instrucciones ni el comportamiento de ninguna pieza. Solo cambiás el nombre, la ubicación, la ficha (frontmatter) y agregás el ejemplo de uso si falta. Si algo te parece mejorable, anotalo en la tabla final, pero no lo modifiques.

DATOS DEL EQUIPO (completar antes de usar)
- Número de grupo: NN    (dos dígitos, por ejemplo 03. Docentes: 00)
- Integrantes del grupo (nombre y apellido - usuario de GitHub):
    Nombre Apellido - usuario
    Nombre Apellido - usuario
- Quién hizo cada pieza (nombre original de la pieza -> autor; colaboradores si los hubo):
    revisor-prs -> autor: Nombre Apellido
    jira-ticket -> autor: Nombre Apellido; colaboradores: Nombre Apellido
- Herramienta con la que trabajamos: claude-code | cursor | codex
- Carpeta donde están nuestras piezas: (ruta)
- Carpeta de salida: (ruta donde dejar las piezas listas)

PASO 1. Identificar cada pieza
Recorré la carpeta indicada y listá cada skill, agente o comando. Para cada uno decidí el tipo:
- skill: un paquete de instrucciones que la IA carga cuando la tarea lo necesita.
- agente: un asistente con rol propio (subagente).
- comando: una instrucción que se ejecuta con /nombre.

PASO 2. Ponerle nombre
- Formato: gNN-nombre-descriptivo. Ejemplo: g03-planify-jira-ticket
- Solo minúsculas, números y guiones. Sin espacios, acentos ni ñ (diseno, no diseño).
- Máximo 64 caracteres.
- El nombre tiene que decir qué hace (g05-generador-de-casos-de-prueba, no g05-agente-1).
- Si ya empieza con el prefijo del grupo, no lo repitas.
- No puede haber dos piezas del grupo con el mismo nombre.

PASO 3. Ubicar los archivos
- skill: carpeta skills/gNN-nombre/ con un archivo SKILL.md. Si no estaba en ese formato, convertila: frontmatter con name y description, y debajo las instrucciones originales tal cual. Los archivos de apoyo (scripts, plantillas, ejemplos) van dentro de la misma carpeta.
- agente: carpeta agentes/gNN-nombre/ con el archivo en el formato original de su herramienta.
- comando: carpeta comandos/gNN-nombre/ con el archivo en el formato original de su herramienta.
- Si el archivo original no admite frontmatter YAML (por ejemplo, TOML o JSON), creá un archivo metadata.yml en la misma carpeta con los campos del paso 4.
- El nombre de la carpeta tiene que ser exactamente igual al campo name.

PASO 4. Completar la ficha
Agregá al frontmatter (o a metadata.yml) estos campos. Donde dice "lista común", usá primero los valores listados; solo si ninguno encaja, escribí uno nuevo.

name: gNN-nombre
description: una o dos oraciones en español. Qué hace y cuándo usarla. Mencioná la tecnología o el caso concreto para que se distinga de otras parecidas.
metadata:
  tipo: skill | agente | comando
  area: [lista común, uno o más] frontend, backend, mobile, datos, ia, qa, devops, seguridad, gestion, diseno, documentacion
  fase: [lista común, uno o más] planificacion, analisis, diseno, desarrollo, testing, revision, despliegue, mantenimiento
  tecnologias: [lista común] en minúsculas, nombre oficial, sin versión (react, nestjs, flutter, postgresql). Si sirve para cualquier tecnología: [agnostico]
  metodologia: [lista común, opcional] scrum, kanban, agnostico
  herramientas: [lista común] claude-code, cursor, codex, otra
  requiere: [lista común] servicios externos o conexiones MCP que necesita (jira, github, figma, google-sheets...). Si no necesita nada: []
  grupo: "NN"   (entre comillas, igual al prefijo del nombre)
  autor:        (una sola persona, según "Quién hizo cada pieza")
    nombre: Nombre Apellido
    github: usuario
  colaboradores:   (opcional, mismo formato, una persona por línea)
    - nombre: Nombre Apellido
      github: usuario
  responsables: [usuario de GitHub del autor]
  madurez: [lista común] experimental (recién hecha, poco probada), probado (se probó varias veces), usado-en-proyecto (se usó en el proyecto real)
  relacionados: []

PASO 5. Ejemplo de uso
- Si la pieza no tiene una sección "## Ejemplo de uso", agregala al final con este formato:
    ## Ejemplo de uso
    **Pedido:** (algo concreto que un usuario le pediría)
    **Resultado:** (qué devuelve o qué hace, en una o dos oraciones)
- Basate solo en lo que dicen las instrucciones de la pieza. No le atribuyas capacidades que no tiene.
- Marcá en la tabla final "ejemplo generado" para que el grupo lo revise.

PASO 6. Si algo no encaja
- Usá primero los valores de la lista. Si de verdad ninguno encaja, escribí uno nuevo en minúsculas, sin acentos y con guiones, y marcalo como "valor nuevo" en la tabla final.
- Si no estás seguro de la madurez, poné experimental.
- Si una pieza no figura en "Quién hizo cada pieza", NO adivines el autor: dejalo vacío y marcalo como "falta autor" en la tabla final.
- Usá solo integrantes de la lista del grupo como autor o colaboradores.
- Si una pieza no tiene instrucciones claras o parece incompleta, anotalo en la tabla final.

PASO 7. Mostrar el resultado
Al terminar, mostrame:
1. Una tabla con estas columnas: nombre | tipo | autor | colaboradores | area | fase | tecnologias | requiere | madurez | dudas
2. Cuántas piezas quedaron como autor de cada integrante.
3. La lista de piezas que tuviste que convertir de formato o a las que les agregaste el ejemplo.
4. Cualquier cosa que te haya parecido rara o incompleta.

No hagas commit, no subas nada y no abras ningún Pull Request. Primero reviso yo la tabla.
