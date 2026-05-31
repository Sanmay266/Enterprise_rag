from typing import List, Dict

from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self):

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    def rerank(
        self,
        query: str,
        results: List[Dict],
    ) -> List[Dict]:

        pairs = []

        for result in results:

            pairs.append(
                (
                    query,
                    result["content"]
                )
            )

        scores = self.model.predict(
            pairs
        )

        for result, score in zip(
            results,
            scores,
        ):

            result[
                "rerank_score"
            ] = float(score)

        results.sort(
            key=lambda x: x[
                "rerank_score"
            ],
            reverse=True,
        )

        return results