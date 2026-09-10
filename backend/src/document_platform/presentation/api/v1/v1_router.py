from fastapi import APIRouter

from document_platform.presentation.api.v1.documents import router as document_router

router = APIRouter(prefix="/v1")
router.include_router(document_router)
