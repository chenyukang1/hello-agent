import os

from openrouter import OpenRouter

from schema.message import ModelReply, ToolCall

client = OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY"))
model = os.getenv("OPENROUTER_API_MODEL", "xiaomi/mimo-v2.6-flash")


# openrouter call
def call_model(messages, tools) -> ModelReply:
    # tool protocol conversion
    api_tools = [
        {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["input_schema"],
            },
        }
        for tool in tools
    ]

    print(f"[openrouter] send messages: {messages}, tools: {api_tools}")

    response = client.chat.send(
        max_tokens=1024,
        messages=messages,
        model="xiaomi/mimo-v2.6-flash",
        tools=api_tools,
        tool_choice="auto",
    )

    print(f"[openrouter] response: {response}")

    tool_calls = []
    if response.choices[0].message.tool_calls:
        tool_calls = [
            ToolCall(
                id=call.id,
                type=call.type,
                name=call.function.name,
                input=call.function.arguments,
            )
            for call in response.choices[0].message.tool_calls
        ]

    return ModelReply(
        finish_reason=response.choices[0].finish_reason,
        content=response.choices[0].message.content,
        tool_calls=tool_calls,
    )
