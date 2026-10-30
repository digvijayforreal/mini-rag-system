from app.services.vector_store import get_vector_store


def retrieve_documents(
    question: str,
    document_id: str = "orion_sample",
    k: int = 3
):
    vector_store = get_vector_store()

    return vector_store.similarity_search_with_score(
        query=question,
        k=k,
        pre_filter={
            "document_id": {"$eq": document_id}
        }
    )