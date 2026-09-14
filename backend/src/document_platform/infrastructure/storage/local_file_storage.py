import asyncio
from pathlib import Path
from uuid import UUID

import aiofiles

from document_platform.application.storage.ports import FileStorage


class LocalFileStorage(FileStorage):
    def __init__(self, root_path: Path):
        self._root_path = root_path
        self._root_path.mkdir(parents=True, exist_ok=True)

    async def save(self, file_id: UUID, content: bytes):
        file_path = self._root_path / str(file_id)

        async with aiofiles.open(file_path, "wb") as file:
            await file.write(content)

    async def get(self, file_id: UUID) -> bytes:
        file_path = self._root_path / str(file_id)
        if not file_path.is_file():
            raise FileNotFoundError(f"File not found: {file_id}")

        async with aiofiles.open(file_path, "rb") as file:
            return await file.read()

    async def delete(self, file_id: UUID):
        file_path = self._root_path / str(file_id)
        if file_path.exists():
            await asyncio.to_thread(file_path.unlink())
