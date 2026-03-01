# bot.py
# Copyright (c) 2026 mattisva
# Licensed under the MIT License
import discord
from config import Meta
from on_ready import on_ready_event
from commands import info_commands, admin_commands
from utils.logger import safe_send, log

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    Meta.print_console and print(f"[STARTUP] Bot logged in as {client.user}")
    try:
        await on_ready_event(client)
    except Exception as e:
        Meta.print_console and print(f"[ERROR on_ready] {e}")


@client.event
async def on_message(message: discord.Message):
    Meta.print_console and print(f"[DEBUG] MESSAGE from {message.author}: {message.content}")

    if message.author == client.user:
        return
    if not message.content.lower().startswith("!bot"):
        return

    command_text = message.content[5:].strip()

    # Admin commands first:
    try:
        handled = await admin_commands.handle_admin(message, command_text)
        if handled:
            Meta.print_console and print(f"[DEBUG] ADMIN command handled: {command_text}")
            return
    except Exception as e:
        Meta.print_console and print(f"[ERROR admin_commands] {e}")
        try: 
            if Meta.output: await safe_send(message.channel, f"Error executing admin command: {e}")
        except: pass

    # Info commands next:
    try:
        handled = await info_commands.handle_info(message, command_text)
        if handled:
            Meta.print_console and print(f"[DEBUG] INFO command handled: {command_text}")
            return
    except Exception as e:
        Meta.print_console and print(f"[ERROR info_commands] {e}")
        try:
            if Meta.output: await safe_send(message.channel, f"Error executing info command: {e}")
        except: pass


if __name__ == "__main__":
    Meta.print_console and print("[STARTUP] Starting bot...")
    try:
        client.run(Meta.TOKEN)
    except Exception as e:
        Meta.print_console and print(f"[CRITICAL] Bot failed to start: {e}")