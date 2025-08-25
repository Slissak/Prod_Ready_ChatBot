import os
import sys
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv

# Add project root to sys.path to allow importing from backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.app.config import JOB_ROLE_MAPPING

# --- Configuration ---
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'backend', '.env')
load_dotenv(dotenv_path=dotenv_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
SOURCE_DOCS_DIR = os.path.join(os.path.dirname(__file__), 'job_descriptions/')

if not all([OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_INDEX_NAME]):
    raise ValueError("API keys must be set.")

pc = Pinecone(api_key=PINECONE_API_KEY)
embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY)

def load_and_chunk_documents():
    print(f"Loading documents based on config...")
    all_chunks = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)

    for role_id, role_info in JOB_ROLE_MAPPING.items():
        pdf_path = os.path.join(SOURCE_DOCS_DIR, role_info["pdf_filename"])
        
        if not os.path.exists(pdf_path):
            print(f"Warning: PDF file not found for role '{role_id}': {pdf_path}")
            continue

        print(f"Processing {role_info['pdf_filename']} for role ID: {role_id}...")
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        chunks = text_splitter.split_documents(documents)
        
        for chunk in chunks:
            chunk.metadata['role_id'] = role_id
            
        all_chunks.extend(chunks)
        print(f"  -> Created {len(chunks)} chunks.")
        
    return all_chunks

def ingest_data():
    try:
        chunks = load_and_chunk_documents()
        if not chunks:
            print("No data to ingest. Exiting.")
            return

        print(f"Connecting to Pinecone index: '{PINECONE_INDEX_NAME}'...")
        index = pc.Index(PINECONE_INDEX_NAME)
        
        # --- NEW: Check if the index has any vectors before deleting ---
        index_stats = index.describe_index_stats()
        if index_stats.total_vector_count > 0:
            print("Clearing existing data from index...")
            index.delete(delete_all=True)
        else:
            print("Index is already empty. Skipping deletion.")

        print("Creating embeddings and uploading to Pinecone...")
        vectors_to_upsert = []
        for i, chunk in enumerate(chunks):
            embedding = embeddings_model.embed_query(chunk.page_content)
            vector = {
                "id": f"jd_chunk_{i}",
                "values": embedding,
                "metadata": {
                    "text": chunk.page_content,
                    "role_id": chunk.metadata['role_id'],
                    "source": chunk.metadata.get('source', 'Unknown'),
                    "page": chunk.metadata.get('page', 0)
                }
            }
            vectors_to_upsert.append(vector)
        
        print(f"Upserting {len(vectors_to_upsert)} vectors in batches...")
        index.upsert(vectors=vectors_to_upsert, batch_size=100)
        print("Successfully uploaded all vectors to Pinecone.")

    except Exception as e:
        print(f"An error occurred during data ingestion: {e}")

if __name__ == "__main__":
    print("Starting data ingestion process...")
    ingest_data()
    print("Ingestion process finished.")
