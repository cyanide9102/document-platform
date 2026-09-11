from fastapi import APIRouter

from document_platform.presentation.api.v1.documents import router as document_router

router = APIRouter(prefix="/api")

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(document_router)


router.include_router(v1_router)
