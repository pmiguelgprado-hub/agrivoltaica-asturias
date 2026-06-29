import React from 'react';
import {useCurrentFrame, spring, useVideoConfig, interpolate} from 'remotion';
import {theme} from '../theme';

// Rótulo inferior (nombre / cargo) que entra y sale con spring.
export const LowerThird: React.FC<{
  primary: string;
  secondary: string;
  outAtFrame: number;
}> = ({primary, secondary, outAtFrame}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({frame, fps, durationInFrames: Math.round(0.7 * fps)});
  const exit = interpolate(frame, [outAtFrame - 12, outAtFrame], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const y = (1 - enter) * 50 + exit * 50;
  const opacity = enter * (1 - exit);

  return (
    <div
      style={{
        position: 'absolute',
        left: 90,
        bottom: 120,
        transform: `translateY(${y}px)`,
        opacity,
        fontFamily: theme.font,
      }}
    >
      <div
        style={{
          display: 'inline-block',
          padding: '18px 30px',
          borderRadius: 16,
          background: theme.card,
          backdropFilter: 'blur(6px)',
          borderLeft: `5px solid ${theme.amber}`,
        }}
      >
        <div style={{color: theme.cream, fontSize: 42, fontWeight: 800, letterSpacing: -0.5}}>
          {primary}
        </div>
        <div style={{color: theme.textDim, fontSize: 26, marginTop: 4}}>{secondary}</div>
      </div>
    </div>
  );
};
