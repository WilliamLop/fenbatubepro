"use client";

import React, { useState } from 'react';
import { VideoExtractResponse, MediaFormatOption, BACKEND_API_URL } from '@/lib/api';
import { Download, Film, Music, Check, Sparkles, Clock, User } from 'lucide-react';

interface MediaPreviewCardProps {
  data: VideoExtractResponse;
}

export const MediaPreviewCard: React.FC<MediaPreviewCardProps> = ({ data }) => {
  const [selectedFormat, setSelectedFormat] = useState<MediaFormatOption>(data.formats[0]);
  const [isDownloading, setIsDownloading] = useState(false);

  const handleDownload = () => {
    setIsDownloading(true);

    // Construir la URL completa apuntando a nuestro Proxy de descarga en el backend
    const downloadUrl = selectedFormat.download_url.startsWith('http')
      ? selectedFormat.download_url
      : `${BACKEND_API_URL}${selectedFormat.download_url}`;

    // Disparar la descarga directa nativa del navegador sin abrir pestañas emergentes
    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = `${data.platform}_${data.id}.${selectedFormat.extension}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    setTimeout(() => setIsDownloading(false), 2000);
  };

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  return (
    <div className="w-full max-w-3xl mx-auto mt-8 glass-panel rounded-3xl p-6 shadow-2xl border border-white/10 relative overflow-hidden">
      <div className="absolute top-0 right-0 w-64 h-64 bg-cyan-500/10 rounded-full filter blur-3xl pointer-events-none" />

      <div className="flex flex-col md:flex-row gap-6 items-center">
        {/* Vista previa Thumbnail */}
        <div className="relative w-full md:w-56 h-64 md:h-56 rounded-2xl overflow-hidden bg-slate-900 border border-slate-800 flex-shrink-0">
          <img
            src={data.thumbnail || 'https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?q=80&w=600&auto=format&fit=crop'}
            alt={data.title}
            className="w-full h-full object-cover"
          />
          <div className="absolute top-3 left-3 px-3 py-1 rounded-full text-xs font-bold uppercase bg-slate-950/80 backdrop-blur-md text-cyan-400 border border-cyan-500/30">
            {data.platform}
          </div>
          {data.duration_seconds > 0 && (
            <div className="absolute bottom-3 right-3 px-2 py-0.5 rounded bg-slate-950/80 backdrop-blur-md text-xs text-slate-300 flex items-center gap-1">
              <Clock className="w-3 h-3" /> {formatDuration(data.duration_seconds)}
            </div>
          )}
        </div>

        {/* Detalles y Formatos */}
        <div className="flex-1 w-full flex flex-col justify-between space-y-4">
          <div>
            <div className="flex items-center space-x-2 text-slate-400 text-sm mb-1">
              <User className="w-4 h-4 text-cyan-400" />
              <span className="font-semibold text-slate-200">@{data.author}</span>
            </div>
            <h3 className="text-lg font-bold text-white line-clamp-2 leading-snug">
              {data.title}
            </h3>
          </div>

          {/* Opciones de Calidad / Formato */}
          <div className="space-y-2">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 block">
              Seleccionar Calidad de Descarga
            </span>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {data.formats.map((fmt) => {
                const isSelected = selectedFormat.format_id === fmt.format_id;
                return (
                  <button
                    key={fmt.format_id}
                    onClick={() => setSelectedFormat(fmt)}
                    className={`p-3 rounded-xl border text-left flex items-center justify-between transition-all ${
                      isSelected
                        ? 'bg-cyan-500/10 border-cyan-400 text-white shadow-lg shadow-cyan-500/10'
                        : 'bg-slate-900/60 border-slate-800 text-slate-300 hover:border-slate-700'
                    }`}
                  >
                    <div className="flex items-center space-x-2.5">
                      {fmt.extension === 'mp3' ? (
                        <Music className="w-4 h-4 text-purple-400" />
                      ) : (
                        <Film className="w-4 h-4 text-cyan-400" />
                      )}
                      <div>
                        <div className="text-xs font-bold">{fmt.quality_label}</div>
                        <div className="text-[10px] text-slate-400 uppercase">
                          {fmt.extension} {fmt.has_watermark ? '(Con Marca)' : '(Sin Marca)'}
                        </div>
                      </div>
                    </div>
                    {isSelected && <Check className="w-4 h-4 text-cyan-400" />}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Botón Acción Descargar */}
          <button
            onClick={handleDownload}
            disabled={isDownloading}
            className="w-full glow-button py-3.5 px-6 rounded-xl text-slate-950 font-extrabold text-base flex items-center justify-center space-x-2 shadow-xl cursor-pointer"
          >
            <Download className="w-5 h-5" />
            <span>{isDownloading ? 'Iniciando descarga...' : `Descargar ${selectedFormat.quality_label}`}</span>
            <Sparkles className="w-4 h-4 ml-1" />
          </button>
        </div>
      </div>
    </div>
  );
};
