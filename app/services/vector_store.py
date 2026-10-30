from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch

from app.core.config import (
    MONGODB_URI,
    DB_NAME,
    COLLECTION_NAME,
    INDEX_NAME,
    EMBEDDING_FIELD
)

from app.services.embeddings import JinaEmbeddings

client = MongoClient(
    MONGODB_URI,
    serverSelectionTimeoutMS=5000
)

collection = client[DB_NAME][COLLECTION_NAME]


def get_vector_store():
    return MongoDBAtlasVectorSearch(
        collection=collection,
        embedding=JinaEmbeddings(),
        index_name=INDEX_NAME,
        text_key="text",
        embedding_key=EMBEDDING_FIELD,
        relevance_score_fn="cosine",
        auto_create_index=False
    )