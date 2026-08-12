import base64
import httpx
from urllib.parse import quote, unquote
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

class MediaProxyService:
    """
    Servidor Proxy de Streaming que soporta decodificación Base64 de la URL de origen
    para evitar truncamiento de parámetros query (&) y garantizar la entrega de video MP4
    con Status 200/206 compatible con QuickTime.
    """

    @classmethod
    def encode_target(cls, url: str) -> str:
        """Codifica la URL objetivo en base64url seguro."""
        return base64.urlsafe_b64encode(url.encode("utf-8")).decode("utf-8")

    @classmethod
    def decode_target(cls, encoded: str) -> str:
        """Decodifica el string base64url a la URL original sin alteración."""
        try:
            # Añadir padding si es necesario
            padded = encoded + "=" * (-len(encoded) % 4)
            return base64.urlsafe_b64decode(padded.encode("utf-8")).decode("utf-8")
        except Exception:
            return unquote(encoded)

    @classmethod
    async def stream_media(cls, target_encoded: str, filename: str = "video.mp4") -> StreamingResponse:
        if not target_encoded:
            raise HTTPException(status_code=400, detail="URL de destino vacía.")

        target_url = cls.decode_target(target_encoded)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Accept-Encoding": "identity",
        }
        
        if "instagram" in target_url or "cdninstagram" in target_url or "fbcdn" in target_url:
            headers["Referer"] = "https://www.instagram.com/"
        elif "ssstik" in target_url or "tikcdn" in target_url:
            headers["Referer"] = "https://ssstik.io/"

        client = httpx.AsyncClient(follow_redirects=True, timeout=30.0)
        
        try:
            req = client.build_request("GET", target_url, headers=headers)
            res = await client.send(req, stream=True)

            if res.status_code not in (200, 206):
                await res.aclose()
                await client.aclose()
                raise HTTPException(
                    status_code=400,
                    detail=f"El servidor de origen del video devolvió un error ({res.status_code}). Intenta de nuevo."
                )

            async def file_generator():
                try:
                    async for chunk in res.aiter_bytes(chunk_size=1024 * 64):
                        yield chunk
                finally:
                    await res.aclose()
                    await client.aclose()

            safe_filename = quote(filename)
            content_length = res.headers.get("content-length")
            
            response_headers = {
                "Content-Disposition": f'attachment; filename="{filename}"; filename*=UTF-8\'\'{safe_filename}',
                "Access-Control-Expose-Headers": "Content-Disposition, Content-Length",
                "Cache-Control": "no-cache",
            }
            if content_length:
                response_headers["Content-Length"] = content_length

            return StreamingResponse(
                file_generator(),
                media_type="video/mp4" if filename.endswith(".mp4") else "audio/mpeg",
                headers=response_headers
            )

        except HTTPException:
            raise
        except Exception as e:
            await client.aclose()
            raise HTTPException(
                status_code=500,
                detail=f"Error al establecer conexión con el stream de origen: {str(e)}"
            )
