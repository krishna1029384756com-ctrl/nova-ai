"""NOVA tool registry and executor.

This module is the single place where NOVA exposes actions that can be
executed on the PC.  Higher-level code can discover available tools and
execute them without importing individual implementation modules.
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional

from modules import pc


@dataclass
class ToolResult:
    """Standard result returned by every NOVA tool."""

    success: bool
    output: str
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "output": self.output,
            "error": self.error,
        }


@dataclass(frozen=True)
class Tool:
    """Definition of an executable NOVA tool."""

    name: str
    description: str
    handler: Callable[..., Any]


_TOOLS: Dict[str, Tool] = {}


def register_tool(name: str, description: str, handler: Callable[..., Any]) -> None:
    """Register or replace a tool in the global registry."""
    normalized = name.strip().lower()
    if not normalized:
        raise ValueError("Tool name cannot be empty")
    _TOOLS[normalized] = Tool(normalized, description.strip(), handler)


def get_tool(name: str) -> Optional[Tool]:
    """Return a registered tool by name, or None if it does not exist."""
    return _TOOLS.get(name.strip().lower())


def list_tools() -> list[dict[str, str]]:
    """Return tool metadata in a model-friendly format."""
    return [
        {"name": tool.name, "description": tool.description}
        for tool in sorted(_TOOLS.values(), key=lambda item: item.name)
    ]


def execute_tool(name: str, **arguments: Any) -> ToolResult:
    """Execute a registered tool and normalize its result/errors."""
    tool = get_tool(name)
    if tool is None:
        return ToolResult(False, "", f"Unknown tool: {name}")

    try:
        result = tool.handler(**arguments)
    except TypeError as exc:
        return ToolResult(False, "", f"Invalid arguments for {tool.name}: {exc}")
    except Exception as exc:
        return ToolResult(False, "", f"Tool {tool.name} failed: {exc}")

    if isinstance(result, ToolResult):
        return result

    if isinstance(result, bool):
        return ToolResult(result, "Success" if result else "Action failed")

    return ToolResult(True, str(result))


# ---------------------------------------------------------------------------
# Built-in PC tools
# ---------------------------------------------------------------------------


def _open_app(app_name: str) -> ToolResult:
    if not app_name or not app_name.strip():
        return ToolResult(False, "", "app_name is required")

    if pc.open_app(app_name):
        return ToolResult(True, f"Opened {app_name.strip()}.")

    return ToolResult(False, "", f"Could not open app: {app_name.strip()}")


def _search_web(query: str) -> ToolResult:
    if not query or not query.strip():
        return ToolResult(False, "", "query is required")

    pc.search_web(query.strip())
    return ToolResult(True, f"Searching the web for \"{query.strip()}\".")


def _open_website(url: str) -> ToolResult:
    if not url or not url.strip():
        return ToolResult(False, "", "url is required")

    pc.open_website(url.strip())
    return ToolResult(True, f"Opening {url.strip()}.")


register_tool("open_app", "Open a supported desktop application by name.", _open_app)
register_tool("search_web", "Open a Google search for a query.", _search_web)
register_tool("open_website", "Open a website URL in the default browser.", _open_website)
