from pysondb import db
import discord
from discord.ext import commands, bridge
from .error_handling import error_embed

db_instance = db.getDb("database.json")

def db_create_user_record(user_id, discord_username=""):
    user_data = {
        "id": 0,
        "user_id": user_id,
        "username": discord_username,
        "lastfm": {
            "username": ""
        }
    }
    db_instance.add(user_data)
    return "success"

class database_helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    async def db_create_user(self, user_id):
        user = await self.bot.fetch_user(user_id)
        try:
            return db_create_user_record(user.id, user.name)
        except Exception as e:
            embed = await error_embed(e, "database_helper")
            return embed
def setup(bot):
    bot.add_cog(database_helper(bot))