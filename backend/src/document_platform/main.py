from contextlib import asynccontextmanager

from fastapi import FastAPI

from document_platform.config.settings import settings
from document_platform.infrastructure.temporal.client import create_temporal_client
from document_platform.presentation.api.router import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.temporal_client = await create_temporal_client(settings.temporal)

    yield


app = FastAPI(
    title="Document Processing & Signing Platform",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(api_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
