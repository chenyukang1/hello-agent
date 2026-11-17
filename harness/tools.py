from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Tool:
    name: str
    run: Callable[[dict], Any]
    description: str = ""  # advertised to the model
    input_schema: dict = field(default_factory=dict)
    is_read_only: bool = False
    is_concurrency_safe: bool = False  # may batch in parallel
    is_edit: bool = False


class Registry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool):
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def schemas(self) -> list[dict]:
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema,
            }
            for tool in self._tools.values()
        ]
