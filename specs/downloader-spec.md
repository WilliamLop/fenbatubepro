# 📋 Technical Specification: Media Downloader API v1

## 1. Overview
API REST asíncrona construida en FastAPI para extraer metadatos y enlaces de descarga directa en Alta Calidad (HD / 1080p / MP3 / No-Watermark) desde enlaces de Instagram y TikTok.

---

## 2. API Endpoints Contract

### `POST /api/v1/extract`
Analiza la URL proporcionada por el usuario y retorna la vista previa con las opciones de descarga disponibles.

#### Request Body (`application/json`)
```json
{
  "url": "https://www.tiktok.com/@username/video/71234567890"
}
```

#### Response Body 200 OK (`application/json`)
```json
{
  "id": "71234567890",
  "platform": "tiktok",
  "title": "Amazing travel video #viral",
  "author": "john_doe",
  "author_avatar": "https://p16-sign.tiktokcdn.com/...",
  "thumbnail": "https://p16-sign.tiktokcdn.com/...",
  "duration_seconds": 34,
  "formats": [
    {
      "format_id": "hd_no_watermark",
      "quality_label": "HD Sin Marca de Agua (1080p)",
      "extension": "mp4",
      "has_watermark": false,
      "filesize_approx_mb": 14.2,
      "download_url": "https://v16-webapp-prime.tiktok.com/..."
    },
    {
      "format_id": "watermark",
      "quality_label": "Original (Con Marca)",
      "extension": "mp4",
      "has_watermark": true,
      "filesize_approx_mb": 12.0,
      "download_url": "https://v16-webapp-prime.tiktok.com/..."
    },
    {
      "format_id": "audio_mp3",
      "quality_label": "Solo Audio (MP3 320kbps)",
      "extension": "mp3",
      "has_watermark": false,
      "filesize_approx_mb": 1.5,
      "download_url": "https://v16-webapp-prime.tiktok.com/..."
    }
  ]
}
```

#### Error Responses
* `400 Bad Request`: URL no válida o plataforma no soportada.
* `422 Unprocessable Entity`: La URL ingresada no coincide con los patrones Regex esperados.
* `500 Internal Server Error`: Bloqueo temporal por parte del proveedor o error de extracción.

---

## 3. Supported URL Regex Validation

### Instagram:
* Posts / Reels: `r"^https?:\/\/(www\.)?instagram\.com\/(p|reel|reels|tv)\/([A-Za-z0-9_-]+)"`

### TikTok:
* Desktop URL: `r"^https?:\/\/(www\.)?tiktok\.com\/@[\w.-]+\/video\/\d+"`
* Short/Mobile URL: `r"^https?:\/\/(vm|vt)\.tiktok\.com\/[A-Za-z0-9_-]+"`

---

## 4. Extractor Engine Specs (`yt-dlp` integration)
* `format`: `'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'`
* `outtmpl`: `'%(id)s.%(ext)s'`
* `quiet`: `True`
* `no_warnings`: `True`
* `extract_flat`: `False`
