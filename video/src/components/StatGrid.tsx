import React from 'react';
import {useCurrentFrame, spring, useVideoConfig} from 'remotion';
import {theme} from '../theme';

export type Stat = {value: string; label: string};

// Rejilla de cifras clave que aparecen escalonadas.
export const StatGrid: React.FC<{stats: Stat[]}> = ({stats}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  return (
    <div
      style={{
        position: 'absolute',
        top: 340,
        left: 0,
        width: '100%',
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: 28,
        padding: '0 160px',
      }}
    >
      {stats.map((s, i) => {
        const delay = Math.round((0.3 + i * 0.25) * fps);
        const pop = spring({frame: frame - delay, fps, durationInFrames: Math.round(0.5 * fps)});
        return (
          <div
            key={s.label}
            style={{
              background: theme.card,
              border: `1px solid ${theme.stroke}`,
              borderLeft: `5px solid ${theme.green}`,
              borderRadius: 18,
              padding: '30px 32px',
              transform: `translateY(${(1 - pop) * 30}px) scale(${0.92 + pop * 0.08})`,
              opacity: pop,
              boxShadow: '0 16px 40px rgba(0,0,0,0.3)',
            }}
          >
            <div
              style={{
                color: theme.amberSoft,
                fontFamily: theme.font,
                fontSize: 58,
                fontWeight: 800,
                letterSpacing: -1.5,
                lineHeight: 1,
              }}
            >
              {s.value}
            </div>
            <div style={{color: theme.textDim, fontFamily: theme.font, fontSize: 26, marginTop: 12, lineHeight: 1.3}}>
              {s.label}
            </div>
          </div>
        );
      })}
    </div>
  );
};
