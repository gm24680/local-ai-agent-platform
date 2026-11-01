# Local AI Agent Automation Platform

A self-hosted AI agent built with Python, Ollama, and Qwen3 4B on Ubuntu Server.

The project demonstrates local LLM inference, Python tool calling, Linux system monitoring, and web search integration.

## Features

### Local AI Inference
- Uses Ollama to run Qwen3 4B locally.
- Processes natural language requests.
- Does not require a cloud LLM API for inference.

### Linux System Monitoring
The agent can retrieve:
- Operating system and kernel version
- CPU core count
- Total and available memory
- Root filesystem free space
- System load averages

### Web Search
- Uses the DDGS Python library.
- Retrieves up to five search results.
- Displays source URLs and snippets separately from the model response.

### Agent Tool Execution
- Uses Ollama's Python tool-calling interface.
- Restricts execution to explicitly registered functions.
- Limits tool-calling iterations.
- Handles tool execution errors.

## Technologies

- Python 3
- Ubuntu Server
- Ollama
- Qwen3 4B
- DDGS
- Git

## Architecture

User Request
    |
    v
Python AI Agent
    |
    v
Ollama API / Qwen3 4B
    |
    v
Tool Selection
    |
    +-- get_server_status()
    |
    +-- search_web()
    |
    v
Tool Results
    |
    v
AI Response + Search Evidence

## Installation

1. Install Python 3.10 or newer and create a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install Python dependencies.

```bash
pip install -r requirements.txt
```

3. Install Ollama from https://ollama.com and download the model.

```bash
ollama pull qwen3:4b
```

4. Ensure the Ollama service is running.

5. Start the agent.

```bash
python agent.py
```

## Example Requests

Check the server's CPU, memory, and disk status.

Search the web for current developments in Linux security.

## Security

- System monitoring functions are read-only.
- The agent uses an explicit tool allowlist.
- Arbitrary shell command execution is not exposed.
- Private datasets, credentials, and local environments are excluded from version control.

Web results are untrusted external information and should not be treated as verified facts.

## Future Improvements

- Remote Linux server monitoring via SSH
- Security log analysis
- Scheduled infrastructure reports
- Web dashboard
- Docker deployment
- Automated testing

## Project Status

Active development. Local inference, system monitoring, and web search tools are implemented.
