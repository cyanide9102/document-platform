from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SchemaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    size: int
    created_at: datetime
