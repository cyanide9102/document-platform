from abc import ABC, abstractmethod
from typing import BinaryIO


class DocumentProcessor(ABC):
    @abstractmethod
    async def process(self, document: BinaryIO, schema: BinaryIO):
        pass
