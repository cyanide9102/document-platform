from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from document_platform.application.unit_of_work import UnitOfWork
from document_platform.infrastructure.persistence.repositories import (
    SqlAlchemyDocumentRepository,
)


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.documents = SqlAlchemyDocumentRepository(session)

    async def __aenter__(self) -> "SqlAlchemyUnitOfWork":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ):
        if exc_type is not None:
            await self.rollback()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
