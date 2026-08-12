import asyncio
import yt_dlp
from typing import Dict, Any, List
from urllib.parse import quote
from fastapi import HTTPException
from app.schemas.media import VideoExtractResponse, MediaFormatOption
from app.services.validators import validate_media_url, resolve_url_redirects
from app.services.tiktok_fallback import TikTokFallbackScraper

class ExtractorEngine:
    """
    Motor de extracción optimizado para entregar streams MP4 progresivos (Video + Audio combinados H.264/AAC),
    garantizando reproducibilidad 100% en QuickTime Player y fallbacks resilientes para TikTok e Instagram.
    """

    @staticmethod
    def _extract_sync_ytdlp(url: str) -> Dict[str, Any]:
        # Formato optimizado: Prioriza streams MP4 progresivos únicos (video + audio en un solo archivo)
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'skip_download': True,
            'format': 'best[ext=mp4]/b[ext=mp4]/best',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return ydl.sanitize_info(info)

    @classmethod
    async def extract_media(cls, raw_url: str) -> VideoExtractResponse:
        # Step 1: Resolver redirecciones de URLs cortas (vt.tiktok.com, vm.tiktok.com, ig.me)
        canonical_url = await resolve_url_redirects(raw_url)
        is_valid, platform = validate_media_url(canonical_url)

        if not is_valid or not platform:
            raise HTTPException(
                status_code=400,
                detail="La URL proporcionada no pertenece a una publicación válida de Instagram o TikTok."
            )

        # Para TikTok, intentar PRIMERO el scraper directo de TikWM para obtener video HD sin marca de agua inmediato
        if platform == "tiktok":
            fallback_data = await TikTokFallbackScraper.extract(canonical_url)
            if fallback_data and fallback_data.get("hd_url"):
                encoded_hd = quote(fallback_data["hd_url"], safe="")
                encoded_music = quote(fallback_data["music_url"], safe="") if fallback_data.get("music_url") else ""

                formats = [
                    MediaFormatOption(
                        format_id="hd_no_watermark",
                        quality_label="HD Sin Marca de Agua (1080p)",
                        extension="mp4",
                        has_watermark=False,
                        download_url=f"/api/v1/download?url={encoded_hd}&filename=tiktok_{fallback_data['id']}_hd.mp4"
                    )
                ]
                if encoded_music:
                    formats.append(
                        MediaFormatOption(
                            format_id="audio_mp3",
                            quality_label="Solo Audio (MP3)",
                            extension="mp3",
                            has_watermark=False,
                            download_url=f"/api/v1/download?url={encoded_music}&filename=tiktok_{fallback_data['id']}_audio.mp3"
                        )
                    )

                return VideoExtractResponse(
                    id=str(fallback_data["id"]),
                    platform="tiktok",
                    title=fallback_data["title"],
                    author=fallback_data["author"],
                    author_avatar=fallback_data.get("author_avatar"),
                    thumbnail=fallback_data.get("thumbnail") or "",
                    duration_seconds=int(fallback_data.get("duration_seconds") or 0),
                    formats=formats
                )

        # Step 2: Extracción primaria con yt-dlp (especialmente para Instagram)
        info = None
        try:
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, cls._extract_sync_ytdlp, canonical_url)
        except Exception as primary_error:
            print(f"[ExtractorEngine] yt-dlp error para {platform}: {primary_error}")

        if not info:
            raise HTTPException(
                status_code=500,
                detail="No se pudo procesar el contenido. Verifica la conexión a internet o que la publicación no sea privada."
            )

        # Obtener enlace de video directo combinando pistas progresivas
        direct_url = info.get("url")
        if not direct_url and "formats" in info:
            # Buscar el mejor formato MP4 que contenga video y audio
            for fmt in reversed(info["formats"]):
                if fmt.get("url") and fmt.get("vcodec") != "none" and fmt.get("acodec") != "none":
                    direct_url = fmt["url"]
                    break
            if not direct_url and len(info["formats"]) > 0:
                direct_url = info["formats"][-1].get("url")

        if not direct_url:
            raise HTTPException(status_code=500, detail="No se encontraron enlaces directos de video reproducibles.")

        encoded_direct = quote(direct_url, safe="")
        media_id = str(info.get("id", "video"))

        formats = [
            MediaFormatOption(
                format_id="hd_best",
                quality_label="Alta Calidad HD (1080p)",
                extension="mp4",
                has_watermark=False,
                filesize_approx_mb=round(info.get("filesize_approx", 0) / (1024 * 1024), 2) if info.get("filesize_approx") else None,
                download_url=f"/api/v1/download?url={encoded_direct}&filename={platform}_{media_id}.mp4"
            )
        ]

        return VideoExtractResponse(
            id=media_id,
            platform=platform,
            title=info.get("title") or info.get("description") or f"Video de {platform.capitalize()}",
            author=info.get("uploader") or info.get("uploader_id") or "Creador",
            author_avatar=info.get("thumbnail"),
            thumbnail=info.get("thumbnail") or "",
            duration_seconds=int(info.get("duration") or 0),
            formats=formats
        )
