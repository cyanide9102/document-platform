from datetime import datetime
from uuid import UUID

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from document_platform.infrastructure.persistence.database import Base


class DocumentModel(Base):
    __tablename__ = "documents"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    original_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    content_type: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )

    size: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    content_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
