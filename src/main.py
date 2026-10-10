# Imports

import discord
import asyncio
import random
import time
import aiohttp
import os

# Import Discord Gateway Bridge\
from discord.ext import bridge
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

# Define bot client with prefix, intents, and RPC
client = CozyProgression(intents=CozyProgression.intents, command_prefix="!", activity=discord.Game(name="!commands"))

# Listen for all events
@client.listen()
async def on_ready():
    print(f"Logged in as: {client.user.name}")

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
