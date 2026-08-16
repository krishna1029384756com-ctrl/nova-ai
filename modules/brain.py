from datetime import datetime

from modules import commands
from modules import memory
from modules import ai

import config


class Brain:

    def __init__(self):
        self.name = "NOVA"
        self.version = "0.4"

    def chat(self, message):
        original = message
        message = message.lower().strip()

        if message == "":
            return "Please type or say something."

        # 1. Is this an action command (open app, search, etc)? These stay
        #    rule-based on purpose - deterministic and instant, no need to
        #    ask an AI model whether "open notepad" means open notepad.
        command_reply = commands.handle_command(message)
        if command_reply:
            memory.add_exchange(original, command_reply)
            return command_reply

        # 2. Otherwise, this is a real conversation - try the local AI model.
        reply = self._think(original)
        memory.add_exchange(original, reply)
        return reply

    def _think(self, message):
        try:
            history = memory.get_history(limit=config.AI_HISTORY_LENGTH)
            return ai.generate_reply(message, history)
        except Exception as e:
            # Configured AI provider not ready (model not downloaded, package
            # not installed, service not running, missing API key, etc.) -
            # fall back to basic replies rather than leaving NOVA silent.
            print(f"[AI] '{config.AI_PROVIDER}' provider unavailable, using basic replies instead ({e})")
            return self._converse(message.lower().strip())

    def _converse(self, message):
        # Fallback rule-based replies, used only when the configured AI
        # provider isn't reachable/ready.
        if "who are you" in message or "your name" in message:
            return "I'm NOVA. I'm in basic mode right now - the AI model isn't ready yet."

        if any(word in message for word in ["hello", "hey nova", "hi nova"]):
            return "Hello Krishna! How can I help you?"

        if message in ("hi", "yo", "sup", "hey"):
            return "Hi! What do you need?"

        if "how are you" in message:
            return "Running smoothly! How about you?"

        if "thank" in message:
            return "You're welcome!"

        if "joke" in message:
            return "Why do programmers prefer dark mode? Because light attracts bugs."

        if "what time" in message or message == "time":
            return datetime.now().strftime("It's %I:%M %p.")

        if "date" in message:
            return datetime.now().strftime("Today is %A, %B %d, %Y.")

        if "bye" in message or "exit" in message or "quit" in message:
            return "Goodbye, Krishna!"

        return f'I heard: "{message}" — I don\'t have a specific response for that (the AI model isn\'t ready yet).'


brain = Brain()
