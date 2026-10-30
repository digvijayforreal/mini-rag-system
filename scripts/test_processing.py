from app.services.pdf_loader import load_pdf
from app.services.chunker import split_documents

documents = load_pdf("data/sample.pdf")

print("Total pages:", len(documents))

chunks = split_documents(documents)

print("Total chunks:", len(chunks))

for i, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {i}")
    print("Page:", chunk.metadata["page"])
    print("Characters:", len(chunk.page_content))
    print("Text:", chunk.page_content[:150])