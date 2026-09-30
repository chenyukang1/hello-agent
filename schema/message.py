from dataclasses import dataclass
from enum import StrEnum


class Role(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass
class Message:
    role: Role
    cotent: str


@dataclass
class ToolCall:
    id: str
    type: str
    name: str
    input: str


@dataclass
class ModelReply:
    finish_reason: str | None
    content: str | None
    tool_calls: list[ToolCall]
