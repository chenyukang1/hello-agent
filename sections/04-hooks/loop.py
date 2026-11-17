from collections.abc import Callable

import permissions
from hooks import Hooks
from tools import Registry, Tool

from schema.message import ModelReply, ToolCall


def loop(
    messages: list,
    call_model: Callable[..., ModelReply],
    registry: Registry,
    allow_rules: set | None = None,
    approver: Callable[..., bool] | None = None,
    hooks: Hooks = None,
    mode=permissions.DEFAULT,
    max_steps=10,
):
    hooks = hooks or Hooks()
    allow_rules = allow_rules or set()
    approver = approver or (lambda name, args: False)

    for _ in range(max_steps):
        response = call_model(messages, tools=registry.schemas())

        if response.finish_reason != "tool_calls":
            return response.content

        messages.append(to_assistant_message(response))

        if not response.tool_calls:
            continue

        for tool_call in response.tool_calls:
            tool = registry.get(tool_call.name)
            content = execute_tool_call(tool, tool_call, mode, allow_rules, approver, hooks)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": content,
                }
            )

    raise RuntimeError("Error: fetch max steps")


def to_assistant_message(response):
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
    return assistant_message


def execute_tool_call(tool: Tool | None, tool_call: ToolCall, mode, allow_rules, approver, hooks: Hooks):
    name, args = tool_call.name, tool_call.input
    if tool is None:
        return f"Error: no tool {name}"

    blocked, args, message = hooks.fire_pre(name, args)
    if blocked:
        return message

    decision = permissions.decide(tool, mode, allow_rules)
    if decision == "deny":
        return f"{name} not allowed in {mode} mode"

    if decision == "ask" and not approver(name, args):
        return f"{name} denied by user"

    res = str(tool.run(args))
    hooks.fire_post(name, args, res)
    return res
