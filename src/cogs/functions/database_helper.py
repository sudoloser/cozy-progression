from pysondb import db
import discord
from discord.ext import commands, bridge
from .error_handling import error_embed

db_instance = db.getDb("database.json")

class database_helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    async def db_create_user(self, user_id):
        user = await self.bot.fetch_user(user_id)
        try:
            user_data = {
                "id": 0,
                "user_id": user.id,
                "username": user.name,
                "lastfm": {
                    "username": ""
                }
            }

            db_instance.add(user_data)
            return "success"
        except Exception as e:
            embed = await error_embed(e, "database_helper")
            return embed
def setup(bot):
    bot.add_cog(database_helper(bot))