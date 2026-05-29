import fitz

from app.ingestion.schemas.document import Document


class PDFLoader:

    @staticmethod
    def load(file_path: str) -> Document:

        pdf = fitz.open(file_path)

        pages = []

        for page_num, page in enumerate(pdf):

            text = page.get_text()

            pages.append(text)

        combined_text = "\n".join(pages)

        return Document(
            content=combined_text,
            metadata={
                "source": file_path,
                "file_type": "pdf",
                "total_pages": len(pdf),
            }
        )