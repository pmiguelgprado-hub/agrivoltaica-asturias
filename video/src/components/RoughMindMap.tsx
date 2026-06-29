import React, {useMemo} from 'react';
import {useCurrentFrame, spring, useVideoConfig, interpolate} from 'remotion';
import {loadFont} from '@remotion/google-fonts/Kalam';
import {roughRoundedRect, roughArrow, roughUnderline, RPath} from '../rough';

const {fontFamily: hand} = loadFont();

const ink = '#1b1b1b';

type Node = {
  id: string;
  x: number;
  y: number;
  w: number;
  h: number;
  file: string;
  role: string;
  icon: string;
  fill: string;
};

const W = 190;
const H = 104;

const nodes: Node[] = [
  {id: 'pvgis', x: 70, y: 130, w: W, h: H, file: 'PVGIS', role: 'datos solares reales', icon: '🛰️', fill: '#e9f1f6'},
  {id: 'solar', x: 80, y: 380, w: W, h: H, file: 'solar.py', role: 'producción FV', icon: '☀️', fill: '#fdf3e2'},
  {id: 'agri', x: 350, y: 408, w: W, h: H, file: 'agrivoltaic.py', role: 'energía ↔ pasto', icon: '⚖️', fill: '#edf5e6'},
  {id: 'perfil', x: 620, y: 380, w: W, h: H, file: 'perfil.py', role: 'autoconsumo horario', icon: '⏱️', fill: '#f2edf7'},
  {id: 'econ', x: 890, y: 408, w: W, h: H, file: 'economics.py', role: 'ahorro · payback', icon: '💶', fill: '#fdf3e2'},
  {id: 'informe', x: 1170, y: 210, w: W, h: H, file: 'informe.py', role: 'informe imprimible', icon: '🖨️', fill: '#f0f0f0'},
  {id: 'impacto', x: 1170, y: 560, w: W, h: H, file: 'impacto.py', role: 'granja → concejo', icon: '📍', fill: '#edf5e6'},
];

const byId = (id: string) => nodes.find((n) => n.id === id)!;
const rightC = (n: Node) => [n.x + n.w, n.y + n.h / 2] as const;
const leftC = (n: Node) => [n.x, n.y + n.h / 2] as const;
const botC = (n: Node) => [n.x + n.w / 2, n.y + n.h] as const;
const topC = (n: Node) => [n.x + n.w / 2, n.y] as const;

type Edge = {from: readonly [number, number]; to: readonly [number, number]; seed: number; afterIndex: number};

const edges: Edge[] = [
  {from: botC(byId('pvgis')), to: topC(byId('solar')), seed: 91, afterIndex: 1},
  {from: rightC(byId('solar')), to: leftC(byId('agri')), seed: 92, afterIndex: 2},
  {from: rightC(byId('agri')), to: leftC(byId('perfil')), seed: 93, afterIndex: 3},
  {from: rightC(byId('perfil')), to: leftC(byId('econ')), seed: 94, afterIndex: 4},
  {from: [byId('econ').x + byId('econ').w, byId('econ').y + 28], to: leftC(byId('informe')), seed: 95, afterIndex: 5},
  {from: [byId('econ').x + byId('econ').w, byId('econ').y + 76], to: leftC(byId('impacto')), seed: 96, afterIndex: 6},
];

