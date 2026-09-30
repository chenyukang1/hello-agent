from loop import loop
from tools import Registry, Tool

from model.openrouter import call_model


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
            "type": "object",
            "properties": {
                "file_name": {
                    "type": "string",
                    "description": "Path of the file to read",
                }
            },
            "required": ["file_name"],
            "additionalProperties": False,
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


if __name__ == "__main__":
    demo()
