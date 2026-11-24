import json
import time
from dataclasses import dataclass
from pathlib import Path

USAGE_FILE = ".usage.json"


@dataclass
class Skill:
    name: str
    description: str
    path: Path


def load_skills(skills_dir):
    """load skills from skills_dir"""
    skills = []
    for sub in sorted(Path(skills_dir).iterdir()):
        md = sub / "SKILL.md"
        if md.is_file():
            meta, _body = _split(md.read_text())
            skills.append(Skill(meta.get("name", sub.name), meta.get("description", ""), md))


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
