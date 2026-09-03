from typing import Optional

from modules.tools import execute_tool


# ============================================================
# COMMAND TRIGGERS
# ============================================================

OPEN_TRIGGERS = (
    "open ",
    "launch ",
    "start ",
)

SEARCH_TRIGGERS = (
    "search for ",
    "google ",
    "search ",
)

WEBSITE_TRIGGERS = (
    "go to ",
    "visit ",
)


# ============================================================
# COMMAND HANDLER
# ============================================================

def handle_command(message: str) -> Optional[str]:
    """
    Detect a simple NOVA action command and execute it
    through the central tool registry.

    Returns:
        str  -> command was handled
        None -> normal conversation / no command
    """

    # Invalid input
    if not isinstance(message, str):
        return None

    text = message.strip().lower()

    if not text:
        return None

    # ========================================================
    # OPEN APP
    # ========================================================

    for trigger in OPEN_TRIGGERS:

        if text.startswith(trigger):

            target = text[len(trigger):].strip()

            if not target:
                return None

            result = execute_tool(
                "open_app",
                app_name=target,
            )

            if result.success:
                return f"Opening {target}..."

            # If the app wasn't found, try it as a website.
            website_result = execute_tool(
                "open_website",
                url=target,
            )

            if website_result.success:
                return (
                    f'I don\'t recognize "{target}" as an app, '
                    "so I opened it as a website instead."
                )

            return f'Could not open "{target}".'

    # ========================================================
    # SEARCH WEB
    # ========================================================

    for trigger in SEARCH_TRIGGERS:

        if text.startswith(trigger):

            query = text[len(trigger):].strip()

            if not query:
                return None

            result = execute_tool(
                "search_web",
                query=query,
            )

            if result.success:
                return f'Searching the web for "{query}"...'

            return f'Could not search for "{query}".'

    # ========================================================
    # OPEN WEBSITE
    # ========================================================

    for trigger in WEBSITE_TRIGGERS:

        if text.startswith(trigger):

            site = text[len(trigger):].strip()

            if not site:
                return None

            result = execute_tool(
                "open_website",
                url=site,
            )

            if result.success:
                return f"Opening {site}..."

            return f"Could not open {site}."

    # ========================================================
    # NOT A COMMAND
    # ========================================================

    return None