// Mapa mental "a mano" estilo Excalidraw/Nate Herk dentro de una tarjeta blanca.
export const RoughMindMap: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  // Trazos rough: deterministas (seed fijo), memorizados sin depender del frame.
  const nodePaths = useMemo(
    () => nodes.map((n, i) => roughRoundedRect(n.x, n.y, n.w, n.h, 16, {seed: 10 + i, fill: n.fill})),
    [],
  );
  const edgePaths = useMemo(
    () => edges.map((e) => roughArrow(e.from[0], e.from[1], e.to[0], e.to[1], {seed: e.seed})),
    [],
  );
  const underline = useMemo(() => roughUnderline(470, 152, 330, {seed: 77}), []);

  const headIn = spring({frame, fps, durationInFrames: Math.round(0.6 * fps)});

  return (
    <div
      style={{
        position: 'absolute',
        left: 80,
        top: 80,
        width: 1760,
        height: 920,
        background: '#fbfaf7',
        borderRadius: 26,
        boxShadow: '0 30px 90px rgba(0,0,0,0.5)',
        overflow: 'hidden',
        fontFamily: hand,
      }}
    >
      {/* titular a mano con palabra subrayada */}
      <div
        style={{
          position: 'absolute',
          left: 64,
          top: 58,
          fontFamily: hand,
          fontWeight: 700,
          fontSize: 60,
          color: ink,
          opacity: headIn,
          transform: `translateY(${(1 - headIn) * 16}px)`,
        }}
      >
        Cómo se calcula, paso a paso
      </div>

      <svg width={1760} height={920} style={{position: 'absolute', inset: 0}}>
        {/* subrayado */}
        <g opacity={interpolate(frame, [10, 22], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}>
          {underline.map((p, i) => (
            <path key={`u${i}`} d={p.d} stroke={p.stroke} strokeWidth={p.strokeWidth} fill="none" strokeLinecap="round" />
          ))}
        </g>

        {/* flechas */}
        {edgePaths.map((paths, ei) => {
          const delay = Math.round((0.5 + edges[ei].afterIndex * 0.45) * fps);
          const op = interpolate(frame - delay, [0, 8], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
          return (
            <g key={`e${ei}`} opacity={op}>
              {paths.map((p, i) => (
                <path key={i} d={p.d} stroke={p.stroke} strokeWidth={p.strokeWidth} fill="none" strokeLinecap="round" />
              ))}
            </g>
          );
        })}

        {/* nodos (caja rough) */}
        {nodePaths.map((paths, ni) => {
          const delay = Math.round((0.4 + ni * 0.45) * fps);
          const pop = spring({frame: frame - delay, fps, durationInFrames: Math.round(0.5 * fps)});
          const n = nodes[ni];
          const cx = n.x + n.w / 2;
          const cy = n.y + n.h / 2;
          return (
            <g key={`n${ni}`} opacity={pop} transform={`translate(${cx} ${cy}) scale(${0.85 + pop * 0.15}) translate(${-cx} ${-cy})`}>
              {paths.map((p: RPath, i) => (
                <path key={i} d={p.d} stroke={p.stroke} strokeWidth={p.strokeWidth} fill={p.fill} strokeLinecap="round" />
              ))}
            </g>
          );
        })}
      </svg>

      {/* etiquetas HTML sobre los nodos (alineadas a coords del SVG) */}
      {nodes.map((n, ni) => {
        const delay = Math.round((0.4 + ni * 0.45) * fps);
        const pop = spring({frame: frame - delay, fps, durationInFrames: Math.round(0.5 * fps)});
        return (
          <div
            key={n.id}
            style={{
              position: 'absolute',
              left: n.x,
              top: n.y,
              width: n.w,
              height: n.h,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              gap: 2,
              opacity: pop,
              fontFamily: hand,
              textAlign: 'center',
              padding: '0 8px',
            }}
          >
            <div style={{fontSize: 26}}>{n.icon}</div>
            <div style={{fontWeight: 700, fontSize: 26, color: ink, lineHeight: 1}}>{n.file}</div>
            <div style={{fontWeight: 400, fontSize: 19, color: '#5a554e', lineHeight: 1.05}}>{n.role}</div>
          </div>
        );
      })}

      {/* conclusión abajo */}
      <FooterNote frame={frame} fps={fps} />
    </div>
  );
};

const FooterNote: React.FC<{frame: number; fps: number}> = ({frame, fps}) => {
  const delay = Math.round(3.4 * fps);
  const op = interpolate(frame - delay, [0, 12], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div
      style={{
        position: 'absolute',
        left: 64,
        bottom: 48,
        right: 64,
        background: '#fcf3df',
        border: '2px solid #e8a13a',
        borderRadius: 14,
        padding: '18px 26px',
        fontFamily: hand,
        fontSize: 28,
        color: ink,
        opacity: op,
      }}
    >
      ☀️ Cada módulo pasa su resultado al siguiente — todo parte de datos reales de PVGIS.
    </div>
  );
};
