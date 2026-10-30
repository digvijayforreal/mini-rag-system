from app.services.vector_store import collection

print("Database:", collection.database.name)
print("Collection:", collection.name)

print("Total documents:", collection.count_documents({}))

print("\nStored document IDs:")

pipeline = [
    {
        "$group": {
            "_id": "$document_id",
            "count": {"$sum": 1}
        }
    }
]

for doc in collection.aggregate(pipeline):
    print("Document ID:", doc["_id"])
    print("Chunks:", doc["count"])
    print("-------------------")