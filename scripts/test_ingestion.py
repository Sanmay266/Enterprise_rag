from app.ingestion.loaders.text_loader import TextLoader
from app.ingestion.parsers.text_cleaner import TextCleaner
from app.ingestion.chunkers.recursive import RecursiveChunker
from app.ingestion.embeddings.embedder import Embedder

from app.storage.qdrant.vector_store import QdrantVectorStore


def test_qdrant():

    document = TextLoader.load("sample.txt")

    cleaned_text = TextCleaner.clean(document.content)

    document.content = cleaned_text

    chunker = RecursiveChunker(
        chunk_size=100,
        chunk_overlap=20,
    )

    chunks = chunker.chunk(document)

    embedder = Embedder()

    embeddings = embedder.embed_chunks(chunks)

    vector_store = QdrantVectorStore()

    vector_store.create_collection(
        vector_size=len(embeddings[0]),
    )

    vector_store.add_chunks(
        chunks=chunks,
        embeddings=embeddings,
    )

    print("\nChunks stored successfully in Qdrant!")


if __name__ == "__main__":

    test_qdrant()