import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from document_platform.domain.documents.entities import Document
from document_platform.infrastructure.persistence.unit_of_work import (
    SqlAlchemyUnitOfWork,
)


@pytest.mark.asyncio
async def test_add_and_get_document(database_session: AsyncSession):
    unit_of_work = SqlAlchemyUnitOfWork(database_session)
    document = Document.create(" invoice.xml ")

    async with unit_of_work:
        await unit_of_work.documents.add(document)
        await unit_of_work.commit()

        result = await unit_of_work.documents.get_by_id(document.id)

    assert result is not None
    assert result.id == document.id
    assert result.name == "invoice.xml"
    assert result.status == document.status
    assert result.created_at == document.created_at
    assert result.updated_at == document.updated_at
