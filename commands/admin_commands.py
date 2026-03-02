# commands/admin_commands.py
# Copyright (c) 2026 mattisva
# Licensed under the MIT License
import discord
from utils.logger import safe_send, log
from config import Meta
from utils.checks import is_admin


async def handle_admin(message, command_text: str) -> bool:
    guild = message.guild
    member = message.author
    cmd = command_text.lower().strip()

    if not is_admin(member):
        return False  # Not handled → allow other modules to check

    try:
        # echo
        if cmd.startswith("echo"):
            await safe_send(message.channel, command_text[5:].strip())
            await log(f"{member} used echo", guild)
            return True

        # version
        elif cmd == "version":
            await safe_send(message.channel, Meta.version)
            await log(f"{member} used version", guild)
            return True

        # cc - create channel
        elif cmd.startswith("cc"):
            parts = command_text.split()
            if len(parts) < 2:
                await safe_send(message.channel, "Please specify a channel name.")
                return True

            category = None
            if len(parts) > 2:
                category = discord.utils.get(guild.categories, name=parts[2])

            new_channel = await guild.create_text_channel(
                name=parts[1],
                category=category,
                reason=f"Created by {member}"
            )

            await safe_send(message.channel, f"Channel created: {new_channel.mention}")
            await log(f"{member} created channel {parts[1]}", guild)
            return True

        # dc - delete channel
        elif cmd.startswith("dc"):
            parts = command_text.split()
            if len(parts) < 2:
                await safe_send(message.channel, "Please specify a channel name.")
                return True

            target = discord.utils.get(guild.channels, name=parts[1])
            if not target:
                await safe_send(message.channel, "Channel not found.")
                return True

            await target.delete(reason=f"Deleted by {member}")
            await safe_send(message.channel, f"Channel {parts[1]} deleted.")
            await log(f"{member} deleted channel {parts[1]}", guild)
            return True

        # cf - create category (aka folder)
        elif cmd.startswith("cf"):
            parts = command_text.split()
            if len(parts) < 2:
                await safe_send(message.channel, "Please specify a category name.")
                return True

            new_cat = await guild.create_category(
                name=parts[1],
                reason=f"Created by {member}"
            )

            await safe_send(message.channel, f"Category created: {new_cat.name}")
            await log(f"{member} created category {parts[1]}", guild)
            return True

        # df - celete category (aka folder)
        elif cmd.startswith("df"):
            parts = command_text.split()
            if len(parts) < 2:
                await safe_send(message.channel, "Please specify a category name.")
                return True

            target = discord.utils.get(guild.categories, name=parts[1])
            if not target:
                await safe_send(message.channel, "Category not found.")
                return True

            await target.delete(reason=f"Deleted by {member}")
            await safe_send(message.channel, f"Category {parts[1]} deleted.")
            await log(f"{member} deleted category {parts[1]}", guild)
            return True

        return False

    except discord.Forbidden:
        await safe_send(message.channel, "I do not have permission to perform this action.")
        return True
    except discord.HTTPException as e:
        await safe_send(message.channel, f"Discord API error: {e}")
        return True
    except Exception as e:
        print(f"Error in admin_commands: {e}")
        await safe_send(message.channel, "An unexpected error occurred.")
        return True

# TODO:
# - Add role commands
# - Add premission system
# - - Add premisson commands