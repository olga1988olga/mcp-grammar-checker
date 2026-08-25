# mcp-grammar-checker

A small [MCP](https://modelcontextprotocol.io) server that exposes [LanguageTool](https://languagetool.org)'s grammar and style checking as a tool, so an MCP client (Claude Code, Claude Desktop, or any other MCP-compatible host) can check text for issues directly.

## Why

Built to give an AI coding assistant a real, tool-backed way to check grammar/style — rather than relying only on the model's own judgment — while learning MCP hands-on for a Solution Architect AI application.

## Tool

### `check_grammar(text: str, language: str = "de-DE") -> str`

Checks the given text using the public LanguageTool API and returns a formatted list of issues found (message, suggested replacements, surrounding context), or a confirmation that no issues were found.

## Setup

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone <this-repo>
cd mcp-grammar-checker
uv sync
```

## Running standalone

```bash
uv run python server.py
```

The server communicates over stdio and expects to be launched by an MCP client, not run interactively.

## Using with Claude Code / Claude Desktop

Add to your MCP config (e.g. `.claude/settings.json` or the Claude Desktop config file):

```json
{
  "mcpServers": {
    "grammar-checker": {
      "command": "uv",
      "args": ["run", "--directory", "/absolute/path/to/mcp-grammar-checker", "python", "server.py"]
    }
  }
}
```

Restart the client, and the `check_grammar` tool will be available.

## Notes

- Uses the public LanguageTool API (`api.languagetool.org`), which is rate-limited. For heavier use, LanguageTool can be [self-hosted](https://dev.languagetool.org/http-server.html).
- Supports any language LanguageTool supports (e.g. `en-US`, `de-DE`, `fr`) via the `language` parameter.
