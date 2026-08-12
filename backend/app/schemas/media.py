from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field

class MediaFormatOption(BaseModel):
    format_id: str = Field(..., description="Identificador único de la calidad/formato")
    quality_label: str = Field(..., description="Etiqueta legible ej: 1080p Full HD")
    extension: str = Field(..., description="Extensión del archivo: mp4 o mp3")
    has_watermark: bool = Field(default=False, description="Indica si contiene marca de agua")
    filesize_approx_mb: Optional[float] = Field(None, description="Tamaño aproximado en MB")
    download_url: str = Field(..., description="URL directa de descarga del stream")

class VideoExtractRequest(BaseModel):
    url: str = Field(..., example="https://www.tiktok.com/@username/video/71234567890")

class VideoExtractResponse(BaseModel):
    id: str
    platform: str  # "instagram" | "tiktok"
    title: str
    author: str
    author_avatar: Optional[str] = None
    thumbnail: str
    duration_seconds: int
    formats: List[MediaFormatOption]
