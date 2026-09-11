import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from document_platform.domain.documents import Document
from document_platform.infrastructure.persistence.unit_of_work import (
    SqlAlchemyUnitOfWork,
)


@pytest.mark.asyncio
async def test_add_and_get_document(database_session: AsyncSession):
    unit_of_work = SqlAlchemyUnitOfWork(database_session)

    document = Document.create(
        name=" invoice.xml ",
        content_type="application/xml",
        size=1024,
    )

    document.attach_storage(f"documents/{document.id}/invoice.xml")
    document.mark_uploaded()

    async with unit_of_work:
        await unit_of_work.documents.add(document)
        await unit_of_work.commit()

        result = await unit_of_work.documents.get_by_id(document.id)

    assert result is not None
    assert result.id == document.id
    assert result.name == "invoice.xml"
    assert result.storage_key == f"documents/{document.id}/invoice.xml"
    assert result.content_type == "application/xml"
    assert result.size == 1024
    assert result.status == document.status
    assert result.created_at == document.created_at
    assert result.updated_at == document.updated_at
