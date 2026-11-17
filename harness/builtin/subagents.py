from harness.loop import Session, loop
from harness.tools import Tool

SUBAGENTS_SCHEMA = {
    "type": "object",
    "properties": {"description": {"type": "string"}},
    "required": ["description"],
}


def agent_tool(call_model, registry, parent_session: Session):
    """subagents tool run child agents loop"""

    def spawn(args):
        """inner loop"""
        child_session = Session(mode=parent_session.mode, allow_rules=parent_session.allow_rules)
        mesaages = [{"role": "user", "content": args["description"]}]
        return loop(messages=mesaages, call_model=call_model, registry=registry, session=child_session)

    return Tool(
        "Agent",
        spawn,
        description="Delegate a subtask to a fresh subagent; returns only its final answer.",
        input_schema=SUBAGENTS_SCHEMA,
        is_read_only=True,
    )
