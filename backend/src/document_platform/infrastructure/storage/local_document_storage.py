from pathlib import Path
from typing import BinaryIO
from uuid import UUID

from document_platform.application.documents.ports import DocumentStorage


class LocalDocumentStorage(DocumentStorage):
    def __init__(self, root_path: Path):
        self._documents_path = root_path / "documents"

        self._documents_path.mkdir(parents=True, exist_ok=True)

    async def save(self, document_id: UUID, content: BinaryIO):
        file_path = self._documents_path / str(document_id)

        with file_path.open("wb") as file:
            while chunk := content.read(1024 * 1024):
                file.write(chunk)

    async def get(self, document_id: UUID) -> BinaryIO:
        file_path = self._documents_path / str(document_id)
        if not file_path.is_file():
            raise FileNotFoundError(f"Content not found for document: {document_id}")

        return file_path.open("rb")

    async def delete(self, document_id: UUID):
        file_path = self._documents_path / str(document_id)
        if file_path.exists():
            file_path.unlink()
