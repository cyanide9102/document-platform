from abc import ABC, abstractmethod
from typing import BinaryIO
from uuid import UUID


class DocumentStorage(ABC):
    @abstractmethod
    async def save(self, document_id: UUID, content: BinaryIO) -> str:
        pass

    @abstractmethod
    async def get(self, document_id: UUID) -> BinaryIO:
        pass

    @abstractmethod
    async def delete(self, document_id: UUID):
        pass
