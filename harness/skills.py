from dataclasses import dataclass
from pathlib import Path


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


def _split(text):
    """Minimal SKILL.md parse into (frontmatter dict, body). ponytail: assumes a
    well-formed '---\\n<key: value>...\\n---\\n<body>' header (real CC uses YAML)."""
    _, frontmatter, body = text.split("---", 2)
    meta = {
        k.strip(): v.strip()
        for k, v in (line.split(":", 1) for line in frontmatter.strip().splitlines() if ":" in line)
    }
    return meta, body.strip()


if __name__ == "__main__":
    load_skills(".")
