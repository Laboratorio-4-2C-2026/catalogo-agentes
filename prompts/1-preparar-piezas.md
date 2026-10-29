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
- Herramientas en las que usamos o probamos las piezas (una o varias): claude-code, cursor, codex, otra
- Madurez de las piezas, si la saben (por pieza o para todas): experimental | probado | usado-en-proyecto
- Carpeta donde están nuestras piezas: (ruta)
- Carpeta donde está (o donde clonar) el repo del catálogo: (ruta; si la dejás vacía, usá la carpeta actual)

PASO 0. Preparar el repo del catálogo
El repo es https://github.com/Laboratorio-4-2C-2026/catalogo-agentes. Las piezas se dejan directamente adentro de una copia local.
- Si la carpeta indicada (o la actual) ya es una copia del repo (git remote get-url origin dice Laboratorio-4-2C-2026/catalogo-agentes), usala: git checkout main y git pull.
- Si no hay copia, clonalo en esa carpeta:
    - Si está instalada la CLI de GitHub y tiene sesión (gh auth status no da error): gh repo clone Laboratorio-4-2C-2026/catalogo-agentes
    - Si no: git clone https://github.com/Laboratorio-4-2C-2026/catalogo-agentes.git
- Si el clone o el pull fallan por permisos, frená y avisame: tengo que aceptar las invitaciones de GitHub a la organización y al repo.
- Creá una rama que empiece con el número de grupo, por ejemplo gNN-carga-inicial (si ya existe, usá otra: gNN-carga-2). No trabajes en main.
- Leé taxonomia.yml del repo: sus valores son las listas comunes del paso 4 (pueden tener más valores que los de este prompt).
- Mirá qué carpetas gNN- del grupo ya existen en skills/, agentes/ y comandos/, para no repetir nombres. Si una pieza ya está en el catálogo, no la dupliques: anotala en la tabla final como "ya existe" (para cambiarla se usa el Prompt 2).

PASO 1. Identificar cada pieza
Recorré la carpeta indicada y listá cada skill, agente o comando. Para cada uno decidí el tipo:
- skill: un paquete de instrucciones que la IA carga cuando la tarea lo necesita.
- agente: un asistente con rol propio (subagente).
- comando: una instrucción que se ejecuta con /nombre.
Si la misma pieza aparece copiada en más de una carpeta (por ejemplo, una copia para cada herramienta), tomala una sola vez y anotalo en la tabla final.

PASO 2. Ponerle nombre
- Formato: gNN-nombre-descriptivo. Ejemplo: g03-planify-jira-ticket
- Solo minúsculas, números y guiones. Sin espacios, acentos, ñ ni guiones bajos (flutter-frontend-agent, no flutter_frontend_agent).
- Máximo 64 caracteres.
- El nombre tiene que decir qué hace (g05-generador-de-casos-de-prueba, no g05-agente-1).
- Si ya empieza con el prefijo del grupo, no lo repitas.
- No puede haber dos piezas del grupo con el mismo nombre.

PASO 3. Ubicar los archivos (dentro de la copia del repo)
- skill: carpeta skills/gNN-nombre/ con un archivo SKILL.md. Si no estaba en ese formato, convertila: frontmatter con name y description, y debajo las instrucciones originales tal cual. Los archivos de apoyo (scripts, plantillas, ejemplos) van dentro de la misma carpeta.
- agente: carpeta agentes/gNN-nombre/ con el archivo principal renombrado a gNN-nombre.md (por ejemplo agentes/g03-qa-agent/g03-qa-agent.md). Mantené el formato original de su herramienta.
- comando: carpeta comandos/gNN-nombre/ con el archivo principal renombrado a gNN-nombre.md, en el formato original de su herramienta.
- Si el archivo original no admite frontmatter YAML (por ejemplo, TOML o JSON), dejalo con su nombre original y creá al lado un metadata.yml con los campos del paso 4 y un EJEMPLO.md con el ejemplo de uso del paso 5.
- El nombre de la carpeta tiene que ser exactamente igual al campo name.

PASO 4. Completar la ficha
Agregá al frontmatter (o a metadata.yml) estos campos. Donde dice "lista común", usá primero los valores de taxonomia.yml; solo si ninguno encaja, escribí uno nuevo.

