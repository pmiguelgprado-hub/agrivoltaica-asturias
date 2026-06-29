import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {theme, sec} from './theme';
import {blocks} from './script';
import {AnimatedBackground} from './components/AnimatedBackground';
import {FaceCam} from './components/FaceCam';
import {StorySection} from './components/StorySection';
import {MindMap} from './components/MindMap';
import {ScreenshotShowcase} from './components/ScreenshotShowcase';
import {LowerThird} from './components/LowerThird';
import {ProgressBar} from './components/ProgressBar';

export type BecaVideoProps = {
  hasFootage: boolean;
};

// Vídeo de motivación de 2 min (Anexo 2). Estilo "Equilibrado":
// la cara de Pablo conduce; los overlays ilustran SU historia; el proyecto
// (la app) protagoniza solo el cierre.
//
// IMPORTANTE: la cámara se monta UNA sola vez a nivel raíz y dura los 120 s.
// Si se metiera dentro de cada <Sequence>, el OffthreadVideo reiniciaría el
// clip (y su audio) en cada bloque. En el cierre, un fondo opaco la tapa pero
// el audio sigue sonando (la narración final va en la misma toma continua).
export const BecaVideo: React.FC<BecaVideoProps> = ({hasFootage}) => {
  return (
    <AbsoluteFill style={{backgroundColor: theme.bg, fontFamily: theme.font}}>
      <AnimatedBackground />

      {/* Cámara continua: una sola instancia, todo el vídeo. */}
      <FaceCam hasFootage={hasFootage} />

      {blocks.map((block) => {
        const from = sec(block.from);
        const dur = sec(block.to - block.from);
        const isClosing = block.kind === 'closing';
        const isMindmap = block.kind === 'mindmap';

        return (
          <Sequence key={block.from} from={from} durationInFrames={dur}>
            {isClosing ? (
              // Fondo opaco que tapa la cámara (el audio sigue) + la app.
              <>
                <AnimatedBackground />
                <ScreenshotShowcase durationInFrames={dur} />
              </>
            ) : (
              <>
                <StorySection block={block} localDuration={dur} hideKeywords={isMindmap} />
                {isMindmap && (
                  <div
                    style={{
                      position: 'absolute',
                      left: 30,
                      top: 360,
                      transform: 'scale(0.78)',
                      transformOrigin: 'top left',
                    }}
                  >
                    <MindMap />
                  </div>
                )}
              </>
            )}
          </Sequence>
        );
      })}

      {/* rótulo de nombre durante la presentación */}
      <Sequence from={sec(2)} durationInFrames={sec(11)}>
        <LowerThird
          primary="Pablo Miguel González Prado"
          secondary="Máster en Ingeniería Industrial · EPI Gijón"
          outAtFrame={sec(11) - 1}
        />
      </Sequence>

      <ProgressBar />
    </AbsoluteFill>
  );
};
