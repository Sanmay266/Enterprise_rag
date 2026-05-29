from typing import List

from app.ingestion.embeddings.embedder import Embedder

from app.storage.qdrant.client import get_qdrant_client


class Retriever:

    def __init__(
        self,
        collection_name: str = "scalable_rag",
    ):

        self.collection_name = collection_name

        self.client = get_qdrant_client()

        self.embedder = Embedder()

    def search(
        self,
        query: str,
        limit: int = 3,
    ) -> List[dict]:

        # Convert query into embedding
        query_embedding = self.embedder.embed_text(
            query
        )

        # Search Qdrant
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=limit,
        ).points

        # Format results
        formatted_results = []

        for result in results:

            formatted_results.append({
                "score": result.score,
                "content": result.payload.get("content"),
                "metadata": result.payload,
            })

        return formatted_results