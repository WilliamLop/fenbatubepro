from fastapi import APIRouter, HTTPException, Query
from app.schemas.media import VideoExtractRequest, VideoExtractResponse
from app.services.extractor_engine import ExtractorEngine
from app.services.download_proxy import MediaProxyService

router = APIRouter()

@router.post("/extract", response_model=VideoExtractResponse)
async def extract_video_info(payload: VideoExtractRequest):
    """
    Endpoint principal para extraer información y enlaces de descarga en HD de Instagram / TikTok.
    """
    if not payload.url:
        raise HTTPException(status_code=400, detail="Debes proporcionar una URL válida.")
    
    return await ExtractorEngine.extract_media(payload.url)

@router.get("/download")
async def download_media(
    target: str = Query(..., description="String Base64 de la URL objetivo de descarga"),
    filename: str = Query("video.mp4", description="Nombre del archivo final de salida")
):
    """
    Proxy Streamer que retransmite el contenido en Base64 agregando las cabeceras requeridas,
    garantizando descargas directas en .mp4 100% compatibles con QuickTime Player.
    """
    return await MediaProxyService.stream_media(target_encoded=target, filename=filename)
