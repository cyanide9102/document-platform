from datetime import UTC, datetime
from uuid import UUID, uuid4

from .enums import DocumentStatus


class Document:
    def __init__(
        self,
        id: UUID,
        name: str,
        original_name: str,
        content_type: str | None,
        size: int,
        content_hash: str,
        status: DocumentStatus,
        created_at: datetime,
        updated_at: datetime,
    ):
        self.id = id
        self.name = name
        self.original_name = original_name
        self.content_type = content_type
        self.size = size
        self.content_hash = content_hash
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def create(
        cls,
        name: str,
        content_type: str | None,
        size: int,
        content_hash: str,
    ) -> "Document":
        normalized_name = name.strip()
        if not normalized_name:
            raise ValueError("Document name cannot be empty.")

        if "/" in normalized_name or "\\" in normalized_name:
            raise ValueError("Document name cannot contain a path.")

        if size < 0:
            raise ValueError("Document size cannot be negative.")

        normalized_content_hash = content_hash.strip()
        if len(normalized_content_hash) != 64:
            raise ValueError("Document content hash must be a SHA-256 hash.")

        if any(
            character not in "0123456789abcdefABCDEF"
            for character in normalized_content_hash
        ):
            raise ValueError("Document content hash must be a hexadecimal string.")

        now = datetime.now(UTC)

        return cls(
            id=uuid4(),
            name=normalized_name,
            original_name=normalized_name,
            content_type=content_type,
            size=size,
            content_hash=normalized_content_hash,
            status=DocumentStatus.UPLOADED,
            created_at=now,
            updated_at=now,
        )

    def rename(self, name: str):
        normalized_name = name.strip()
        if not normalized_name:
            raise ValueError("Document name cannot be empty.")

        self.name = normalized_name
        self.updated_at = datetime.now(UTC)

    def start_processing(self):
        if self.status not in (DocumentStatus.UPLOADED, DocumentStatus.FAILED):
            raise ValueError(f"Cannot start processing from status '{self.status}'.")

        self.status = DocumentStatus.PROCESSING
        self.updated_at = datetime.now(UTC)

    def mark_processed(self):
        if self.status != DocumentStatus.PROCESSING:
            raise ValueError(
                f"Cannot mark document as processed from status '{self.status}'."
            )

        self.status = DocumentStatus.PROCESSED
        self.updated_at = datetime.now(UTC)

    def mark_failed(self):
        if self.status != DocumentStatus.PROCESSING:
            raise ValueError(
                f"Cannot mark document as failed from status '{self.status}'."
            )

        self.status = DocumentStatus.FAILED
        self.updated_at = datetime.now(UTC)
