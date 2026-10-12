import discord
from datetime import timedelta

from .functions import error_handling
from .functions.error_handling import error_embed

from discord.ext import bridge, commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(description="Kick a member")
    @bridge.has_permissions(kick_members=True)
    async def kick(self, ctx, member:discord.Member, reason:str="No reason provided"):
        await ctx.defer()

        # Bots are exempt from the admin protection so they can still be kicked
        if member.guild_permissions.administrator and not member.bot:
            return await ctx.respond(embed=discord.Embed(title="Failure", description="You can't kick another admin", color=discord.Color.red()))
        try:
            try:
                kickembed = discord.Embed(title="Kick", description=f"You have been kicked from {ctx.guild.name}", color=discord.Color.red())
                await member.send(embed=kickembed)

            except:
                pass
            await member.kick(reason=reason)
            embed = discord.Embed(title="Success", description=f"Successfully kicked member,'{member.name}'.", color=discord.Color.green())
            await ctx.respond(embed=embed)
        except Exception as e:
            embed = await error_embed(ctx, e)
            await ctx.respond(embed=embed)

    @bridge.bridge_command(description="Ban a member")
    @bridge.has_permissions(ban_members=True)
    async def ban(self, ctx, member:discord.Member, reason:str="No reason provided"):
        await ctx.defer()

        # Bots are exempt from the admin protection so they can still be banned
        if member.guild_permissions.administrator and not member.bot:
            return await ctx.respond(embed=discord.Embed(title="Failure", description="You cannot ban another admin", color=discord.Color.red()))
        try:
            try:
                embed = discord.Embed(title="Banned", description=f"You have been banned from {ctx.guild.name}", color=discord.Color.red())
                await member.send(embed=embed)

            except:
                pass
            await member.ban(reason=reason)
            embed = discord.Embed(title="Success", description=f"Successfully banned member,'{member.name}'.", color=discord.Color.green())
            await ctx.respond(embed=embed)
        except Exception as e:
            embed = await error_embed(ctx, e)
            await ctx.respond(embed=embed)

    @bridge.bridge_command(description="Unban a member")
    @bridge.has_permissions(ban_members=True)

    async def unban(self, ctx, userid, reason:str="No reason provided"):
        try:
            user = await self.bot.fetch_user(int(userid))
            guild = ctx.guild
            await guild.unban(user)

            embed = discord.Embed(
                title="Success",
                description=f"Successfully unbanned {user.name}",
                color = discord.Color.green()
            )

            await ctx.respond(embed=embed)

            try:
                embed = discord.Embed(
                    title="Unbanned",
                    description=f"You have been unbanned from {ctx.guild.name}.",
                    color=discord.Color.green()
                )
                embed.add_field(
                    name="Reason",
                    value=f"{reason}",
                )
                await user.send(embed=embed)
            except:
                pass
        except Exception as e:
            embed = await error_embed(ctx, e)
            await ctx.respond(embed=embed)

    @bridge.bridge_command(description="Timeout a user")
    @bridge.has_permissions(moderate_members=True)

    async def timeout(self, ctx, member:discord.Member, minutes:int=0, hours:int=0):
        duration = timedelta(minutes=minutes, hours=hours)

        status = False

        if minutes==0 and hours==0:
            return await ctx.respond("Duration cannot be 0 hours and 0 minutes!")

        try:
            await member.timeout(duration)
            embed = discord.Embed(title="Success", description=f"Successfully timed out {member.mention} for `{hours} Hours`, and `{minutes} Minutes`.", color=discord.Color.green())
            status = True

        except Exception as e:
            embed = await error_embed(ctx, e)
            pass
        await ctx.respond(embed=embed)
        embed2 = discord.Embed(title="Timed out", description=f"You have been timed out for `{hours} Hours`, and `{minutes} Minutes` in {ctx.guild.name}", color=discord.Color.red())

        if status==True:
            try:
                await member.send(embed=embed2)
            except:
                pass

    @bridge.bridge_command(description="Purge messages")
    @bridge.has_permissions(manage_messages=True)

    async def purge(self, ctx, amount:int, member:discord.Member=None):
        if member!=None:
            msg = []
            try:
                async for m in ctx.channel.history():
                    if len(msg) == amount:
                        break
                    if m.author.id == member.id:
                        msg.append(m)
                await ctx.channel.delete_messages(msg)
                return await ctx.respond(f"{amount} Messages from {member.mention} has been purged.", ephemeral=True)
            except Exception as e:
                embed = await error_embed(ctx, e)
                embed.add_field(
                    name="Requested user",
                    value=f"{member.mention}"
                )
                return await ctx.respond(embed=embed, ephemeral=True)
        await ctx.respond("Purging messages...")
        # +2 covers the command message and the bot's own reply
        await ctx.channel.purge(limit=amount+2)
        message = await ctx.send(f"Purged {amount} messages.\n-# Deleting in 2 seconds")
        await message.delete()

    @bridge.bridge_command(description="Nukes a channel")
    @bridge.has_permissions(manage_channels=True)
    
    async def nuke(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            await ctx.respond("Please specifiy a channel to nuke.")
        else:
            try:
                await ctx.defer()
                await ctx.send("Deleting channel...")

                cloned_channel = await channel.clone(name=f"{channel.name}")
                await channel.delete()

                await cloned_channel.send(f"Successfully nuked channel {ctx.author.mention}")
            except Exception as e:
                embed = await error_embed(ctx, e)
                await ctx.respond(embed=embed)
    @bridge.bridge_command(description="Send the 'do not message' warning")
    @bridge.has_permissions(administrator=True)
    
    async def honeypot(self, ctx):
        embed = discord.Embed(
            title="Honeypot",
            description="DO NOT SEND MESSAGES IN THIS CHANNEL!",
            color=discord.Color.red()
        )
        embed.add_field(
            name="What will happen if i do?",
            value="You will get kicked. That's it.",
            inline=False
        )
        embed.add_field(
            name="Why have this",
            value="In practice, it helps defend against compromised accounts by kicking them and deleting their messages.",
            inline=False
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
