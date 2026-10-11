import discord
from discord.ext import bridge, commands

class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Honeypot channel: any human message here is treated as a compromised account
        channel_id = 1558806012478226432
        invite_link = "https://discord.gg/VNjED7ucfD"
        guild = message.guild
        user = message.author

        if message.channel.id == channel_id:
            if user == self.bot.user:
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
                    await message.delete()
                    await user.send(embed=embed)
                    await user.kick(reason="Honey pot")
                except Exception as e:
                    print(e)

def setup(bot):
    bot.add_cog(Listener(bot))
