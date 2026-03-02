# commands/help_command.py
# Copyright (c) 2026 mattisva
# Licensed under the MIT License
from config import Meta

HELP_TEXT = f"""
**open_bot {Meta.version} Commands**

━━━━━━━━━━━━━━━━━━━━
**Moderation / Admin**
━━━━━━━━━━━━━━━━━━━━
!bot echo <text> → Bot repeats the text (admin only)
!bot version → Show bot version
!bot cc <name> [category] → Create text channel
!bot dc <name> → Delete channel
!bot cf <name> → Create category
!bot df <name> → Delete category

━━━━━━━━━━━━━━━━━━━━
**Information**
━━━━━━━━━━━━━━━━━━━━
!bot help → Show this help message
!bot userinfo @user → Show user information
!bot serverinfo → Show server information
!bot channelinfo <name> → Show channel information
!bot roleinfo <name> → Show role information

━━━━━━━━━━━━━━━━━━━━
**Fun**
━━━━━━━━━━━━━━━━━━━━
!bot rint <a>-<b> → Random integer between a and b
!bot rchoose <a>-<b> → Randomly choose a or b
!bot ping → Replies pong
!bot ai <message> → Chat with AI

━━━━━━━━━━━━━━━━━━━━
https://github.com/mattsva/open_bot
Copyright (c) 2026 mattisva
Licensed under the MIT License
"""