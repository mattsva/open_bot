# commands/info_commands.py
# Copyright (c) 2026 mattisva
# Licensed under the MIT License
import discord
from utils.logger import safe_send, log
from commands.help_command import HELP_TEXT
from config import Meta


async def handle_info(message, command_text: str) -> bool:
    guild = message.guild
    member = message.author
    cmd = command_text.lower().strip()

    try:
        # help
        if cmd == "help":
            if Meta.output:
                await safe_send(message.channel, HELP_TEXT)

            if Meta.print_console:
                print(f"[HELP] {member} requested help")

            await log(f"{member} requested help", guild)
            return True

        # userinfo
        elif cmd.startswith("userinfo"):
            if not message.mentions:
                await safe_send(message.channel, "Please mention a user.")
                return True

            target = message.mentions[0]
            roles = [r.name for r in target.roles if r.name != "@everyone"]
            joined = target.joined_at.strftime("%Y-%m-%d %H:%M") if target.joined_at else "Unknown"

            response = (
                f"**User Info: {target}**\n"
                f"Roles: {', '.join(roles) or 'None'}\n"
                f"Joined: {joined}\n"
                f"Status: {target.status}"
            )

            await safe_send(message.channel, response)
            await log(f"{member} used userinfo", guild)
            return True

        # serverinfo
        elif cmd == "serverinfo":
            response = (
                f"**Server Info: {guild.name}**\n"
                f"Created: {guild.created_at.strftime('%Y-%m-%d %H:%M')}\n"
                f"Members: {guild.member_count}\n"
                f"Channels: {len(guild.channels)}"
            )

            await safe_send(message.channel, response)
            await log(f"{member} used serverinfo", guild)
            return True

        # channelinfo
        elif cmd.startswith("channelinfo"):
            parts = command_text.split()
            if len(parts) < 2:
                await safe_send(message.channel, "Please specify a channel name.")
                return True

            target = discord.utils.get(guild.channels, name=parts[1])
            if not target:
                await safe_send(message.channel, "Channel not found.")
                return True

            category = target.category.name if target.category else "None"

            response = (
                f"**Channel Info: {target.name}**\n"
                f"Type: {type(target).__name__}\n"
                f"Category: {category}"
            )

            await safe_send(message.channel, response)
            await log(f"{member} used channelinfo", guild)
            return True

        # roleinfo
        elif cmd.startswith("roleinfo"):
            parts = command_text.split()
            if len(parts) < 2:
                await safe_send(message.channel, "Please specify a role name.")
                return True

            target = discord.utils.get(guild.roles, name=parts[1])
            if not target:
                await safe_send(message.channel, "Role not found.")
                return True

            response = (
                f"**Role Info: {target.name}**\n"
                f"Members: {len(target.members)}\n"
                f"Color: {target.color}\n"
                f"Permissions: {target.permissions}"
            )

            await safe_send(message.channel, response)
            await log(f"{member} used roleinfo", guild)
            return True

        return False

    except Exception as e:
        print(f"Error in info_commands: {e}")
        await safe_send(message.channel, "An error occurred while processing your request.")
        return True

# TODO:
# - Add info about the WebApp-System