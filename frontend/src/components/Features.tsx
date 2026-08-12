import React from 'react';
import { Zap, ShieldCheck, Sparkles, Smartphone, DownloadCloud, Flame } from 'lucide-react';

export const Features: React.FC = () => {
  const items = [
    {
      icon: <Sparkles className="w-6 h-6 text-cyan-400" />,
      title: "TikTok Sin Marca de Agua",
      description: "Descarga videos limpios en resolución HD original 1080p sin logotipos molestos."
    },
    {
      icon: <Flame className="w-6 h-6 text-pink-400" />,
      title: "Instagram Reels & Posts",
      description: "Compatible con Reels, carruseles, publicaciones de feed y audios de tendencias."
    },
    {
      icon: <Zap className="w-6 h-6 text-yellow-400" />,
      title: "Extracción Ultra Rápida",
      description: "Procesamiento asíncrono con motor FastAPI que obtiene los enlaces de descarga en milisegundos."
    },
    {
      icon: <Smartphone className="w-6 h-6 text-purple-400" />,
      title: "100% Responsivo & Móvil",
      description: "Diseñado perfectamente para funcionar desde cualquier iPhone, Android, Tablet o PC."
    },
    {
      icon: <DownloadCloud className="w-6 h-6 text-emerald-400" />,
      title: "Extracción de Audio MP3",
      description: "Convierte cualquier Reel o TikTok a audio MP3 de alta fidelidad con 1 clic."
    },
    {
      icon: <ShieldCheck className="w-6 h-6 text-blue-400" />,
      title: "Sin Registros ni Anuncios",
      description: "Totalmente privado y gratis. No requiere registrarte ni instalar extensiones."
    }
  ];

  return (
    <section className="py-16 max-w-6xl mx-auto px-4">
      <div className="text-center mb-12">
        <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          ¿Por qué elegir <span className="gradient-text">MediaStreamer HD</span>?
        </h2>
        <p className="mt-2 text-slate-400 text-sm sm:text-base max-w-xl mx-auto">
          La mejor tecnología de extracción de contenidos con calidad original sin pérdida.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {items.map((item, idx) => (
          <div
            key={idx}
            className="glass-panel p-6 rounded-2xl border border-white/5 hover:border-cyan-500/30 transition-all duration-300 group hover:-translate-y-1"
          >
            <div className="w-12 h-12 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              {item.icon}
            </div>
            <h3 className="text-lg font-bold text-white mb-2">{item.title}</h3>
            <p className="text-slate-400 text-sm leading-relaxed">{item.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
};
