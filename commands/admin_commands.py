# commands/admin_commands.py
import discord
from utils.logger import safe_send, log
from config import Meta
from utils.checks import is_admin

async def handle_admin(message, command_text: str):
    guild = message.guild
    member = message.author

    if not is_admin(member):
        await safe_send(message.channel, "You must be an admin to use this command.")
        return

    try:
        if command_text.lower().startswith("echo"):
            await safe_send(message.channel, command_text[5:].strip())

        elif command_text.lower() == "version":
            await safe_send(message.channel, Meta.version)

        elif command_text.lower().startswith("cc"):
            parts = command_text.split()
            channel_name = parts[1] if len(parts) > 1 else None
            category_name = parts[2] if len(parts) > 2 else None
            if not channel_name:
                await safe_send(message.channel, "Please specify a channel name.")
                return
            category = discord.utils.get(guild.categories, name=category_name) if category_name else None
            new_channel = await guild.create_text_channel(name=channel_name, category=category, reason=f"Created by {member}")
            await safe_send(message.channel, f"Channel created: {new_channel.mention}")

        elif command_text.lower().startswith("dc"):
            parts = command_text.split()
            if len(parts) < 2:
                await safe_send(message.channel, "Please specify a channel name to delete.")
                return
            target = discord.utils.get(guild.channels, name=parts[1])
            if not target:
                await safe_send(message.channel, "Channel not found.")
                return
            await target.delete(reason=f"Deleted by {member}")
            await safe_send(message.channel, f"Channel {parts[1]} deleted.")

        elif command_text.lower().startswith("cf"):
            parts = command_text.split()
            if len(parts) < 2:
                await safe_send(message.channel, "Please specify a category name.")
                return
            new_cat = await guild.create_category(name=parts[1], reason=f"Created by {member}")
            await safe_send(message.channel, f"Category created: {new_cat.name}")

        elif command_text.lower().startswith("df"):
            parts = command_text.split()
            if len(parts) < 2:
                await safe_send(message.channel, "Please specify a category name.")
                return
            target = discord.utils.get(guild.categories, name=parts[1])
            if not target:
                await safe_send(message.channel, "Category not found.")
                return
            await target.delete(reason=f"Deleted by {member}")
            await safe_send(message.channel, f"Category {parts[1]} deleted.")

        await log(f"{member} used admin command: {command_text}", guild)

    except discord.Forbidden:
        await safe_send(message.channel, "I do not have permission to perform this action.")
    except discord.HTTPException as e:
        await safe_send(message.channel, f"Discord API error: {e}")
    except Exception as e:
        print(f"Error in admin_commands: {e}")
        await safe_send(message.channel, "An unexpected error occurred.")