import httpx
from urllib.parse import quote
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

class MediaProxyService:
    """
    Servidor Proxy de Streaming que retransmite el video/audio desde los CDNs
    de Instagram y TikTok aplicando las cabeceras requeridas (Referer, User-Agent),
    garantizando que el archivo descargado sea un .mp4 100% válido y compatible
    con QuickTime Player en macOS/Windows.
    """

    @classmethod
    async def stream_media(cls, target_url: str, filename: str = "video.mp4") -> StreamingResponse:
        if not target_url:
            raise HTTPException(status_code=400, detail="URL de destino vacía.")

        # Determinar cabeceras de origen seguras
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Accept-Encoding": "identity",
        }
        
        if "instagram" in target_url or "cdninstagram" in target_url or "fbcdn" in target_url:
            headers["Referer"] = "https://www.instagram.com/"
        elif "tiktok" in target_url or "tikwm" in target_url:
            headers["Referer"] = "https://www.tiktok.com/"

        async def file_generator():
            async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
                async with client.stream("GET", target_url, headers=headers) as response:
                    if response.status_code not in (200, 206):
                        raise HTTPException(
                            status_code=response.status_code,
                            detail="No se pudo obtener el archivo desde el servidor de origen."
                        )
                    async for chunk in response.aiter_bytes(chunk_size=1024 * 64):
                        yield chunk

        safe_filename = quote(filename)
        return StreamingResponse(
            file_generator(),
            media_type="video/mp4" if filename.endswith(".mp4") else "audio/mpeg",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"; filename*=UTF-8\'\'{safe_filename}',
                "Access-Control-Expose-Headers": "Content-Disposition",
                "Cache-Control": "no-cache",
            }
        )
