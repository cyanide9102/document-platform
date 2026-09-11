from abc import ABC, abstractmethod
from typing import BinaryIO
from uuid import UUID


class DocumentStorage(ABC):
    @abstractmethod
    async def save(
        self,
        document_id: UUID,
        filename: str,
        content: BinaryIO,
    ) -> str:
        pass

    @abstractmethod
    async def get(self, storage_key: str) -> BinaryIO:
        pass

    @abstractmethod
    async def delete(self, storage_key: str):
        pass
