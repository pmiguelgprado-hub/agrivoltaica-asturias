import React from 'react';
import {Img, staticFile, useCurrentFrame, useVideoConfig, interpolate, spring} from 'remotion';

// iPhone realista (Dynamic Island, biseles, esquinas) con la captura de la app
// haciendo scroll vertical lento dentro de la pantalla.
export const PhoneMockup: React.FC<{
  src: string;
  imgWidth: number;
  imgHeight: number;
  durationInFrames: number;
}> = ({src, imgWidth, imgHeight, durationInFrames}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const outerW = 470;
  const outerH = 952;
  const bezel = 15;
  const screenW = outerW - bezel * 2;
  const screenH = outerH - bezel * 2;

  // la imagen se escala al ancho de pantalla; scroll = de arriba hasta el final
  const scaledH = (imgHeight / imgWidth) * screenW;
  const maxScroll = Math.max(0, scaledH - screenH);
  const scrollY = interpolate(frame, [Math.round(0.8 * fps), durationInFrames - Math.round(0.5 * fps)], [0, -maxScroll], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const enter = spring({frame, fps, durationInFrames: Math.round(0.8 * fps)});

  return (
    <div
      style={{
        width: outerW,
        height: outerH,
        borderRadius: 62,
        background: 'linear-gradient(145deg, #2a2a2e, #0c0c0e)',
        padding: bezel,
        boxShadow: '0 40px 110px rgba(0,0,0,0.6), inset 0 0 0 2px rgba(255,255,255,0.06)',
        transform: `translateY(${(1 - enter) * 40}px) scale(${0.94 + enter * 0.06})`,
        opacity: enter,
        position: 'relative',
      }}
    >
      {/* pantalla */}
      <div
        style={{
          width: screenW,
          height: screenH,
          borderRadius: 48,
          overflow: 'hidden',
          background: '#fff',
          position: 'relative',
        }}
      >
        <Img
          src={staticFile(src)}
          style={{
            width: screenW,
            display: 'block',
            transform: `translateY(${scrollY}px)`,
          }}
        />
      </div>

      {/* Dynamic Island */}
      <div
        style={{
          position: 'absolute',
          top: bezel + 14,
          left: '50%',
          transform: 'translateX(-50%)',
          width: 122,
          height: 35,
          borderRadius: 20,
          background: '#000',
          zIndex: 2,
        }}
      />
    </div>
  );
};
