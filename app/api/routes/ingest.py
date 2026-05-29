from pathlib import Path

from fastapi import (
    APIRouter,
    UploadFile,
    File,
)

from app.ingestion.pipelines.ingestion_pipeline import (
    IngestionPipeline,
)

from app.storage.sqlite.document_repository import (
    DocumentRepository,
)

router = APIRouter()

UPLOAD_DIR = "uploads"

Path(
    UPLOAD_DIR
).mkdir(
    exist_ok=True
)


@router.post("/ingest")
async def ingest_document(
    file: UploadFile = File(...)
):

    file_path = (
        Path(UPLOAD_DIR)
        / file.filename
    )

    with open(
        file_path,
        "wb",
    ) as buffer:

        content = await file.read()

        buffer.write(content)

    pipeline = IngestionPipeline()

    result = pipeline.ingest(
        str(file_path)
    )

    repository = DocumentRepository()

    repository.add_document(
        filename=file.filename,
        chunk_count=result[
            "chunks_created"
        ],
        status="indexed",
    )

    return {
        "message": (
            "Document ingested successfully"
        ),
        "result": result,
    }