from abc import ABC, abstractmethod
from types import TracebackType

from document_platform.domain.documents.repositories import DocumentRepository


class UnitOfWork(ABC):
    documents: DocumentRepository

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ):
        pass

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass
