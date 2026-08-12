export interface MediaFormatOption {
  format_id: string;
  quality_label: string;
  extension: string;
  has_watermark: boolean;
  filesize_approx_mb?: number;
  download_url: string;
}

export interface VideoExtractResponse {
  id: string;
  platform: 'instagram' | 'tiktok';
  title: string;
  author: string;
  author_avatar?: string;
  thumbnail: string;
  duration_seconds: number;
  formats: MediaFormatOption[];
}

// URL oficial del nuevo backend en Render para fenbatubepro
export const BACKEND_API_URL =
  process.env.NEXT_PUBLIC_API_URL || 'https://fenbatubepro-api.onrender.com';

export async function extractMediaInfo(url: string): Promise<VideoExtractResponse> {
  const response = await fetch(`${BACKEND_API_URL}/api/v1/extract`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ url }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Error al conectar con el servidor.' }));
    throw new Error(errorData.detail || 'No se pudo procesar el video. Verifica la URL.');
  }

  return response.json();
}
