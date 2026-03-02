# bot.py
# Copyright (c) 2026 mattisva
# Licensed under the MIT License
import threading
import discord
from config import Meta
from on_ready import on_ready_event
from commands import info_commands, admin_commands, fun_commands
from utils.logger import safe_send
from utils.ai import Ollama
from web.app import start_web
from db_log.main import db_add_message

# intents
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

# events
@client.event
async def on_ready():
    if Meta.print_console:
        print(f"[STARTUP] Logged in as {client.user}")

    try:
        await on_ready_event(client)
    except Exception as e:
        print(f"[ERROR on_ready] {e}")

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if Meta.print_console:
        print(f"[DEBUG] {message.author}: {message.content}")
    
    if Meta.db_log_is_active:
        db_add_message(message.author, message.content)

    prefix = "!bot"
    if not message.content.lower().startswith(prefix):
        return

    command_text = message.content[len(prefix):].strip()
    if not command_text:
        return

    # Admin
    try:
        handled = await admin_commands.handle_admin(message, command_text)
        if handled:
            return
    except Exception as e:
        print(f"[ERROR admin_commands] {e}")
        if Meta.output:
            await safe_send(message.channel, "Error executing admin command.")
        return

    # Info
    try:
        handled = await info_commands.handle_info(message, command_text)
        if handled:
            return
    except Exception as e:
        print(f"[ERROR info_commands] {e}")
        if Meta.output:
            await safe_send(message.channel, "Error executing info command.")
        return

    # Fun
    try:
        handled = await fun_commands.handle_fun(message, command_text)
        if handled:
            return
    except Exception as e:
        print(f"[ERROR fun_commands] {e}")
        if Meta.output:
            await safe_send(message.channel, "Error executing fun command.")
        return

if __name__ == "__main__":
    if Meta.print_console:
        print("[STARTUP] Starting bot...")
    try:
        Ollama.startup()
    except Exception as e:
        print(f"[CRITICAL] Ollama failed to start: {e}")
    try:
        if Meta.web_active: # start WebApp when enabled 
            web_thread = threading.Thread(target=start_web, daemon=True)
            web_thread.start()
    except Exception as e:
        print(f"[CRITICAL] Web failed to start: {e}")
    try:
        client.run(Meta.TOKEN)
    except Exception as e:
        print(f"[CRITICAL] Bot failed to start: {e}")