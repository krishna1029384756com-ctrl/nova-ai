import json
import re
from datetime import datetime

from modules import commands
from modules import memory
from modules import ai
from modules.tools import execute_tool, list_tools

import config


class Brain:

    def __init__(self):
        self.name = "NOVA"
        self.version = "0.5"

    # ============================================================
    # MAIN CHAT
    # ============================================================

    def chat(self, message):
        original = message

        if not isinstance(message, str):
            return "I couldn't understand that request."

        message = message.strip()

        if not message:
            return "Please type or say something."

        # --------------------------------------------------------
        # 1. Fast deterministic commands
        # --------------------------------------------------------
        command_reply = commands.handle_command(message.lower())

        if command_reply:
            memory.add_exchange(original, command_reply)
            return command_reply

        # --------------------------------------------------------
        # 2. AI + tool system
        # --------------------------------------------------------
        reply = self._think(original)

        memory.add_exchange(original, reply)

        return reply

    # ============================================================
    # THINK
    # ============================================================

    def _think(self, message):
        try:
            history = memory.get_history(
                limit=config.AI_HISTORY_LENGTH
            )

            # Ask the AI whether it should use a tool.
            decision = self._ask_ai_for_action(
                message,
                history,
            )

            # ----------------------------------------------------
            # AI requested a tool
            # ----------------------------------------------------
            if decision["type"] == "tool":

                tool_name = decision.get("tool")
                arguments = decision.get("arguments", {})

                if not isinstance(arguments, dict):
                    arguments = {}

                result = execute_tool(
                    tool_name,
                    **arguments,
                )

                # ------------------------------------------------
                # Tool succeeded
                # ------------------------------------------------
                if result.success:
                    return self._format_tool_success(
                        tool_name,
                        arguments,
                        result.output,
                    )

                # ------------------------------------------------
                # Tool failed
                # ------------------------------------------------
                return (
                    f"I couldn't complete that action. "
                    f"{result.error or 'The tool failed.'}"
                )

            # ----------------------------------------------------
            # Normal AI response
            # ----------------------------------------------------
            return decision["response"]

        except Exception as exc:
            print(
                f"[AI] Tool-enabled thinking failed: {exc}"
            )

            return self._converse(
                message.lower().strip()
            )

    # ============================================================
    # AI ACTION DECISION
    # ============================================================

    def _ask_ai_for_action(self, message, history):
        """
        Ask the configured AI to return either:

        Normal response:
        {
            "type": "response",
            "response": "..."
        }

        Tool call:
        {
            "type": "tool",
            "tool": "open_app",
            "arguments": {
                "app_name": "notepad"
            }
        }
        """

        tool_text = self._build_tool_description()

        system_prompt = f"""
You are NOVA, a personal AI assistant.

You have access to these tools:

{tool_text}

You MUST return ONLY valid JSON.

There are two possible response types.

NORMAL RESPONSE:
{{
  "type": "response",
  "response": "your normal answer"
}}

TOOL CALL:
{{
  "type": "tool",
  "tool": "tool_name",
  "arguments": {{}}
}}

Rules:

1. Use a tool when the user asks you to perform an action.
2. Do not invent tools.
3. Only use tools from the provided tool list.
4. Put tool parameters inside "arguments".
5. For normal conversation, use type "response".
6. Do not use Markdown.
7. Do not add explanations outside the JSON.
8. Never output fake tool results.
9. If you are unsure which tool to use, return a normal response.

Available tools:
{tool_text}
""".strip()

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        # Add conversation history
        for exchange in history:
            messages.append(
                {
                    "role": "user",
                    "content": exchange["message"],
                }
            )

            messages.append(
                {
                    "role": "assistant",
                    "content": exchange["reply"],
                }
            )

        messages.append(
            {
                "role": "user",
                "content": message,
            }
        )

        raw_response = ai.generate_raw_messages(messages)

        return self._parse_ai_action(raw_response)

    # ============================================================
    # TOOL DESCRIPTION
    # ============================================================

    def _build_tool_description(self):
        tools = list_tools()

        if not tools:
            return "No tools are currently available."

        lines = []

        for tool in tools:
            lines.append(
                f'- {tool["name"]}: {tool["description"]}'
            )

        return "\n".join(lines)

    # ============================================================
    # PARSE AI JSON
    # ============================================================

    def _parse_ai_action(self, text):
        if not isinstance(text, str):
            return {
                "type": "response",
                "response": str(text),
            }

        text = text.strip()

        # Remove optional Markdown code fences.
        text = re.sub(
            r"^```(?:json)?\s*",
            "",
            text,
            flags=re.IGNORECASE,
        )

        text = re.sub(
            r"\s*```$",
            "",
            text,
            flags=re.IGNORECASE,
        )

        try:
            data = json.loads(text)

        except json.JSONDecodeError:
            # Model ignored the JSON rule.
            # Treat its output as a normal response.
            return {
                "type": "response",
                "response": text,
            }

        if not isinstance(data, dict):
            return {
                "type": "response",
                "response": text,
            }

        response_type = data.get("type")

        # --------------------------------------------------------
        # Normal response
        # --------------------------------------------------------

        if response_type == "response":

            response = data.get(
                "response",
                "",
            )

            if not isinstance(response, str):
                response = str(response)

            return {
                "type": "response",
                "response": response.strip(),
            }

        # --------------------------------------------------------
        # Tool call
        # --------------------------------------------------------

        if response_type == "tool":

            tool_name = data.get("tool")
            arguments = data.get("arguments", {})

            if not isinstance(tool_name, str):
                return {
                    "type": "response",
                    "response": (
                        "I couldn't determine which action to perform."
                    ),
                }

            if not isinstance(arguments, dict):
                arguments = {}

            # Security:
            # Only allow tools registered in tools.py.
            if not any(
                tool["name"] == tool_name
                for tool in list_tools()
            ):
                return {
                    "type": "response",
                    "response": (
                        f"I don't have access to the tool "
                        f"'{tool_name}'."
                    ),
                }

            return {
                "type": "tool",
                "tool": tool_name,
                "arguments": arguments,
            }

        # Unknown format
        return {
            "type": "response",
            "response": text,
        }

    # ============================================================
    # TOOL SUCCESS MESSAGE
    # ============================================================

    def _format_tool_success(
        self,
        tool_name,
        arguments,
        output,
    ):
        if tool_name == "open_app":
            app_name = arguments.get(
                "app_name",
                "application",
            )
            return f"Opening {app_name}..."

        if tool_name == "search_web":
            query = arguments.get(
                "query",
                "",
            )
            return f'Searching the web for "{query}"...'

        if tool_name == "open_website":
            url = arguments.get(
                "url",
                "",
            )
            return f"Opening {url}..."

        return output or "Done."

    # ============================================================
    # BASIC FALLBACK
    # ============================================================

    def _converse(self, message):

        if "who are you" in message or "your name" in message:
            return (
                "I'm NOVA. I'm currently running in "
                "basic mode."
            )

        if any(
            word in message
            for word in [
                "hello",
                "hey nova",
                "hi nova",
            ]
        ):
            return "Hello Krishna! How can I help you?"

        if message in (
            "hi",
            "yo",
            "sup",
            "hey",
        ):
            return "Hi! What do you need?"

        if "how are you" in message:
            return "Running smoothly!"

        if "thank" in message:
            return "You're welcome!"

        if "joke" in message:
            return (
                "Why do programmers prefer dark mode? "
                "Because light attracts bugs."
            )

        if (
            "what time" in message
            or message == "time"
        ):
            return datetime.now().strftime(
                "It's %I:%M %p."
            )

        if "date" in message:
            return datetime.now().strftime(
                "Today is %A, %B %d, %Y."
            )

        if any(
            word in message
            for word in [
                "bye",
                "exit",
                "quit",
            ]
        ):
            return "Goodbye, Krishna!"

        return (
            f'I heard: "{message}" '
            "but I don't have a specific response."
        )


brain = Brain()