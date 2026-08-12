"use client";

import React, { useState } from 'react';
import { Navbar } from '@/components/Navbar';
import { UrlForm } from '@/components/UrlForm';
import { MediaPreviewCard } from '@/components/MediaPreviewCard';
import { Features } from '@/components/Features';
import { extractMediaInfo, VideoExtractResponse } from '@/lib/api';
import { Sparkles, Shield, RefreshCw } from 'lucide-react';

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [mediaData, setMediaData] = useState<VideoExtractResponse | null>(null);

  const handleExtract = async (url: string) => {
    setLoading(true);
    setError(null);
    try {
      const data = await extractMediaInfo(url);
      setMediaData(data);
    } catch (err: any) {
      setError(err.message || 'Ocurrió un error inesperado al analizar el video.');
      setMediaData(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#070913] text-slate-100 flex flex-col selection:bg-cyan-500 selection:text-slate-950 relative overflow-hidden">
      {/* Luces de fondo Neón Glass */}
      <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-cyan-500/15 rounded-full blur-[140px] pointer-events-none animate-pulse-glow" />
      <div className="absolute top-[20%] right-[-10%] w-[500px] h-[500px] bg-purple-600/15 rounded-full blur-[140px] pointer-events-none animate-pulse-glow" />

      <Navbar />

      <main className="flex-1 max-w-6xl mx-auto px-4 py-12 w-full flex flex-col items-center justify-start relative z-10">
        {/* Banner Hero */}
        <div className="text-center max-w-3xl mx-auto mb-10">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-300 text-xs font-semibold mb-4">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Descargas en Máxima Calidad 1080p HD</span>
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white leading-tight">
            Descargar Videos de <br />
            <span className="gradient-text">Instagram & TikTok HD</span>
          </h1>

          <p className="mt-4 text-slate-400 text-base sm:text-lg max-w-xl mx-auto leading-relaxed">
            Pega el enlace de cualquier Reel, publicación o video de TikTok y descárgalo al instante en la mejor calidad sin marca de agua.
          </p>
        </div>

        {/* Input Formulario */}
        <UrlForm onSubmit={handleExtract} isLoading={loading} error={error} />

        {/* Vista previa de Metadatos con key única para forzar re-montaje limpio del componente */}
        {mediaData && (
          <div className="w-full">
            <MediaPreviewCard key={mediaData.id} data={mediaData} />
            <div className="text-center mt-4">
              <button
                onClick={() => setMediaData(null)}
                className="text-xs text-slate-400 hover:text-cyan-400 transition-colors inline-flex items-center gap-1"
              >
                <RefreshCw className="w-3 h-3" /> Descargar otro video
              </button>
            </div>
          </div>
        )}

        {/* Características & Beneficios */}
        <Features />
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950/80 py-8 text-center text-xs text-slate-500">
        <div className="max-w-6xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <Shield className="w-4 h-4 text-slate-400" />
            <span>MediaStreamer HD © 2026. Todos los derechos reservados.</span>
          </div>
          <div className="flex space-x-4">
            <a href="#" className="hover:text-slate-300">Términos</a>
            <a href="#" className="hover:text-slate-300">Privacidad</a>
            <a href="#" className="hover:text-slate-300">Contacto</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
