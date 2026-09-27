from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class Tool:
    name: str
    run: Callable[[dict], Any]
    description: str = ""
    input_shcema: dict = {}
    is_read_only: bool = False
    is_edit: bool = False


class Registry:
    def register(self, tool):
        self._tools[tool.name] = tool

    def get(self, name):
        return self._tools.get(name)
