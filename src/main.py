# Imports

import discord
import asyncio
import random
import time
import aiohttp
import os
from discord.ext.pages import Paginator, Page

# Import Discord Gateway Bridge\
from discord.ext import bridge, commands
# Import load_dotenv
from dotenv import load_dotenv

# Load dotenv for BOT_TOKEN
load_dotenv()

# Create and setup event listener
# in a looped background task so that the bot doesnt freeze.
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Define bot class
class CozyProgression(bridge.Bot):
    # Load bot token
    TOKEN = os.getenv("BOT_TOKEN")
    # Define intents
    intents = discord.Intents.all()
    # Disable help command
    help_command = None

# Define bot client with prefix and intents
client = CozyProgression(intents=CozyProgression.intents, command_prefix="!", help_command=CozyProgression.help_command)

# Error Handling
# Define a client event with context & exceptions
@client.event
async def on_application_command_error(ctx:discord.ApplicationContext, error:discord.DiscordException):
    # If the error is commands.CommandOnCooldown, then respond with a message
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond("This command is currently on cooldown.")
    # If the error is about missing permissions, then respond with a message
    elif isinstance(error, commands.MissingPermissions):
        await ctx.respond("You do not have the required permissions to run this command.")
    # If the error is about the bot having missing permissions, then respond with a message
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.respond("I do not have enough permissions to do this action!")
    # If the error is about an nsfw channel being required to run the command, respond with a message
    elif isinstance(error, commands.NSFWChannelRequired):
        await ctx.respond("This command can only be used in an NSFW channel.")
    # All other, respond with error
    else:
       embed = discord.Embed(
        title="Failure", 
        description="This action could not be completed with the following error:", 
        color=discord.Color.red
       )

       embed.add_field(
        name="Error",
        value=f"`{error}`"
       )

       await ctx.respond(embed=embed)

# Listen for all events
@client.listen()
async def on_ready():
    print(f"Logged in as: {client.user.name}")
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="!help"
        )
    )

# Define "Ping, pong!" command in the bridge
@client.bridge_command(description="Ping, pong!")
# Define "Ping, pong!" command with context "(ctx)"
async def ping(ctx):
    # Defines latency variable
    # ---
    # str() converts the following value to a String
    # ---
    # client.latency calls the gateway and calculates
    # how long it takes for the machine to send and
    # recieve data
    # ---
    # .split() removes chars from the specified index, [1:3] extracts index 1 through 3
    # and returns that value to the variable
    latency = (str(client.latency)).split('.')[1][1:3]

    # Return the command with f string.
    # This is the quilivent of the following snipped of code in JS:
    # return "Pong! Bot replied in ${latency}";
    await ctx.respond(f"Pong! Bot replied in {latency} ms")

# Define pages list
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
                description="**/links\n/download\n/ram\n/crash**"
            )
        ],
    ),
    Page(
        embeds = [
            discord.Embed(
                title="Moderation",
                description="**/ban\n/kick\n/timeout\n/purge\n/nick\n/role\n/automod enable**"
            )
        ],
    ),
    Page(
        embeds = [
            discord.Embed(
                title="Utilities",
                description="**/changelog\n/mod\n/banner\n/avatar\n/random number\n/random color**"
            )
        ],
    ),
]

@client.bridge_command(description="Information about the bot")
async def help(ctx):
    paginator = Paginator(pages=pages)

    # Tries sending the interaction response. This will only work
    # if its a slash command
    try: await paginator.respond(ctx.interaction)
    # For prefix commands, we send it as a regluar message
    except: await paginator.send(ctx)

# Check all files in the cogs directory
for filename in os.listdir("./cogs"):
    # Check if file name is a python file, if it is:
    if filename.endswith(".py"):
        # Then load extension without the ".py" 
        # cogs. loads the cog into our bot
        # {filename[:-3]} removes the last 3 chars from the filename (the ".py")
        client.load_extension(f"cogs.{filename[:-3]}")
        print(f"Load {filename}")

# Define main process
async def main_bot():
    print("Bot is starting...")
    
    # Start the bot with the token
    await client.start(CozyProgression().TOKEN)

# This checks if the Python module name is "main,"
# which only happens if the file is being ran directly. 
# If the file is not being ran directly, the bot will not start
if __name__ == "__main__":
    # Tells the event loop to keep running until everything else in the bot is done running
    loop.run_until_complete(asyncio.gather(main_bot()))
