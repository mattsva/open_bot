# commands/own_json.py
# Copyright (c) 2026 mattisva
# Licensed under the MIT License - see the LICENSE file in the project root for details.
import json
import random
import discord
from pathlib import Path
from utils.logger import safe_send, log
from utils.checks import is_admin
from config import Meta

JSON_DIR = Path(__file__).parent / "json"
COMMANDS = []

def load_json_commands():
    for file in JSON_DIR.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                for cmd in data.get("commands", []):
                    cmd["__file"] = file.name
                    COMMANDS.append(cmd)
            except json.JSONDecodeError as e:
                print(f"Failed to load {file}: {e}")

def render(text: str, context: dict) -> str:
    for k, v in context.items():
        text = text.replace(f"{{{k}}}", str(v))
    return text

async def execute_actions(message, cmd_def, args):
    guild = message.guild
    user = message.author
    context = {
        "user": user,
        "channel": message.channel,
        "guild": guild,
        **args
    }

    for action in cmd_def["actions"]:
        t = action["type"]

        if t == "send_message":
            content = render(action["content"], context)
            await safe_send(message.channel, content)

        elif t == "log":
            msg = render(action["message"], context)
            await log(msg, guild)

        elif t == "random_int":
            raw = render(action["range"], context)
            if "-" in raw:
                a, b = raw.split("-", 1)
                try:
                    val = random.randint(int(a), int(b))
                    await safe_send(message.channel, val)
                except ValueError:
                    await safe_send(message.channel, "Invalid range format.")

        else:
            print(f"Unknown action type: {t}")

async def handle_json(message, command_text: str) -> bool:
    cmd = command_text.strip().split()
    if not cmd:
        return False
    name = cmd[0].lower()
    rest = " ".join(cmd[1:])

    for cmd_def in COMMANDS:
        if name == cmd_def["trigger"]:
            # admin check
            if cmd_def.get("admin_only") and not is_admin(message.author):
                await safe_send(message.channel, "Admin only.")
                return True

            # argument parser
            args = {}
            arg_defs = cmd_def.get("args", [])
            tokens = rest.split()
            idx = 0
            for arg_def in arg_defs:
                key = arg_def["name"]
                if arg_def.get("rest"):
                    args[key] = " ".join(tokens[idx:]) if idx < len(tokens) else ""
                    break
                else:
                    if idx < len(tokens):
                        args[key] = tokens[idx]
                        idx += 1
                    else:
                        args[key] = ""

            # start action
            await execute_actions(message, cmd_def, args)
            return True

    return False

# load commands
load_json_commands()