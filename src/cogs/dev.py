import discord

from .functions import error_handling
from .functions.error_handling import error_embed

from .functions.color_from_image import colorFromImage

from .functions.lastfm_api import lastFmApi

from .functions.database_helper import database_helper

from discord.ext import bridge, commands

from pysondb import db

db_instance = db.getDb("database.json")

class dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_group()
    async def test(self, ctx):
        pass

    @test.command(description="Test error handling")
    async def error_handling(self, ctx):
        test = "Test passed!"
        try:
            embed_obj = await error_embed(ctx, test)
            await ctx.respond(embed=embed_obj)
        except Exception as e:
            embed = discord.Embed(
                title="Failure", 
                description="Failed to complete action due to the following:"
            )
            embed.add_field(
                name="Error",
                value=e
            )

            await ctx.respond(embed=embed)
    
    @test.command(description="Test extracting primary image from url")
    async def colorfromimage(self, ctx, image_url: str = "https://fastly.picsum.photos/id/651/536/354.jpg?hmac=uH5tft1mZIFbtwn8QSl34B-BJIAJqENj0Oy6TNodX2c", format: str = "rgb"):
        try:
            await ctx.defer()
            
            if format == "rgb":
                color = await colorFromImage(image_url, "rgb")
            elif format == "hls":
                color = await colorFromImage(image_url, "hls")
            elif format == "hsv":
                color = await colorFromImage(image_url, "hsv")
            elif format == "hex":
                color = await colorFromImage(image_url, "hex")

            if format == "hex":
                colorint = int(color, 16)
                embed = discord.Embed(
                    title="Color Test",
                    description="Passed the color test",
                    color=colorint
                )
            else:
                embed = discord.Embed(
                    title="Color Test",
                    description="Passed the color test",
                )
            embed.set_image (
                url=image_url
            )
            embed.add_field(
                name="Color",
                value=color
            )

            await ctx.respond(embed=embed)
        except Exception as e:
            embed = await error_embed(e)
            await ctx.respond(embed=embed)

    @test.command(description="Test LastFM api function")
    async def lastfm(self, ctx, username: str = None, subcommand: str = None):
        await ctx.defer()
        user = ctx.author

        subcommand = subcommand.lower() if subcommand is not None else None

        user_body = None
        try: 
            users = db_instance.getByQuery({"user_id": user.id})
            if users:
                user_body = users[0]
        except:
            pass

        if subcommand == None:
            if user_body and username == None:
                username = user_body["lastfm"]["username"]
            if username == None:
                e = "Please provide a username, or set one by using !test lastfm [username] set"
                embed = await error_embed(e)
                await ctx.respond(embed=embed)
            else:
                try:
                    artist, trackName, image, nowPlaying = await lastFmApi(username)
                    
                    color = await colorFromImage(image, "hex")
                    color = int(color, 16)

                    embed = discord.Embed(
                        title="Lastfm",
                        color=color
                    )
                    embed.add_field(
                        name="Track",
                        value=trackName
                    )
                    embed.add_field(
                        name="Artist",
                        value=artist
                    )
                    embed.set_image(
                        url=image
                    )
                    if nowPlaying == "true":
                        embed.set_footer(
                            text="Now Playing"
                        )
                    await ctx.respond(embed=embed)

                except Exception as e:
                    embed = await error_embed(e)
                    await ctx.respond(embed=embed)      
        elif subcommand == "set":
            if username == None:
                e = "Please provide a username by using !test lastfm [username] set"
                embed = await error_embed(e)
                await ctx.respond(embed=embed)
            else:
                if user_body:
                    if "lastfm" not in user_body:
                        user_body["lastfm"] = {}

                    user_body["lastfm"]["username"] = username

                    db_instance.update({"user_id": user.id}, user_body)
                    await ctx.respond("Set username successfully!")
                else:
                    response = await database_helper.db_create_user(self, user.id)
                    if isinstance(response, discord.Embed):
                        return await ctx.respond(embed=response)
                    elif response == "success":
                        print(user.id)
                        users = db_instance.getByQuery({"user_id": user.id})
                        if users:
                            user_body = users[0]
                        user_body["lastfm"]["username"] = username

                        db_instance.update({"user_id": user.id}, user_body)
                        await ctx.respond("Set username successfully!")


def setup(bot):
    bot.add_cog(dev(bot))