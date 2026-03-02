# commands/info_commands.py
# Copyright (c) 2026 mattisva
# Licensed under the MIT License
import discord
from utils.logger import safe_send, log
from commands.help_command import HELP_TEXT
from config import Meta
import random

async def handle_info(message, command_text: str):
    guild = message.guild
    member = message.author

    try:
        # rint
        if command_text.lower().startswith("rint"):
            a = int(command_text[5:(command_text.find("-"))].strip())
            b = int(command_text[(command_text.find("-"))+1:].strip())
            await safe_send(message.channel, random.choice([a, b]))
        
        elif command_text.lower().startswith("rchoose"):
            a = str(command_text[8:(command_text.find("-"))].strip())
            b = str(command_text[(command_text.find("-"))+1:].strip())
            await safe_send(message.channel, random.choice([a, b]))


        # log usage
        await log(f"{member} used info command: {command_text}", guild)

    except Exception as e:
        print(f"Error in info_commands: {e}")
        await safe_send(message.channel, "An error occurred while processing your request.")