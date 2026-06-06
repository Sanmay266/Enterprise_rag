from rank_bm25 import BM25Okapi

from app.storage.sqlite.document_repository import (
    DocumentRepository,
)


class BM25Retriever:

    # BM25 retrieval over the SQLite chunk registry.

    def __init__(self):

        self.repository = DocumentRepository()

        chunks = self.repository.get_all_chunks()

        self.documents = []

        self.metadata = []

        for chunk in chunks:

            self.documents.append(
                chunk[3]
            )

            self.metadata.append(
                {
                    "document_id": chunk[1],
                    "chunk_id": chunk[2],
                }
            )

        tokenized_docs = [
            doc.lower().split()
            for doc in self.documents
        ]

        if tokenized_docs:

            self.bm25 = BM25Okapi(
                tokenized_docs
            )

        else:

            self.bm25 = None

    def search(
        self,
        query: str,
        limit: int = 5,
    ):

        if self.bm25 is None:

            return []

        tokenized_query = (
            query.lower().split()
        )

        scores = self.bm25.get_scores(
            tokenized_query
        )

        ranked = sorted(
            zip(
                scores,
                self.documents,
                self.metadata,
            ),
            key=lambda x: x[0],
            reverse=True,
        )

        results = []

        for score, doc, meta in ranked[:limit]:

            results.append(
                {
                    "score": float(score),
                    "content": doc,
                    "metadata": meta,
                }
            )

        return results