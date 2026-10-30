import os
import requests

from dotenv import load_dotenv
from langchain_core.embeddings import Embeddings

load_dotenv()


class JinaEmbeddings(Embeddings):

    def __init__(self):
        self.api_key = os.getenv("JINA_API_KEY")
        self.model = os.getenv(
            "JINA_MODEL",
            "jina-embeddings-v3"
        )

        self.url = "https://api.jina.ai/v1/embeddings"

        if not self.api_key:
            raise ValueError("JINA_API_KEY not found in .env")

    def _embed(self, texts: list[str], task: str):

        payload = {
            "model": self.model,
            "task": task,
            "dimensions": 1024,
            "input": texts
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            self.url,
            headers=headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()["data"]
        data.sort(key=lambda item: item["index"])

        return [item["embedding"] for item in data]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._embed(texts, "retrieval.passage")

    def embed_query(self, text: str) -> list[float]:
        return self._embed([text], "retrieval.query")[0]