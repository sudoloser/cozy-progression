import hashlib
import aiohttp

async def get_url_hash(url: str, algorithm='sha256') -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                hasher = getattr(hashlib, algorithm)()
                hasher.update(content)
                return hasher.hexdigest()
            else:
                raise Exception(f"Failed to fetch file: HTTP {response.status}")