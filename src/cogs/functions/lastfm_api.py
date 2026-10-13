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


async def lastFmApi(username: str = None, command: str = None):
    if not username:
        raise ValueError("Please provide a username when calling this function.")
    apiKey = os.getenv("LASTFM_API_KEY")
    if not apiKey:
        raise ValueError("LASTFM_API_KEY is missing. Add it to .env and restart the bot.")
    apiUrl = f"https://ws.audioscrobbler.com/2.0/?method=user.getRecentTracks&user={username}&api_key={apiKey}&format=json&limit=1"
    if not command:
        async with aiohttp.ClientSession() as session:
            async with session.get(apiUrl) as response:
                data = await response.json()
                if response.status != 200 or "recenttracks" not in data:
                    raise RuntimeError(f"LastFM API error: {data.get('message', data)}")

                tracks = data["recenttracks"].get("track", [])
                if isinstance(tracks, dict):
                    tracks = [tracks]
                if not tracks:
                    raise ValueError(f"No recent tracks found for user '{username}'.")

                object1 = tracks[0]

                try:
                    artist = object1["artist"]["#text"]
                    trackName = object1["name"]
                    image = object1["image"][1]["#text"]
                except (KeyError, IndexError, TypeError) as e:
                    raise ValueError(f"Unexpected LastFM response format: {e}")

                if not image:
                    raise ValueError("No artwork found for the latest track.")
                
                try:
                    nowPlaying = object1["@attr"]["nowplaying"]
                except:
                    nowPlaying = "false"

                return artist, trackName, image, nowPlaying