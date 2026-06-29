import React from 'react';
import {AbsoluteFill, OffthreadVideo, staticFile, useCurrentFrame, spring, useVideoConfig} from 'remotion';
import {theme} from '../theme';

// Cámara de Pablo a la derecha. Si hay grabación (public/pablo.mp4) la muestra;
// si no, enseña un marcador con instrucciones de grabación.
export const FaceCam: React.FC<{hasFootage: boolean}> = ({hasFootage}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({frame, fps, durationInFrames: Math.round(0.8 * fps)});
  const x = (1 - enter) * 80;

  return (
    <AbsoluteFill
      style={{
        alignItems: 'flex-end',
        justifyContent: 'center',
        paddingRight: 70,
      }}
    >
      <div
        style={{
          width: 760,
          height: 860,
          borderRadius: 28,
          overflow: 'hidden',
          transform: `translateX(${x}px)`,
          opacity: enter,
          border: `1px solid ${theme.stroke}`,
          boxShadow: '0 30px 80px rgba(0,0,0,0.45)',
          background: theme.bgAlt,
          position: 'relative',
        }}
      >
        {hasFootage ? (
          <OffthreadVideo
            src={staticFile('pablo.mp4')}
            style={{width: '100%', height: '100%', objectFit: 'cover'}}
          />
        ) : (
          <PlaceholderCam />
        )}
      </div>
    </AbsoluteFill>
  );
};

const PlaceholderCam: React.FC = () => (
  <AbsoluteFill
    style={{
      alignItems: 'center',
      justifyContent: 'center',
      flexDirection: 'column',
      gap: 22,
      border: `3px dashed ${theme.stroke}`,
      borderRadius: 28,
      margin: 18,
      textAlign: 'center',
      padding: 40,
      fontFamily: theme.font,
    }}
  >
    <div style={{fontSize: 90}}>🎬</div>
    <div style={{color: theme.cream, fontSize: 38, fontWeight: 700}}>Tu vídeo aquí</div>
    <div style={{color: theme.textDim, fontSize: 24, lineHeight: 1.5, maxWidth: 520}}>
      Graba en horizontal, cara y hombros, luz por delante.
      <br />
      Guárdalo como <b style={{color: theme.amberSoft}}>public/pablo.mp4</b> y pon{' '}
      <b style={{color: theme.amberSoft}}>hasFootage: true</b>.
    </div>
  </AbsoluteFill>
);
