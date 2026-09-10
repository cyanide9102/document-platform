import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from document_platform.domain.documents.entities import Document
from document_platform.infrastructure.persistence.repositories.document_repositories import (  # noqa: E501
    SqlAlchemyDocumentRepository,
)


@pytest.mark.asyncio
async def test_add_and_get_document(
    session: AsyncSession,
) -> None:
    repository = SqlAlchemyDocumentRepository(session)

    document = Document.create(" invoice.xml ")

    await repository.add(document)

    result = await repository.get_by_id(document.id)

    assert result is not None
    assert result.id == document.id
    assert result.name == "invoice.xml"
    assert result.status == document.status
    assert result.created_at == document.created_at
    assert result.updated_at == document.updated_at
