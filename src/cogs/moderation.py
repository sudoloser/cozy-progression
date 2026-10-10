import discord
from datetime import timedelta

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
    @bridge.bridge_command(description="Ban a member")
    # Permission check
    @bridge.has_permissions(ban_members=True)
    # Defining the 'ban' command
    # ---
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
    # ------------------------ TIMEOUT COMMAND ------------------------------
    @bridge.bridge_command(description="Timeout a user")
    @bridge.has_permissions(moderate_members=True)

    async def timeout(self, ctx, member:discord.Member, minutes:int=0, hours:int=0):
        # Define a duration variable with minutes and hours as the measurement
        # ---
        # timedelta includes timers, which is needed for this command.
        duration = timedelta(minutes=minutes, hours=hours)
  
        status = False
        
        # Check if the user did not pass any time
        if minutes==0 and hours==0:
            return await ctx.respond("Duration cannot be 0 hours and 0 minutes!")
        
        # Try to time out user
        try:
            await member.timeout(duration)
            embed = discord.Embed(title="Sucess", description=f"Sucessfully timed out {member.mention} for `{hours} Hours`, and `{minutes} Minutes`.", color=discord.Color.green())
            status = True
        
        # Catch errors
        except Exception as e:
            embed = discord.Embed(title="Failure", description=f"Could not timeout user {member.mention} because of the following error: `{e}`", color=discord.Color.red())
            pass
        await ctx.respond(embed=embed)
        embed2 = discord.Embed(title="Timed out", description=f"You have been timed out for `{hours} Hours`, and `{minutes} Minutes` in {ctx.guild.name}", color=discord.Color.red())
        
        # Check if the timeout went through, and if it did, try to send the user the embed
        if status==True:
            try:
                await member.send(embed=embed2)
            except:
                pass
    # ------------------------ PURGE COMMAND ------------------------------
    @bridge.bridge_command(description="Purge messages")
    @bridge.has_permissions(manage_messages=True)

    async def purge(self, ctx, amount:int, member:discord.Member=None):
        # Check if the user specified another user
        if member!=None:
            # Create a msg list
            msg = []
            # Check all msgs in the channel the command was ran from
            async for m in ctx.channel.history():
                # Break once reached the specified amount
                if len(msg) == amount:
                    break
                # Add msg to the msg list if it matches the specified users ID
                if m.author.id == member.id:
                    msg.append(m)
                    print(f"{member.id}")
                # Delete messages in the msg list
                await ctx.channel.delete_messages(msg)
                # Respond and exit function
                return await ctx.respond(f"{amount} Messages from {member.mention} has been purged.", ephemeral=True)
        await ctx.respond("Purging messages...")
        # Add 2 to compensate for the command message, and bot message
        await ctx.channel.purge(limit=amount+2)
# Setup cog
def setup(bot): 
    # Add cog to the bot
    bot.add_cog(Moderation(bot))