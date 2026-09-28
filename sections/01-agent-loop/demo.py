from dotenv import load_dotenv
from loop import loop

from schema.openrouter import call_model

load_dotenv()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Return the current UTC time as an ISO 8601 string.",
        },
    },
]


TURNS = [
    "What time is it right now? Answer in one sentence.",
    "Was that before or after noon, UTC?",  # only answerable if turn 1 is still in context
]


def demo():
    messages = []
    for turn in TURNS:
        messages.append({"role": "user", "content": turn})
        reply = loop(messages=messages, tools=tools, call_model=call_model)
        print("you ->", turn)
        print("01 agent_loop ->", reply)


if __name__ == "__main__":
    demo()
