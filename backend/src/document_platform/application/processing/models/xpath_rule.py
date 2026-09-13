from pydantic import BaseModel, ConfigDict, Field


class XPathRule(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str = Field(min_length=1)
    expression: str = Field(min_length=1)
    namespaces: dict[str, str] = Field(default_factory=dict)
