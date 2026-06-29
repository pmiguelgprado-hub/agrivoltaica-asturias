import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, spring, useVideoConfig, interpolate, Sequence} from 'remotion';
import {theme} from '../theme';

// Cierre: la herramienta entra en escena con un suave Ken Burns + rótulo.
// Aquí SÍ protagoniza el proyecto (decisión "Equilibrado": al final).
type Shot = {file: string; caption: string};

const defaultShots: Shot[] = [
  {file: 'desktop.png', caption: 'Calcula la energía de una finca con datos reales (PVGIS)'},
  {file: 'impacto.png', caption: 'Ahorro, amortización y luz que sigue llegando al pasto'},
];

export const ScreenshotShowcase: React.FC<{durationInFrames: number; shots?: Shot[]}> = ({
  durationInFrames,
  shots = defaultShots,
}) => {
  const per = Math.floor(durationInFrames / shots.length);
  return (
    <AbsoluteFill>
      {shots.map((s, i) => (
        <Sequence key={s.file} from={i * per} durationInFrames={per}>
          <Shot file={s.file} caption={s.caption} duration={per} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

const Shot: React.FC<{file: string; caption: string; duration: number}> = ({file, caption, duration}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({frame, fps, durationInFrames: Math.round(0.6 * fps)});
  const zoom = interpolate(frame, [0, duration], [1.04, 1.12]);
  const fade = interpolate(frame, [duration - 10, duration], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', opacity: enter * fade}}>
      <div
        style={{
          width: 1360,
          height: 740,
          borderRadius: 22,
          overflow: 'hidden',
          border: `1px solid ${theme.stroke}`,
          boxShadow: '0 40px 100px rgba(0,0,0,0.5)',
        }}
      >
        <Img
          src={staticFile(file)}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            objectPosition: 'top center',
            display: 'block',
            transform: `scale(${zoom})`,
          }}
        />
      </div>
      <div
        style={{
          marginTop: 36,
          color: theme.cream,
          fontFamily: theme.font,
          fontSize: 40,
          fontWeight: 700,
          textAlign: 'center',
          maxWidth: 1300,
          textShadow: '0 4px 24px rgba(0,0,0,0.5)',
        }}
      >
        {caption}
      </div>
    </AbsoluteFill>
  );
};
