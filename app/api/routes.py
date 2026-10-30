from fastapi import APIRouter

from app.schemas.models import QuestionRequest
from app.pipelines.rag_pipeline import ask_document

from fastapi import APIRouter, UploadFile, File
from app.services.ingestion_service import ingest_pdf

router = APIRouter()




router = APIRouter()


@router.post("/ask")
def ask_question(request: QuestionRequest):

    result = ask_document(
        question=request.question,
        document_id=request.document_id
    )

    return {
        "question": request.question,
        "document_id": request.document_id,
        "answer": result["answer"],
        "sources": result["sources"]
    }

@router.post("/upload")
def upload_document(file: UploadFile = File(...)):
    return ingest_pdf(file)