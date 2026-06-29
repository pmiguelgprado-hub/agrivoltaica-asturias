import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, spring, useVideoConfig, interpolate} from 'remotion';
import {theme} from './theme';
import {AnimatedBackground} from './components/AnimatedBackground';

// Composición corta (5 s) para verificar que el pipeline de render funciona.
export const Sample: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const titleIn = spring({frame, fps, durationInFrames: Math.round(0.8 * fps)});
  const zoom = interpolate(frame, [0, 150], [1.05, 1.15]);

  return (
    <AbsoluteFill style={{fontFamily: theme.font}}>
      <AnimatedBackground />
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 40}}>
        <div
          style={{
            color: theme.cream,
            fontSize: 76,
            fontWeight: 800,
            textAlign: 'center',
            transform: `translateY(${(1 - titleIn) * 40}px)`,
            opacity: titleIn,
            letterSpacing: -2,
          }}
        >
          Becas Excelencia FCRA 2026
        </div>
        <div
          style={{
            width: 1100,
            borderRadius: 20,
            overflow: 'hidden',
            border: `1px solid ${theme.stroke}`,
            boxShadow: '0 30px 80px rgba(0,0,0,0.5)',
          }}
        >
          <Img src={staticFile('desktop.png')} style={{width: '100%', display: 'block', transform: `scale(${zoom})`}} />
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
