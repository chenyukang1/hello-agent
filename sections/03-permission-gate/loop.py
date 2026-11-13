from collections.abc import Callable

import permissions
from tools import Registry

from schema.message import ModelReply


def loop(
    messages,
    call_model: Callable[..., ModelReply],
    registry: Registry,
    mode=permissions.DEFAULT,
    allow_rules=None,
    approver=None,
    max_steps=10,
):
    allow_rules = allow_rules or set()
    approver = approver or (lambda name, args: False)

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
                res = lambda content, tool_call=tool_call: {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": content,
                }
                tool = registry.get(tool_call.name)
                if tool is None:
                    content = f"Error: no tool {tool_call.name}"
                else:
                    decision = permissions.decide(tool, mode, allow_rules)
                    if decision == "deny":
                        content = f"{tool_call.name} not allowed in {mode} mode"
                    elif decision == "ask" and not approver(
                        tool_call.name, tool_call.input
                    ):
                        content = f"{tool_call.name} denied by user"
                    else:
                        content = str(tool.run(tool_call.input))
                messages.append(res(content, tool_call))
        else:
            messages.append(assistant_message)

    raise RuntimeError("Error: fetch max steps")
