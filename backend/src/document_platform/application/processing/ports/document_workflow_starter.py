from abc import ABC, abstractmethod
from uuid import UUID


class DocumentWorkflowStarter(ABC):
    @abstractmethod
    async def start(self, document_id: UUID):
        pass
