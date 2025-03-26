# duckduckgo-ai-chat

[![PyPI](https://img.shields.io/pypi/v/duckduckgo-ai-chat.svg)](https://pypi.org/project/duckduckgo-ai-chat/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/duckduckgo-ai-chat?include_prereleases&label=changelog)](https://github.com/sukhbinder/duckduckgo-ai-chat/releases)
[![Tests](https://github.com/sukhbinder/duckduckgo-ai-chat/actions/workflows/test.yml/badge.svg)](https://github.com/sukhbinder/duckduckgo-ai-chat/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/duckduckgo-ai-chat/blob/master/LICENSE)

CLI to use DuckDuckGo AI Chat service from terminal

> Based on the ideas of [duckduckGO-chat-cli](https://github.com/benoitpetit/duckduckGO-chat-cli)

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

This produces.
```bash
usage: duckchat [-h] [-m {1,2,3,4,5}] [-y] [-q QUERY]

CLI to use DuckDuckGo AI Chat service from terminal

optional arguments:
  -h, --help            show this help message and exit
  -m {1,2,3,4,5}, --model {1,2,3,4,5}
                        Select a model by key:
                         1: gpt-4o-mini
                         2: claude-3-haiku-20240307
                         3: meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo
                         4: mistralai/Mistral-Small-24B-Instruct-2501
                         5: o3-mini
  -y, --yes             If provided, means user accept terms of service.
  -q QUERY, --query QUERY
                        First query to submit to the model

```

## Using ``duckchat`` with initial Query

Now we can pass initial context when invoking a model with `duckchat`

```bash
cat app.py | duckchat --yes --model 4 --query "Explain this code" 
```

or launch a model with an initial query

```bash
duckchat -y -m 4 -q "How to use pytest-vcr?" 
```

![query demo](https://raw.githubusercontent.com/sukhbinder/duckduckgo-aichat/main/query-demo.gif)

## Using ``Duckchat`` with ``uv``

Use duckchat without installing with ``uv``

```bash
uv run --with duckduckgo-ai-chat duckchat
```

## Saving conversations in ``duckchat``
Now user can save their conversaions using the ``/save`` command within the ``duckchat`` interface.

![Save demo](https://raw.githubusercontent.com/sukhbinder/duckduckgo-aichat/main/duckchat-save-option.png)

And the saved file looks like this

![Saved example](https://raw.githubusercontent.com/sukhbinder/duckduckgo-aichat/main/duckchat-saved-example.png)


## Available Models

| Model Name | Actual Model   | Performance    | Recommended Usage | Characteristics         |
|------------|----------------|----------------|---------------------|--------------------------|
| GPT-4o mini | gpt-4o-mini     | Fast           | Quick, simple tasks  | Default model, Versatile  |
| Claude 3 Haiku | claude-3-haiku-20240307 | Balanced      | Technical discussions | Good context handling, Structured responses|
| Llama 3.3 70B | meta-llama/Llama-3.3-70B-Instruct-Turbo | Code optimized | Programming tasks     | Documentation analysis, Code generation|
| Mistral Small 3 | mistralai/Mistral-Small-24B-Instruct-2501 | Knowledge focused | Complex topics        | Detailed explanations, In-depth analysis|
| o3-mini    | o3-mini          | Very fast      | Simple queries        | Lightweight, Quick responses|


## Installation

Install this tool using `pip`:

```bash
pip install duckduckgo-ai-chat
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

## Disclaimer
By using this client you accept [DuckDuckGo AI Chat ToS](https://duckduckgo.com/aichat/privacy-terms)
