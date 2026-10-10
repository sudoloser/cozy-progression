import discord
import os
import requests

from discord.ext import bridge, commands

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # ------------------ CHANGELOG COMMAND ---------------------------
    @bridge.bridge_command(description="Check latest changelog")

    # Define Command
    async def changelog(self, ctx):
        # This url is used to fetch the raw markdown link of the latest version changelog
        base_url = "https://raw.githubusercontent.com/sudoloser/cozy-progression/refs/heads/main/CHANGELOG/latest.md"

        try:
            # Fetch the latest changelog URL
            response = requests.get(base_url)

            # Asign that to a variable
            latest = response.text
            
            # Get the latest changelog
            response = requests.get(latest)

            content = response.text

            await ctx.respond(content)
        except Exception as e:
            await ctx.respond(f"Failed to get latest changelog from `{latest}`.\nGithub may be down\nError: `{e}`")
# Setup cog
def setup(bot): 
    # Add cog to the bot
    bot.add_cog(Utils(bot))