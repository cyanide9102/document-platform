from datetime import UTC, datetime
from uuid import UUID, uuid4

from .enums import DocumentStatus


class Document:
    def __init__(
        self,
        id: UUID,
        name: str,
        storage_key: str | None,
        content_type: str | None,
        size: int,
        status: DocumentStatus,
        created_at: datetime,
        updated_at: datetime,
    ):
        self.id = id
        self.name = name
        self.storage_key = storage_key
        self.content_type = content_type
        self.size = size
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def create(
        cls,
        name: str,
        content_type: str | None,
        size: int,
    ) -> "Document":
        normalized_name = name.strip()
        if not normalized_name:
            raise ValueError("Document name cannot be empty.")

        if size < 0:
            raise ValueError("Document size cannot be negative.")

        now = datetime.now(UTC)

        return cls(
            id=uuid4(),
            name=normalized_name,
            storage_key=None,
            content_type=content_type,
            size=size,
            status=DocumentStatus.DRAFT,
            created_at=now,
            updated_at=now,
        )

    def attach_storage(self, storage_key: str):
        if self.storage_key is not None:
            raise ValueError("Document already has a storage key.")

        normalized_storage_key = storage_key.strip()
        if not normalized_storage_key:
            raise ValueError("Storage key cannot be empty.")

        self.storage_key = normalized_storage_key
        self.updated_at = datetime.now(UTC)

    def mark_uploaded(self):
        if self.storage_key is None:
            raise ValueError("Cannot mark document as uploaded without storage key.")

        self.status = DocumentStatus.UPLOADED
        self.updated_at = datetime.now(UTC)
