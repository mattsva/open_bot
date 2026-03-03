# commands/admin_commands.py
# Copyright (c) 2026 mattisva
# Licensed under the MIT License
import discord
from utils.logger import safe_send, log
from config import Meta
from utils.checks import is_admin
from db_log.main import db_show_messages


async def handle_admin(message, command_text: str) -> bool:
    guild = message.guild
    member = message.author

    cmd_raw = command_text.strip()
    cmd = cmd_raw.lower()

    if not is_admin(member):
        return False

    try:
        parts = cmd_raw.split()

        # echo
        if cmd.startswith("echo"):
            await safe_send(message.channel, cmd_raw[5:].strip())
            await log(f"{member} used echo", guild)
            return True

        # version
        elif cmd == "version":
            await safe_send(message.channel, Meta.version)
            await log(f"{member} used version", guild)
            return True
        
        elif cmd.startswith("dblog"):
            action = cmd_raw[6:].strip()
            if action == "on":
                Meta.db_log_is_active = True
                await safe_send(message.channel, "DB log is now activated")
                await log(f"{member} used dblog on", guild)
            elif action == "off":
                Meta.db_log_is_active = False
                await safe_send(message.channel, "DB log is now deactivated")
                await log(f"{member} used dblog off", guild)
            elif action == "show":
                await safe_send(message.channel, db_show_messages())
                await log(f"{member} used dblog show", guild)
            else:
                await safe_send(message.channel, f"WebApp cannot do: {action}")
                await log(f"{member} tried dblog {action}", guild)
            return True

        # cc - create channel
        elif cmd.startswith("cc"):
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

        # cf - create category
        elif cmd.startswith("cf"):
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

        # df - delete category
        elif cmd.startswith("df"):
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

        # webapp on/off
        elif cmd.startswith("webapp"):
            action = cmd_raw[6:].strip()
            if action == "on":
                Meta.web_active = True
                await safe_send(message.channel, "WebApp is now activated")
                await log(f"{member} used webapp on", guild)
            elif action == "off":
                Meta.web_active = False
                await safe_send(message.channel, "WebApp is now deactivated")
                await log(f"{member} used webapp off", guild)
            else:
                await safe_send(message.channel, f"WebApp cannot do: {action}")
                await log(f"{member} tried webapp {action}", guild)
            return True

        # cr - create role with optional color
        elif cmd.startswith("cr"):
            if len(parts) < 2:
                await safe_send(message.channel, "Please specify a role name.")
                return True

            role_name = parts[1]
            role_color = discord.Color.default()

            if len(parts) >= 3:
                hex_color = parts[2].replace("#", "")
                try:
                    role_color = discord.Color(int(hex_color, 16))
                except ValueError:
                    await safe_send(message.channel, "Invalid color format. Use hex like #ff0000")
                    return True

            existing = discord.utils.get(guild.roles, name=role_name)
            if existing:
                await safe_send(message.channel, "Role already exists.")
                return True

            new_role = await guild.create_role(
                name=role_name,
                color=role_color,
                reason=f"Created by {member}"
            )
            await safe_send(message.channel, f"Role created: {new_role.mention}")
            await log(f"{member} created role {role_name} with color {role_color}", guild)
            return True

        # dr - delete role
        elif cmd.startswith("dr"):
            if len(parts) < 2:
                await safe_send(message.channel, "Please specify a role name.")
                return True

            role_name = parts[1]
            role = discord.utils.get(guild.roles, name=role_name)
            if not role:
                await safe_send(message.channel, "Role not found.")
                return True

            await role.delete(reason=f"Deleted by {member}")
            await safe_send(message.channel, f"Role {role_name} deleted.")
            await log(f"{member} deleted role {role_name}", guild)
            return True

        # ar - add role to member
        elif cmd.startswith("ar"):
            if len(parts) < 3 or not message.mentions:
                await safe_send(message.channel, "Usage: ar @user RoleName")
                return True

            target_member = message.mentions[0]
            role_name = parts[2]
            role = discord.utils.get(guild.roles, name=role_name)
            if not role:
                await safe_send(message.channel, "Role not found.")
                return True

            await target_member.add_roles(role, reason=f"Added by {member}")
            await safe_send(message.channel, f"Role {role_name} added to {target_member.mention}.")
            await log(f"{member} added role {role_name} to {target_member}", guild)
            return True

        # rr - remove role from member
        elif cmd.startswith("rr"):
            if len(parts) < 3 or not message.mentions:
                await safe_send(message.channel, "Usage: rr @user RoleName")
                return True

            target_member = message.mentions[0]
            role_name = parts[2]
            role = discord.utils.get(guild.roles, name=role_name)
            if not role:
                await safe_send(message.channel, "Role not found.")
                return True

            await target_member.remove_roles(role, reason=f"Removed by {member}")
            await safe_send(message.channel, f"Role {role_name} removed from {target_member.mention}.")
            await log(f"{member} removed role {role_name} from {target_member}", guild)
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
# - Add premission system
# - - Add premisson commands