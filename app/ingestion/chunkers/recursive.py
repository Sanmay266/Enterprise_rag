from typing import List

from app.ingestion.chunkers.base import BaseChunker
from app.ingestion.schemas.document import Document, Chunk


class RecursiveChunker(BaseChunker):

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
        min_chunk_size: int = 50,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size

    def chunk(self, document: Document) -> List[Chunk]:

        text = document.content

        chunks = []

        start = 0
        chunk_id = 0

        while start < len(text):

            end = start + self.chunk_size

            chunk_text = text[start:end].strip()

            # Skip tiny meaningless chunks
            if len(chunk_text) < self.min_chunk_size:
                break

            chunk = Chunk(
                content=chunk_text,
                metadata={
                    **document.metadata,
                    "chunk_id": chunk_id,
                    "start_index": start,
                    "end_index": end,
                }
            )

            chunks.append(chunk)

            start += self.chunk_size - self.chunk_overlap

            chunk_id += 1

        return chunks