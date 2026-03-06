# commands/own_json.py
# Copyright (c) 2026 mattisva
# Licensed under the MIT License
import json
import random
import asyncio
import discord
import ast
import operator
from datetime import timedelta
from pathlib import Path
from utils.logger import safe_send
from utils.checks import is_admin
from utils.ai import Ollama
from config import Meta

# THIS IS A EXPERIMENTAL FEATURE

JSON_DIR = Path(__file__).parent / "json"
COMMANDS = []

SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,

    ast.UAdd: operator.pos,
    ast.USub: operator.neg,

    ast.Lt: operator.lt,
    ast.Gt: operator.gt,
    ast.LtE: operator.le,
    ast.GtE: operator.ge,
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,

    ast.BitAnd: operator.and_,
    ast.BitOr: operator.or_,
}
def safe_eval(expr: str, default=0):
    try:
        def _eval(node):

            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float, bool)):
                    return node.value
                raise ValueError("Invalid constant")

            elif isinstance(node, ast.UnaryOp):
                op = SAFE_OPERATORS.get(type(node.op))
                if not op:
                    raise ValueError("Operator not allowed")
                return op(_eval(node.operand))

            elif isinstance(node, ast.BinOp):
                op = SAFE_OPERATORS.get(type(node.op))
                if not op:
                    raise ValueError("Operator not allowed")
                return op(_eval(node.left), _eval(node.right))

            elif isinstance(node, ast.Compare):
                left = _eval(node.left)
                for op, comp in zip(node.ops, node.comparators):
                    func = SAFE_OPERATORS.get(type(op))
                    if not func:
                        raise ValueError("Comparison not allowed")
                    right = _eval(comp)
                    if not func(left, right):
                        return False
                    left = right
                return True

            else:
                raise ValueError(f"Unsafe node: {type(node)}")

        tree = ast.parse(expr, mode="eval")
        return _eval(tree.body)

    except Exception:
        return default

def render(text: str, context: dict) -> str:
    if not isinstance(text, str):
        return text
    for k, v in context.items():
        text = text.replace(f"{{{k}}}", str(v))
    return text

