<<<<<<< Updated upstream
"""NOVA tool registry and executor.

This module is the single place where NOVA exposes actions that can be
executed on the PC.  Higher-level code can discover available tools and
execute them without importing individual implementation modules.
=======
"""
NOVA Tool Registry

Central system for registering and executing NOVA tools.

Flow:

    Brain
      ↓
    Commands
      ↓
    Tool Registry
      ↓
    PC / other systems
>>>>>>> Stashed changes
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional

from modules import pc


<<<<<<< Updated upstream
@dataclass
class ToolResult:
    """Standard result returned by every NOVA tool."""

    success: bool
    output: str
=======
# ============================================================
# TOOL RESULT
# ============================================================

@dataclass
class ToolResult:
    """
    Standard result returned by every NOVA tool.
    """

    success: bool
    output: str = ""
>>>>>>> Stashed changes
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "output": self.output,
            "error": self.error,
        }


<<<<<<< Updated upstream
@dataclass(frozen=True)
class Tool:
    """Definition of an executable NOVA tool."""
=======
# ============================================================
# TOOL DEFINITION
# ============================================================

@dataclass(frozen=True)
class Tool:
    """
    Description of a registered NOVA tool.
    """
>>>>>>> Stashed changes

    name: str
    description: str
    handler: Callable[..., Any]


<<<<<<< Updated upstream
_TOOLS: Dict[str, Tool] = {}


def register_tool(name: str, description: str, handler: Callable[..., Any]) -> None:
    """Register or replace a tool in the global registry."""
    normalized = name.strip().lower()
    if not normalized:
        raise ValueError("Tool name cannot be empty")
    _TOOLS[normalized] = Tool(normalized, description.strip(), handler)


def get_tool(name: str) -> Optional[Tool]:
    """Return a registered tool by name, or None if it does not exist."""
=======
# ============================================================
# TOOL REGISTRY
# ============================================================

_TOOLS: Dict[str, Tool] = {}


def register_tool(
    name: str,
    description: str,
    handler: Callable[..., Any],
) -> None:
    """
    Register a tool.
    """

    name = name.strip().lower()

    if not name:
        raise ValueError("Tool name cannot be empty.")

    if not callable(handler):
        raise TypeError(f"Handler for '{name}' is not callable.")

    _TOOLS[name] = Tool(
        name=name,
        description=description.strip(),
        handler=handler,
    )


def get_tool(name: str) -> Optional[Tool]:
    """
    Get a registered tool.
    """

    if not isinstance(name, str):
        return None

>>>>>>> Stashed changes
    return _TOOLS.get(name.strip().lower())


def list_tools() -> list[dict[str, str]]:
<<<<<<< Updated upstream
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
=======
    """
    Return all registered tools.
    """

    return [
        {
            "name": tool.name,
            "description": tool.description,
        }
        for tool in sorted(
            _TOOLS.values(),
            key=lambda tool: tool.name,
        )
    ]


# ============================================================
# TOOL EXECUTOR
# ============================================================

def execute_tool(
    name: str,
    **arguments: Any,
) -> ToolResult:
    """
    Execute a registered tool safely.
    """

    tool = get_tool(name)

    if tool is None:
        return ToolResult(
            success=False,
            error=f"Unknown tool: {name}",
        )

    try:
        result = tool.handler(**arguments)

    except TypeError as exc:
        return ToolResult(
            success=False,
            error=f"Invalid arguments for '{tool.name}': {exc}",
        )

    except Exception as exc:
        return ToolResult(
            success=False,
            error=f"Tool '{tool.name}' failed: {exc}",
        )

    # Tool already returned a ToolResult
    if isinstance(result, ToolResult):
        return result

    # Boolean result
    if isinstance(result, bool):
        return ToolResult(
            success=result,
            output="Success" if result else "Action failed",
        )

    # Any other result
    return ToolResult(
        success=True,
        output=str(result),
    )


# ============================================================
# BUILT-IN TOOL IMPLEMENTATIONS
# ============================================================

def _open_app(app_name: str) -> ToolResult:
    """
    Open a desktop application.
    """

    if not isinstance(app_name, str):
        return ToolResult(
            success=False,
            error="app_name must be a string.",
        )

    app_name = app_name.strip()

    if not app_name:
        return ToolResult(
            success=False,
            error="app_name is required.",
        )

    try:
        success = pc.open_app(app_name)

    except Exception as exc:
        return ToolResult(
            success=False,
            error=f"Could not open app '{app_name}': {exc}",
        )

    if success:
        return ToolResult(
            success=True,
            output=f"Opened {app_name}.",
        )

    return ToolResult(
        success=False,
        error=f"Application not found: {app_name}",
    )


def _search_web(query: str) -> ToolResult:
    """
    Search the web using NOVA's PC module.
    """

    if not isinstance(query, str):
        return ToolResult(
            success=False,
            error="query must be a string.",
        )

    query = query.strip()

    if not query:
        return ToolResult(
            success=False,
            error="query is required.",
        )

    try:
        pc.search_web(query)

        return ToolResult(
            success=True,
            output=f'Searching the web for "{query}".',
        )

    except Exception as exc:
        return ToolResult(
            success=False,
            error=f"Web search failed: {exc}",
        )


def _open_website(url: str) -> ToolResult:
    """
    Open a website.
    """

    if not isinstance(url, str):
        return ToolResult(
            success=False,
            error="url must be a string.",
        )

    url = url.strip()

    if not url:
        return ToolResult(
            success=False,
            error="url is required.",
        )

    try:
        pc.open_website(url)

        return ToolResult(
            success=True,
            output=f"Opened {url}.",
        )

    except Exception as exc:
        return ToolResult(
            success=False,
            error=f"Could not open website '{url}': {exc}",
        )


# ============================================================
# REGISTER BUILT-IN TOOLS
# ============================================================

register_tool(
    name="open_app",
    description="Open a desktop application by name.",
    handler=_open_app,
)

register_tool(
    name="search_web",
    description="Search the web using a search query.",
    handler=_search_web,
)

register_tool(
    name="open_website",
    description="Open a website in the default browser.",
    handler=_open_website,
)
>>>>>>> Stashed changes
