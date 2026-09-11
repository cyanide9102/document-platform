from pathlib import Path
from typing import BinaryIO
from uuid import UUID

from document_platform.application.documents.ports import DocumentStorage


class LocalDocumentStorage(DocumentStorage):
    def __init__(self, root_path: Path):
        self._root_path = root_path
        self._documents_path = root_path / "documents"

        self._documents_path.mkdir(parents=True, exist_ok=True)

    async def save(
        self,
        document_id: UUID,
        filename: str,
        content: BinaryIO,
    ) -> str:
        document_directory = self._documents_path / str(document_id)
        document_directory.mkdir(parents=True, exist_ok=True)

        normalized_filename = Path(filename).name
        if not normalized_filename:
            raise ValueError("Document filename cannot be empty.")

        storage_key = f"documents/{document_id}/{normalized_filename}"
        file_path = self._resolve_storage_path(storage_key)

        with file_path.open("wb") as file:
            while chunk := content.read(1024 * 1024):
                file.write(chunk)

        return storage_key

    async def get(self, storage_key: str) -> BinaryIO:
        file_path = self._resolve_storage_path(storage_key)
        if not file_path.is_file():
            raise FileNotFoundError(f"Document content not found: {storage_key}")

        return file_path.open("rb")

    async def delete(self, storage_key: str):
        file_path = self._resolve_storage_path(storage_key)
        if file_path.exists():
            file_path.unlink()

    def _resolve_storage_path(self, storage_key: str) -> Path:
        file_path = (self._root_path / storage_key).resolve()
        if self._root_path not in file_path.parents:
            raise ValueError("Storage key resolves outside storage root.")

        return file_path
