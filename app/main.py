from fastapi import FastAPI

from app.core.config import get_settings
from app.core.logger import setup_logging

from app.api.routes.health import (
    router as health_router
)

from app.api.routes.chat import (
    router as chat_router
)

from app.api.routes.ingest import (
    router as ingest_router
)



settings = get_settings()

setup_logging()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)


app.include_router(health_router)

app.include_router(chat_router)

app.include_router(
    ingest_router
)



@app.get("/")
async def root():

    return {
        "message": "Enterprise RAG API running",
        "version": settings.APP_VERSION,
    }