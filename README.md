# duckduckgo-ai-chat

[![PyPI](https://img.shields.io/pypi/v/duckduckgo-ai-chat.svg)](https://pypi.org/project/duckduckgo-ai-chat/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/duckduckgo-ai-chat?include_prereleases&label=changelog)](https://github.com/sukhbinder/duckduckgo-ai-chat/releases)
[![Tests](https://github.com/sukhbinder/duckduckgo-ai-chat/actions/workflows/test.yml/badge.svg)](https://github.com/sukhbinder/duckduckgo-ai-chat/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/duckduckgo-ai-chat/blob/master/LICENSE)

CLI to use DuckDuckGo AI Chat service from terminal

> Based on the ideas of [duckduckGO-chat-cli](https://github.com/benoitpetit/duckduckGO-chat-cli)

## Disclaimer
By using this client you accept [DuckDuckGo AI Chat ToS](https://duckduckgo.com/aichat/privacy-terms)

## Available Models

| Model | Performance | Best For | Features |
|-------|------------|----------|-----------|
| **GPT-4o mini** | Fast | Quick answers & basic tasks | • General-purpose |
| **Claude 3 Haiku** | Balanced | Technical discussions | • Good context handling<br>• Structured responses |
| **Llama 3.3** | Code-optimized | Programming tasks | • Documentation analysis<br>• Code generation |
| **Mixtral 8x7B** | Knowledge-focused | Complex topics | • Detailed explanations<br>• Deep analysis |
| **o3-mini** | Fastest | Simple queries | • Lightweight<br>• Quick responses |


## Installation

Install this tool using `pip`:

```bash
pip install duckduckgo-ai-chat
```
## Usage

![Duckduck-aichat](https://raw.githubusercontent.com/sukhbinder/duckduckgo-aichat/main/demo-duckchat.gif)


For help, run:
```bash
duckchat --help
```
You can also use:
```bash
python -m duckchat --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd duckduckgo-ai-chat
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
