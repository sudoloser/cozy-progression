import discord
import os
import requests

from discord.ext import bridge, commands

class Utils(commands.Cog):
    @bridge.bridge_command(description="Check latest changelog")
    async def changelog(self, ctx):
        base_url = "https://"
        try:
            response = requests.get('')