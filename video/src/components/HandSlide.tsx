import React, {useMemo} from 'react';
import {AbsoluteFill, useCurrentFrame, spring, useVideoConfig, interpolate} from 'remotion';
import {loadFont} from '@remotion/google-fonts/Kalam';
import {roughUnderline} from '../rough';

const {fontFamily: hand} = loadFont();
export const HAND = hand;
export const INK = '#1b1b1b';
export const CANVAS = '#0d0d0d';

// Tarjeta blanca infografía sobre canvas negro + titular manuscrito con
// subrayado a mano opcional. Estilo Excalidraw/Nate Herk.
export const HandSlide: React.FC<{
  heading?: string;
  underline?: {x: number; w: number; y: number};
  children?: React.ReactNode;
  pad?: number;
}> = ({heading, underline, children, pad = 64}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const headIn = spring({frame, fps, durationInFrames: Math.round(0.6 * fps)});

  const underPaths = useMemo(
    () => (underline ? roughUnderline(underline.x, underline.y, underline.w, {seed: 31}) : []),
    [underline],
  );
  const underOp = interpolate(frame, [12, 24], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill style={{backgroundColor: CANVAS}}>
      <div
        style={{
          position: 'absolute',
          left: 80,
          top: 80,
          right: 80,
          bottom: 80,
          background: '#fbfaf7',
          borderRadius: 26,
          boxShadow: '0 30px 90px rgba(0,0,0,0.5)',
          overflow: 'hidden',
          fontFamily: hand,
        }}
      >
        {heading && (
          <div
            style={{
              position: 'absolute',
              left: pad,
              top: 54,
              fontFamily: hand,
              fontWeight: 700,
              fontSize: 60,
              color: INK,
              opacity: headIn,
              transform: `translateY(${(1 - headIn) * 16}px)`,
            }}
          >
            {heading}
          </div>
        )}
        {underline && (
          <svg width="100%" height="100%" style={{position: 'absolute', inset: 0, pointerEvents: 'none'}}>
            <g opacity={underOp}>
              {underPaths.map((p, i) => (
                <path key={i} d={p.d} stroke={p.stroke} strokeWidth={p.strokeWidth} fill="none" strokeLinecap="round" />
              ))}
            </g>
          </svg>
        )}
        {children}
      </div>
    </AbsoluteFill>
  );
};
