from abc import ABC, abstractmethod
from typing import BinaryIO
from uuid import UUID


class FileStorage(ABC):
    @abstractmethod
    async def save(self, file_id: UUID, content: BinaryIO):
        pass

    @abstractmethod
    async def get(self, file_id: UUID) -> BinaryIO:
        pass

    @abstractmethod
    async def delete(self, file_id: UUID):
        pass
