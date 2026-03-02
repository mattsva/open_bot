# commands/fun_commands.py
# Copyright (c) 2026 mattisva
# Licensed under the MIT License
import asyncio
import random
from utils.logger import safe_send, log
from config import Meta
from utils.ai import Ollama


async def handle_fun(message, command_text: str) -> bool:
    guild = message.guild
    member = message.author

    try:
        cmd = command_text.lower()

        # rint - random int in range <a>-<b>
        if cmd.startswith("rint"):
            payload = command_text[4:].strip()

            if "-" not in payload:
                await safe_send(message.channel, "Usage: rint <a>-<b>")
                return True

            parts = payload.split("-")
            if len(parts) != 2:
                await safe_send(message.channel, "Usage: rint <a>-<b>")
                return True

            a = int(parts[0].strip())
            b = int(parts[1].strip())

            result = random.randint(a, b)
            await safe_send(message.channel, result)

            await log(f"{member} used rint: {a}-{b}", guild)
            return True

        elif cmd.startswith("rchoose"):
            payload = command_text[7:].strip()

            parts = [p.strip() for p in payload.split("-") if p.strip()]

            if len(parts) < 2:
                await safe_send(message.channel, "Usage: rchoose <a>-<b>-<c>-...")
                return True

            result = random.choice(parts)
            await safe_send(message.channel, result)

            await log(f"{member} used rchoose: {parts}", guild)
            return True

        # ping - pong
        elif cmd.startswith("ping"):
            await safe_send(message.channel, "pong")
            await log(f"{member} used ping", guild)
            return True

        # AI Chat
        elif cmd.startswith("ai"):
            content = command_text[2:].strip()

            if not content:
                await safe_send(message.channel, "Usage: ai <message>")
                return True

            # Run blocking AI call in thread
            response = await asyncio.to_thread(Ollama.ai, content)

            await safe_send(message.channel, response)
            await log(f"{member} used ai command", guild)
            return True

            # TODO:
            # - Add verification
            # - Add ratelimit

        return False  # no command matched

    except Exception as e:
        print(f"Error in fun_commands: {e}")
        await safe_send(message.channel, "An error occurred while processing your request.")
        return True