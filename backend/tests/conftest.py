from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from document_platform.infrastructure.persistence.database import engine


@pytest_asyncio.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with engine.connect() as connection:
        transaction = await connection.begin()

        session = AsyncSession(
            bind=connection,
            expire_on_commit=False,
        )

        try:
            yield session
        finally:
            await session.close()
            await transaction.rollback()
