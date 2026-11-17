from harness import hooks, permissions
from harness.builtin import exit_plan_mode, todo_tool
from harness.hooks import Hooks
from harness.loop import Session, loop
from harness.tools import Registry
from model.openrouter import call_model

TURNS = [
    "Make a 2-step todo list for cleaning a kitchen, then say done.",
]


def demo():
    session = Session(mode=permissions.DEFAULT)

    registry = Registry()
    registry.register(tool=todo_tool(session))
    registry.register(tool=exit_plan_mode(session))

    debug_hooks = Hooks()
    debug_hooks.register(hooks.PRE_TOOL_USE, lambda name, args: print(f"[debug] tool used {name} with {args}"))
    debug_hooks.register(
        hooks.POST_TOOL_USE, lambda name, args, res: print(f"[debug] tool {name} with {args} res: {res}")
    )

    messages = []
    for turn in TURNS:
        messages.append({"role": "user", "content": turn})
        reply = loop(messages, call_model=call_model, registry=registry, session=session, hooks=debug_hooks)
        print(f"you -> {turn}")
        print(f"model -> {reply}")


if __name__ == "__main__":
    # args = {
    #     "todos": [
    #         {"step": "Clear and wipe down countertops, stove, and sink", "status": "pending"},
    #         {"step": "Sweep and mop the floor", "status": "pending"},
    #     ]
    # }
    # print(list(args["todos"]))
    demo()
