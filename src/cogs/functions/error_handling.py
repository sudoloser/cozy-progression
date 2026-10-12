import discord

async def error_embed(error):
    embed = discord.Embed(
        title="Failure",
        description="Failure to complete action due to the following:",
        color=0xBB2124
    )
    embed.add_field(
        name="Error",
        value=f"`{error}`"
    )

    return embed