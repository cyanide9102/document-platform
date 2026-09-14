from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from document_platform.infrastructure.persistence.database import Base


class XmlSchemaXPathRuleModel(Base):
    __tablename__ = "xml_schema_xpath_rules"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
    )

    schema_id: Mapped[UUID] = mapped_column(
        ForeignKey("xml_schemas.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    expression: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    namespaces: Mapped[dict[str, str]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    rule_type: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="extract",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "schema_id",
            "name",
            name="uq_xml_schema_xpath_rules_schema_id_name",
        ),
    )
