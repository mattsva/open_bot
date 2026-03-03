# on_ready.py
# Copyright (c) 2026 mattisva
# Licensed under the MIT License - see the LICENSE file in the project root for details.
import discord
from utils.logger import log
from config import Meta

async def on_ready_event(client: discord.Client):
    print(f"Bot logged in as {client.user}")
    guild = client.get_guild(Meta.GUILD_ID)
    if guild:
        await log("Bot is online", guild)
    print("Bot is ready. Responding to commands.")