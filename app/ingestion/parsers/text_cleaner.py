import re


class TextCleaner:

    @staticmethod
    def clean(text: str) -> str:

        # Collapse whitespace
        text = re.sub(r"\s+", " ", text)

        # Remove excessive newlines
        text = re.sub(r"\n+", "\n", text)

        return text.strip()