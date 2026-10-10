import discord

# We import commands here because the cog system is a subclass of commands
from discord.ext import bridge, commands

class Moderation(commands.Cog):
    # Cog instructor. Links the command to our main bot instance so it knows what bot it belongs to
    def __init__(self, bot):
        self.bot = bot
    # ------------------------ Kick COMMAND ------------------------------
    # Bridge dectorers. Allows us to use both prefix and slash
    @bridge.bridge_command(description="Kick a member")
    # Permission check
    @bridge.has_permissions(kick_members=True)
    # Defining the 'kick' command
    # ---
    # ctx give infomation about who sent it, where it was sent, etc
    # member:discord.Member requires a member as the first option
    # reason:str="" allows for giving a reason, if no reason provided,
    # it falls back to "No reason provided"
    async def kick(self, ctx, member:discord.Member, reason:str="No reason provided"):
        # Allows the bot to think (to bypass timeouts), and shows the typing indicator
        await ctx.defer()
        # Check if the specified user has admin, if so, do not kick them. 
        if member.guild_permissions.administrator:
            # allows you to kick bots by passing the if check
            if member.bot:
                pass
            # Return failure response in an embed
            else:
                return await ctx.respond(embed=discord.Embed(title="Failure", description="You can't kick another admin", color=discord.Color.red()))
            # Try to kick user
            try:
                try:
                    # Define kickembed embed
                    kickembed = discord.Embed(title="Kick", description=f"You have been kicked from {ctx.guild.name}", color=discord.Color.red())
                    # Send the member the kick embed
                    await member.send(embed=kickembed)
                
                # If the bot can not send the user a message for whatever reason, we pass and move on to kicking
                except:
                    pass
                # Kick member with reason
                await member.kick(reason=reason)
                # Define success embed
                embed = discord.Embed(title="Sucess", description=f"Sucessfully kicked member,'{member.name}'.", color=discord.Color.green())
                # Send success embed
                await ctx.respond(embed=embed)
            # Catch errors and asign them to the value of "e"
            except Exception as e:
                # Define failure embed with error
                embed = discord.Embed(title="Failure", description=f"Failed to kick, '{member.name}'. Error: `{e}`.", color=discord.Color.red())
                # Send faiure embed
                await ctx.respond(embed=embed)
    # ------------------------ BAN COMMAND ------------------------------
    # Bridge dectorers. Allows us to use both prefix and slash
    @bridge.bridge_command(description="Ban a member")
    # Permission check
    @bridge.has_permissions(kick_members=True)
    # Defining the 'ban' command
    # ---
    # ctx give infomation about who sent it, where it was sent, etc
    # member:discord.Member requires a member as the first option
    # reason:str="" allows for giving a reason, if no reason provided,
    # it falls back to "No reason provided"
    async def ban(self, ctx, member:discord.Member, reason:str="No reason provided"):
        # Allows the bot to think (to bypass timeouts), and shows the typing indicator
        await ctx.defer()
        # Check if the specified user has admin, if so, do not kick them. 
        if member.guild_permissions.administrator:
            # allows you to kick bots by passing the if check
            if member.bot:
                pass
            # Return failure response in an embed
            else:
                return await ctx.respond(embed=discord.Embed(title="Failure", description="You cannot ban another admin", color=discord.Color.red()))
            # Try to kick user
            try:
                try:
                    # Define banembed embed
                    banembed = discord.Embed(title="Kick", description=f"You have been banned from {ctx.guild.name}", color=discord.Color.red())
                    # Send the member the kick embed
                    await member.send(embed=banembed)
                
                # If the bot can not send the user a message for whatever reason, we pass and move on to kicking
                except:
                    pass
                # Ban member with reason
                await member.ban(reason=reason)
                # Define success embed
                embed = discord.Embed(title="Sucess", description=f"Sucessfully banned member,'{member.name}'.", color=discord.Color.green())
                # Send success embed
                await ctx.respond(embed=embed)
            # Catch errors and asign them to the value of "e"
            except Exception as e:
                # Define failure embed with error
                embed = discord.Embed(title="Failure", description=f"Failed to ban, '{member.name}'. Error: `{e}`.", color=discord.Color.red())
                # Send faiure embed
                await ctx.respond(embed=embed)
# Setup cog
def setup(bot): 
    # Add cog to the bot
    bot.add_cog(Moderation(bot))