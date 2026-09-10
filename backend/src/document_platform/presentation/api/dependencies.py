from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from document_platform.application.documents.use_cases import (
    CreateDocumentUseCase,
    GetDocumentUseCase,
    ListDocumentsUseCase,
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


async def get_create_document_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> CreateDocumentUseCase:
    return CreateDocumentUseCase(unit_of_work)


async def get_get_document_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> GetDocumentUseCase:
    return GetDocumentUseCase(unit_of_work)


async def get_list_documents_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
) -> ListDocumentsUseCase:
    return ListDocumentsUseCase(unit_of_work)
