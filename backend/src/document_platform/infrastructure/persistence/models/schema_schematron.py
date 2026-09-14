from datetime import datetime
from uuid import UUID

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from document_platform.infrastructure.persistence.database import Base


class XmlSchemaSchematronModel(Base):
    __tablename__ = "xml_schema_schematrons"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
    )

    schema_id: Mapped[UUID] = mapped_column(
        ForeignKey("xml_schemas.id", ondelete="CASCADE"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    size: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    content_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "schema_id",
            name="uq_xml_schema_schematrons_schema_id",
        ),
    )
