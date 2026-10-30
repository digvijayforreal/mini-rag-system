import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

DB_NAME = "rag_database"
COLLECTION_NAME = "documents"

INDEX_NAME = "jina_vector_index"
EMBEDDING_FIELD = "embedding_jina"
DIMENSIONS = 1024

if not MONGODB_URI:
    raise ValueError("MONGODB_URI missing from .env")