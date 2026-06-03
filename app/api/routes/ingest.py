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

    repository = DocumentRepository()

    document_id = repository.add_document(
        filename=file.filename,
        chunk_count=0,
        status="processing",
    )

    pipeline = IngestionPipeline()

    result = pipeline.ingest(
        str(file_path),
        document_id=document_id,
    )

    return {
        "message": "Document ingested successfully",
        "document_id": document_id,
        "result": result,
    }