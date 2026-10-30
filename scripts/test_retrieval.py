from app.services.retriever import retrieve_documents


question = "Who coordinates the Orion project?"

results = retrieve_documents(question)

print("Question:", question)
print("Retrieved chunks:", len(results))

for index, (document, score) in enumerate(results, start=1):

    print(f"\n--- Result {index} ---")
    print("Score:", round(score, 4))
    print("Page:", document.metadata.get("page"))
    print("Text:", document.page_content)