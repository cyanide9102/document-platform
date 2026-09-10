from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from document_platform.application.documents.use_cases import (
    CreateDocumentUseCase,
    GetDocumentUseCase,
    ListDocumentsUseCase,
)
from document_platform.presentation.api.dependencies import (
    get_create_document_use_case,
    get_get_document_use_case,
    get_list_documents_use_case,
)
from document_platform.presentation.api.v1.schemas.documents import (
    CreateDocumentRequest,
    DocumentResponse,
)

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
    request: CreateDocumentRequest,
    use_case: CreateDocumentUseCase = Depends(get_create_document_use_case),
) -> DocumentResponse:
    document = await use_case.execute(request.name)

    return DocumentResponse(
        id=document.id,
        name=document.name,
        status=document.status,
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
            status=document.status,
        )
        for document in documents
    ]


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
        status=document.status,
    )
