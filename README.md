# Mini RAG System

**A Document-Based AI Question Answering System powered by Retrieval-Augmented Generation (RAG), MongoDB Atlas Vector Search, Jina Embeddings, and Groq.**

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/Framework-LangChain-green.svg)](https://www.langchain.com/)
[![MongoDB](https://img.shields.io/badge/Vector%20Database-MongoDB%20Atlas-green.svg)](https://www.mongodb.com/atlas)
[![Groq](https://img.shields.io/badge/LLM-Groq-orange.svg)](https://groq.com/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)

## Overview

Mini RAG System is a document-based AI assistant that allows users to upload PDF documents and ask questions about their content.

It uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from uploaded documents and generate answers using a Large Language Model (LLM).

Instead of answering questions entirely from its pre-trained knowledge, the system uses document retrieval to ground its responses in the uploaded content.

The project combines document ingestion, text extraction, chunking, embeddings, vector search, and LLM-based answer generation into one workflow.

## Key Features

### 1. PDF Document Ingestion

- Upload PDF documents.
- Extract text from uploaded PDFs.
- Process documents into manageable text chunks.
- Associate chunks with their respective document IDs.
- Store document content and metadata for retrieval.

### 2. Text Chunking

Large documents are divided into smaller chunks to improve retrieval accuracy.

- Split extracted text into manageable sections.
- Maintain document metadata.
- Generate embeddings for individual chunks.
- Store chunks for semantic retrieval.

### 3. Vector Embeddings

The system uses **Jina AI's `jina-embeddings-v3`** embedding model through its hosted API.

- Convert document chunks into numerical vectors.
- Generate query embeddings.
- Use 1024-dimensional embeddings.
- Support semantic similarity search.

### 4. MongoDB Atlas Vector Search

MongoDB Atlas is used as the vector database.

- Store document chunks and their embeddings.
- Perform semantic vector searches.
- Retrieve the most relevant document sections.
- Filter retrieval by document ID.
- Support multiple documents.

**Vector Search Configuration:**

| Setting | Value |
|---|---|
| Database | `rag_database` |
| Collection | `documents` |
| Vector Index | `jina_vector_index` |
| Embedding Field | `embedding_jina` |
| Embedding Dimensions | 1024 |
| Retrieval Candidates | 80 |
| Retrieved Chunks | 3 |

### 5. LLM-Based Answer Generation

The system uses Groq Cloud to generate answers from retrieved document context.

- Uses `openai/gpt-oss-120b`.
- Supplies retrieved document chunks as context.
- Generates answers based on available document information.
- Avoids relying on unrelated general knowledge.

### 6. Document-Grounded Responses

One of the main objectives is to keep responses grounded in the uploaded documents.

If the requested information cannot be found in the document, the system returns:

> I could not find that information in the uploaded document.

This helps reduce unsupported answers and hallucinations.

### 7. Document-Based Retrieval

Each document can be identified using its document ID.

This allows the retrieval system to search within the relevant document instead of mixing information from unrelated uploads.

## How RAG Works

The application follows two main processes: document ingestion and question answering.

### Document Ingestion Pipeline

```text
       UPLOAD PDF
            |
            v
       EXTRACT TEXT
            |
            v
       TEXT CHUNKING
            |
            v
      JINA EMBEDDINGS
            |
            v
    GENERATE VECTORS
            |
            v
   MONGODB ATLAS STORAGE
```

### Question Answering Pipeline

```text
       USER QUESTION
             |
             v
      QUERY EMBEDDING
             |
             v
     MONGODB VECTOR SEARCH
             |
             v
    RETRIEVE TOP 3 CHUNKS
             |
             v
       BUILD CONTEXT
             |
             v
       GROQ LLM
             |
             v
     DOCUMENT-GROUNDED
          ANSWER
             |
             v
        USER RESPONSE
```

If the retrieval process cannot find sufficient relevant information, the system uses a predefined refusal response instead of generating an unsupported answer.

## Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python 3.12+ |
| Backend | FastAPI |
| RAG Framework | LangChain |
| LLM Provider | Groq Cloud |
| Language Model | GPT-OSS 120B |
| Embedding Model | Jina Embeddings v3 |
| Vector Database | MongoDB Atlas |
| PDF Processing | PyPDF |
| Text Splitting | LangChain Text Splitters |
| HTTP Requests | Requests |
| Package Manager | uv |
| Frontend | HTML, CSS, JavaScript |

## Project Structure

```text
mini-rag-system/
│
├── app/
│
├── data/
│
├── frontend/
│
├── scripts/
│
├── src/
│   └── mini_rag_system/
│
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

## Getting Started

### Prerequisites

Make sure you have:

- Python 3.12 or higher
- uv package manager
- MongoDB Atlas account
- Groq API key
- Jina AI API key

### 1. Clone the Repository

```bash
git clone https://github.com/digvijayforreal/mini-rag-system.git

cd mini-rag-system
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Configure Environment Variables

Create a `.env` file in the project root and configure your API credentials.

```env
GROQ_API_KEY=your_groq_api_key

JINA_API_KEY=your_jina_api_key

MONGODB_URI=your_mongodb_connection_string
```

Never commit your `.env` file or expose your API keys.

### 4. Configure MongoDB Atlas

Create a MongoDB Atlas database and configure the vector search index.

Use the following configuration:

| Field | Value |
|---|---|
| Database | `rag_database` |
| Collection | `documents` |
| Index Name | `jina_vector_index` |
| Vector Field | `embedding_jina` |
| Dimensions | `1024` |
| Similarity | `cosine` |

Ensure the vector index configuration matches the embedding field and dimensions used by the application.

### 5. Run the Application

Use the project's configured entry point:

```bash
uv run mini-rag-system
```

If you use a different development entry point, follow the corresponding application startup command in the source code.

## Example Usage

1. Start the application.
2. Open the web interface.
3. Upload a PDF document.
4. Allow the system to process and index the document.
5. Enter a question related to the uploaded document.
6. The system retrieves relevant chunks from MongoDB.
7. Groq generates an answer using the retrieved context.
8. If the answer is not supported by the document, the system returns its refusal message.

**Example:**

Question:

```text
Who is the project coordinator?
```

Expected answer:

```text
Mira Shah
```

An unrelated question:

```text
Who won the FIFA World Cup?
```

Expected response:

```text
I could not find that information in the uploaded document.
```

*The example uses the sample document included during development.*

## Important Design Principles

- **Grounded Generation:** Answers should be based on retrieved document content.
- **Semantic Retrieval:** Use vector similarity instead of relying only on keyword matching.
- **Document Isolation:** Use document IDs to keep retrieval scoped to the relevant document.
- **Controlled Responses:** Refuse questions that cannot be answered from the available document context.
- **Modular Architecture:** Keep ingestion, embedding, retrieval, and generation responsibilities separate.

## Future Improvements

- Persistent conversation history.
- Better multi-document management.
- Source references and page-level citations.
- Improved retrieval evaluation.
- Configurable chunk sizes and retrieval parameters.
- Enhanced document-processing support.
- More detailed frontend monitoring.

## Author

**Digvijay Mali**

GitHub: [@digvijayforreal](https://github.com/digvijayforreal)

Project: [Mini RAG System](https://github.com/digvijayforreal/mini-rag-system)

---

**Built with Python, LangChain, MongoDB Atlas, Jina AI, and Groq.**