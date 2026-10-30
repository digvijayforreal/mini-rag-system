from pypdf import PdfReader
from langchain_core.documents import Document


def load_pdf(pdf_path: str) -> list[Document]:
    reader = PdfReader(pdf_path)
    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": pdf_path,
                        "page": page_number
                    }
                )
            )

    return documents