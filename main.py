from harness import hooks, permissions
from harness.builtin import agent_tool, find_file_tool
from harness.hooks import Hooks
from harness.loop import Session, loop
from harness.tools import Registry
from model.openrouter import call_model

TURNS = [
    "Use the Agent tool to find the contetn of a.txt",
]


def demo():
    session = Session(mode=permissions.DEFAULT)

    sub_registry = Registry()
    sub_registry.register(tool=find_file_tool())

    parent_registry = Registry()
    parent_registry.register(tool=agent_tool(call_model=call_model, registry=sub_registry, parent_session=session))

    debug_hooks = Hooks()
    debug_hooks.register(hooks.PRE_TOOL_USE, lambda name, args: print(f"[debug] tool used {name} with {args}"))
    debug_hooks.register(
        hooks.POST_TOOL_USE, lambda name, args, res: print(f"[debug] tool {name} with {args} res: {res}")
    )

    messages = []
    for turn in TURNS:
        messages.append({"role": "user", "content": turn})
        reply = loop(messages, call_model=call_model, registry=parent_registry, session=session, hooks=debug_hooks)
        print(f"you -> {turn}")
        print(f"model -> {reply}")


if __name__ == "__main__":
    demo()