name: gNN-nombre
description: una o dos oraciones en español, aunque la pieza esté en otro idioma. Qué hace y cuándo usarla. Mencioná la tecnología o el caso concreto para que se distinga de otras parecidas.
metadata:
  tipo: skill | agente | comando
  area: [lista común, uno o más] frontend, backend, mobile, datos, ia, qa, devops, seguridad, gestion, diseno, documentacion
  fase: [lista común, uno o más] planificacion, analisis, diseno, desarrollo, testing, revision, despliegue, mantenimiento
  tecnologias: [lista común] en minúsculas, nombre oficial, sin versión (react, nestjs, flutter, postgresql). Si sirve para cualquier tecnología: [agnostico]
  metodologia: [lista común, opcional] scrum, kanban, agnostico
  herramientas: [lista común] las de DATOS DEL EQUIPO en las que esta pieza se usó o probó: claude-code, cursor, codex, otra
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

Si el frontmatter original ya tenía otros datos:
- Campos propios de la herramienta (por ejemplo tools, skills, model, allowed-tools): conservalos tal cual, al mismo nivel que name y description.
- Si ya tenía un bloque metadata con otras claves, conservalas dentro de metadata junto a las nuevas.
- Si el frontmatter original no es YAML válido (por ejemplo, una description sin comillas que contiene ": "), reescribilo como YAML válido (con comillas donde haga falta) sin cambiar el contenido de ningún campo.

PASO 5. Ejemplo de uso
- Si la pieza no tiene una sección "## Ejemplo de uso", agregala al final con este formato:
    ## Ejemplo de uso
    **Pedido:** (algo concreto que un usuario le pediría)
    **Resultado:** (qué devuelve o qué hace, en una o dos oraciones)
- Basate solo en lo que dicen las instrucciones de la pieza. No le atribuyas capacidades que no tiene.
- Marcá en la tabla final "ejemplo generado" para que el grupo lo revise.

PASO 6. Referencias a otras piezas del grupo
- Si una pieza nombra a otra del mismo grupo en un campo de configuración del frontmatter (por ejemplo, una lista skills: de un agente), actualizá ese nombre al nuevo con prefijo gNN, para que la herramienta la siga encontrando.
- Si la nombra dentro del texto de las instrucciones, no lo cambies: anotalo en la tabla final como "referencia a revisar".

PASO 7. Si algo no encaja
- Usá primero los valores de la lista. Si de verdad ninguno encaja, escribí uno nuevo en minúsculas, sin acentos y con guiones, y marcalo como "valor nuevo" en la tabla final.
- Si DATOS DEL EQUIPO no dice la madurez de una pieza, poné experimental y marcalo como "madurez sin confirmar" en la tabla final.
- Si no sabés en qué herramientas se usó una pieza, usá las de DATOS DEL EQUIPO y marcalo como "herramientas sin confirmar".
- Si una pieza no figura en "Quién hizo cada pieza", NO adivines el autor: dejalo vacío y marcalo como "falta autor" en la tabla final.
- Usá solo integrantes de la lista del grupo como autor o colaboradores.
- Si una pieza no tiene instrucciones claras o parece incompleta, anotalo en la tabla final.

PASO 8. Mostrar el resultado
Al terminar, mostrame:
1. Una tabla con estas columnas: nombre | tipo | autor | colaboradores | area | fase | tecnologias | requiere | madurez | dudas
2. Cuántas piezas quedaron como autor de cada integrante.
3. La lista de archivos que renombraste o convertiste de formato, y las piezas a las que les agregaste el ejemplo.
4. Cualquier cosa que te haya parecido rara o incompleta.

Recomendado antes de subir: revisá las fichas con la skill g03-revisor-de-fichas del catálogo (skills/g03-revisor-de-fichas/SKILL.md), en modo local.

No hagas commit, no subas nada y no abras ningún Pull Request. Primero reviso yo la tabla.

PASO 9. Subir (solo cuando yo te lo confirme)
- git add skills agentes comandos, y un commit con un mensaje como "Agregar piezas del grupo NN".
- git push -u origin <la rama del paso 0>
- Si está la CLI de GitHub: gh pr create --base main --title "Piezas del grupo NN" --body "Carga de piezas del grupo NN". Si no, pasame el link para abrir el Pull Request desde GitHub.
- Después, esperá el comentario automático del bot en el PR y contame qué dice. Si hay errores, corregilos en la misma rama y volvé a hacer push.
