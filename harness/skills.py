import json
import time
from dataclasses import dataclass
from pathlib import Path

from harness.tools import Tool

USAGE_FILE = ".usage.json"


@dataclass
class Skill:
    name: str
    description: str
    path: Path


def load_skills(skills_dir: str):
    """load skills from skills_dir"""
    skills = []
    for sub in sorted(Path(skills_dir).iterdir()):
        md = sub / "SKILL.md"
        if md.is_file():
            meta, _body = _split(md.read_text())
            skills.append(Skill(meta.get("name", sub.name), meta.get("description", ""), md))


def write_skill(skills_dir: str, name: str, description: str, body: str) -> Path:
    """write skill with name in skllis dir"""
    base_path = Path(skills_dir).resolve()
    skill_path = (base_path / name / "SKILL.md").resolve()
    skill_path.parent.mkdir(parents=True, exist_ok=True)
    skill_path.write_text(f"---\nname: {name}\ndescription: {description}\n---\n{body}\n")
    return skill_path


def write_skill_tool(skills_dir: str) -> Tool:
    """write skill tool"""

    def write(args):
        write_skill(skills_dir, name=args["name"], description=args["description"], body=args["body"])
        return f"skill {args['name']!r} saved"

    return Tool(
        name="write skill",
        run=write,
        description="Save a reusable skill (name, description, body) for future runs.",
        input_schema={
            "type": "object",
            "properties": {"name": {"type": "string"}, "description": {"type": "string"}, "body": {"type": "string"}},
            "required": ["name", "description", "body"],
        },
    )


def catalog_prompt(skills: list[Skill], base_dir: str):
    """skills catalog prompt"""
    lines = [f"{s.name}:{s.description} (read {s.path.relative_to(base_dir)})" for s in skills]
    return "Available skills (read a skill's path with the Read tool to load it):\n" + "\n".join(lines)


def record_use(skills_dir: Path, name: str):
    """函数说明。"""
    skills_path = Path(skills_dir) / USAGE_FILE
    usage = json.loads(skills_path.read_text()) if skills_path.exists() else {}
    properties = usage.setdefault(name, {"uses": 0})
    properties["uses"] += 1
    properties["last_used_at"] = time.time()
    skills_path.write_text(json.dumps(usage))
    return properties


def _split(text):
    """Minimal SKILL.md parse into (frontmatter dict, body). ponytail: assumes a
    well-formed '---\\n<key: value>...\\n---\\n<body>' header (real CC uses YAML)."""
    _, frontmatter, body = text.split("---", 2)
    meta = {
        k.strip(): v.strip()
        for k, v in (line.split(":", 1) for line in frontmatter.strip().splitlines() if ":" in line)
    }
    return meta, body.strip()
