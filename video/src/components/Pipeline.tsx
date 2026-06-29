import React from 'react';
import {useCurrentFrame, spring, useVideoConfig} from 'remotion';
import {theme} from '../theme';

// Pipeline de cálculo del proyecto: de los datos solares al informe.
// Cada etapa = un módulo real de app/core/. Aparecen escalonadas con flechas.
export type Stage = {file: string; role: string};

const monoFont = '"SF Mono", "JetBrains Mono", Menlo, Consolas, monospace';

export const Pipeline: React.FC<{stages: Stage[]}> = ({stages}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  return (
    <div
      style={{
        position: 'absolute',
        top: 360,
        left: 0,
        width: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 6,
        padding: '0 40px',
        flexWrap: 'nowrap',
      }}
    >
      {stages.map((s, i) => {
        const delay = Math.round((0.4 + i * 0.5) * fps);
        const pop = spring({frame: frame - delay, fps, durationInFrames: Math.round(0.5 * fps)});
        const arrow = spring({
          frame: frame - delay + Math.round(0.25 * fps),
          fps,
          durationInFrames: Math.round(0.3 * fps),
        });
        return (
          <React.Fragment key={s.file}>
            <div
              style={{
                width: 218,
                minHeight: 210,
                borderRadius: 18,
                background: theme.card,
                border: `1px solid ${theme.stroke}`,
                borderTop: `4px solid ${theme.amber}`,
                padding: '22px 16px',
                transform: `translateY(${(1 - pop) * 30}px) scale(${0.9 + pop * 0.1})`,
                opacity: pop,
                boxShadow: '0 16px 40px rgba(0,0,0,0.35)',
                display: 'flex',
                flexDirection: 'column',
                gap: 12,
              }}
            >
              <div style={{color: theme.amberSoft, fontFamily: monoFont, fontSize: 24, fontWeight: 700}}>
                {s.file}
              </div>
              <div style={{color: theme.text, fontFamily: theme.font, fontSize: 23, lineHeight: 1.3}}>
                {s.role}
              </div>
            </div>
            {i < stages.length - 1 && (
              <div style={{color: theme.green, fontSize: 40, fontWeight: 800, opacity: arrow}}>›</div>
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
};
