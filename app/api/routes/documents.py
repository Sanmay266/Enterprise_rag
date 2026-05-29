from fastapi import APIRouter

from app.storage.sqlite.document_repository import (
    DocumentRepository,
)

router = APIRouter()


@router.get("/documents")
async def list_documents():

    repository = DocumentRepository()

    documents = repository.get_all_documents()

    return {
        "documents": documents
    }