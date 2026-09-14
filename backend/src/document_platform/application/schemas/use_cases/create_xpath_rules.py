from uuid import UUID

from document_platform.application.schemas.dtos.create_xpath_rule import (
    CreateXPathRuleRequest,
)
from document_platform.application.unit_of_work import UnitOfWork
from document_platform.domain.schemas import XmlSchemaXPathRule


class CreateXPathRulesUseCase:
    def __init__(self, unit_of_work: UnitOfWork):
        self._unit_of_work = unit_of_work

    async def execute(
        self,
        schema_id: UUID,
        requests: list[CreateXPathRuleRequest],
    ) -> list[XmlSchemaXPathRule]:
        async with self._unit_of_work:
            schema = await self._unit_of_work.schemas.get_by_id(schema_id)
            if schema is None:
                raise ValueError(f"Schema not found: {schema_id}")

            rules: list[XmlSchemaXPathRule] = []
            for request in requests:
                rule = XmlSchemaXPathRule.create(
                    schema_id=schema_id,
                    name=request.name,
                    expression=request.expression,
                    namespaces=request.namespaces,
                    rule_type=request.rule_type,
                )

                await self._unit_of_work.schema_xpath_rules.add(rule)
                rules.append(rule)

            await self._unit_of_work.commit()

            return rules
