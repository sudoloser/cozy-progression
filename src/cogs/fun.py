import discord
import random
import asyncio

from discord.ext import bridge, commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
     # ------------- 8BALL COMMAND ----------------
    @bridge.bridge_command(description="Ask an eightball!")
    async def ball(self, ctx, *, question):
        feelings = [
            "affirmative",
            "negative",
            "neutral",
            "funny"
        ]
        responses_affirmative = [
            "Yes",
            "Very likely",
            "Extremely likely",
            "Without a doubt",
            "It is certain",
            "Signs point to yes",
            "As I see it, yes",
            "You may rely on it",
            "Outlook good",
            "Definitely",
            "Affirmative",
            "Count on it",
            "All signs say go",
            "You bet",
            "The stars align in your favor",
        ]
        responses_neutral = [
            "Reply hazy, try again",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
            "Unclear at this time",
            "The future is cloudy",
            "Ask a different question",
            "Indecisive winds blow",
            "Time will tell",
            "It remains to be seen",
            "Consult your intuition",
            "The mists are too thick",
            "Patience is required",
            "Ask someone else",
        ]
        responses_negative = [
            "Don't count on it",
            "My reply is no",
            "Outlook not so good",
            "Very unlikely",
            "Extremely doubtful",
            "Negative",
            "Not in a million years",
            "Forget about it",
            "The answer is no",
            "Unfavorable outcome",
            "Don't hold your breath",
            "Not looking good",
            "Hard pass",
            "Avoid that path",
            "The cosmos says no",
        ]
        responses_funny = [
            "Well, that's maybe a yes, that's maybe a no, but quite frankly, i do not know.",
            "Ask me if I care",
            "Only if you do a little dance",
            "Error 404: Answer not found",
            "Does a bear sleep in the woods?",
            "Outlook looks suspiciously good",
        ]
        embed = discord.Embed(
            title = "placeholder",
            description = "You shouldn't be seeing this"
        )
        feeling = random.choice(feelings)
        
        if feeling == "affirmative":
            response = random.choice(responses_affirmative)

            embed = discord.Embed(
                title="The 8ball has spoken!",
                description=f"The 8ball has decided: `{response}`",
                color = discord.Color.green()
            )
            embed.add_field(
                name="Your question:",
                value=question
            )
        elif feeling == "neutral":
            response = random.choice(responses_neutral)

            embed = discord.Embed(
                title="The 8ball has spoken!",
                description=f"The 8ball has decided: `{response}`",
                color = discord.Color.yellow()
            )
            embed.add_field(
                name="Your question:",
                value=question
            )
        elif feeling == "negative":
            response = random.choice(responses_negative)

            embed = discord.Embed(
                title="The 8ball has spoken!",
                description=f"The 8ball has decided: `{response}`",
                color = discord.Color.red()
            )
            embed.add_field(
                name="Your question:",
                value=question
            )
        elif feeling == "funny":
            response = random.choice(responses_funny)

            embed = discord.Embed(
                title="The 8ball has spoken!",
                description=f"The 8ball has decided: `{response}`",
                color = discord.Color.green()
            )
            embed.add_field(
                name="Your question:",
                value=question
            )
        await ctx.send("The 8ball is deciding...")
        await asyncio.sleep(2)

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))
