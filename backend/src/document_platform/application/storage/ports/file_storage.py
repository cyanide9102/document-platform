from abc import ABC, abstractmethod
from uuid import UUID


class FileStorage(ABC):
    @abstractmethod
    async def save(self, file_id: UUID, content: bytes):
        pass

    @abstractmethod
    async def get(self, file_id: UUID) -> bytes:
        pass

    @abstractmethod
    async def delete(self, file_id: UUID):
        pass
