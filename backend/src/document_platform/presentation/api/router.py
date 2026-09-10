from fastapi import APIRouter

from document_platform.presentation.api.v1.v1_router import router as v1_router

router = APIRouter(prefix="/api")
router.include_router(v1_router)
