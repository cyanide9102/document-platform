from abc import ABC, abstractmethod

from document_platform.application.processing.models import (
    ProcessingConfiguration,
    ProcessingResult,
)


class DocumentProcessor(ABC):
    @abstractmethod
    async def process(
        self,
        document: bytes,
        schema: bytes,
        configuration: ProcessingConfiguration,
    ) -> ProcessingResult:
        pass
