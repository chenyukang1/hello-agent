from ..loop import Session
from ..permissions import ACCEPT_EDITS
from ..tools import Tool

TODOS_SCHEMA = {
    "type": "object",
    "properties": {
        "todos": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"step": {"type": "string"}, "status": {"type": "string"}},
                "required": ["step", "status"],
            },
        },
    },
    "required": ["todos"],
}


def todo_tool(session: Session) -> Tool:
    """record the plan as a list of steps on the session"""

    def write(args) -> str:
        """write todos"""
        session.todos = list(args["todos"])
        done = sum(1 for t in session.todos if t.get("status") == "completed")
        return f"{len(session.todos)} todos {done} done"

    return Tool(
        "TodoWrite",
        write,
        description="Record the plan as a checklist of {step, status} items.",
        input_schema=TODOS_SCHEMA,
        is_read_only=True,
    )


def exit_plan_mode(session: Session, to_mode=ACCEPT_EDITS) -> Tool:
    """once the plan is approved, leave plan mode for `to_mode`"""

    def exit_plan(args) -> str:
        session.mode = to_mode
        return f"plan approved, mode now {to_mode}"

    return Tool("ExitPlanMode", exit_plan, description="Present the plan and leave plan mode once the user approves.")
