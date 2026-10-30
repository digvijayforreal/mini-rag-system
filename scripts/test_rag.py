from app.pipelines.rag_pipeline import ask_document


questions = [
    "Who coordinates the Orion project?",
    "What is the maximum uploaded file size?",
    "Which model does Pipeline A use?",
    "What is Orion's project budget?",
    "Who won the 2022 FIFA World Cup?"
]

for question in questions:

    print("\n" + "=" * 60)
    print("Question:", question)

    result = ask_document(question)

    print("Answer:", result["answer"])
    print("Source pages:", result["sources"])