from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from document_platform.application.documents.use_cases import (
    CreateDocument,
    GetDocument,
    ListDocuments,
)
from document_platform.presentation.api.dependencies import (
    get_create_document,
    get_get_document,
    get_list_documents,
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
    use_case: CreateDocument = Depends(get_create_document),
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
    use_case: ListDocuments = Depends(get_list_documents),
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
    use_case: GetDocument = Depends(get_get_document),
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
