import os
import chromadb
import logging
import requests
from typing import List, Dict
import docx
import PyPDF2

# Configuration
DATA_FOLDER = "data"
DB_FOLDER = "db"
BASE_URL = "http://localhost:1234"

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_embeddings(texts: List[str]) -> List[List[float]]:
    url = f"{BASE_URL}/v1/embeddings"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "nomic-ai/nomic-embed-text-v1.5-GGUF/nomic-embed-text-v1.5.Q4_K_M.gguf",
        "input": texts
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return [item["embedding"] for item in response.json()["data"]]

def read_text_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def read_docx_file(file_path: str) -> str:
    doc = docx.Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def read_pdf_file(file_path: str) -> str:
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        return "\n".join([page.extract_text() for page in reader.pages])

def process_file(file_path: str) -> List[Dict[str, str]]:
    _, file_extension = os.path.splitext(file_path)
    
    if file_extension == '.txt':
        content = read_text_file(file_path)
    elif file_extension == '.docx':
        content = read_docx_file(file_path)
    elif file_extension == '.pdf':
        content = read_pdf_file(file_path)
    else:
        logger.warning(f"Unsupported file type: {file_path}")
        return []

    paragraphs = content.split('\n\n')
    return [{"content": p, "source": file_path} for p in paragraphs if p.strip()]

def create_vector_database():
    # Connect to ChromaDB
    chroma_client = chromadb.PersistentClient(path=DB_FOLDER)
    
    # Create or get the collection
    collection = chroma_client.get_or_create_collection("wms_knowledge_base")

    # Process all files in the data folder
    all_documents = []
    for root, _, files in os.walk(DATA_FOLDER):
        for file in files:
            file_path = os.path.join(root, file)
            all_documents.extend(process_file(file_path))

    # Batch process documents
    batch_size = 100
    for i in range(0, len(all_documents), batch_size):
        batch = all_documents[i:i+batch_size]
        
        texts = [doc["content"] for doc in batch]
        embeddings = get_embeddings(texts)
        
        collection.add(
            embeddings=embeddings,
            documents=[doc["content"] for doc in batch],
            metadatas=[{"source": doc["source"]} for doc in batch],
            ids=[f"doc_{j}" for j in range(i, i+len(batch))]
        )
        
        logger.info(f"Processed {i+len(batch)} documents")

    logger.info("Vector database creation completed")

if __name__ == "__main__":
    create_vector_database()

