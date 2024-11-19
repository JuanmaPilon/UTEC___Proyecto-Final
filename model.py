# python model.py
import chromadb
import fitz  # PyMuPDF para leer PDFs
import requests
import os
import logging

 Rutas para PDFs y base de datos
PDF_FOLDER = "pdf"
DB_FOLDER = "db"
BASE_URL = "http://localhost:1234"  # LMStudio está corriendo en este puerto

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)

# Conectar a ChromaDB con persistencia
chroma_client = chromadb.PersistentClient(path=DB_FOLDER)

# Crear o obtener la colección
collection = chroma_client.get_or_create_collection(name="my_collection")

def get_embeddings(texts):
    url = f"{BASE_URL}/v1/embeddings"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "nomic-ai/nomic-embed-text-v1.5-GGUF/nomic-embed-text-v1.5.Q4_K_M.gguf",
        "input": texts
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return [item["embedding"] for item in response.json()["data"]]

# Función para extraer texto de PDFs de la carpeta /pdf
def extract_text_from_pdfs(directory):
    texts = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            filepath = os.path.join(directory, filename)
            with fitz.open(filepath) as doc:
                text = ""
                for page in doc:
                    text += page.get_text()
                texts.append(text)
    return texts

# Función para cargar PDFs y almacenar embeddings en ChromaDB
def load_and_store_pdfs(directory):
    pdf_texts = extract_text_from_pdfs(directory)
    if pdf_texts:
        # Obtener embeddings de los textos extraídos
        embeddings = get_embeddings(pdf_texts)
        # Añadir los textos y embeddings a la colección en ChromaDB
        collection.upsert(
            documents=pdf_texts,
            embeddings=embeddings,
            ids=[f"doc_{i}" for i in range(len(pdf_texts))]
        )
        logging.info(f"Se han agregado {len(pdf_texts)} documentos a ChromaDB y persistido en {DB_FOLDER}.")
    else:
        logging.info("No se encontraron archivos PDF en el directorio.")

def query_chromadb(query_text):
    query_embedding = get_embeddings([query_text])[0]
    # Buscar en la colección de ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )
    # Filtrar resultados por distancia
    filtered_results = [doc for doc, distance in zip(results['documents'][0], results['distances'][0]) if distance < 0.1]
    return filtered_results

def chat_completions(messages, temperature=0.5):
    bot_name = "Asistente WMS"
    system_prompt = {
        "role": "system",
        "content": f"Eres un asistente virtual llamado {bot_name}, enfocado solo en responder preguntas relacionadas al sistema WMS (Warehouse Management System), de forma concreta y precisa, basado exclusivamente en la documentación del programa: Manual Básico de Usuario WMS 10.0, Manual Avanzado de Usuario WMS 10.0, Reglas de Almacenaje 10.0 y License Plate Number 10.0."
    }
    messages_with_prompt = [system_prompt] + messages
    # Extraer la última pregunta del usuario
    user_question = messages[-1]["content"]
    # Consultar la base de datos de vectores
    relevant_docs = query_chromadb(user_question)
    # Construir el contexto a partir de los documentos filtrados
    context = "\n".join(relevant_docs) if relevant_docs else "No se encontró información relevante."
    # Incluir el contexto en el mensaje del sistema
    system_prompt["content"] += f"\nBasado en los siguientes documentos:\n{context}"
    try:
        # Llamada a la API del modelo con la temperatura ajustada
        response = requests.post(
            f"{BASE_URL}/v1/chat/completions",
            json={
                "messages": messages_with_prompt,
                "temperature": temperature  # Usar el parámetro de temperatura
            }
        )
        response.raise_for_status()
        result = response.json()
        logging.info(f"Respuesta del modelo: {result}")
        return result
    except requests.RequestException as e:
        logging.error(f"Error al obtener la respuesta del modelo: {e}")
        return {"choices": [{"message": {"content": "Error al comunicarse con el servidor."}}]}

# Llama a la función para cargar y almacenar PDFs si es necesario
if __name__ == "__main__":
    load_and_store_pdfs(PDF_FOLDER)
