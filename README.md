# Local AI Agent Lab

A small local AI agent project built with Python and Ollama on Ubuntu Server.

## How it works

- Ollama runs a language model locally.
- Python sends the user’s request to the model.
- Python exposes a limited set of tools the model can request.
- The agent returns a response based on the tool results.

## Current agent

The agent can read basic server information:

- Operating system
- CPU core count
- Memory
- Free space on the root disk
- System load average

The status tool is read-only. The agent cannot run arbitrary shell commands.

## Requirements

- Ubuntu Server
- Python 3
- Ollama
- A model downloaded in Ollama
- Python virtual environment

## Run

```bash

source .venv/bin/activate
python agent.py
