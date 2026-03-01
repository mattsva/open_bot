# utils/logger.py
# Copyright (c) 2026 mattisva
# Licensed under the MIT License
import discord
import datetime
from config import Meta

async def safe_send(channel, content):
    # Send message to a channel if config.Meta.output is True; Always prints to console if config.Meta.print_console
    if Meta.print_console:
        print(f"[SAFE_SEND {datetime.datetime.now()}] {channel}: {content}")

    if Meta.output:
        try:
            await channel.send(content)
        except Exception as e:
            Meta.print_console and print(f"[SAFE_SEND ERROR] Failed to send to {channel}: {e}")


async def log(text, guild):
    # Log message to log channel and / or console based on config.Meta settings
    timestamp = datetime.datetime.now()

    if Meta.print_console:
        print(f"[LOG {timestamp}] {text}")

    if not Meta.log:
        return

    log_channel = discord.utils.get(guild.text_channels, name="log")
    if log_channel and log_channel.permissions_for(guild.me).send_messages:
        try:
            await log_channel.send(f"[{timestamp}] {text}")
        except Exception as e:
            Meta.print_console and print(f"[LOG ERROR] Failed to send log message: {e}")