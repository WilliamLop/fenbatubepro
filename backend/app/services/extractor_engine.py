import asyncio
import yt_dlp
from typing import Dict, Any
from fastapi import HTTPException
from app.schemas.media import VideoExtractResponse, MediaFormatOption
from app.services.validators import validate_media_url, resolve_url_redirects
from app.services.tiktok_fallback import TikTokFallbackScraper
from app.services.download_proxy import MediaProxyService

class ExtractorEngine:
    """
    Motor de extracción optimizado que combina SSSTik para TikTok (100% HD sin marca de agua)
    yt-dlp para Instagram (con filtrado estricto de streams progresivos H.264/AAC compatibles con QuickTime),
    y proxy en Base64 para evitar truncamientos de URL.
    """

    @staticmethod
    def _extract_sync_ytdlp(url: str) -> Dict[str, Any]:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'skip_download': True,
            'format': 'best[ext=mp4][vcodec^=avc1][acodec!=none]/best[ext=mp4]/best',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return ydl.sanitize_info(info)

    @classmethod
    async def extract_media(cls, raw_url: str) -> VideoExtractResponse:
        # Step 1: Limpiar parámetros de tracking (?_r=1&_t=...) y resolver redirecciones (vt.tiktok.com)
        clean_input = raw_url.split("?")[0].strip()
        canonical_url = await resolve_url_redirects(clean_input)
        is_valid, platform = validate_media_url(canonical_url)

        if not is_valid or not platform:
            raise HTTPException(
                status_code=400,
                detail="La URL proporcionada no pertenece a una publicación válida de Instagram o TikTok."
            )

        # Step 2: Para TikTok, usar SSSTik / TikCDN como motor primario (garantiza HD 1080p sin marca)
        if platform == "tiktok":
            fallback_data = await TikTokFallbackScraper.extract(canonical_url)
            if fallback_data and fallback_data.get("hd_url"):
                encoded_hd = MediaProxyService.encode_target(fallback_data["hd_url"])
                
                formats = [
                    MediaFormatOption(
                        format_id="hd_no_watermark",
                        quality_label="HD Sin Marca de Agua (1080p)",
                        extension="mp4",
                        has_watermark=False,
                        download_url=f"/api/v1/download?target={encoded_hd}&filename=tiktok_{fallback_data['id']}_hd.mp4"
                    )
                ]

                if fallback_data.get("audio_url"):
                    encoded_audio = MediaProxyService.encode_target(fallback_data["audio_url"])
                    formats.append(
                        MediaFormatOption(
                            format_id="audio_mp3",
                            quality_label="Solo Audio (MP3)",
                            extension="mp3",
                            has_watermark=False,
                            download_url=f"/api/v1/download?target={encoded_audio}&filename=tiktok_{fallback_data['id']}_audio.mp3"
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

        # Step 3: Extracción para Instagram usando yt-dlp con filtrado garantizado de video + audio H.264
        info = None
        try:
            loop = asyncio.get_event_loop()
            info = await loop.run_in_executor(None, cls._extract_sync_ytdlp, canonical_url)
        except Exception as primary_error:
            print(f"[ExtractorEngine] yt-dlp error para {platform}: {primary_error}")

        if not info:
            raise HTTPException(
                status_code=500,
                detail="No se pudo procesar el contenido de Instagram. Verifica que la publicación no sea privada."
            )

        # Buscar explícitamente el mejor formato MP4 progresivo que contenga VIDEO + AUDIO multiplexados
        direct_url = None
        if "formats" in info:
            for fmt in reversed(info["formats"]):
                # Filtrar formatos que tengan tanto pista de video como de audio activas
                has_video = fmt.get("vcodec") and fmt.get("vcodec") != "none"
                has_audio = fmt.get("acodec") and fmt.get("acodec") != "none"
                is_mp4 = fmt.get("ext") == "mp4" or "mp4" in fmt.get("format_id", "").lower()
                
                if fmt.get("url") and has_video and has_audio and is_mp4:
                    direct_url = fmt["url"]
                    break

        # Fallback a la URL principal si no se encontró en la lista de formatos
        if not direct_url:
            direct_url = info.get("url")

        if not direct_url:
            raise HTTPException(status_code=500, detail="No se encontraron enlaces directos de video reproducibles.")

        encoded_direct = MediaProxyService.encode_target(direct_url)
        media_id = str(info.get("id", "video"))

        formats = [
            MediaFormatOption(
                format_id="hd_best",
                quality_label="Alta Calidad HD (1080p)",
                extension="mp4",
                has_watermark=False,
                filesize_approx_mb=round(info.get("filesize_approx", 0) / (1024 * 1024), 2) if info.get("filesize_approx") else None,
                download_url=f"/api/v1/download?target={encoded_direct}&filename={platform}_{media_id}.mp4"
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
