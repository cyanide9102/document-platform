from dataclasses import dataclass


@dataclass(frozen=True)
class CreateXPathRuleRequest:
    name: str
    expression: str
    namespaces: dict[str, str]
