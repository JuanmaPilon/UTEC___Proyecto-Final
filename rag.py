from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Configuración
TEXT_EMBEDDING_MODEL = "BAAI/bge-m3"
VECTOR_DB_PATH = "db"
VECTOR_DB_NAME = "WMS_VectorDB"

# Inicializa el modelo de embeddings y Chroma
text_embedder = HuggingFaceEmbeddings(model_name=TEXT_EMBEDDING_MODEL)
vector_db = Chroma(
    persist_directory=VECTOR_DB_PATH,
    embedding_function=text_embedder,
    collection_name=VECTOR_DB_NAME
)

def find_relevant_context(query, n_results=5, max_tokens=3000):
    # Busca los documentos más relevantes en la base de datos
    results = vector_db.similarity_search_with_score(query, k=n_results)
    
    # Ordena los resultados por puntuación (de mayor a menor relevancia)
    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
    
    # Inicializa el contexto y el contador de tokens
    context_parts = []
    token_count = 0
    
    # Agrega documentos al contexto hasta alcanzar el límite de tokens
    for doc, score in sorted_results:
        doc_tokens = len(doc.page_content.split())
        if token_count + doc_tokens > max_tokens:
            break
        context_parts.append(f"Relevancia: {score:.4f}\n{doc.page_content}")
        token_count += doc_tokens
    
    # Une los documentos del contexto
    full_context = "\n\n---\n\n".join(context_parts)
    
    return full_context

def split_context(context, max_tokens=2000):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_tokens,
        chunk_overlap=100,
        length_function=len
    )
    return text_splitter.split_text(context)

