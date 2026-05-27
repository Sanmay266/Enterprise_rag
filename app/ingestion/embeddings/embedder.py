from typing import List

from sentence_transformers import SentenceTransformer

from app.ingestion.schemas.document import Chunk


class Embedder:

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en-v1.5",
    ):

        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> List[float]:

        embedding = self.model.encode(text)

        return embedding.tolist()

    def embed_chunks(self, chunks: List[Chunk]) -> List[List[float]]:

        texts = [chunk.content for chunk in chunks]

        embeddings = self.model.encode(texts)

        return embeddings.tolist()