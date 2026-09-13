from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from document_platform.domain.schemas import (
    XmlSchemaXPathRule,
    XmlSchemaXPathRuleRepository,
)
from document_platform.infrastructure.persistence.mappers import (
    XmlSchemaXPathRuleMapper,
)
from document_platform.infrastructure.persistence.models import XmlSchemaXPathRuleModel


class SqlAlchemyXmlSchemaXPathRuleRepository(XmlSchemaXPathRuleRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, rule: XmlSchemaXPathRule):
        model = XmlSchemaXPathRuleMapper.to_model(rule)

        self._session.add(model)

    async def list_by_schema_id(self, schema_id: UUID) -> list[XmlSchemaXPathRule]:
        statement = (
            select(XmlSchemaXPathRuleModel)
            .where(XmlSchemaXPathRuleModel.schema_id == schema_id)
            .order_by(XmlSchemaXPathRuleModel.created_at.asc())
        )

        result = await self._session.execute(statement)
        models = result.scalars().all()

        return [XmlSchemaXPathRuleMapper.to_domain(model) for model in models]

    async def get_by_id(self, rule_id: UUID) -> XmlSchemaXPathRule | None:
        statement = select(XmlSchemaXPathRuleModel).where(
            XmlSchemaXPathRuleModel.id == rule_id
        )

        result = await self._session.execute(statement)
        model = result.scalar_one_or_none()
        if model is None:
            return None

        return XmlSchemaXPathRuleMapper.to_domain(model)

    async def delete(self, rule_id):
        statement = delete(XmlSchemaXPathRuleModel).where(
            XmlSchemaXPathRuleModel.id == rule_id
        )
        await self._session.execute(statement)
