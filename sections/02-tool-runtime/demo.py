from loop import loop
from tools import Registry, Tool

from schema.openrouter import call_model


def find_file(file_name):
    return "hello, agent"


TURNS = [
    "What's the content of a.txt?",
]


def demo():
    tool = Tool(
        "find_file",
        run=find_file,
        description="Obtain the content of file.",
        input_schema={
            "type": "function",
            "function": {
                "name": "find_file",
                "description": "Return the current UTC time as an ISO 8601 string.",
            },
            "parameters": {"file_name": ""},
        },
    )
    registry = Registry()
    registry.register(tool=tool)

    messages = []
    for turn in TURNS:
        messages.append({"role": "user", "content": turn})
        reply = loop(messages, call_model=call_model, registry=registry)
        print(f"you -> {turn}")
        print(f"02 tool-runtime -> {reply}")
