"""
the allow / ask / deny decision between a
model's tool request and execution. Introduced in section 3, then carried
forward unchanged. Modes mirror Claude Code's types/permissions.ts.
"""

from tools import Tool

DEFAULT, ACCEPT_EDITS, PLAN, BYPASS = (
    "default",
    "acceptEdits",
    "plan",
    "bypassPermissions",
)


def decide(tool: Tool, mode: str, allow_rules: set) -> str:
    """Return 'allow', 'ask', or 'deny' for running `tool` under `mode`."""
    if mode == BYPASS:
        return "allow"

    if mode == PLAN:
        if tool.is_read_only:
            return "allow"
        if tool.name == "ExitPlanMode":
            return "ask"
        return "deny"

    if tool.is_read_only or tool.name in allow_rules:
        return "allow"

    if mode == ACCEPT_EDITS and tool.is_edit:
        return "allow"

    return "ask"
