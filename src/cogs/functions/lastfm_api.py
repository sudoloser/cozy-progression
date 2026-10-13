import aiohttp
import os


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

        except Exception as e:
            pass