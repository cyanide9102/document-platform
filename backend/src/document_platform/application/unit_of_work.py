from abc import ABC, abstractmethod
from types import TracebackType

from document_platform.domain.documents.repositories import DocumentRepository
from document_platform.domain.schemas.repositories import XmlSchemaRepository


class UnitOfWork(ABC):
    documents: DocumentRepository
    schemas: XmlSchemaRepository

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
