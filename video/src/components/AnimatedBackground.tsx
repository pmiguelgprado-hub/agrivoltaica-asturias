import React from 'react';
import {AbsoluteFill, useCurrentFrame, interpolate} from 'remotion';
import {theme} from '../theme';

// Fondo cálido con un "sol" que respira suave y un horizonte de pradera.
export const AnimatedBackground: React.FC = () => {
  const frame = useCurrentFrame();
  const sunY = interpolate(Math.sin(frame / 90), [-1, 1], [-12, 12]);
  const glow = interpolate(Math.sin(frame / 70), [-1, 1], [0.35, 0.55]);

  return (
    <AbsoluteFill style={{backgroundColor: theme.bg}}>
      <AbsoluteFill
        style={{
          background: `radial-gradient(1100px 700px at 26% ${30 + sunY}%, rgba(232,161,58,${glow}), transparent 60%)`,
        }}
      />
      <AbsoluteFill
        style={{
          background: `radial-gradient(900px 600px at 85% 110%, rgba(122,160,90,0.35), transparent 60%)`,
        }}
      />
      {/* horizonte de pradera */}
      <AbsoluteFill
        style={{
          top: 'auto',
          height: 160,
          background: `linear-gradient(180deg, transparent, ${theme.greenDark})`,
          opacity: 0.5,
        }}
      />
    </AbsoluteFill>
  );
};
