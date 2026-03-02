# commands/help_command.py
# Copyright (c) 2026 mattisva
# Licensed under the MIT License
from config import Meta

HELP_TEXT = f"""
**open_bot {Meta.version} Commands**

**1. Moderation / Server Management**
- `!bot mute <user>` → Mute a user (requires role or timeout)
- `!bot unmute <user>` → Unmute a user
- `!bot kick <user>` → Kick a user from the server
- `!bot ban <user>` → Ban a user
- `!bot unban <user>` → Unban a user
- `!bot rc <channel> <newname>` → Rename a channel
- `!bot ru <user> <newname>` → Rename a user (nickname)
- `!bot move <channel> <category>` → Move a channel to another category
- `!bot lock <channel>` → Remove write permissions for all except admins/bots
- `!bot unlock <channel>` → Restore write permissions

**2. Admin / Utility**
- `!bot echo <text>` → Bot repeats the text (admin only)
- `!bot version` → Show bot version
- `!bot cc <channelname> [categoryname]` → Create a text channel
- `!bot dc <channelname>` → Delete a text channel
- `!bot cf <categoryname>` → Create a category
- `!bot df <categoryname>` → Delete a category

**3. Information Commands (Everyone)**
- `!bot userinfo <user>` → Show user's roles, join date, status
- `!bot serverinfo` → Show server info: creation date, channels, members
- `!bot channelinfo <channel>` → Show channel type, category, permissions
- `!bot roleinfo <role>` → Show role color, member count, permissions

**4. Fun Commands (Everyone)**
- `!bot rint <number1>-<number2>` → random number between number1 and number2
- `!bot rchoose <text1>-<text2>` → random choosen text that is text1 or text2

---

https://github.com/mattsva/open_bot
Copyright (c) 2026 mattisva
Licensed under the MIT License

"""