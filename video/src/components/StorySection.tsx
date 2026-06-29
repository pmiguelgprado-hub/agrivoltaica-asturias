import React from 'react';
import {useCurrentFrame, spring, useVideoConfig, interpolate} from 'remotion';
import {theme} from '../theme';
import type {Block} from '../script';

// Panel izquierdo: chip de sección + titular grande + palabras-clave que
// hacen "pop" de forma escalonada. Es lo que da el aire "Nate Herk".
export const StorySection: React.FC<{
  block: Block;
  localDuration: number;
  hideKeywords?: boolean;
}> = ({block, localDuration, hideKeywords}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const titleIn = spring({frame, fps, durationInFrames: Math.round(0.8 * fps)});
  const chipIn = spring({frame, fps, durationInFrames: Math.round(0.5 * fps)});
  const outStart = localDuration - 10;
  const out = interpolate(frame, [outStart, localDuration], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const groupOpacity = 1 - out;

  return (
    <div
      style={{
        position: 'absolute',
        left: 90,
        top: 220,
        width: 880,
        fontFamily: theme.font,
        opacity: groupOpacity,
      }}
    >
      {/* chip */}
      <div
        style={{
          display: 'inline-block',
          padding: '10px 20px',
          borderRadius: 999,
          background: 'rgba(232,161,58,0.16)',
          border: `1px solid rgba(232,161,58,0.5)`,
          color: theme.amberSoft,
          fontSize: 24,
          fontWeight: 700,
          transform: `translateY(${(1 - chipIn) * 20}px)`,
          opacity: chipIn,
          marginBottom: 28,
        }}
      >
        {block.chip}
      </div>

      {/* titular */}
      <div
        style={{
          color: theme.cream,
          fontSize: 84,
          fontWeight: 800,
          lineHeight: 1.04,
          letterSpacing: -2,
          whiteSpace: 'pre-line',
          transform: `translateY(${(1 - titleIn) * 30}px)`,
          opacity: titleIn,
          textShadow: '0 6px 30px rgba(0,0,0,0.4)',
        }}
      >
        {block.title}
      </div>

      {/* palabras-clave escalonadas */}
      {!hideKeywords && (
      <div style={{marginTop: 40, display: 'flex', flexDirection: 'column', gap: 18}}>
        {block.keywords.map((kw, i) => {
          const delay = Math.round((0.9 + i * 0.45) * fps);
          const kIn = spring({frame: frame - delay, fps, durationInFrames: Math.round(0.5 * fps)});
          return (
            <div
              key={kw}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 16,
                transform: `translateX(${(1 - kIn) * -30}px)`,
                opacity: kIn,
              }}
            >
              <div
                style={{
                  width: 14,
                  height: 14,
                  borderRadius: 4,
                  background: theme.green,
                  flexShrink: 0,
                }}
              />
              <span style={{color: theme.text, fontSize: 36, fontWeight: 600}}>{kw}</span>
            </div>
          );
        })}
      </div>
      )}
    </div>
  );
};
