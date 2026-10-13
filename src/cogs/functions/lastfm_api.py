import aiohttp
import os

from pysondb import db

from .database_helper import db_create_user_record

db_instance = db.getDb("database.json")


def fmapi_get_username(user_id):
    try:
        users = db_instance.getByQuery({"user_id": user_id})
        if users:
            return users[0].get("lastfm", {}).get("username") or None
    except:
        pass
    return None


def fmapi_set_username(user_id, username, discord_username=""):
    users = db_instance.getByQuery({"user_id": user_id})
    if users:
        user_body = users[0]
        if "lastfm" not in user_body:
            user_body["lastfm"] = {}
        user_body["lastfm"]["username"] = username
        db_instance.update({"user_id": user_id}, user_body)
    else:
        db_create_user_record(user_id, discord_username)
        users = db_instance.getByQuery({"user_id": user_id})
        if users:
            user_body = users[0]
            user_body["lastfm"]["username"] = username
            db_instance.update({"user_id": user_id}, user_body)
    return "success"


apiKey = os.getenv("LASTFM_API_KEY")

async def lastFmApi(username: str = None, command: str = None):
    apiUrl = f"https://ws.audioscrobbler.com/2.0/?method=user.getRecentTracks&user={username}&api_key={apiKey}&format=json&limit=1"
    if not username:
        raise ValueError("Please provide a username when calling this function.")
    elif not command:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(apiUrl) as response:
                    response = await response.json()

                    recenttracks = response["recenttracks"]
                    
                    track = recenttracks["track"]
                    object1 = track[0]

                    artist = object1["artist"]["#text"]
                    trackName = object1["name"]

                    image = object1["image"][1]["#text"]
                    
                    try:
                        nowPlaying = object1["@attr"]["nowplaying"]
                    except:
                        nowPlaying = "false"

                    return artist, trackName, image, nowPlaying

        except Exception:
            raise