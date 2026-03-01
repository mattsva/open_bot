# commands/info_commands.py
import discord
from utils.logger import safe_send, log
from commands.help_command import HELP_TEXT
from config import Meta

async def handle_info(message, command_text: str):
    guild = message.guild
    member = message.author

    try:
        # Help command
        if command_text.lower() == "help":
            if Meta.output:
                await safe_send(message.channel, HELP_TEXT)
            if Meta.print_console:
                print(f"[HELP] {member} requested help")
            await log(f"{member} requested help", guild)
            return  # handled, no further processing

        # userinfo
        if command_text.lower().startswith("userinfo"):
            if len(message.mentions) == 0:
                await safe_send(message.channel, "Please mention a user.")
                return
            target = message.mentions[0]
            roles = [r.name for r in target.roles if r.name != "@everyone"]
            join_date = target.joined_at.strftime("%Y-%m-%d %H:%M")
            status = str(target.status)
            response = f"**User Info: {target}**\nRoles: {', '.join(roles) or 'none'}\nJoined: {join_date}\nStatus: {status}"
            await safe_send(message.channel, response)

        # serverinfo
        elif command_text.lower() == "serverinfo":
            channels = len(guild.channels)
            members = guild.member_count
            created = guild.created_at.strftime("%Y-%m-%d %H:%M")
            response = f"**Server Info: {guild.name}**\nCreated: {created}\nMembers: {members}\nChannels: {channels}"
            await safe_send(message.channel, response)

        # channelinfo
        elif command_text.lower().startswith("channelinfo"):
            parts = command_text.split()
            if len(parts) < 2:
                await safe_send(message.channel, "Please specify a channel name.")
                return
            target = discord.utils.get(guild.channels, name=parts[1])
            if not target:
                await safe_send(message.channel, "Channel not found.")
                return
            category = target.category.name if target.category else "None"
            perms = target.permissions_for(guild.me)
            response = f"**Channel Info: {target.name}**\nType: {type(target).__name__}\nCategory: {category}\nPermissions for bot: {perms}"
            await safe_send(message.channel, response)

        # roleinfo
        elif command_text.lower().startswith("roleinfo"):
            parts = command_text.split()
            if len(parts) < 2:
                await safe_send(message.channel, "Please specify a role name.")
                return
            target = discord.utils.get(guild.roles, name=parts[1])
            if not target:
                await safe_send(message.channel, "Role not found.")
                return
            members = len(target.members)
            color = str(target.color)
            perms = target.permissions
            response = f"**Role Info: {target.name}**\nMembers: {members}\nColor: {color}\nPermissions: {perms}"
            await safe_send(message.channel, response)

        # log usage
        await log(f"{member} used info command: {command_text}", guild)

    except Exception as e:
        print(f"Error in info_commands: {e}")
        await safe_send(message.channel, "An error occurred while processing your request.")