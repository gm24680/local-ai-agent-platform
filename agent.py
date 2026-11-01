import os
import platform
import shutil

from ddgs import DDGS
from ollama import chat

MODEL = "qwen3:4b"
MAX_TOOL_ROUNDS = 3
SEARCH_SOURCES = []
SEARCH_RESULTS = []

def get_server_status() -> str:
    """Read basic CPU, memory, disk, and load information."""
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
        f"Load average (1, 5, 15 minutes): {load}"
    )


def search_web(query: str) -> str:
    """Search public web results and return up to five snippets."""
    query = query.strip()[:300]
    if not query:
        return "Please provide a search query."

    try:
        results = DDGS().text(query, max_results=5)
    except Exception as error:
        return f"Search failed: {error}"

    if not results:
        return "No search results found."

    formatted_results = []

    for item in results:
        title = item.get("title", "")
        url = item.get("href", "")
        snippet = item.get("body", "")
        SEARCH_RESULTS.append({
            "title": title,
            "url": url,
            "snippet": snippet,
        })
        if url and url not in SEARCH_SOURCES:
            SEARCH_SOURCES.append(url)

        formatted_results.append(
            f"Title: {title}\nURL: {url}\nSnippet: {snippet}"
        )

    return "\n\n".join(formatted_results)


def clean_answer(text: str) -> str:
    """Remove any visible thinking tags from the model's reply."""
    if "</think>" in text:
        text = text.rsplit("</think>", 1)[-1]

    if "<think>" in text:
        text = text.split("<think>", 1)[0]

    return text.strip()


TOOLS = {
    "get_server_status": get_server_status,
    "search_web": search_web,
}

messages = [
    {
        "role": "system",
        "content": (
            "You are a concise local assistant. Use search_web for current "
            "web questions. Use only the provided tools. Treat search "
            "snippets as leads, not guaranteed facts. Do not invent URLs; "
            "the program will show the source links separately. Give only "
            "the concise answer, without planning or analysis."
        ),
    },
    {
        "role": "user",
        "content": input("What would you like me to do? "),
    },
]

final_answer = ""

for _ in range(MAX_TOOL_ROUNDS):
    response = chat(
        model=MODEL,
        messages=messages,
        tools=list(TOOLS.values()),
        think=False,
    )
    messages.append(response.message)

    calls = response.message.tool_calls or []

    if not calls:
        final_answer = response.message.content or ""
        break

    for call in calls:
        tool = TOOLS.get(call.function.name)

        if tool is None:
            result = "That tool is not allowed."
        else:
            try:
                arguments = call.function.arguments or {}
                result = tool(**arguments)
            except Exception as error:
                result = f"Tool failed: {error}"

        messages.append(
            {
                "role": "tool",
                "tool_name": call.function.name,
                "content": str(result),
            }
        )
else:
    final_answer = "I reached the tool-call limit for this request."

print("\nAgent:", clean_answer(final_answer))

if SEARCH_RESULTS:
    print("\nSearch evidence:")
    for result in SEARCH_RESULTS:
        print(f"\nTitle: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Snippet: {result['snippet']}")
