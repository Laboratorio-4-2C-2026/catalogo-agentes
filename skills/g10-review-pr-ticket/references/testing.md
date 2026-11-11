# Pruebas de funcionamiento

Aplicar las ramas pertinentes al cambio; esta referencia no exige repetir todos los casos en cada PR.

## Entorno y diagnostico

- Registrar comandos reales y sus codigos de salida. Un arnes debe reportar sus aserciones fallidas aunque termine con codigo cero; preferir un codigo distinto de cero ante fallos o guardar estados explicitos por escenario.
- Una falla del arnes no es un defecto de producto. Comprobar primero los mocks, selectores, navegacion y tiempos. Corregir el arnes, repetir los escenarios afectados y conservar el resultado final sin esconder problemas del producto.
- Comparar con la base el comportamiento sospechoso mediante una comprobacion acotada: diff, archivos originales o reproduccion aislada. No ejecutar toda la suite de la base sin una razon concreta.
- Si el entorno bloquea red, procesos o acceso a Docker, usar el mecanismo de autorizacion del entorno. No recurrir a rutas alternativas para eludir una denegacion.
- Inicializar un entorno vacio puede activar condiciones previas al alcance. Distinguirlas del flujo revisado. Una configuracion provisional solo es aceptable para servicios no ejercitados y debe declararse; nunca simular silenciosamente un proveedor cuya integracion se pretende comprobar.

## UI y contratos

Verificar el camino feliz completo y recargar o volver a entrar para comprobar persistencia. Observar solicitudes y respuestas, validaciones, payload, metodo, encabezados y campos relevantes; no guardar headers Authorization o cuerpos con secretos.

Usar datos claramente distintos para varias identidades. No hacer login con otra cuenta solo para poblar tarjetas o probar iniciales si puede resolverse con datos controlados. Mantener las pruebas con HTTP simulado separadas de las ejecutadas contra el backend real. Si se intercepta autenticacion para probar UI, declararlo: no es una validacion de seguridad.

Para errores reproducibles, simular solo el fallo relevante: rechazo de la API, timeout o respuesta invalida. Comprobar que se informa el estado correcto, se conserva lo que el ticket exige y se puede reintentar. Si el flujo tiene operaciones parciales, distinguir cambios persistidos de vista previa y de mensaje de exito.

Comprobar estados durante operaciones pendientes cuando sean relevantes: doble envio, cancelacion, cambio de seleccion o navegacion. Evaluar esos resultados por impacto; una carrera excepcional no implica automaticamente pedir cambios.

Sincronizar pruebas con condiciones observables: URL final, estado del componente, respuesta HTTP, dimensiones naturales de una imagen o evento de permisos. La presencia de un elemento no garantiza que su contenido haya terminado de cargar. Evitar esperas fijas como prueba de exito.

## Si el cambio incluye imagenes, archivos o camara

- Comprobar que elegir o capturar no envia el archivo antes del evento que exige el ticket, por ejemplo Guardar. Verificar preview, formato real y dimensiones, no solo extension de archivo.
- Para multipart, comprobar el nombre de campo y que el navegador genere el boundary; no fijar manualmente Content-Type multipart sin boundary.
- Probar cancelar selector/camara, repetir el mismo archivo, seleccionar uno invalido, fallo de subida y reintento. Diferenciar foto persistida de preview pendiente al evaluar si se conserva la anterior.
- Probar foto ausente y descarga fallida en los componentes que la consumen. Un mock HTTP 404 que devuelve una imagen valida puede seguir decodificandose: usar una respuesta que represente la falla pretendida.
- Para webcam, comprobar apertura, captura y liberacion de tracks al cancelar, cerrar o desmontar. Incluir el cierre mientras el permiso esta pendiente si hay logica asincrona para ese caso. Considerar la ejecucion repetida de efectos de React StrictMode al disenar mocks.
- Distinguir webcam simulada, permiso simulado, emulacion movil y dispositivo fisico. Un input con capture en emulacion demuestra el contrato de la UI, no que se abra una camara nativa real.
- Probar aviso al recargar/cerrar o navegacion interna solo como requisito si el ticket lo exige; si se evalua como mejora, etiquetarlo como tal.

## Prueba real con login manual

Preparar servicios y asegurar conectividad antes de abrir la sesion. Esperar que termine la navegacion del login antes de abrir la pantalla objetivo; usar reintentos acotados frente a una carga transitoria y mantener el navegador disponible para diagnostico. No automatizar cambios reales hasta tener autorizacion para el cambio concreto.

Despues de la accion autorizada, comprobar respuesta, estado persistido al recargar y contenido descargado. Si se prueban imagenes, esperar que termine su descarga y validar naturalWidth/naturalHeight o decodificacion equivalente. Una lectura inmediata de complete=false no prueba un fallo.

Ante errores, preservar la evidencia necesaria sin registrar secretos. No repetir escrituras reales automaticamente cuando no se conoce si la primera operacion persistio; consultar estado antes de reintentar. Informar el cambio efectivo realizado en la cuenta.
