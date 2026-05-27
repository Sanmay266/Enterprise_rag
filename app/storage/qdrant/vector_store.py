from typing import List
from uuid import uuid4

from qdrant_client.models import Distance, VectorParams, PointStruct

from app.ingestion.schemas.document import Chunk
from app.storage.qdrant.client import get_qdrant_client


class QdrantVectorStore:

    def __init__(
        self,
        collection_name: str = "scalable_rag",
    ):

        self.client = get_qdrant_client()

        self.collection_name = collection_name

    def create_collection(
        self,
        vector_size: int,
    ):

        collections = self.client.get_collections().collections

        collection_names = [
            collection.name
            for collection in collections
        ]

        if self.collection_name in collection_names:
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )

    def add_chunks(
        self,
        chunks: List[Chunk],
        embeddings: List[List[float]],
    ):

        points = []

        for chunk, embedding in zip(chunks, embeddings):

            point = PointStruct(
                id=str(uuid4()),
                vector=embedding,
                payload={
                    "content": chunk.content,
                    **chunk.metadata,
                }
            )

            points.append(point)

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )