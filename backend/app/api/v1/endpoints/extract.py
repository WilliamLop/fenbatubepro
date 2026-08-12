from fastapi import APIRouter, HTTPException
from app.schemas.media import VideoExtractRequest, VideoExtractResponse
from app.services.extractor_engine import ExtractorEngine

router = APIRouter()

@router.post("/extract", response_model=VideoExtractResponse)
async def extract_video_info(payload: VideoExtractRequest):
    """
    Endpoint principal para extraer información y enlaces de descarga en HD de Instagram / TikTok.
    """
    if not payload.url:
        raise HTTPException(status_code=400, detail="Debes proporcionar una URL válida.")
    
    return await ExtractorEngine.extract_media(payload.url)
