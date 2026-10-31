import os
import platform
import shutil

from ollama import chat

MODEL = "qwen3:4b"


def get_server_status() -> str:
    """Read basic CPU, memory, and disk information."""
    memory = {}

    with open("/proc/meminfo", encoding="utf-8") as file:
        for line in file:
            key, value = line.split(":", 1)
            if key in ("MemTotal", "MemAvailable"):
                memory[key] = int(value.strip().split()[0]) // 1024

    disk = shutil.disk_usage("/")
    load = os.getloadavg()

    return (
        f"Operating system: {platform.system()} {platform.release()}\n"
        f"CPU cores: {os.cpu_count()}\n"
        f"Memory total: {memory['MemTotal']} MiB\n"
        f"Memory available: {memory['MemAvailable']} MiB\n"
        f"Root disk free: {disk.free // (1024 ** 3)} GiB\n"
        f"Load average: {load}"
    )


# Only functions listed here are available to the agent.
TOOLS = {
    "get_server_status": get_server_status,
}

messages = [
    {
        "role": "system",
        "content": (
            "Answer with only a concise final response. For server status, "
            "summarize the metrics in bullets. Do not include your planning "
            "or analysis. Use only the tools provided, and never claim a "
            "tool action succeeded unless it did."
        ),
    },
    {
        "role": "user",
        "content": input("What would you like me to do? "),
    },
]

for _ in range(3):
    response = chat(
        model=MODEL,
        messages=messages,
        tools=list(TOOLS.values()),
        think=False,
    )
    messages.append(response.message)

    calls = response.message.tool_calls or []
    if not calls:
        print("\nAgent:", response.message.content)
        break

    for call in calls:
        tool = TOOLS.get(call.function.name)
        if tool is None:
            result = "That tool is not allowed."
        else:
            result = tool(**(call.function.arguments or {}))

        messages.append({
            "role": "tool",
            "tool_name": call.function.name,
            "content": str(result),
        })
else:
    print("\nAgent: I reached the tool-call limit for this request.")
