from pathlib import Path
from typing import BinaryIO
from uuid import UUID

from document_platform.application.storage.ports import FileStorage


class LocalFileStorage(FileStorage):
    def __init__(self, root_path: Path):
        self._root_path = root_path
        self._root_path.mkdir(parents=True, exist_ok=True)

    async def save(self, file_id: UUID, content: BinaryIO):
        file_path = self._root_path / str(file_id)

        with file_path.open("wb") as file:
            while chunk := content.read(1024 * 1024):
                file.write(chunk)

    async def get(self, file_id: UUID) -> BinaryIO:
        file_path = self._root_path / str(file_id)
        if not file_path.is_file():
            raise FileNotFoundError(f"File not found: {file_id}")

        return file_path.open("rb")

    async def delete(self, file_id: UUID):
        file_path = self._root_path / str(file_id)
        if file_path.exists():
            file_path.unlink()
