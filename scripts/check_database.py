from app.services.vector_store import collection

print("Total documents:", collection.count_documents({}))

print(
    "Matching document IDs:",
    collection.count_documents({
        "document_id": "orion_sample"
    })
)

sample = collection.find_one({})

if sample:
    print("Available fields:", list(sample.keys()))
    print("Document ID:", sample.get("document_id"))
    print("Embedding dimensions:", len(sample.get("embedding_jina", [])))


print("\n--- VECTOR SEARCH INDEXES ---")

for index in collection.list_search_indexes():
    print("Index name:", index.get("name"))
    print("Index type:", index.get("type"))
    print("Status:", index.get("status"))
    print("Queryable:", index.get("queryable"))
    print("Definition:", index.get("latestDefinition"))    