# config.py
# Copyright (c) 2026 mattisva
# Licensed under the MIT License - see the LICENSE file in the project root for details.
import os
from dotenv import load_dotenv

load_dotenv()
# Example .env:
# BOT_TOKEN="THIS_IS_A_WEIRD_BOT_TOKEN_LOL"
# GUILD_ID="6969696969696969"

class Meta:
    # DO NOT CHANGE
    version = "v0.0.0.-e10.u19" # DO NOT CHANGE (unless you change it and want to update the version)
    GUILD_ID = os.getenv("GUILD_ID") # DO NOT CHANGE
    TOKEN = os.getenv("BOT_TOKEN") # DO NOT CHANGE
    ai_messages = [] # DO NOT CHANGE

    ## Change thoose:

    # Output and log
    log = True
    print_console = True
    output = True
    db_log_is_active = True

    # Roles
    admin_role = "admin"

    # AI
    ai_system = "ollama" # ollama or gpt4all
    ai_is_active  = True
    if ai_system == "ollama":
        ai_model = "gpt-oss:latest"
    elif ai_system == "gpt4all":
        ai_model = "orca-mini-3b-gguf2-q4_0.gguf"
    ai_needs_admin = False
    ai_blacklistet = None # role that is blacklistet to use AI
    ai_gpt4all_maxtokens = 3

    # WebApp
    web_active = True # Activate web server
    web_debug = False # Flask debug mode
    only_localhost = True # True = 127.0.0.1 only, False = accessible in WLAN

# TODO:
# - Add more customisable options # edit: it gets more! ;)