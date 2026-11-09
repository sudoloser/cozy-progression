import re
import hashlib

from .functions.hash import get_url_hash
from .functions.discbl import search_hash

import discord
from discord.ext import bridge, commands

class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Honeypot channel: any user message here is treated as a compromised account
        channel_id = 1558806012478226432
        invite_link = "https://discord.gg/VNjED7ucfD"
        guild = message.guild
        user = message.author
        
        # DiscBL
        supported_extensions = ('.gif', '.png')
        url_pattern = r'https?://[^\s>]+'

        if message.channel.id == channel_id:
            if user == self.bot.user:
                return
            elif user.guild_permissions.administrator:
                return
            else:
                try:
                    embed = discord.Embed(
                        title = "Kicked",
                        description = f"You have been **kicked** from {guild.name}.",
                        color = discord.Color.red()
                    )
                    embed.add_field(
                        name = "Reason",
                        value = "You messaged in the honey pot. This indicates that you may have been hacked."
                    )
                    embed.add_field(
                        name = "What to do now?",
                        value = "Assuming you didn't do this on purpose, please:\n1. change your password\n2. run a full offline windows defender scan\nand then you can join back."
                    )
                    embed.add_field(
                        name="Invite",
                        value=f"[Invite link]({invite_link})"
                    )
                    
                    user_msgs = []
                    for channel in guild.text_channels:
                        await channel.purge(limit=5, check=lambda msg: msg.author == user)

                    await user.send(embed=embed)
                    await user.kick(reason="Honey pot")
                except Exception as e:
                    print(e)
        if message.content:
            found_urls = re.findall(url_pattern, message.content)

            for url in found_urls:
                clean_url = url.rstrip('.,;!?')

                if clean_url.lower().endswith(supported_extensions):
                    print(f"Found media URL in text: {clean_url}")

                    file_hash = await get_url_hash(clean_url)

                    found = await search_hash(file_hash)

                    if found == True:
                        await message.delete()
def setup(bot):
    bot.add_cog(Listener(bot))
