import discord
from datetime import timedelta

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
            embed = discord.Embed(title="Failure", description=f"Failed to kick, '{member.name}'. Error: `{e}`.", color=discord.Color.red())
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
            embed = discord.Embed(title="Failure", description=f"Failed to ban, '{member.name}'. Error: `{e}`.", color=discord.Color.red())
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
            embed = discord.Embed(
                title="Failure",
                description=f"Failed to unban {userid} with the following error:",
                color=discord.Color.red()
            )
            embed.add_field(
                name="Error",
                value=f"{e}"
            )
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
            embed = discord.Embed(title="Failure", description=f"Could not timeout user {member.mention} because of the following error: `{e}`", color=discord.Color.red())
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
        embed = discord.Embed(
            title="Failure",
            description="Could not delete messages, please check the following error:",
            color=discord.Color.red()
        )
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
                embed.add_field(
                    name="Error",
                    value=f"`{e}`",
                )
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

def setup(bot):
    bot.add_cog(Moderation(bot))
