from fastapi import HTTPException

from app.services.vector_store import collection
from app.services.retriever import retrieve_documents
from app.services.llm_service import (
    get_rag_chain,
    get_refusal_chain
)


def ask_document(question: str, document_id: str):

    exists = collection.find_one(
        {"document_id": document_id},
        {"_id": 1}
    )

    if not exists:
        raise HTTPException(
            status_code=404,
            detail="Document not found. Upload a PDF first."
        )

    results = retrieve_documents(
        question=question,
        document_id=document_id,
        k=5
    )

    context_parts = []
    pages = set()

    for document, score in results:
        page = document.metadata.get("page")

        if isinstance(page, int):
            pages.add(page)

        context_parts.append(
            f"[Page {page}]\n{document.page_content}"
        )

    context = "\n\n---\n\n".join(context_parts)

    # No retrieved context
    if not results:
        refusal = get_refusal_chain().invoke({
            "question": question
        })

        return {
            "answer": refusal.strip(),
            "sources": [],
            "supported": False
        }

    # Ask the LLM to answer only from retrieved context
    answer = get_rag_chain().invoke({
        "context": context,
        "question": question
    }).strip()

    # Check whether answer is unsupported
    old_refusals = [
        "I could not find that information in the uploaded document.",
        "I could not find that information in the uploaded documents."
    ]

    unsupported = (
        answer.upper() == "UNSUPPORTED"
        or answer in old_refusals
    )

    if unsupported:
        answer = get_refusal_chain().invoke({
            "question": question
        }).strip()

        return {
            "answer": answer,
            "sources": [],
            "supported": False
        }

    return {
        "answer": answer,
        "sources": sorted(pages),
        "supported": True
    }