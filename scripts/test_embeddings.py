from app.services.embeddings import JinaEmbeddings

embeddings = JinaEmbeddings()

# Test document embedding
texts = [
    "Orion is a document assistant.",
    "Mira Shah coordinates the Orion project."
]

document_vectors = embeddings.embed_documents(texts)

print("Document vectors:", len(document_vectors))
print("Embedding dimensions:", len(document_vectors[0]))

# Test question embedding
question = "Who coordinates Orion?"

query_vector = embeddings.embed_query(question)

print("Query dimensions:", len(query_vector))
print("First 5 vector values:", query_vector[:5])