import uuid
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import UploadFile, HTTPException

from app.services.pdf_loader import load_pdf
from app.services.chunker import split_documents
from app.services.vector_store import get_vector_store


def ingest_pdf(file: UploadFile):

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    document_id = str(uuid.uuid4())
    temp_path = None

    try:
        # Save PDF temporarily
        with NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp:
            temp_path = Path(temp.name)
            file.file.seek(0)

            while chunk := file.file.read(1024 * 1024):
                temp.write(chunk)

        # Extract PDF text
        documents = load_pdf(str(temp_path))

        if not documents:
            raise HTTPException(
                status_code=400,
                detail="No extractable text found in PDF"
            )

        # Split into chunks
        chunks = split_documents(documents)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No text chunks generated"
            )

        # Add metadata
        for index, chunk in enumerate(chunks):
            chunk.metadata["document_id"] = document_id
            chunk.metadata["filename"] = file.filename
            chunk.metadata["source"] = file.filename
            chunk.metadata["chunk_index"] = index

        # Embed and store documents
        vector_store = get_vector_store()
        ids = vector_store.add_documents(chunks)

        return {
            "message": "PDF uploaded successfully",
            "document_id": document_id,
            "filename": file.filename,
            "total_chunks": len(ids)
        }

    finally:
        if temp_path:
            temp_path.unlink(missing_ok=True)