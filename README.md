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

### Pre requisitos: Cuda toolkit y PyThorch
- [Página oficial de Cuda toolkit](https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exe_local)
- [Página oficial de PyThorch](https://pytorch.org/get-started/locally/)
### Método 1: Instalación manual
Instala las siguientes bibliotecas de Python una por una:
```bash
pip install numpy==1.26.4
pip install scikit-learn==1.5.2
pip install requests==2.32.3
pip install tqdm==4.66.5
pip install streamlit==1.38.0
pip install python-docx==1.1.2
pip install pypdf==5.1.0
pip install sentence-transformers==2.7.0
pip install chromadb==0.5.20
pip install llama-index-embeddings-huggingface
pip install llama-index-embeddings-instructor
pip install llama-index
pip install langchain==0.3.12
pip install langchain-community==0.3.12
pip install langchain-core==0.3.25
pip install langchain-huggingface==0.1.2
pip install langchain-chroma==0.1.4
pip install langchain-openai==0.1.14
pip install langchain-text-splitters==0.3.3
pip install langchainhub==0.1.21
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
