import asyncio
import yt_dlp
from typing import Dict, Any
from fastapi import HTTPException
from app.schemas.media import VideoExtractResponse, MediaFormatOption
from app.services.validators import validate_media_url

class ExtractorEngine:
    """
    Motor de extracción asíncrono basado en yt-dlp con opciones optimizadas para HD.
    """
    
    @staticmethod
    def _extract_sync(url: str) -> Dict[str, Any]:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'skip_download': True,
            'format': 'bestvideo+bestaudio/best',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return ydl.sanitize_info(info)

    @classmethod
    async def extract_media(cls, url: str) -> VideoExtractResponse:
        is_valid, platform = validate_media_url(url)
        if not is_valid or not platform:
            raise HTTPException(
                status_code=400,
                detail="La URL proporcionada no pertenece a una publicación válida de Instagram o TikTok."
            )
            
        try:
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, cls._extract_sync, url)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al extraer metadatos del contenido: {str(e)}"
            )

        formats = []
        
        # Procesar opciones de video en alta calidad
        formats.append(
            MediaFormatOption(
                format_id="hd_best",
                quality_label="Alta Calidad HD (1080p)",
                extension="mp4",
                has_watermark=False if platform == "tiktok" else False,
                filesize_approx_mb=round(info.get("filesize_approx", 0) / (1024 * 1024), 2) if info.get("filesize_approx") else None,
                download_url=info.get("url") or (info["requested_formats"][0]["url"] if "requested_formats" in info else "")
            )
        )
        
        # Procesar extracción de audio si está disponible
        if info.get("url") or "requested_formats" in info:
            formats.append(
                MediaFormatOption(
                    format_id="audio_mp3",
                    quality_label="Solo Audio (MP3)",
                    extension="mp3",
                    has_watermark=False,
                    download_url=info.get("url") or (info["requested_formats"][-1]["url"] if "requested_formats" in info else "")
                )
            )

        return VideoExtractResponse(
            id=str(info.get("id", "media_id")),
            platform=platform,
            title=info.get("title") or info.get("description") or f"Video de {platform.capitalize()}",
            author=info.get("uploader") or info.get("uploader_id") or "Creador",
            author_avatar=info.get("thumbnail"),
            thumbnail=info.get("thumbnail") or "",
            duration_seconds=int(info.get("duration") or 0),
            formats=formats
        )
