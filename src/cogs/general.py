import discord

from discord.ext import bridge, commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot =bot
    
    # ------------ HELP COMMAND ------------
    @bridge.bridge_command(description="List of commands")
    async def commands(self, ctx):
        response = "# List of commands:\n\n## Moderation:\n\n- **!kick**\n- **!ban**\n- **!purge**\n\n## Utility:\n\n- **!changelog**"

        await ctx.respond(response)

def setup(bot): 
    # Add cog to the bot
    bot.add_cog(General(bot))