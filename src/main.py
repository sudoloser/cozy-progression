import discord
import asyncio
import random
import time
import aiohttp
import os
from discord.ext.pages import Paginator, Page

from .cogs import functions
from .cogs.functions import error_handling
from .cogs.function.error_handling import error_embed

from discord.ext import bridge, commands
from dotenv import load_dotenv

load_dotenv()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

class CozyProgression(bridge.Bot):
    TOKEN = os.getenv("BOT_TOKEN")
    intents = discord.Intents.all()
    help_command = None

client = CozyProgression(intents=CozyProgression.intents, command_prefix="!", help_command=CozyProgression.help_command)

@client.event
async def on_application_command_error(ctx:discord.ApplicationContext, error:discord.DiscordException):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond("This command is currently on cooldown.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.respond("You do not have the required permissions to run this command.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.respond("I do not have enough permissions to do this action!")
    elif isinstance(error, commands.NSFWChannelRequired):
        await ctx.respond("This command can only be used in an NSFW channel.")
    else:
        embed = await error_embed(ctx, e)

        await ctx.respond(embed=embed)

client.persistent_views_added = False

class Ticket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.select(
        custom_id = "ticketing-1",
        placeholder = "Open a ticket",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="Report",
                description="Report a user"
            ),
            discord.SelectOption(
                label="Suggestion",
                description="Suggest an improvement for the server"
            ),
            discord.SelectOption(
                label="Mod request",
                description="Request a mod to be added to Cozy Progression"
            ),
            discord.SelectOption(
                label="Other",
                description="All other"
            )
        ]
    )
    async def ticketCallback(self, select, interaction):
        maintainers_roleid = 1558926793333940344
        role = interaction.guild.get_role(1558459120124694691)

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, embed_links=True),
            interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            
            role: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                embed_links=True
            )
        }

        # Channel ends up like "ticket-x.v.c."
        channel = await interaction.guild.create_text_channel(f"ticket-{interaction.user.name}", overwrites=overwrites, reason=f"Ticket for {interaction.user.name}")
        await interaction.response.send_message(f"Ticket opened at {channel.mention}", ephemeral=True)

        if select.values[0]=="Report":
            embed = discord.Embed(
                title="Report a user",
                description=f"Welcome to your ticket, {interaction.user.mention}. The support team will be with you shortly.",
                color=discord.Color.green(),

            )
            embed.add_field(
                name="What we need from you:",
                value="1. The user's username or user id\n2. A valid reason for the report\n3. A link to the message.\n>Note:\n>If the message was deleted, you may send us a screenshot."
            )
            await channel.send(embed=embed, view=CloseTicket())
        elif select.values[0]=="Mod request":
            embed = discord.Embed(
                title="Mod request",
                description=f"Welcome to your ticket, {interaction.user.mention}. The maintainer team will be with you shortly.",
                color=discord.Color.green(),

            )
            embed.add_field(
                name="What we need from you:",
                value="1. The mod's name, Modrinth **and** CurseForge link.\n> If the mod is not on CurseForge, or if the mod is only on CurseForge, it will be added as a **recommended mod**. Recommended mods are **NOT** included in the modpack, but are mentioned in the description as recommended.\n2. Why it would fit in with either cozy or progression"
            )
            await channel.send(f"{interaction.user.mention}, <@&{maintainers_roleid}>", embed=embed, view=CloseTicket())
        elif select.values[0]=="Suggestion":
            embed = discord.Embed(
                title="Server suggestion",
                description=f"Welcome to your ticket, {interaction.user.mention}. The server managers will be with you shortly.",
                color=discord.Color.green(),

            )
            await channel.send(embed=embed, view=CloseTicket())
        else:
            embed = discord.Embed(
                title="Other",
                description=f"Welcome to your ticket, {interaction.user.mention}. The support team will be with you shortly.",
                color=discord.Color.green(),

            )
            await channel.send(embed=embed, view=CloseTicket())

class CloseTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(
        label="Close ticket",
        style=discord.ButtonStyle.danger,
        emoji="🔒",
        custom_id="closeticket"
    )
    async def callback(self, button, interaction):
        await interaction.response.send_message("Closing this ticket...")
        await asyncio.sleep(2)
        await interaction.channel.delete()

@client.listen()
async def on_ready():
    print(f"Logged in as: {client.user.name}")
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="!help"
        )
    )

    # Persistent views must be re-registered on every restart
    if not client.persistent_views_added:
        client.add_view(Ticket())
        client.add_view(CloseTicket())
        client.persistent_views_added = True

@client.bridge_command(description="Ping, pong!")
async def ping(ctx):
    latency = (str(client.latency)).split('.')[1][1:3]

    await ctx.respond(f"Pong! Bot replied in {latency} ms")

pages = [
    Page(
        embeds=[
            discord.Embed(
                title="Cozy Progression Bot",
                description="Cozy Progression Bot is a multi purpose bot built with the Cozy Progression modpack in mind.",
            )
        ],
    ),
    Page(
        embeds = [
            discord.Embed(
                title="General",
                description="**/links\n/source\n/download\n/ram\n/crash**"
            )
        ],
    ),
    Page(
        embeds = [
            discord.Embed(
                title="Moderation",
                description="**/ban\n/kick\n/timeout\n/purge\n/nick\n/role\n/automod enable\n/ticketing\n/honeypot**"
            )
        ],
    ),
    Page(
        embeds = [
            discord.Embed(
                title="Utilities",
                description="**/changelog\n/mod\n/banner\n/avatar\n/random number\n/random color\n/dice d6\n/dice d20**"
            )
        ],
    ),
    Page(
        embeds = [
            discord.Embed(
                title="Fun",
                description="**/8ball**"
            )
        ]
    )
]

@client.bridge_command(description="Information about the bot")
async def help(ctx):
    paginator = Paginator(pages=pages)

    # Slash commands use interaction response, prefix commands use regular send
    try: await paginator.respond(ctx.interaction)
    except: await paginator.send(ctx)

@client.bridge_command(description="Start the ticketing system")
@bridge.has_permissions(administrator=True)
async def ticketing(ctx):
    embed = discord.Embed(
        title="Create a ticket",
        description="Choose a category below for your ticket",
        color=discord.Color.green()
    )
    await ctx.respond("Successfully started ticketing system", ephemeral=True)
    await ctx.send(embed=embed, view=Ticket())

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")
        print(f"Load {filename}")

async def main_bot():
    print("Bot is starting...")
    await client.start(CozyProgression().TOKEN)

if __name__ == "__main__":
    loop.run_until_complete(asyncio.gather(main_bot()))
