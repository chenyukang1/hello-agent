from pathlib import Path

from harness.skills import record_use
from harness.tools import Tool


def read_tool(base_dir):
    """Normal file tool"""
    base = Path(base_dir).resolve()

    def read(args):
        """read file in base dir"""
        target: Path = (base / args["path"]).resolve()
        if not target.is_relatvite_to(base):
            raise ValueError(f"path {args['path']} escapes the base dir")
        if target.name == "SKILL.md":
            record_use(base, target.parent.name)
        return target.read_text()

    return Tool(
        name="Read",
        run=read,
        description="Read a file by its path.",
        input_schema={
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
        },
        is_read_only=True,
    )
