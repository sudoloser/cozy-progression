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
    # ---------------------- NICK COMMAND ---------------------------
    @bridge.bridge_command(description="Change a user's nickname")
    @bridge.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member:discord.Member, *, nick:str):
        await member.edit(nick=nick)
        await ctx.respond(f"Changed {member.mention}'s nickname to {nick}")
    # ---------------------- ROLE COMMAND ---------------------------
    @bridge.bridge_command(description="Add or remove a role from a user")
    @bridge.has_permissions(manage_roles=True)
    async def role(self, ctx, member:discord.Member, role:discord.Role):
        success = discord.Embed(title="Success", description=f"Added role `{role}` to {member.mention}.", color=discord.Color.green())
        success2 = discord.Embed(title="Success", description=f"Removed role `{role}` from {member.mention}.", color=discord.Color.green())
        
        if member==None or role==None:
            return await ctx.respond("Please specify the targeted user and role.")
        try:
            if role in member.roles:
                await member.remove_roles(role)
                await ctx.respond(embed=success2)
            else:
                await member.add_roles(role)
                await ctx.respond(embed=success)

        except Exception as e:
            failure = discord.Embed(title="failure", description=f"Failure to add role `{role}` to {member.mention} with the following error:\n`{e}`", color=discord.Color.red())
            return await ctx.respond(embed=failure)
    # ---------------------- BANNER COMMAND -------------------------
    @bridge.bridge_command(description="Shows a user's banner")
    async def banner(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        user = await self.bot.fetch_user(member.id)

        if user.banner:
            embed = discord.Embed (
                title="Banner",
                description=f"{member.mention}'s Banner"
            )
            embed.set_image (
                url=user.banner
            )
            await ctx.respond(embed=embed)
        else:
            await ctx.respond("You either:\n- Used the command on its own\nor\n- The user does not have an banner set")
    # ---------------------- AVATAR COMMAND -------------------------
    @bridge.bridge_command(description="Shows a user's avatar")
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        user = await self.bot.fetch_user(member.id)

        if user.avatar:
            embed = discord.Embed (
                title="Avatar",
                description=f"{member.mention}'s Avatar"
            )
            embed.set_image (
                url=user.avatar
            )
            await ctx.respond(embed=embed)
        else:
            await ctx.respond("You either:\n- Used the command on its own\nor\n- The user does not have an avatar set")
# Setup cog
def setup(bot): 
    # Add cog to the bot
    bot.add_cog(Utils(bot))