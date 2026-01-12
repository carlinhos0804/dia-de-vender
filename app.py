import React, { useState } from 'react';
import { Story } from '../types';

interface StoryCardProps {
  story: Story;
}

const StoryCard: React.FC<StoryCardProps> = ({ story }) => {
  const [copied, setCopied] = useState<string | null>(null);

  const copyToClipboard = (text: string, type: string) => {
    navigator.clipboard.writeText(text);
    setCopied(type);
    setTimeout(() => setCopied(null), 2000);
  };

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-xl transition-all hover:border-blue-500/50">
      <div className="flex items-center justify-between mb-4">
        <span className="bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">
          Story {story.id}
        </span>
      </div>

      <div className="space-y-4">
        <div>
          <label className="text-blue-400 text-xs font-semibold uppercase block mb-1">🎥 O que gravar (Visual)</label>
          <p className="text-slate-200 text-sm leading-relaxed">{story.visual}</p>
        </div>

        <div className="relative group">
          <label className="text-blue-400 text-xs font-semibold uppercase block mb-1">📝 O que escrever (Legenda)</label>
          <div className="flex items-start gap-2">
            <p className="text-slate-200 text-sm italic flex-grow">"{story.legenda}"</p>
            <button 
              onClick={() => copyToClipboard(story.legenda, 'legenda')}
              className="text-slate-400 hover:text-white transition-colors"
              title="Copiar legenda"
            >
              {copied === 'legenda' ? <i className="fas fa-check text-green-500"></i> : <i className="far fa-copy"></i>}
            </button>
          </div>
        </div>

        <div className="bg-slate-900/50 p-4 rounded-lg border border-slate-700/50">
          <label className="text-blue-400 text-xs font-semibold uppercase block mb-1">💬 O que falar (Script)</label>
          <div className="flex items-start gap-2">
            <p className="text-slate-300 text-sm leading-relaxed flex-grow">{story.fala}</p>
            <button 
              onClick={() => copyToClipboard(story.fala, 'fala')}
              className="text-slate-400 hover:text-white transition-colors"
              title="Copiar script de fala"
            >
              {copied === 'fala' ? <i className="fas fa-check text-green-500"></i> : <i className="far fa-copy"></i>}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StoryCard;
