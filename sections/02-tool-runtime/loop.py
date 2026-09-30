from tools import Registry


def loop(messages, call_model, registry: Registry, max_steps=10):
    for _ in range(max_steps):
        response = call_model(messages, tools=registry.schemas())
        if response.content:
            messages.append({"role": "assistant", "content": response.content})

        if response.finish_reason != "tool_calls":
            return response.content

        if response.tool_calls:
            for tool_call in response.tool_calls:
                tool = registry.get(tool_call.name)
                if tool is None:
                    content = f"Error: no tool {tool_call.name}"
                else:
                    content = str(tool.run(tool_call.input))
                messages.append(
                    {"role": "tool", "tool_call_id": tool_call.id, "content": content}
                )

    raise RuntimeError("Error: fetch max steps")
