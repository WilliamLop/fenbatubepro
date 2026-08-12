"use client";

import React, { useState } from 'react';
import { Clipboard, ArrowRight, Loader2, XCircle, CheckCircle2 } from 'lucide-react';

interface UrlFormProps {
  onSubmit: (url: string) => void;
  isLoading: boolean;
  error?: string | null;
}

export const UrlForm: React.FC<UrlFormProps> = ({ onSubmit, isLoading, error }) => {
  const [url, setUrl] = useState('');

  const handlePaste = async () => {
    try {
      const text = await navigator.clipboard.readText();
      if (text) {
        setUrl(text);
      }
    } catch {
      // Ignorar si no hay permisos de portapapeles
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (url.trim()) {
      onSubmit(url.trim());
    }
  };

  const isInstagram = url.includes('instagram.com');
  const isTikTok = url.includes('tiktok.com');

  return (
    <div className="w-full max-w-3xl mx-auto">
      <form onSubmit={handleSubmit} className="relative">
        <div className="glass-panel glass-input p-2 sm:p-3 rounded-2xl flex items-center space-x-2 shadow-2xl">
          <div className="flex-1 flex items-center px-3 space-x-2">
            <input
              type="url"
              placeholder="Pega el enlace de Instagram o TikTok aquí..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              required
              className="w-full bg-transparent text-white placeholder-slate-400 text-sm sm:text-base focus:outline-none"
            />
            {url && (
              <button
                type="button"
                onClick={() => setUrl('')}
                className="text-slate-400 hover:text-white transition-colors"
              >
                <XCircle className="w-5 h-5" />
              </button>
            )}
          </div>

          <div className="flex items-center space-x-2">
            {!url && (
              <button
                type="button"
                onClick={handlePaste}
                className="hidden sm:inline-flex items-center space-x-1.5 px-3 py-2 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-slate-300 text-xs font-medium border border-slate-700 transition-all"
              >
                <Clipboard className="w-3.5 h-3.5" />
                <span>Pegar</span>
              </button>
            )}

            <button
              type="submit"
              disabled={isLoading || !url.trim()}
              className="glow-button px-5 py-3 rounded-xl text-slate-950 font-bold text-sm sm:text-base flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span className="hidden sm:inline">Analizando...</span>
                </>
              ) : (
                <>
                  <span>Descargar</span>
                  <ArrowRight className="w-5 h-5" />
                </>
              )}
            </button>
          </div>
        </div>
      </form>

      {/* Badges de detección de plataforma */}
      <div className="mt-3 flex items-center justify-between text-xs px-2 text-slate-400">
        <div className="flex items-center space-x-3">
          <span className={`flex items-center gap-1 transition-colors ${isInstagram ? 'text-pink-400 font-semibold' : ''}`}>
            {isInstagram ? <CheckCircle2 className="w-3.5 h-3.5" /> : null} Instagram Reel / Post
          </span>
          <span>•</span>
          <span className={`flex items-center gap-1 transition-colors ${isTikTok ? 'text-cyan-400 font-semibold' : ''}`}>
            {isTikTok ? <CheckCircle2 className="w-3.5 h-3.5" /> : null} TikTok (Sin marca de agua)
          </span>
        </div>
      </div>

      {error && (
        <div className="mt-4 p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm flex items-center space-x-2">
          <XCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
};
