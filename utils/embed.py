# utils/embed.py
# Copyright (c) 2026 mattisva
# Licensed under the MIT License - see the LICENSE file in the project root for details.
import discord
import json
async def send_embed(channel, title: str, desc: str, field: tuple):
    embed = discord.Embed(title=title, description=desc, color=0x00ff00)

    for i in field:
        embed.add_field(name=i[0], value=i[1], inline=False)

    await channel.send(embed=embed)

def json_to_tuple(data):
    ret = tuple()

    for entry in data:
        ret += ((entry["author"], entry["content"]),)

    return ret