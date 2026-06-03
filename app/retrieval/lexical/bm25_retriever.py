from typing import List, Dict, Any
from rank_bm25 import BM25Okapi

class BM25Retriever:
    def __init__(self):
        self.bm25 = None
        self.documents = []
        self.metadata = []

    def _tokenize(self, text: str) -> List[str]:
        if not isinstance(text, str):
            text = str(text)
        return text.lower().split()

    def fit(self, documents: List[str], metadata: List[Dict[str, Any]]) -> None:
        self.documents = documents
        self.metadata = metadata
        
        tokenized_corpus = [self._tokenize(doc) for doc in self.documents]
        self.bm25 = BM25Okapi(tokenized_corpus)

    def search(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        if not self.bm25:
            return []
            
        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)
        
        results = []
        for i, score in enumerate(scores):
            if score > 0:
                results.append({
                    "score": float(score),
                    "content": self.documents[i],
                    "metadata": self.metadata[i]
                })
                
        results = sorted(results, key=lambda x: x["score"], reverse=True)
        return results[:limit]
