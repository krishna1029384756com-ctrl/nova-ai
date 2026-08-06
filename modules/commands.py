from modules import pc

# Words to strip so "open notepad please" -> "notepad"
OPEN_TRIGGERS = ["open ", "launch ", "start "]
SEARCH_TRIGGERS = ["search for ", "google ", "search "]
WEBSITE_TRIGGERS = ["go to ", "visit "]


def handle_command(message):
    """
    Checks if the message is a PC/action command (open app, search web, etc).
    Returns a reply string if handled, or None if this isn't a command
    (so brain.py can fall back to normal conversation).
    """
    message = message.lower().strip()

    for trigger in OPEN_TRIGGERS:
        if message.startswith(trigger):
            target = message[len(trigger):].strip()
            if not target:
                return None
            if pc.open_app(target):
                return f"Opening {target}..."
            pc.open_website(target)
            return f"I don't recognize \"{target}\" as an app, so I opened it as a website instead."

    for trigger in SEARCH_TRIGGERS:
        if message.startswith(trigger):
            query = message[len(trigger):].strip()
            if not query:
                return None
            pc.search_web(query)
            return f"Searching the web for \"{query}\"..."

    for trigger in WEBSITE_TRIGGERS:
        if message.startswith(trigger):
            site = message[len(trigger):].strip()
            if not site:
                return None
            pc.open_website(site)
            return f"Opening {site}..."

    return None
