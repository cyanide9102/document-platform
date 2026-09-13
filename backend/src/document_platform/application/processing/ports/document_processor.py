from abc import ABC, abstractmethod
from typing import BinaryIO

from document_platform.application.processing.models import (
    ProcessingConfiguration,
    ProcessingResult,
)


class DocumentProcessor(ABC):
    @abstractmethod
    async def process(
        self,
        document: BinaryIO,
        schema: BinaryIO,
        configuration: ProcessingConfiguration,
    ) -> ProcessingResult:
        pass