def load_json_commands():
    COMMANDS.clear()
    if not JSON_DIR.exists():
        return
    for file in JSON_DIR.glob("*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for cmd in data.get("commands", []):
                    cmd["__file"] = file.name
                    COMMANDS.append(cmd)
        except Exception as e:
            print(f"[JSON LOAD ERROR] {file}: {e}")

async def execute_actions(message, actions, context):
    for action in actions:
        t = action["type"]
        # TODO:
        # - Make more actions 
        try:
            if t in ("send_message", "reply", "send_dm", "send_embed"):
                await handle_messaging(message, action, context)
            elif t in ("create_channel", "delete_channel", "create_role", "delete_role",
                       "add_role", "remove_role", "set_channel_topic"):
                await handle_guild_actions(message, action, context)
            elif t in ("kick_member", "ban_member", "timeout_member"):
                await handle_moderation(message, action, context)
            elif t == "if":
                await handle_if(message, action, context)
            elif t == "loop":
                await handle_loop(message, action, context)
            elif t == "delay":
                await asyncio.sleep(int(action.get("seconds", 1)))
            elif t == "set_meta":
                if hasattr(Meta, action["field"]):
                    setattr(Meta, action["field"], action["value"])
            elif t == "require_role":
                role = discord.utils.get(message.guild.roles, name=render(action["role"], context))
                if not role or role not in message.author.roles:
                    return
            elif t == "random_choice":
                await safe_send(message.channel, random.choice(action["options"]))
            elif t == "math":
                result = safe_eval(render(action["expression"], context))
                await safe_send(message.channel, result)
            elif t == "call_ai":
                if not Meta.ai_is_active:
                    await safe_send(message.channel, "AI disabled.")
                else:
                    prompt = render(action["prompt"], context)
                    response = await asyncio.to_thread(Ollama.ai, prompt)
                    await safe_send(message.channel, response)
            else:
                print(f"[UNKNOWN ACTION] {t}")
        except Exception as e:
            print(f"[ERROR EXEC ACTION {t}] {e}")
            await safe_send(message.channel, f"Error executing custom command.")

async def handle_messaging(message, action, context):
    t = action["type"]
    if t == "send_message":
        await safe_send(message.channel, render(action["content"], context))
    elif t == "reply":
        await message.reply(render(action["content"], context))
    elif t == "send_dm":
        await message.author.send(render(action["content"], context))
    elif t == "send_embed":
        embed = discord.Embed(
            title=render(action.get("title", ""), context),
            description=render(action.get("description", ""), context),
            color=int(action.get("color", "0x3498db"), 16)
        )
        await message.channel.send(embed=embed)

async def handle_guild_actions(message, action, context):
    t = action["type"]
    try:
        if t == "create_channel":
            name = render(action["name"], context)
            if name:
                await message.guild.create_text_channel(name=name)
        elif t == "delete_channel":
            name = render(action["name"], context)
            ch = discord.utils.get(message.guild.channels, name=name)
            if ch: await ch.delete()
        elif t == "create_role":
            name = render(action["name"], context)
            if name:
                await message.guild.create_role(name=name)
        elif t == "delete_role":
            name = render(action["name"], context)
            role = discord.utils.get(message.guild.roles, name=name)
            if role: await role.delete()
        elif t == "add_role":
            name = render(action["role"], context)
            role = discord.utils.get(message.guild.roles, name=name)
            if role: await message.author.add_roles(role)
        elif t == "remove_role":
            name = render(action["role"], context)
            role = discord.utils.get(message.guild.roles, name=name)
            if role: await message.author.remove_roles(role)
        elif t == "set_channel_topic":
            await message.channel.edit(topic=render(action["topic"], context))
    except Exception as e:
        await safe_send(message.channel, f"Guild action failed: {e}")

async def handle_moderation(message, action, context):
    t = action["type"]
    try:
        if t == "kick_member":
            await message.author.kick()
        elif t == "ban_member":
            await message.author.ban()
        elif t == "timeout_member":
            seconds = int(action.get("seconds", 60))
            await message.author.timeout(discord.utils.utcnow() + timedelta(seconds=seconds))
    except Exception as e:
        await safe_send(message.channel, f"Moderation action failed: {e}")

async def handle_if(message, action, context):
    cond_expr = render(action["condition"], context)
    try:
        if cond_expr == "is_admin":
            if is_admin(message.author):
                await execute_actions(message, action["then"], context)
            elif "else" in action:
                await execute_actions(message, action["else"], context)
        elif safe_eval(cond_expr, default=False):
            await execute_actions(message, action["then"], context)
        elif "else" in action:
            await execute_actions(message, action["else"], context)
    except Exception:
        if "else" in action:
            await execute_actions(message, action["else"], context)

async def handle_loop(message, action, context):
    count_raw = render(str(action.get("count", "1")), context)
    try:
        count = int(count_raw)
    except ValueError:
        await safe_send(message.channel, f"Invalid loop count: {count_raw}, using 1.")
        count = 1
    for _ in range(count):
        await execute_actions(message, action["actions"], context)

async def handle_json(message, command_text: str) -> bool:
    parts = command_text.strip().split()
    if not parts: return False
    trigger = parts[0].lower()
    rest = " ".join(parts[1:])
    for cmd_def in COMMANDS:
        if trigger == cmd_def["trigger"]:
            if cmd_def.get("admin_only") and not is_admin(message.author):
                await safe_send(message.channel, "Admin only.")
                return True
            args, idx = {}, 0
            tokens = rest.split()
            for arg_def in cmd_def.get("args", []):
                key = arg_def["name"]
                if arg_def.get("rest"):
                    args[key] = " ".join(tokens[idx:])
                    break
                args[key] = tokens[idx] if idx < len(tokens) else ""
                idx += 1
            context = {**args, "user": message.author, "guild": message.guild, "channel": message.channel}
            await execute_actions(message, cmd_def["actions"], context)
            return True
    return False

load_json_commands()