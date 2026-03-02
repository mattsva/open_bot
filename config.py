# config.py
# Copyright (c) 2026 mattisva
# Licensed under the MIT License
import os
from dotenv import load_dotenv

load_dotenv()
# Example .env:
# BOT_TOKEN="THIS_IS_A_WEIRD_BOT_TOKEN_LOL"
# GUILD_ID="6969696969696969"

class Meta:
    # DO NOT CHANGE
    version = "v0.0.0.-e5.u5" # DO NOT CHANGE (unless you change it and want to update the version)
    GUILD_ID = os.getenv("GUILD_ID") # DO NOT CHANGE
    TOKEN = os.getenv("BOT_TOKEN") # DO NOT CHANGE
    ai_messages = [] # DO NOT CHANGE

    ## Change thoose:

    # Output
    log = True
    print_console = True
    output = True

    # Roles
    admin_role = "admin"

    # AI
    ai_model = "gpt-oss:latest"

    # WebApp
    web_active = True # True to activate web server
    web_debug = False # Flask debug mode
    only_localhost = True # True = 127.0.0.1 only, False = accessible in WLAN