# duckduckgo-ai-chat

[![PyPI](https://img.shields.io/pypi/v/duckduckgo-ai-chat.svg)](https://pypi.org/project/duckduckgo-ai-chat/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/duckduckgo-ai-chat?include_prereleases&label=changelog)](https://github.com/sukhbinder/duckduckgo-ai-chat/releases)
[![Tests](https://github.com/sukhbinder/duckduckgo-ai-chat/actions/workflows/test.yml/badge.svg)](https://github.com/sukhbinder/duckduckgo-ai-chat/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/duckduckgo-ai-chat/blob/master/LICENSE)

CLI to use DuckDuckGo AI Chat service from terminal

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
