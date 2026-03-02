# config.py
# Copyright (c) 2026 mattisva
# Licensed under the MIT License
import os
from dotenv import load_dotenv

load_dotenv()
# This loads the ".env" file. pleas change it like this:
# BOT_TOKEN="THIS_IS_A_WEIRD_BOT_TOKEN_LOL" # Your real BOT_TOKEN from the bot tab in the dc-bot-dashboard
# GUILD_ID="6969696969696969" # Your real GUILD_ID / SERVER_ID

class Meta:
    # DO NOT CHANGE:
    version = "v0.0.0.-e3.u0"
    GUILD_ID = os.getenv("GUILD_ID")
    TOKEN = os.getenv("BOT_TOKEN")

    # CHANGE:
    log = True
    print_console = True
    output = True
    admin_role = "admin" # This is admin role on your server