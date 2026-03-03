# commands/help_command.py
# Copyright (c) 2026 mattisva
# Licensed under the MIT License - see the LICENSE file in the project root for details.
from config import Meta

HELP_TEXT = f"""
**open_bot {Meta.version} Commands**

━━━━━━━━━━━━━━━━━━━━
**Moderation / Admin**
━━━━━━━━━━━━━━━━━━━━
`!bot echo <text>` → Bot repeats the text (admin only)
`!bot version →` Show bot version
`!bot cc <name> [category]` → Create text channel
`!bot dc <name>` → Delete channel
`!bot cf <name>` → Create category
`!bot df <name>` → Delete category
`!bot webapp on` → Activates the WebApp/WebInterface
`!bot webapp off` → Deactivates the WebApp/WebInterface
`!bot cr <role> <color>` → Create role <role> with colorcode <color>
`!bot dr <role>` → Delete role <role>
`!bot ar @user <role>` → Add role <role> to user
`!bot rr @user <role>` → Remove role <role> form user
`!bot aai on` → AI fetures on
`!bot aai off` → AI fetures on
`!bot aai show` → show AI model
`!bot mc <model>` → AI model change to <model>
`!bot dblog on` → DB logging system on
`!bot dblog off` → DB logging system off
`!bot dblog show` → Show DB log

━━━━━━━━━━━━━━━━━━━━
**Information**
━━━━━━━━━━━━━━━━━━━━
`!bot help` → Show this help message
`!bot userinfo @user` → Show user information
`!bot serverinfo` → Show server information
`!bot channelinfo <name>` → Show channel information
`!bot roleinfo <name>` → Show role information

━━━━━━━━━━━━━━━━━━━━
**Fun**
━━━━━━━━━━━━━━━━━━━━
`!bot rint <a>-<b>` → Random integer between a and b
`rchoose <a>-<b>-<c>-...` → Randomly choose a, b, c or ...
`!bot ping` → Replies pong
`!bot ai <message>` → Chat with AI

━━━━━━━━━━━━━━━━━━━━
https://github.com/mattsva/open_bot
Copyright (c) 2026 mattisva
Licensed under the MIT License
"""