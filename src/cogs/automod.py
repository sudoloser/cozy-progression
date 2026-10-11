import discord
from discord.ext import commands, bridge
from datetime import timedelta

class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_group()
    async def automod(self, ctx):
        pass

    @automod.command(description="Set up the automod system")
    @bridge.has_permissions(administrator=True)
    async def enable(self, ctx):
        await ctx.defer()
        try:
            metadata = discord.AutoModActionMetadata(custom_message="This message was blocked by anti-spam.")
            await ctx.guild.create_auto_moderation_rule(
                name="Anti-spam", reason="Anti-spam automod",
                enabled=True,
                event_type=discord.AutoModEventType.message_send,
                trigger_type=discord.AutoModTriggerType.spam,
                trigger_metadata=discord.AutoModTriggerMetadata(),
                actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)]
                )
            await ctx.guild.create_auto_moderation_rule(
                name="Block words", reason="Block words automod",
                enabled=True,
                event_type=discord.AutoModEventType.message_send,
                trigger_type=discord.AutoModTriggerType.keyword_preset,
                trigger_metadata=discord.AutoModTriggerMetadata(presets=[
                    discord.AutoModKeywordPresetType.sexual_content,
                    discord.AutoModKeywordPresetType.slurs
                ]
                ),
                actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)]
                )
            await ctx.guild.create_auto_moderation_rule(
                name="Anti-mention", reason="Anti-mention automod",
                enabled=True,
                event_type=discord.AutoModEventType.message_send,
                trigger_type=discord.AutoModTriggerType.mention_spam,
                trigger_metadata=discord.AutoModTriggerMetadata(
                    mention_total_limit=7
                ),
                actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)]
                )
            await ctx.respond("Automod enabled successfully")
        except:
            try:
                rulelist = await ctx.guild.fetch_auto_moderation_rules()
                for rule in rulelist:
                    await rule.delete()
                await ctx.guild.create_auto_moderation_rule(
                name="Anti-spam", reason="Anti-spam automod",
                enabled=True,
                event_type=discord.AutoModEventType.message_send,
                trigger_type=discord.AutoModTriggerType.spam,
                trigger_metadata=discord.AutoModTriggerMetadata(),
                actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)]
                )
                await ctx.guild.create_auto_moderation_rule(
                name="Block words", reason="Block words automod",
                enabled=True,
                event_type=discord.AutoModEventType.message_send,
                trigger_type=discord.AutoModTriggerType.keyword_preset,
                trigger_metadata=discord.AutoModTriggerMetadata(presets=[
                    discord.AutoModKeywordPresetType.sexual_content,
                    discord.AutoModKeywordPresetType.slurs
                ]
                ),
                actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)]
                )
                await ctx.guild.create_auto_moderation_rule(
                name="Anti-mention", reason="Anti-mention automod",
                enabled=True,
                event_type=discord.AutoModEventType.message_send,
                trigger_type=discord.AutoModTriggerType.mention_spam,
                trigger_metadata=discord.AutoModTriggerMetadata(
                    mention_total_limit=7
                ),
                actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)]
                )
                await ctx.respond("Successfully enabled automod")
            except Exception as e:
                await ctx.respond(f"Failed to enable automod: `{e}`")

def setup(bot):
    bot.add_cog(Automod(bot))
