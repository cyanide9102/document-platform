from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse

from document_platform.application.documents.use_cases import (
    CreateDocumentUseCase,
    GetDocumentContentUseCase,
    GetDocumentUseCase,
    ListDocumentsUseCase,
)
from document_platform.presentation.api.dependencies import (
    get_create_document_use_case,
    get_get_document_content_use_case,
    get_get_document_use_case,
    get_list_documents_use_case,
)
from document_platform.presentation.api.v1.schemas import DocumentResponse

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_document(
    file: UploadFile = File(...),
    use_case: CreateDocumentUseCase = Depends(get_create_document_use_case),
) -> DocumentResponse:
    document = await use_case.execute(
        name=file.filename,
        content=file.file,
        content_type=file.content_type,
    )

    return DocumentResponse(
        id=document.id,
        name=document.name,
        original_name=document.original_name,
        content_type=document.content_type,
        size=document.size,
        status=document.status,
        created_at=document.created_at,
        updated_at=document.updated_at,
    )


@router.get(
    "",
    response_model=list[DocumentResponse],
)
async def get_documents(
    use_case: ListDocumentsUseCase = Depends(get_list_documents_use_case),
) -> list[DocumentResponse]:
    documents = await use_case.execute()
    return [
        DocumentResponse(
            id=document.id,
            name=document.name,
            original_name=document.original_name,
            content_type=document.content_type,
            size=document.size,
            status=document.status,
            created_at=document.created_at,
            updated_at=document.updated_at,
        )
        for document in documents
    ]


@router.get("/{document_id}/content")
async def get_document_content(
    document_id: UUID,
    use_case: GetDocumentContentUseCase = Depends(get_get_document_content_use_case),
) -> StreamingResponse:
    document, content = await use_case.execute(document_id)
    if document is None or content is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    return StreamingResponse(
        content,
        media_type=document.content_type or "application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{document.original_name}"',
        },
    )


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
async def get_document(
    document_id: UUID,
    use_case: GetDocumentUseCase = Depends(get_get_document_use_case),
) -> DocumentResponse:
    document = await use_case.execute(document_id)
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    return DocumentResponse(
        id=document.id,
        name=document.name,
        original_name=document.original_name,
        content_type=document.content_type,
        size=document.size,
        status=document.status,
        created_at=document.created_at,
        updated_at=document.updated_at,
    )
