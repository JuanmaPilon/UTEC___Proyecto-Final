import os
import json
import fitz  # PyMuPDF para leer PDFs

PDF_FOLDER = "pdf"
OUTPUT_FILE = "dataset.json"

# Índice de ejemplo
index_example = {
    "Reglas de Almacenaje 10.0.pdf": {
        "Conceptos Básicos": 4,
        "Grupos de Productos": 4,
        "Definición de Grupos de Productos": 4,
        "Definición de Reglas de Agrupación": 6,
        "Ver Grupo de un Producto": 10,
        "Asignación de Grupos a Etiquetas de Recepción": 11,
        "Lógica de Almacenaje": 11,
        "Tipos de Lógicas de Almacenaje": 11,
        "Parametrización de Lógicas de Almacenaje": 11,
        "Estrategia de Almacenaje": 15,
        "Asociación de Estrategia de Almacenaje": 15,
        "Descripción General del Algoritmo": 17,
        "Administración de Estrategias de Almacenaje": 23,
        "Panel de Estrategias": 23,
        "Asignación de Lógicas de Almacenaje a Estrategias": 23,
        "Asociación de Estrategias": 27,
        "Deshabilitación de Estrategias de Almacenaje": 30,
        "Almacenamiento Agrupado basado en Estrategias de Almacenaje": 31,
        "Habilitación de Sugerencias de Almacenaje": 30,
        "Administración de Motivos de Rechazo": 32,
        "Colector de Almacenamiento Agrupado": 34,
        "Rechazo de Sugerencias de Almacenaje": 39
    }
}

# Función para extraer texto de PDFs de la carpeta /pdf
def extract_text_from_pdfs(directory):
    texts = {}
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            filepath = os.path.join(directory, filename)
            with fitz.open(filepath) as doc:
                texts[filename] = [page.get_text() for page in doc]  # Obtener texto directamente
    return texts

# Crea el dataset en formato JSON copiando el texto tal cual desde el PDF
def create_dataset(index, texts, output_file):
    data = []

    # Añadir el mensaje del sistema solo una vez
    system_message = {
        "role": "system",
        "content": "Eres un asistente virtual llamado Asistente WMS, enfocado en responder preguntas relacionadas al sistema WMS (Warehouse Management System), de forma concreta y precisa."
    }
    data.append(system_message)

    # Generar preguntas y respuestas basadas en el índice
    for filename, chapters in index.items():
        for title, start_page in chapters.items():
            user_content = title  # El título será la pregunta
            end_page = get_end_page(chapters, title, start_page)
            assistant_content = extract_relevant_info(texts[filename], start_page, end_page)

            # Añadir los mensajes de usuario y asistente
            data.append({
                "role": "user",
                "content": user_content
            })
            data.append({
                "role": "assistant",
                "content": assistant_content  # Copiar texto del PDF tal como está
            })

    # Guardar el archivo JSON con la estructura generada
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Determina la página final de un capítulo
def get_end_page(chapters, current_title, start_page):
    # Obtener las páginas de inicio de los capítulos
    pages = sorted(set(chapters.values()))
    current_index = pages.index(start_page)
    if current_index + 1 < len(pages):
        return pages[current_index + 1] - 1  # Restar 1 para que no incluya la página del siguiente título
    return start_page  # Si es el último capítulo, usa la misma página

# Extrae el texto relevante entre páginas de inicio y fin (sin procesar)
def extract_relevant_info(text_pages, start_page, end_page):
    # Extrae el texto desde start_page hasta end_page tal cual
    relevant_text = ""
    for page_num in range(start_page - 1, end_page):
        if page_num < len(text_pages):
            relevant_text += text_pages[page_num].strip() + "\n"

    return relevant_text.strip()  # Copiar el texto tal como está

if __name__ == "__main__":
    index = index_example  # Aquí puedes cargar tu índice real
    texts = extract_text_from_pdfs(PDF_FOLDER)
    create_dataset(index, texts, OUTPUT_FILE)
