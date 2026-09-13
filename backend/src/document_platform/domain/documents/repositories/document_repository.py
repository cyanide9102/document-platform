from abc import ABC, abstractmethod
from uuid import UUID

from document_platform.domain.documents.entities.document import Document


class DocumentRepository(ABC):
    @abstractmethod
    async def add(self, document: Document):
        pass

    @abstractmethod
    async def update(self, document: Document):
        pass

    @abstractmethod
    async def get_by_id(self, document_id: UUID) -> Document | None:
        pass

    @abstractmethod
    async def list(self) -> list[Document]:
        pass

    @abstractmethod
    async def count_by_schema_id(self, schema_id: UUID) -> int:
        pass
