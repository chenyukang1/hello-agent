import os

from dotenv import load_dotenv
from loop import loop
from openrouter import OpenRouter, dataclass

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

client = OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY"))

TURNS = [
    "What time is it right now? Answer in one sentence.",
    "Was that before or after noon, UTC?",  # only answerable if turn 1 is still in context
]


@dataclass
class ToolCall:
    id: str
    name: str
    input: str


@dataclass
class ModelReply:
    finish_reason: str | None
    content: str | None
    tool_calls: list[ToolCall]


def demo():
    def model(messages):
        response = client.chat.send(
            max_tokens=1024,
            messages=messages,
            model="xiaomi/mimo-v2.6-flash",
            tools=tools,
            tool_choice="auto",
        )

        tool_calls = []
        if response.choices[0].message.tool_calls:
            tool_calls = [
                ToolCall(
                    id=call.id, name=call.function.name, input=call.function.arguments
                )
                for call in response.choices[0].message.tool_calls
            ]

        return ModelReply(
            finish_reason=response.choices[0].finish_reason,
            content=response.choices[0].message.content,
            tool_calls=tool_calls,
        )

    messages = []
    for turn in TURNS:
        messages.append({"role": "user", "content": turn})
        reply = loop(messages=messages, model=model)
        print("you ->", turn)
        print("01 agent_loop ->", reply)


if __name__ == "__main__":
    demo()
