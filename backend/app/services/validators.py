import re
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

def validate_media_url(url: str) -> Tuple[bool, Optional[str]]:
    """
    Valida si la URL ingresada corresponde a Instagram o TikTok.
    Devuelve una tupla (es_valida, plataforma).
    """
    clean_url = url.strip()
    
    if INSTAGRAM_REGEX.match(clean_url):
        return True, "instagram"
    
    if TIKTOK_DESKTOP_REGEX.match(clean_url) or TIKTOK_SHORT_REGEX.match(clean_url):
        return True, "tiktok"
    
    return False, None
