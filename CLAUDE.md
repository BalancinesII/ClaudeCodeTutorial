# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Create venv and install dependencies
uv venv && uv pip install -e .

# Start the MCP server
uv run main.py

# Run all tests
uv run pytest

# Run a single test
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_convert_docx
```

## Architecture

This project exposes document processing utilities as an MCP (Model Context Protocol) server using `FastMCP`.

- **`main.py`** — Creates the `FastMCP("docs")` server instance and registers tools with `mcp.tool()(fn)`. This is the only place tools are wired up.
- **`tools/`** — Each file defines one or more standalone functions that become MCP tools when registered in `main.py`.
- **`tests/`** — pytest tests. Binary fixture files (`.docx`, `.pdf`) live in `tests/fixtures/` for integration-style tests.

## Defining MCP Tools

Tools are plain Python functions registered in `main.py`:

```python
mcp.tool()(my_function)
```

Follow this pattern for all tool functions:

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does"),
) -> ReturnType:
    """One-line summary.

    Detailed explanation of functionality.
    When to use (and not use) the tool.

    Example:
        Input: ...
        Output: ...
    """
    # implementation
```

- Always annotate every parameter and the return type (e.g. `param: str`, `-> float`).
- Use `Field(description=...)` from pydantic for every parameter — these descriptions surface to AI assistants using the tool.
- Docstrings should explain *when* to use and *when not to use* the tool, plus a concrete usage example.
- After defining a tool function, register it in `main.py` with `mcp.tool()(fn)`.
