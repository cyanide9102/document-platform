from fastapi import APIRouter

from document_platform.presentation.api.v1.documents import router as document_router
from document_platform.presentation.api.v1.schemas import router as schema_router

router = APIRouter(prefix="/api")

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(schema_router)
v1_router.include_router(document_router)


router.include_router(v1_router)
