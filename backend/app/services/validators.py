import re
import httpx
from typing import Tuple, Optional

INSTAGRAM_REGEX = re.compile(
    r"^https?:\/\/(www\.)?instagram\.com\/(p|reel|reels|tv)\/([A-Za-z0-9_-]+)"
)

TIKTOK_DESKTOP_REGEX = re.compile(
    r"^https?:\/\/(www\.)?tiktok\.com\/@[\w.-]+\/video\/\d+"
)

TIKTOK_SHORT_REGEX = re.compile(
    r"^https?:\/\/(vm|vt)\.tiktok\.com\/[A-Za-z0-9_-]+"
)

async def resolve_url_redirects(url: str) -> str:
    """
    Sigue las redirecciones HTTP 301/302 para obtener la URL canónica final
    (por ejemplo, resolviendo vt.tiktok.com -> tiktok.com/@user/video/12345).
    """
    clean_url = url.strip()
    if TIKTOK_SHORT_REGEX.match(clean_url) or "instagram.com/share" in clean_url or "vt.tiktok" in clean_url or "vm.tiktok" in clean_url:
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=5.0) as client:
                resp = await client.head(clean_url, headers={"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"})
                return str(resp.url)
        except Exception:
            pass
    return clean_url

def validate_media_url(url: str) -> Tuple[bool, Optional[str]]:
    """
    Valida la sintaxis de la URL canónica e identifica si es Instagram o TikTok.
    """
    clean_url = url.strip()
    
    if INSTAGRAM_REGEX.search(clean_url):
        return True, "instagram"
    
    if TIKTOK_DESKTOP_REGEX.search(clean_url) or TIKTOK_SHORT_REGEX.search(clean_url) or "tiktok.com" in clean_url:
        return True, "tiktok"
    
    return False, None
