from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from document_platform.infrastructure.persistence.database import (
    engine,
    session_factory,
)


@pytest_asyncio.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    # Transaction is rolled back after every test
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


@pytest_asyncio.fixture
async def database_session() -> AsyncGenerator[AsyncSession, None]:
    # Real session/transaction lifecycle
    async with session_factory() as session:
        yield session
