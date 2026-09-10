from datetime import UTC, datetime
from uuid import UUID, uuid4

from document_platform.domain.documents.enums import DocumentStatus


class Document:
    def __init__(
        self,
        id: UUID,
        name: str,
        status: DocumentStatus,
        created_at: datetime,
        updated_at: datetime,
    ):
        self.id = id
        self.name = name
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def create(cls, name: str) -> "Document":
        normalized_name = name.strip()
        if not normalized_name:
            raise ValueError("Document name cannot be empty.")

        now = datetime.now(UTC)

        return cls(
            id=uuid4(),
            name=normalized_name,
            status=DocumentStatus.DRAFT,
            created_at=now,
            updated_at=now,
        )
