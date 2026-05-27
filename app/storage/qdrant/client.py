from qdrant_client import QdrantClient


def get_qdrant_client():

    client = QdrantClient(
        host="localhost",
        port=6333,
    )

    return client