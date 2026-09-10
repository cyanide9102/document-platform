from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from document_platform.application.documents.use_cases import (
    CreateDocument,
    GetDocument,
    ListDocuments,
)
from document_platform.application.unit_of_work import UnitOfWork
from document_platform.infrastructure.persistence.database import session_factory
from document_platform.infrastructure.persistence.unit_of_work import (
    SqlAlchemyUnitOfWork,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session


async def get_unit_of_work(
    session: AsyncSession = Depends(get_session),
) -> UnitOfWork:
    return SqlAlchemyUnitOfWork(session)


async def get_create_document(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> CreateDocument:
    return CreateDocument(unit_of_work)


async def get_get_document(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> GetDocument:
    return GetDocument(unit_of_work)


async def get_list_documents(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> ListDocuments:
    return ListDocuments(unit_of_work)
