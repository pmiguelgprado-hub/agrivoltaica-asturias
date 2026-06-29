import React, {useMemo} from 'react';
import {AbsoluteFill, Sequence, useCurrentFrame, spring, useVideoConfig, interpolate} from 'remotion';
import {sec} from './theme';
import {HandSlide, HAND, INK, CANVAS} from './components/HandSlide';
import {RoughMindMap} from './components/RoughMindMap';
import {RoughStats, Stat} from './components/RoughStats';
import {PhoneMockup} from './components/PhoneMockup';
import {ProgressBar} from './components/ProgressBar';
import {roughRoundedRect, roughArrow} from './rough';

const stats: Stat[] = [
  {value: '47', label: 'pruebas automáticas en verde', fill: '#edf5e6'},
  {value: '≈20.900', label: 'kWh/año (40 vacas · 17 kWp · Tineo)', fill: '#fdf3e2'},
  {value: '≈1.900 €', label: 'de ahorro al año en la factura', fill: '#fdf3e2'},
  {value: '65 %', label: 'de luz que sigue llegando al pasto', fill: '#edf5e6'},
  {value: '8–9 años', label: 'de amortización con ayudas', fill: '#f2edf7'},
  {value: '≈200 t', label: 'CO₂/año evitadas (escenario concejo)', fill: '#e9f1f6'},
];

export const Estructura: React.FC = () => {
  return (
    <AbsoluteFill style={{backgroundColor: CANVAS}}>
      <Sequence durationInFrames={sec(5)}>
        <Portada />
      </Sequence>

      <Sequence from={sec(5)} durationInFrames={sec(8)}>
        <QueEs />
      </Sequence>

      <Sequence from={sec(13)} durationInFrames={sec(22)}>
        <RoughMindMap />
      </Sequence>

      <Sequence from={sec(35)} durationInFrames={sec(14)}>
        <AppSlide durationInFrames={sec(14)} />
      </Sequence>

      <Sequence from={sec(49)} durationInFrames={sec(9)}>
        <HandSlide heading="En cifras, lo que dice" underline={{x: 470, y: 150, w: 360}}>
          <RoughStats stats={stats} />
        </HandSlide>
      </Sequence>

      <Sequence from={sec(58)} durationInFrames={sec(4)}>
        <Cierre />
      </Sequence>

      <ProgressBar />
    </AbsoluteFill>
  );
};

// ---- portada ----
const Portada: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = spring({frame, fps, durationInFrames: Math.round(1 * fps)});
  const sub = spring({frame: frame - Math.round(0.5 * fps), fps, durationInFrames: Math.round(0.8 * fps)});
  return (
    <HandSlide>
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 24, fontFamily: HAND}}>
        <div style={{fontSize: 110, opacity: t, transform: `scale(${0.7 + t * 0.3})`}}>🐄☀️</div>
        <div
          style={{
            fontFamily: HAND,
            fontWeight: 700,
            fontSize: 96,
            color: INK,
            textAlign: 'center',
            lineHeight: 1.02,
            maxWidth: 1400,
            opacity: t,
            transform: `translateY(${(1 - t) * 28}px)`,
          }}
        >
          Agrivoltaica ganadera asturiana
        </div>
        <div style={{fontFamily: HAND, fontSize: 44, color: '#d6892a', opacity: sub}}>
          estructura del proyecto · beca FCRA 2026
        </div>
      </AbsoluteFill>
    </HandSlide>
  );
};

