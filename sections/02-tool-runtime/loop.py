from collections.abc import Callable

from tools import Registry

from schema.message import ModelReply


def loop(
    messages, call_model: Callable[..., ModelReply], registry: Registry, max_steps=10
):
    for _ in range(max_steps):
        response = call_model(messages, tools=registry.schemas())

        if response.finish_reason != "tool_calls":
            return response.content

        assistant_message = {"role": "assistant", "content": response.content}
        if response.tool_calls:
            assistant_message["tool_calls"] = []
            for tool_call in response.tool_calls:
                assistant_message["tool_calls"].append(
                    {
                        "id": tool_call.id,
                        "type": tool_call.type,
                        "function": {
                            "name": tool_call.name,
                            "arguments": tool_call.input,
                        },
                    }
                )
            messages.append(assistant_message)

            for tool_call in response.tool_calls:
                tool = registry.get(tool_call.name)
                if tool is None:
                    content = f"Error: no tool {tool_call.name}"
                else:
                    content = str(tool.run(tool_call.input))
                messages.append(
                    {"role": "tool", "tool_call_id": tool_call.id, "content": content}
                )
        else:
            messages.append(assistant_message)

    raise RuntimeError("Error: fetch max steps")
