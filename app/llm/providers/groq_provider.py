from groq import Groq

from app.core.config import get_settings


class GroqProvider:

    def __init__(self):

        settings = get_settings()

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful enterprise RAG assistant. "
                        "Answer ONLY using the provided context. "
                        "If answer is not in context, say you don't know."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
        )

        return response.choices[0].message.content