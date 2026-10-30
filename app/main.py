from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="Mini RAG System",
    description="Document-grounded AI Assistant",
    version="2.0.0"
)

# Existing API routes
app.include_router(router)

# Serve CSS and JavaScript
app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIR)),
    name="static"
)

# Serve frontend at root URL
@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")