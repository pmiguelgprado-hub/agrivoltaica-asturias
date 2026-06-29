import React from 'react';
import {useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import {theme} from '../theme';

// Barra de progreso del vídeo (recuerda al espectador que dura 2 min).
export const ProgressBar: React.FC = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const pct = interpolate(frame, [0, durationInFrames], [0, 100]);

  return (
    <div
      style={{
        position: 'absolute',
        left: 0,
        bottom: 0,
        width: '100%',
        height: 8,
        background: 'rgba(255,255,255,0.08)',
      }}
    >
      <div
        style={{
          width: `${pct}%`,
          height: '100%',
          background: `linear-gradient(90deg, ${theme.amber}, ${theme.green})`,
        }}
      />
    </div>
  );
};
