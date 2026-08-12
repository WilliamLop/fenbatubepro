import httpx
from typing import Dict, Any, Optional

class TikTokFallbackScraper:
    """
    Scraper secundario de respaldo para TikTok que consulta la API de TikWM
    en caso de que yt-dlp sea bloqueado o falle por rate-limiting.
    """
    API_URL = "https://www.tikwm.com/api/"

    @classmethod
    async def extract(cls, url: str) -> Optional[Dict[str, Any]]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
        }
        async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
            try:
                response = await client.post(cls.API_URL, data={"url": url, "hd": 1}, headers=headers)
                if response.status_code == 200:
                    res_json = response.json()
                    if res_json.get("code") == 0 and "data" in res_json:
                        data = res_json["data"]
                        # Priorizar URL en HD sin marca de agua
                        hd_url = data.get("hdplay") or data.get("play")
                        watermark_url = data.get("wmplay") or data.get("play")
                        music_url = data.get("music")

                        return {
                            "id": data.get("id", "tiktok_video"),
                            "title": data.get("title") or "TikTok Video",
                            "author": data.get("author", {}).get("nickname") or data.get("author", {}).get("unique_id") or "TikTok Creator",
                            "author_avatar": data.get("author", {}).get("avatar"),
                            "thumbnail": data.get("cover"),
                            "duration_seconds": data.get("duration", 0),
                            "hd_url": f"https://www.tikwm.com{hd_url}" if hd_url and hd_url.startswith("/") else hd_url,
                            "watermark_url": f"https://www.tikwm.com{watermark_url}" if watermark_url and watermark_url.startswith("/") else watermark_url,
                            "music_url": f"https://www.tikwm.com{music_url}" if music_url and music_url.startswith("/") else music_url,
                        }
            except Exception as e:
                print(f"[TikTokFallbackScraper Error]: {e}")
        return None