// ---- qué es ----
const QueEs: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const lead = spring({frame, fps, durationInFrames: Math.round(0.9 * fps)});
  const pillars = [
    {t: 'Preciso', fill: '#edf5e6', seed: 61},
    {t: 'Visual', fill: '#e9f1f6', seed: 62},
    {t: 'Accesible', fill: '#fdf3e2', seed: 63},
  ];
  const PW = 380;
  const PH = 150;
  const xs = [120, 540, 960];
  const py = 560;
  const boxes = useMemo(
    () => pillars.map((p, i) => roughRoundedRect(xs[i], py, PW, PH, 16, {seed: p.seed, fill: p.fill})),
    [],
  );
  return (
    <HandSlide heading="¿Qué es?" underline={{x: 66, y: 150, w: 210}}>
      <div
        style={{
          position: 'absolute',
          left: 66,
          top: 230,
          width: 1500,
          fontFamily: HAND,
          fontSize: 58,
          fontWeight: 400,
          color: INK,
          lineHeight: 1.3,
          opacity: lead,
          transform: `translateY(${(1 - lead) * 22}px)`,
        }}
      >
        Una calculadora que estima, para una granja real, su energía solar, el ahorro y la luz
        que le queda al pasto — <span style={{color: '#d6892a'}}>sin sacar el suelo de la ganadería</span>.
      </div>
      <svg width="100%" height="100%" style={{position: 'absolute', inset: 0}}>
        {boxes.map((paths, i) => {
          const delay = Math.round((0.9 + i * 0.3) * fps);
          const pop = spring({frame: frame - delay, fps, durationInFrames: Math.round(0.5 * fps)});
          const cx = xs[i] + PW / 2;
          const cy = py + PH / 2;
          return (
            <g key={i} opacity={pop} transform={`translate(${cx} ${cy}) scale(${0.88 + pop * 0.12}) translate(${-cx} ${-cy})`}>
              {paths.map((p, j) => (
                <path key={j} d={p.d} stroke={p.stroke} strokeWidth={p.strokeWidth} fill={p.fill} strokeLinecap="round" />
              ))}
            </g>
          );
        })}
      </svg>
      {pillars.map((p, i) => {
        const delay = Math.round((0.9 + i * 0.3) * fps);
        const pop = spring({frame: frame - delay, fps, durationInFrames: Math.round(0.5 * fps)});
        return (
          <div
            key={p.t}
            style={{
              position: 'absolute',
              left: xs[i],
              top: py,
              width: PW,
              height: PH,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontFamily: HAND,
              fontWeight: 700,
              fontSize: 52,
              color: INK,
              opacity: pop,
            }}
          >
            {p.t}
          </div>
        );
      })}
    </HandSlide>
  );
};

// ---- app en iPhone ----
const AppSlide: React.FC<{durationInFrames: number}> = ({durationInFrames}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const headIn = spring({frame, fps, durationInFrames: Math.round(0.7 * fps)});

  const callouts = [
    {text: 'Una sola pantalla,\npocos datos', x: 1080, y: 250, from: [1060, 300], to: [710, 360], seed: 71},
    {text: 'Pensada para el móvil\ndel ganadero', x: 1080, y: 700, from: [1060, 740], to: [710, 760], seed: 73},
  ];
  const arrows = useMemo(
    () => callouts.map((c) => roughArrow(c.from[0], c.from[1], c.to[0], c.to[1], {seed: c.seed, stroke: '#f0c47a'})),
    [],
  );

  return (
    <AbsoluteFill style={{backgroundColor: CANVAS, fontFamily: HAND}}>
      <div style={{position: 'absolute', left: 240, top: 64}}>
        <PhoneMockup src="movil.png" imgWidth={800} imgHeight={3800} durationInFrames={durationInFrames} />
      </div>

      <div
        style={{
          position: 'absolute',
          left: 760,
          top: 110,
          fontFamily: HAND,
          fontWeight: 700,
          fontSize: 76,
          color: '#f6efe3',
          opacity: headIn,
          transform: `translateY(${(1 - headIn) * 18}px)`,
          width: 1040,
          lineHeight: 1.05,
        }}
      >
        La herramienta, en el móvil
      </div>

      <svg width="100%" height="100%" style={{position: 'absolute', inset: 0, pointerEvents: 'none'}}>
        {arrows.map((paths, ai) => {
          const delay = Math.round((1.2 + ai * 0.6) * fps);
          const op = interpolate(frame - delay, [0, 10], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
          return (
            <g key={ai} opacity={op}>
              {paths.map((p, i) => (
                <path key={i} d={p.d} stroke={p.stroke} strokeWidth={p.strokeWidth} fill="none" strokeLinecap="round" />
              ))}
            </g>
          );
        })}
      </svg>

      {callouts.map((c, i) => {
        const delay = Math.round((1.2 + i * 0.6) * fps);
        const pop = spring({frame: frame - delay, fps, durationInFrames: Math.round(0.5 * fps)});
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: c.x,
              top: c.y,
              fontFamily: HAND,
              fontWeight: 700,
              fontSize: 44,
              color: '#f6efe3',
              whiteSpace: 'pre-line',
              opacity: pop,
              transform: `translateY(${(1 - pop) * 14}px)`,
            }}
          >
            {c.text}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// ---- cierre ----
const Cierre: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = spring({frame, fps, durationInFrames: Math.round(0.8 * fps)});
  return (
    <HandSlide>
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 22, fontFamily: HAND}}>
        <div style={{fontFamily: HAND, fontWeight: 700, fontSize: 84, color: INK, opacity: t, transform: `scale(${0.9 + t * 0.1})`}}>
          agrivoltaica-asturias
        </div>
        <div style={{fontFamily: HAND, fontSize: 40, color: '#5a554e', opacity: t}}>
          47 tests · datos PVGIS · Python + Streamlit · licencia 0 €
        </div>
      </AbsoluteFill>
    </HandSlide>
  );
};
