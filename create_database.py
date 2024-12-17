from os import listdir
from os.path import isfile, join
from tqdm import tqdm
import chromadb
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

# Configuración
TEXT_EMBEDDING_MODEL = "BAAI/bge-m3"
VECTOR_DB_NAME = "WMS_VectorDB"
VECTOR_DB_PATH = "db/"
CHUNK_SIZE = 800
OVERLAP = 50

docs_path = "data/"
file_names = [f for f in listdir(docs_path) if isfile(join(docs_path, f))]

# Inicializa Chroma y el modelo de embeddings
chroma_client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
collection = chroma_client.get_or_create_collection(name=VECTOR_DB_NAME)
existing_ids = set(collection.get(ids=None)["ids"])

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=OVERLAP
)

text_embedder = HuggingFaceEmbeddings(model_name=TEXT_EMBEDDING_MODEL)

def write_to_db(filename):
    if not filename.endswith(".pdf"):
        print(f"Skipping non-PDF file: {filename}")
        return  # Salta el archivo si no es un PDF

    print(f"Procesando archivo PDF: {filename}")
    doc = PdfReader(docs_path + filename)
    doc_text = "".join([page.extract_text() for page in doc.pages])

    # Divide el texto en chunks
    chunks = text_splitter.split_text(doc_text)

    # Genera y guarda los embeddings en la base de datos
    for i, chunk in enumerate(chunks):
        doc_id = f"{filename}_{i}"
        if doc_id not in existing_ids:
            embedding = text_embedder.embed_query(chunk)
            collection.add(
                embeddings=[embedding],
                documents=[chunk],
                ids=[doc_id]
            )
    print(f"Archivo PDF {filename} procesado con éxito.")

def process_text_file(filename):
    print(f"Procesando archivo TXT: {filename}")
    with open(docs_path + filename, "r", encoding="utf-8") as file:
        text = file.read()

    # Divide el texto en chunks
    chunks = text_splitter.split_text(text)
    for i, chunk in enumerate(chunks):
        doc_id = f"{filename}_{i}"
        if doc_id not in existing_ids:
            embedding = text_embedder.embed_query(chunk)
            collection.add(
                embeddings=[embedding],
                documents=[chunk],
                ids=[doc_id]
            )
    print(f"Archivo TXT {filename} procesado con éxito.")

for filename in file_names:
    if filename.endswith(".pdf"):
        write_to_db(filename)
    elif filename.endswith(".txt"):
        process_text_file(filename)
    else:
        print(f"Tipo de archivo no compatible: {filename}")
