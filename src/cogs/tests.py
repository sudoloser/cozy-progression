import discord

from .functions import error_handling
from .functions.error_handling import error_embed

from discord.ext import bridge, commands

class tests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_group()
    async def test(self, ctx):
        pass

    @test.command(description="Test error handling")
    async def error_handling(self, ctx):
        test = "Test passed!"
        try:
            embed_obj = await error_embed(ctx, test)
            await ctx.respond(embed=embed_obj)
        except Exception as e:
            embed = discord.Embed(
                title="Failure", 
                description="Failed to complete action due to the following:"
            )
            embed.add_field(
                name="Error",
                value=e
            )

            await ctx.respond(embed=embed)
def setup(bot):
    bot.add_cog(tests(bot))