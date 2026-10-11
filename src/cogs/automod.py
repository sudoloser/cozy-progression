import discord
from discord.ext import commands, bridge
from datetime import timedelta

class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Define a command group. This allows you to have multiple subcommands under one command without doing trickery 
    # "if()" for every subcommand
    @bridge.bridge_group()
    async def automod(self, ctx):
        pass
    # Define command in the group that sets up the automod
    @automod.command(description="Set up the automod system")
    @bridge.has_permissions(administrator=True)
    async def enable(self, ctx):
        # defer lets the bot think & shows the typing indicator
        await ctx.defer()
        try:
            # This defines the metadata variable from the servers automod. This will be
            # Triggered when a message is blocked
            metadata = discord.AutoModActionMetadata(custom_message="This message was blocked by anti-spam.")
            # Create new moderationr rule
            
            # trigger_type=discord.AutoModTriggerType.spam: When a message is sent, it will check for this.
            await ctx.guild.create_auto_moderation_rule(
                name="Anti-spam", reason="Anti-spam automod",
                enabled=True, 
                # This triggers the check on every message sent
                event_type=discord.AutoModEventType.message_send, 
                # This tells Discord what kind of data to look for.
                # Enables default anti spam filter
                trigger_type=discord.AutoModTriggerType.spam, 
                # Provides extra configuration options or settings specific to the chosen trigger type.
                trigger_metadata=discord.AutoModTriggerMetadata(), 
                # Decides the penalty or action the bot should take when the rule is triggered
                # discord.AutoModActionType.block_message: Tells discord to block the messsages before theyre sent
                # metadata: Points to additionl metadata settings
                actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)]
                )
            await ctx.guild.create_auto_moderation_rule(
                name="Block words", reason="Block words automod",
                enabled=True, 
                # This triggers the check on every message sent
                event_type=discord.AutoModEventType.message_send, 
                # This tells Discord what kind of data to look for.
                # Trigger type is for keywords
                trigger_type=discord.AutoModTriggerType.keyword_preset, 
                # Provides extra configuration options or settings specific to the chosen trigger type.
                trigger_metadata=discord.AutoModTriggerMetadata(presets=[
                    # Blocks sexual content and slurs
                    discord.AutoModKeywordPresetType.sexual_content,
                    discord.AutoModKeywordPresetType.slurs
                ] 
                ), 
                # Decides the penalty or action the bot should take when the rule is triggered
                # discord.AutoModActionType.block_message: Tells discord to block the messsages before theyre sent
                # metadata: Points to additionl metadata settings
                actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)]
                )
            await ctx.guild.create_auto_moderation_rule(
                name="Anti-mention", reason="Anti-mention automod",
                enabled=True, 
                # This triggers the check on every message sent
                event_type=discord.AutoModEventType.message_send, 
                # This tells Discord what kind of data to look for.
                # Enables default anti spam filter
                trigger_type=discord.AutoModTriggerType.mention_spam, 
                # Provides extra configuration options or settings specific to the chosen trigger type.
                trigger_metadata=discord.AutoModTriggerMetadata(
                    mention_total_limit=7
                ), 
                # Decides the penalty or action the bot should take when the rule is triggered
                # discord.AutoModActionType.block_message: Tells discord to block the messsages before theyre sent
                # metadata: Points to additionl metadata settings
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
                # This triggers the check on every message sent
                event_type=discord.AutoModEventType.message_send, 
                # This tells Discord what kind of data to look for.
                # Enables default anti spam filter
                trigger_type=discord.AutoModTriggerType.spam, 
                # Provides extra configuration options or settings specific to the chosen trigger type.
                trigger_metadata=discord.AutoModTriggerMetadata(), 
                # Decides the penalty or action the bot should take when the rule is triggered
                # discord.AutoModActionType.block_message: Tells discord to block the messsages before theyre sent
                # metadata: Points to additionl metadata settings
                actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)]
                )
                await ctx.guild.create_auto_moderation_rule(
                name="Block words", reason="Block words automod",
                enabled=True, 
                # This triggers the check on every message sent
                event_type=discord.AutoModEventType.message_send, 
                # This tells Discord what kind of data to look for.
                # Trigger type is for keywords
                trigger_type=discord.AutoModTriggerType.keyword_preset, 
                # Provides extra configuration options or settings specific to the chosen trigger type.
                trigger_metadata=discord.AutoModTriggerMetadata(presets=[
                    # Blocks sexual content and slurs
                    discord.AutoModKeywordPresetType.sexual_content,
                    discord.AutoModKeywordPresetType.slurs
                ] 
                ), 
                # Decides the penalty or action the bot should take when the rule is triggered
                # discord.AutoModActionType.block_message: Tells discord to block the messsages before theyre sent
                # metadata: Points to additionl metadata settings
                actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)]
                )
                await ctx.guild.create_auto_moderation_rule(
                name="Anti-mention", reason="Anti-mention automod",
                enabled=True, 
                # This triggers the check on every message sent
                event_type=discord.AutoModEventType.message_send, 
                # This tells Discord what kind of data to look for.
                # Enables default anti spam filter
                trigger_type=discord.AutoModTriggerType.mention_spam, 
                # Provides extra configuration options or settings specific to the chosen trigger type.
                trigger_metadata=discord.AutoModTriggerMetadata(
                    mention_total_limit=7
                ), 
                # Decides the penalty or action the bot should take when the rule is triggered
                # discord.AutoModActionType.block_message: Tells discord to block the messsages before theyre sent
                # metadata: Points to additionl metadata settings
                actions=[discord.AutoModAction(discord.AutoModActionType.block_message, metadata)]
                )
                await ctx.respond("Successfully enabled autmod")
            except Exception as e:
                await ctx.respond(f"Failed to enable automod: `{e}`")

def setup(bot):
    bot.add_cog(Automod(bot))