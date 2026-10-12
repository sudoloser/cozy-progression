import discord
import os
import aiohttp
import math
import random
import asyncio

from .functions import error_handling
from .functions.error_handling import error_embed

from discord.ext import bridge, commands

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(description="Shows information about the bot")
    async def info(self, ctx):
        base_url="https://raw.githubusercontent.com/sudoloser/cozy-progression/refs/heads/main/info/information.md"

        try:

            async with aiohttp.ClientSession() as session:
                async with session.get(base_url) as response:
                    content = await response.text()
            embed = discord.Embed(
                title="Info",
                description=content,
                color=0x107AB0
                )
            await ctx.respond(embed=embed)
        except Exception as e:
            if len(e) > 1024:
                e = e[:1021] + "..."
            embed = await error_embed(ctx, e)
            await ctx.respond(embed=embed)

    @bridge.bridge_command(description="Check latest changelog")
    async def changelog(self, ctx):
        await ctx.defer()
        # latest.md contains a link to the actual changelog file, so this is a double fetch
        base_url = "https://raw.githubusercontent.com/sudoloser/cozy-progression/refs/heads/main/info/CHANGELOG/latest.md"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url) as response:
                    latest = await response.text()
                async with session.get(latest) as response:
                    content = await response.text()

            await ctx.respond(content)
        except Exception as e:
            embed = await error_embed(ctx, e)
            await ctx.respond(embed=embed)

    @bridge.bridge_command(description="Check if a mod is in the modlist")
    async def mod(self, ctx, *, mod: str = ""):
        await ctx.defer()

        mod = mod.strip()
        modlistlink = "https://github.com/sudoloser/cozy-progression/blob/main/info/modlist.md"
        base_url = "https://raw.githubusercontent.com/sudoloser/cozy-progression/refs/heads/main/info/modlist.txt"

        if not mod:
            await ctx.respond("Please provide a mod name to search for, or use `!mod list` to get a link for the list.")
            return
        elif mod == "list":
            await ctx.respond(f"Click [here]({modlistlink}) for the full modlist.")
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url) as response:
                    text = await response.text()

            modlist = text.splitlines()
            mod_lower = mod.lower()

            content = [line for line in modlist if mod_lower in line.lower()]

            if content:
                description_lines = []
                char_count = 0
                max_chars = 3800

                for line in content:
                    formatted_line = f"- {line}\n"
                    if char_count + len(formatted_line) > max_chars:
                        remaining = len(content) - len(description_lines)
                        description_lines.append(f"\n*...and {remaining} more matches.*")
                        break
                    description_lines.append(formatted_line)
                    char_count += len(formatted_line)

                embed = discord.Embed(
                    title=f"Matched Mods ({len(content)} found):",
                    description="".join(description_lines),
                    color=discord.Color.blue()
                )
                embed.add_field (
                    name="Modlist",
                    value=f"Click [here]({modlistlink}) for the full modlist."
                )
                await ctx.respond(embed=embed)
            else:
                embed = discord.Embed(
                    title="Matched Mods:",
                    description=f"Could not find any mods matching `{mod}`.",
                    color=discord.Color.red()
                )
                await ctx.respond(embed=embed)

    @bridge.bridge_command(description="Change a user's nickname")
    @bridge.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member:discord.Member, *, nick:str):
        await member.edit(nick=nick)
        await ctx.respond(f"Changed {member.mention}'s nickname to {nick}")

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
            embed = await error_embed(ctx, e)
            return await ctx.respond(embed=embed)

    @bridge.bridge_command(description="Shows a user's banner")
    async def banner(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        user = await self.bot.fetch_user(user.id)

        if user.banner:
            embed = discord.Embed (
                title="Banner",
                description=f"{user.mention}'s Banner"
            )
            embed.set_image (
                url=user.banner
            )
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            await ctx.respond("You either:\n- Used the command on its own\nor\n- The user does not have a banner set")

    @bridge.bridge_command(description="Shows a user's avatar")
    async def avatar(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        if user.avatar:
            embed = discord.Embed (
                title="Avatar",
                description=f"{user.mention}'s Avatar"
            )
            embed.set_image (
                url=user.avatar.url
            )
            await ctx.respond(embed=embed)
        else:
            await ctx.respond("You either:\n- Used the command on its own\nor\n- The user does not have an avatar set")

    @discord.message_command()
    async def getMessageId(self, ctx, message:discord.Message):
        await ctx.respond(f"{message.id}", ephemeral=True)

    @discord.user_command()
    async def getUserId(self, ctx, user:discord.User):
        await ctx.respond(f"{user.id}", ephemeral=True)

    @bridge.bridge_group()
    async def random(self, ctx):
        pass

    @random.command(description="Generate a random number")
    async def number(self, ctx, lower:int, upper:int):
        number = random.randrange(lower, upper)
        await ctx.respond(f"Your random number in range of `{lower}` and `{upper}` is the number `{number}`")

    @random.command(description="Generate a random color")
    async def color(self, ctx):
        await ctx.defer()
        rcolor = lambda: random.randint(0, 255)
        color = "%02X%02X%02X" % (rcolor(), rcolor(), rcolor())
        color16 = int(color, 16)

        embed = discord.Embed(
            title=f"#{color}",
            description=f"Random color generated: {color}",
            color=color16
        )

        await ctx.respond(embed=embed)

    @bridge.bridge_group()
    async def dice(self, ctx):
        pass

    @dice.command(description="Roll a D6")
    async def d6(self, ctx):
        sides = [
            1,
            2,
            3,
            4,
            5,
            6
        ]
        random_index = random.choice(sides)
        embed = discord.Embed(
            title="D6",
            description=f"The result was: `{random_index}`"
        )
        rolling = await ctx.send("🎲 Rolling a D6 ...")
        await asyncio.sleep(2)
        await rolling.delete()
        await ctx.respond(embed=embed)

    @dice.command(description="Roll a D20")
    async def d20(self, ctx):
        sides = [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20
        ]
        random_index = random.choice(sides)

        embed = discord.Embed(
            title="D20",
            description=f"The result was: `{random_index}`"
        )
        rolling = await ctx.send("🎲 Rolling a D20 ...")
        await asyncio.sleep(2)
        await rolling.delete()
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Utils(bot))
