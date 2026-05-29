from pathlib import Path

from app.ingestion.loaders.text_loader import TextLoader
from app.ingestion.loaders.pdf_loader import PDFLoader

from app.ingestion.parsers.text_cleaner import TextCleaner

from app.ingestion.chunkers.recursive import RecursiveChunker

from app.ingestion.embeddings.embedder import Embedder

from app.storage.qdrant.vector_store import QdrantVectorStore


class IngestionPipeline:

    def __init__(self):

        self.chunker = RecursiveChunker(
            chunk_size=500,
            chunk_overlap=100,
        )

        self.embedder = Embedder()

        self.vector_store = QdrantVectorStore()

    def load_document(self, file_path: str):

        extension = Path(file_path).suffix.lower()

        if extension == ".txt":
            return TextLoader.load(file_path)

        elif extension == ".pdf":
            return PDFLoader.load(file_path)

        else:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

    def ingest(self, file_path: str):

        # Load document
        document = self.load_document(file_path)

        # Clean text
        cleaned_text = TextCleaner.clean(
            document.content
        )

        document.content = cleaned_text

        # Chunk document
        chunks = self.chunker.chunk(document)

        # Generate embeddings
        embeddings = self.embedder.embed_chunks(
            chunks
        )

        # Create collection
        self.vector_store.create_collection(
            vector_size=len(embeddings[0])
        )

        # Store vectors
        self.vector_store.add_chunks(
            chunks=chunks,
            embeddings=embeddings,
        )

        return {
            "status": "success",
            "file": file_path,
            "chunks_created": len(chunks),
        }