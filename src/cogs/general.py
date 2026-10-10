import discord

from discord.ext import bridge, commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # ------------ HELP COMMAND ------------
    @bridge.bridge_command(description="List of commands")
    async def commands(self, ctx):
        response = "# List of commands:\n\n## Moderation:\n\n- **!kick**\n- **!ban**\n- **!purge**\n## Utility:\n\n- **!changelog**\n- **!nick**"

        await ctx.respond(response)
    # ------------ LINKS COMMAND ------------
    @bridge.bridge_command(description="Send related modpack links")
    async def links(self, ctx):
        # Define a list of links
        links = [
            "- [Modrinth](<https://modrinth.com/modpack/cozyprogression>)",
            "[Twitter](<https://x.com/sudoloser>)"
        ]
        # Separate them with a newline and bulletpoint
        response = "\n- ".join(links)
        embed = discord.Embed(title="Links", description=f"{response}", color=discord.Color.blue())
        await ctx.respond(embed=embed)
    # ------------- DOWNLOAD COMMAND ---------
    @bridge.bridge_command(description="Link to download the modpack")
    async def download(self, ctx):
        embed = discord.Embed(title="Download", description="Search for Cozy Progression directly in your launcher (Prism, CurseForge, GDLauncher), or download the .mrpack manually from [Modrinth](<https://modrinth.com/modpack/cozyprogression>).", color=discord.Color.green())
        await ctx.respond(embed=embed)
    # ------------- RAM COMMAND --------------
    @bridge.bridge_command(description="Recommended allocated ram")
    async def ram(self, ctx):
        embed = discord.Embed(
            title="Allocated Ram",
            description="Assigning the right amount of RAM prevents stuttering and crashes!",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Recommended range",
            value="**4GB Minimum**, but **6 GB – 8 GB** is recommended.",
            inline=False
        )
        embed.add_field(
            name="How to change it",
            value=(
                "• **Prism / GDLauncher:** Settings → Java → Maximum Memory\n"
                "• **CurseForge App:** Settings → Minecraft → Allocated Memory Slider"
            ),
            inline=False
        )

        await ctx.respond(embed=embed)
    # ------------- CRASH COMMAND ------------
    @bridge.bridge_command(description="Shows how to upload crash logs")
    async def crash(self, ctx):
        embed = discord.Embed(
           title="🛠️ How to Share Your Crash Log",
           description="Please do not paste long crash logs directly into chat!",
           color=discord.Color.red(),
        )
        embed.add_field(
            name="1. Find your log file",
            value=(
               "Open your launcher and navigate to your instance folder.\n"
               "Look inside the `crash-reports` or `logs` folder for `latest.log`."
            ),
            inline=False,
        )
        embed.add_field(
            name="2. Upload your log",
            value="Upload the file to **[mclo.gs](https://mclo.gs)** or **[Pastebin](https://pastebin.com)**.",
            inline=False,
        )
        embed.add_field(
            name="3. Share the link",
            value="Paste the generated link here in chat so we can help you figure out what went wrong!",
            inline=False,
        )
        await ctx.respond(embed=embed)
def setup(bot): 
    # Add cog to the bot
    bot.add_cog(General(bot))