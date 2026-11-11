# Uso del workflow

Paquete preparado para compartir. Importar el export JSON en una instancia n8n compatible con sus versiones de nodos. La versión de n8n de origen no está documentada; no se afirma una prueba de importación nueva.

Configurar credenciales propias de GitHub y OpenRouter, y revisar owner/repository tanto en Github Trigger como en Create a review. El HTTP Request usa la URL del diff del evento y no tiene autenticación configurada: no se afirma soporte verificado para repos privados. Revisar las opciones de respuesta y que el nodo entregue el diff en el campo consumido por AI Agent.

El filtro acepta opened/reopened; synchronize no pasa a análisis. El modelo es openrouter/free y el modelo concreto puede variar. La activación produce comentarios en GitHub: probar solo en el repositorio y con los efectos autorizados por quien lo opera. No se activó ni ejecutó para esta entrega.

La copia conserva la lógica y cambia únicamente la firma Marcos AI por Pedro AI, según pedido del autor. La evidencia histórica conserva la firma anterior. Se eliminaron las referencias de credenciales, los webhookId y los campos id, versionId y meta de la instancia original. El workflow se distribuye con active=false. Deben seleccionarse credenciales propias de GitHub y OpenRouter al importarlo; el repositorio del caso se mantiene como ejemplo y debe revisarse en ambos nodos de GitHub antes de activar. No se transfieren credenciales operativas.
