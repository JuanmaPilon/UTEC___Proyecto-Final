# UTEC___Proyecto-Final
# Proyecto: Chatbot Asistente WIS

Este proyecto implementa un chatbot asistente virtual para el sistema WIS (Warehouse Information System). El chatbot utiliza **RAG (Retrieval-Augmented Generation)** para proporcionar respuestas precisas basadas en una base de datos de vectores construida a partir de documentación relevante.

---

## Requisitos previos

### 1. Instalar y configurar LM Studio
Sigue las instrucciones detalladas en el archivo [`LMSTUDIO config.pdf`](./LMSTUDIO%20config.pdf) para configurar LM Studio correctamente. Es esencial que LM Studio esté funcionando como servidor para que el chatbot pueda generar respuestas.

### 2. Instalar Python
Descarga e instala Python desde la página oficial: [https://www.python.org/downloads/](https://www.python.org/downloads/).

---

## Instalación de dependencias

### Método 1: Instalación manual
Instala las siguientes bibliotecas de Python una por una:
```bash
pip install streamlit
pip install requests
pip install chromadb
pip install pypdf2
pip install python-docx
pip install --upgrade langchain langchain-core langchain-community
pip install langchain-huggingface
```

### Método 2: Usando `requirements.txt`
Puedes instalar todas las dependencias de una sola vez utilizando el archivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## Pasos para ejecutar el proyecto

### Paso 1: Crear la base de datos de vectores
Construye la base de datos de vectores a partir de los archivos de documentación:
```bash
python create_database.py
```

### Paso 2: Ejecutar el chatbot
Asegúrate de que el servidor de LM Studio esté en funcionamiento antes de iniciar el chatbot. Luego, ejecuta el siguiente comando:
```bash
streamlit run app.py
```

---

## Notas importantes
- **Servidor LM Studio**: Asegúrate de que el servidor de LM Studio esté configurado correctamente y en ejecución en el puerto definido (por defecto, `localhost:1234`).
- **Documentación**: La documentación utilizada para construir la base de datos de vectores debe estar en la carpeta 'data' definida en `create_database.py`.
- **Configuración adicional**: Si necesitas modificar configuraciones como el puerto de LM Studio o los parámetros del modelo, edita los archivos `model.py` o `rag.py` según sea necesario.

---

## Recursos adicionales
- [Página oficial de Python](https://www.python.org/)
- [Documentación de Streamlit](https://docs.streamlit.io/)
- [LM Studio](https://lmstudio.com/)

---
