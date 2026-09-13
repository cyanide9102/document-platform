from dataclasses import dataclass
from uuid import UUID


@dataclass
class DocumentWorkflowInput:
    document_id: UUID
