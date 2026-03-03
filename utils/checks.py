# utils/checks.py
# Copyright (c) 2026 mattisva
# Licensed under the MIT License - see the LICENSE file in the project root for details.
from config import Meta

def is_admin(member): # Checks if the member is an admin
    roles = [r.name.lower() for r in member.roles]
    return Meta.admin_role in roles

# TODO:
# - Add checks for other things, like blacklist checks and stuff...