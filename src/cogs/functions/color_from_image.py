import aiohttp
import colorsys
import io

from PIL import Image

base_url = "https://www.thecolorapi.com/id?rgb="

fallback_convert_url = base_url + "044, 085, 069"
fallback_image_url = "https://imgs.search.brave.com/DVK3W6IIFXe4rES3j2MidbbG5Ec6VF29rpYqMhDC4pg/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9wcmV2/aWV3LnJlZGQuaXQv/ZXZlcnlvbmUtc2hh/cmUteW91ci1mYXYt/Y2FzZW9oLWltYWdl/LWlsbC1zdGFydC13/aXRoLW1pbmUtdjAt/MXVtcXB5MGIzbnpm/MS5qcGVnP3dpZHRo/PTcwOSZmb3JtYXQ9/cGpwZyZhdXRvPXdl/YnAmcz04ZjM2Nzhl/YTA2OTI0NjZhYWI3/ZTU3NzczZTI1Yjg3/OWM5MzI3NDdj"


async def _fetch_bytes(image_url: str) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url, timeout=aiohttp.ClientTimeout(total=20)) as response:
            response.raise_for_status()
            return await response.read()


def _dominant_rgb(data: bytes) -> tuple[int, int, int]:
    with Image.open(io.BytesIO(data)) as img:
        img = img.convert("RGB")
        img.thumbnail((200, 200))
        quantized = img.quantize(colors=5, method=Image.Quantize.MEDIANCUT)
        palette = quantized.getpalette()[:15]
        counts = sorted(quantized.getcolors(), reverse=True)
        dominant_index = counts[0][1]
        r, g, b = palette[dominant_index * 3: dominant_index * 3 + 3]
        return (r, g, b)


async def colorFromImage(image_url=fallback_image_url, format="rgb"):
    data = await _fetch_bytes(image_url)
    r, g, b = _dominant_rgb(data)

    if format == "rgb":
        return (r, g, b)
    elif format == "hls":
        return colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    elif format == "hsv":
        return colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    elif format == "hex":
        rgb_param = f"{r}, {g}, {b}"
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url + rgb_param) as response:
                payload = await response.json()
                return payload["hex"]["clean"]
    else:
        raise ValueError(f"unknown format: {format}")
