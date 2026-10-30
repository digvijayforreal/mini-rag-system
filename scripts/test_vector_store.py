from app.services.pdf_loader import load_pdf
from app.services.chunker import split_documents
from app.services.vector_store import get_vector_store, collection


def test_vector_storage():

    # Step 1: Load PDF
    documents = load_pdf("data/sample.pdf")
    print("Total PDF pages:", len(documents))

    # Step 2: Split PDF into chunks
    chunks = split_documents(documents)
    print("Total chunks:", len(chunks))

    # Step 3: Add metadata to every chunk
    for index, chunk in enumerate(chunks):
        chunk.metadata["document_id"] = "orion_sample"
        chunk.metadata["chunk_index"] = index

    # Step 4: Initialize MongoDB vector store
    vector_store = get_vector_store()

    # Step 5: Remove previous test records
    # Only deletes documents tagged orion_sample
    collection.delete_many({"document_id": "orion_sample"})

    # Step 6: Generate embeddings and store chunks
    ids = vector_store.add_documents(chunks)

    print("Inserted chunks:", len(ids))

    # Step 7: Verify stored documents
    count = collection.count_documents({
        "document_id": "orion_sample"
    })

    print("Documents in MongoDB:", count)

    # Step 8: Check one stored document
    sample = collection.find_one({
        "document_id": "orion_sample"
    })

    if sample:
        print("Stored text:", sample.get("text", "")[:150])
        print("Page number:", sample.get("page"))
        print(
            "Embedding dimensions:",
            len(sample.get("embedding_jina", []))
        )


if __name__ == "__main__":
    test_vector_storage()