import aiohttp

async def search_hash(file_hash: str):
    base_url = f"https://discbl.sdlsr.dpdns.org/blacklist/search?file_hash={file_hash}"

    async with aiohttp.ClientSession() as session:
        async with session.get(base_url) as response:
            data = await response.json()
    if data["found"] == "true":
        return True
    elif data["found"] == "false":
        return False