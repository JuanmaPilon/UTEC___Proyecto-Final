# Scripts Misceláneos

En esta carpeta se encuentran varios scripts que utilizamos para automatizar tareas relacionadas con el procesamiento de datos y la generación de datasets.

## Estructura de Carpetas

- **`pdf/`**: Contiene los documentos proporcionados por el cliente.
- **`DATASETS/`**: Carpeta que contiene los datasets desarrollados y generados a partir de los documentos.

---

## Scripts

### **`dataset.py`**
- **Descripción**: Crea un archivo JSON en formato de conversación basado en un archivo PDF.
- **Funcionamiento**:
  - Los títulos del índice del PDF serán las preguntas del `user`.
  - El contenido de las páginas asociadas a esos títulos será la respuesta del `assistant`.
  - El script recorre desde la página del título hasta la página del siguiente título para construir las respuestas.

---

### **`data.py`**
- **Descripción**: Similar a `dataset.py`, pero deja las respuestas del `assistant` vacías.
- **Uso**: Permite que las respuestas sean rellenadas manualmente con información específica, lo que permite explicar las imágenes y las referencias a los botones.

---

### **`divide.py`**
- **Descripción**: Divide un dataset JSON en dos archivos separados:
  - Uno que contiene todas las preguntas del `user`.
  - Otro que contiene todas las respuestas del `assistant`.
- **Objetivo**: Esta separación se utilizó para crear variantes de las preguntas manualmente. 
  - Cada pregunta del usuario podía tener 4 variantes diferentes asociadas a la misma respuesta del `assistant`.
  - **Nota**: Este script **solo divide** el dataset; la generación de variantes y el acople de las respuestas se realizó de forma manual.

---

### **`json-to-txt.py`**
- **Descripción**: Convierte un archivo JSON con las respuestas del `assistant` en un archivo de texto plano (`.txt`).
- **Funcionamiento**:
  - Cada respuesta del `assistant` se escribe en el archivo `.txt`.
  - Las respuestas están separadas por saltos de línea entre párrafos.
- **Uso**:
  - El archivo generado (por ejemplo, `assistant_responses.txt` en la carpeta `data`) se utiliza como entrada para un sistema RAG.

---

## Archivos Generados
- **`assistant_responses.txt`**: Archivo de texto que contiene todas las respuestas ordenadas del `assistant`.
- **`DATASETS/`**: Contiene los datasets generados por los scripts anteriores.

---
Es necesario aclarar que para que los escripts funcionen se deben encontrar en la misma carpeta que los archvos, en este repositorio los archivos están en otras carpetas por motivos de orden.
Con estos scripts, se logró automatizar varias tareas clave en el procesamiento de datos y la preparación de datasets para el modelo de lenguaje. Si tienes preguntas, consulta el código fuente de cada script para más detalles.
