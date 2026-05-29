from app.retrieval.retriever import Retriever


def test_retrieval():

    retriever = Retriever()

    results = retriever.search(
        query="What does enterprise RAG improve?",
        limit=3,
    )

    print(results)


if __name__ == "__main__":
    test_retrieval()