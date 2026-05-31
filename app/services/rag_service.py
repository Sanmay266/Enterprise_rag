from typing import List, Dict

from app.retrieval.retriever import Retriever

from app.retrieval.reranking.reranker import (
    Reranker,
)
from app.llm.providers.groq_provider import (
    GroqProvider,
)

self.reranker = Reranker()
class RAGService:

    def __init__(self):

        self.retriever = Retriever()

        self.llm = GroqProvider()

    def retrieve_context(
        self,
        question: str,
        limit: int = 3,
    ) -> List[Dict]:

        results = self.retriever.search(
            query=question,
            limit=limit,
        )

        return results

    def build_context(
        self,
        retrieval_results: List[Dict],
    ) -> str:

        context_blocks = []

        for index, result in enumerate(
            retrieval_results,
            start=1,
        ):

            content = result["content"]

            source = result["metadata"].get(
                "source",
                "unknown",
            )

            block = (
                f"[Document {index}]\n"
                f"Source: {source}\n\n"
                f"{content}"
            )

            context_blocks.append(block)

        return "\n\n".join(context_blocks)

    def build_prompt(
        self,
        question: str,
        context: str,
    ) -> str:

        prompt = f"""
You are an enterprise RAG assistant.

Use ONLY the provided context to answer.

If the answer cannot be found in the context,
respond with:
"I could not find the answer in the provided documents."

-----------------------------
CONTEXT
-----------------------------

{context}

-----------------------------
QUESTION
-----------------------------

{question}

-----------------------------
ANSWER
-----------------------------
"""

        return prompt

    def ask(
        self,
        question: str,
    ) -> Dict:

        # Step 1: Retrieve relevant chunks
        retrieval_results = self.retrieve_context(
            question=question,
            limit=3,
        )

        # Step 2: Build context
        context = self.build_context(
            retrieval_results
        )

        # Step 3: Build prompt
        prompt = self.build_prompt(
            question=question,
            context=context,
        )

        # Step 4: Generate answer
        answer = self.llm.generate(
            prompt=prompt
        )

        return {
            "question": question,
            "answer": answer,
            "sources": retrieval_results,
        }