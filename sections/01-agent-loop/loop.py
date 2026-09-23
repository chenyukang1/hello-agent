from datetime import UTC, datetime


def get_time(_input):
    return datetime.now(UTC).isoformat(timespec="seconds")


HANDLERS = {"get_time": get_time}


def run_tool(tool_name, input):
    fn = HANDLERS.get(tool_name)
    if fn is None:
        return f"Error: no tool {tool_name}"
    try:
        return fn(input)
    except Exception as e:
        return f"Error: {e}"


def loop(messages, model, max_steps=10):
    for _ in range(max_steps):
        response = model(messages)
        messages.append({"role": "assistant", "content": response.content})

        if response.finish_reason != "tool_calls":
            return final_text(response)

        if response.tool_calls:
            for tool_call in response.tool_calls:
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": run_tool(tool_call.name, tool_call.input),
                    }
                )

    return RuntimeError("fetch max steps")


def final_text(response):
    return "".join(response.content)
