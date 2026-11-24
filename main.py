import shutil
import tempfile
from pathlib import Path

from harness import hooks, permissions
from harness.builtin import agent_tool, find_file_tool
from harness.builtin.read import read_tool
from harness.hooks import Hooks
from harness.loop import Session, loop
from harness.skills import catalog_prompt, load_skills, write_skill_tool
from harness.tools import Registry
from model.openrouter import call_model

TURNS = [
    "Use the Agent tool to find the contetn of a.txt",
]

SYSTEM_PROMPT = "You are a tiny agent. Use the provided tools to answer. Be brief."
SKILLS_DIR = "./skills"
BUNDLED = Path(__file__).resolve().parent / "skills"


def demo():
    session = Session(mode=permissions.DEFAULT)

    sub_registry = Registry()
    sub_registry.register(tool=find_file_tool())

    parent_registry = Registry()
    parent_registry.register(tool=agent_tool(call_model=call_model, registry=sub_registry, parent_session=session))
    parent_registry.register(tool=write_skill_tool(SKILLS_DIR))
    parent_registry.register(tool=read_tool(SKILLS_DIR))

    debug_hooks = Hooks()
    debug_hooks.register(hooks.PRE_TOOL_USE, lambda name, args: print(f"[debug] tool used {name} with {args}"))
    debug_hooks.register(
        hooks.POST_TOOL_USE, lambda name, args, res: print(f"[debug] tool {name} with {args} res: {res}")
    )

    skills_dir = Path(tempfile.mkdtemp()) / "skills"
    shutil.copytree(BUNDLED, skills_dir)
    skills = load_skills(skills_dir)
    system_prompt = SYSTEM_PROMPT + "\n\n" + catalog_prompt(skills, skills_dir)

    messages = [{"role": "system", "content": system_prompt}]
    turn = "使用 hello-test 向小明问好"
    messages.append({"role": "user", "content": turn})
    reply = loop(messages, call_model=call_model, registry=parent_registry, session=session, hooks=debug_hooks)
    print(f"you -> {turn}")
    print(f"model -> {reply}")


if __name__ == "__main__":
    demo()
