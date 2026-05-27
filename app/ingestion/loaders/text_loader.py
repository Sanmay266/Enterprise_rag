from pathlib import Path

from app.ingestion.schemas.document import Document


class TextLoader:

    @staticmethod
    def load(file_path: str) -> Document:

        path = Path(file_path)

        text = path.read_text(encoding="utf-8")

        return Document(
            content=text,
            metadata={
                "source": str(path),
                "file_type": "txt",
            }
        )