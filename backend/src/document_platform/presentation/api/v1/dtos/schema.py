from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SchemaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    size: int
    created_at: datetime


class SchemaXPathRuleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    schema_id: UUID
    name: str
    expression: str
    namespaces: dict[str, str] = Field(default_factory=dict)
    created_at: datetime
