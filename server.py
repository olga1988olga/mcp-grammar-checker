"""MCP server exposing LanguageTool grammar/style checking as a tool.

Wraps the public LanguageTool API (https://languagetool.org/) so an MCP
client (e.g. Claude Code, Claude Desktop) can request a grammar/style
check for a piece of text in a given language.

Built with FastMCP 3.x (the `fastmcp` package by jlowin), per the
recommendation from Anthropic's official mcp-server-dev:build-mcp-server
skill — not the frozen FastMCP 1.0 bundled inside the official `mcp` SDK,
which the first version of this server used directly.
"""

import requests
from fastmcp import FastMCP

LANGUAGETOOL_API_URL = "https://api.languagetool.org/v2/check"

mcp = FastMCP("grammar-checker")


@mcp.tool
def check_grammar(text: str, language: str = "de-DE") -> str:
    """Check text for grammar, spelling, and style issues using LanguageTool.

    Args:
        text: The text to check.
        language: Language code, e.g. "de-DE", "en-US". Defaults to "de-DE".

    Returns:
        A formatted list of found issues (message, suggested replacements,
        and the surrounding context), or a confirmation that no issues
        were found.
    """
    response = requests.post(
        LANGUAGETOOL_API_URL,
        data={"text": text, "language": language},
        timeout=15,
    )
    response.raise_for_status()
    matches = response.json().get("matches", [])

    if not matches:
        return "No issues found."

    lines = []
    for match in matches:
        context = match["context"]["text"]
        message = match["message"]
        replacements = [r["value"] for r in match.get("replacements", [])[:3]]
        suggestion = f" Suggested: {', '.join(replacements)}" if replacements else ""
        lines.append(f"- {message}{suggestion}\n  Context: …{context}…")

    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
