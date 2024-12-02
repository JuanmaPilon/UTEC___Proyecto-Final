import chromadb
import requests
from typing import List, Dict

BASE_URL = "http://localhost:1234"
DB_FOLDER = "db"

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

def find_relevant_context(query: str, top_k: int = 3) -> str:
    chroma_client = chromadb.PersistentClient(path=DB_FOLDER)
    collection = chroma_client.get_collection("wms_knowledge_base")
    
    query_embedding = get_embeddings([query])[0]
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    relevant_context = "\n\n".join(results['documents'][0])
    return relevant_context

def augment_prompt_with_context(messages: List[Dict[str, str]], context: str) -> List[Dict[str, str]]:
    system_message = messages[0]
    augmented_content = f"{system_message['content']}\n\nRelevant context:\n{context}"
    augmented_system_message = {"role": "system", "content": augmented_content}
    return [augmented_system_message] + messages[1:]

