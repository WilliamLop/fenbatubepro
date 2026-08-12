from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints.extract import router as extract_router

app = FastAPI(
    title="Media Downloader API",
    description="API de extracción de contenidos en Alta Calidad para Instagram y TikTok",
    version="1.0.0",
)

# Permitir CORS para conexiones desde Next.js Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(extract_router, prefix="/api/v1", tags=["Extraction"])

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok", "service": "Media Downloader API"}
