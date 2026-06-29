import React from 'react';
import {useCurrentFrame, spring, useVideoConfig} from 'remotion';
import {theme} from '../theme';
import {mindmap} from '../script';

// Mapa mental: nodo central "Máster" del que brotan ramas. Las líneas se
// dibujan y los nodos hacen pop escalonado.
export const MindMap: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const cx = 470;
  const cy = 470;
  const radius = 250;
  const branches = mindmap.branches;

  const centerIn = spring({frame, fps, durationInFrames: Math.round(0.6 * fps)});

  return (
    <div style={{position: 'relative', width: 940, height: 900}}>
      <svg width={940} height={900} style={{position: 'absolute', inset: 0}}>
        {branches.map((b, i) => {
          const angle = (Math.PI * 2 * i) / branches.length - Math.PI / 2;
          const x = cx + Math.cos(angle) * radius;
          const y = cy + Math.sin(angle) * radius;
          const delay = Math.round((0.5 + i * 0.35) * fps);
          const draw = spring({frame: frame - delay, fps, durationInFrames: Math.round(0.5 * fps)});
          const lx = cx + (x - cx) * draw;
          const ly = cy + (y - cy) * draw;
          return (
            <line
              key={i}
              x1={cx}
              y1={cy}
              x2={lx}
              y2={ly}
              stroke={theme.amber}
              strokeWidth={3}
              strokeOpacity={0.6}
            />
          );
        })}
      </svg>

      {branches.map((b, i) => {
        const angle = (Math.PI * 2 * i) / branches.length - Math.PI / 2;
        const x = cx + Math.cos(angle) * radius;
        const y = cy + Math.sin(angle) * radius;
        const delay = Math.round((0.8 + i * 0.35) * fps);
        const pop = spring({frame: frame - delay, fps, durationInFrames: Math.round(0.5 * fps)});
        return (
          <Node key={i} x={x} y={y} label={b} scale={pop} accent={theme.green} size={150} fontSize={26} />
        );
      })}

      <Node x={cx} y={cy} label={mindmap.center} scale={centerIn} accent={theme.amber} size={190} fontSize={40} bold />
    </div>
  );
};

const Node: React.FC<{
  x: number;
  y: number;
  label: string;
  scale: number;
  accent: string;
  size: number;
  fontSize: number;
  bold?: boolean;
}> = ({x, y, label, scale, accent, size, fontSize, bold}) => (
  <div
    style={{
      position: 'absolute',
      left: x - size / 2,
      top: y - size / 2,
      width: size,
      height: size,
      borderRadius: '50%',
      background: theme.card,
      border: `2px solid ${accent}`,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      textAlign: 'center',
      transform: `scale(${scale})`,
      opacity: scale,
      color: theme.cream,
      fontFamily: theme.font,
      fontSize,
      fontWeight: bold ? 800 : 600,
      lineHeight: 1.1,
      padding: 12,
      whiteSpace: 'pre-line',
      boxShadow: `0 10px 40px rgba(0,0,0,0.35)`,
    }}
  >
    {label}
  </div>
);
