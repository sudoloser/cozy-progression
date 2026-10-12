import json
import aiohttp

from pylette import extract_colors

base_url = "https://www.thecolorapi.com/id?rgb="

fallback_convert_url = base_url + "044, 085, 069"
fallback_image_url = "https://imgs.search.brave.com/DVK3W6IIFXe4rES3j2MidbbG5Ec6VF29rpYqMhDC4pg/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9wcmV2/aWV3LnJlZGQuaXQv/ZXZlcnlvbmUtc2hh/cmUteW91ci1mYXYt/Y2FzZW9oLWltYWdl/LWlsbC1zdGFydC13/aXRoLW1pbmUtdjAt/MXVtcXB5MGIzbnpm/MS5qcGVnP3dpZHRo/PTcwOSZmb3JtYXQ9/cGpwZyZhdXRvPXdl/YnAmcz04ZjM2Nzhl/YTA2OTI0NjZhYWI3/ZTU3NzczZTI1Yjg3/OWM5MzI3NDdj"

async def colorFromImage(image_url=fallback_image_url, format="rgb"):
    palette = extract_colors(
        image=image_url,
        palette_size=5
    )

    color = palette[0]

    if format == "rgb":
        primaryColor = color.rgb
    elif format == "hls":
        primaryColor = color.hls
    elif format == "hsv":
        primaryColor = color.hsv
    elif format == "hex":
        primaryColor = color.rgb

        primaryColor = str(primaryColor)[1:-1]

        async with aiohttp.ClientSession() as session:
            async with session.get(base_url + primaryColor) as response:
                rgb = await response.json()
                primaryColor = rgb["hex"]
                primaryColor = primaryColor["clean"]

    hex = primaryColor

    return hex