import React, {useMemo} from 'react';
import {useCurrentFrame, spring, useVideoConfig} from 'remotion';
import {HAND, INK} from './HandSlide';
import {roughRoundedRect} from '../rough';

export type Stat = {value: string; label: string; fill: string};

const BW = 500;
const BH = 224;
const COLS = [64, 604, 1144];
const ROWS = [250, 514];

// Cifras clave en cajas dibujadas a mano (rough), aparecen escalonadas.
export const RoughStats: React.FC<{stats: Stat[]}> = ({stats}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const boxes = useMemo(
    () =>
      stats.map((s, i) => {
        const x = COLS[i % 3];
        const y = ROWS[Math.floor(i / 3)];
        return {x, y, paths: roughRoundedRect(x, y, BW, BH, 16, {seed: 40 + i, fill: s.fill}), stat: s};
      }),
    [stats],
  );

  return (
    <>
      <svg width="100%" height="100%" style={{position: 'absolute', inset: 0}}>
        {boxes.map((b, i) => {
          const delay = Math.round((0.3 + i * 0.22) * fps);
          const pop = spring({frame: frame - delay, fps, durationInFrames: Math.round(0.5 * fps)});
          const cx = b.x + BW / 2;
          const cy = b.y + BH / 2;
          return (
            <g key={i} opacity={pop} transform={`translate(${cx} ${cy}) scale(${0.88 + pop * 0.12}) translate(${-cx} ${-cy})`}>
              {b.paths.map((p, j) => (
                <path key={j} d={p.d} stroke={p.stroke} strokeWidth={p.strokeWidth} fill={p.fill} strokeLinecap="round" />
              ))}
            </g>
          );
        })}
      </svg>
      {boxes.map((b, i) => {
        const delay = Math.round((0.3 + i * 0.22) * fps);
        const pop = spring({frame: frame - delay, fps, durationInFrames: Math.round(0.5 * fps)});
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: b.x,
              top: b.y,
              width: BW,
              height: BH,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              gap: 6,
              opacity: pop,
              fontFamily: HAND,
              textAlign: 'center',
              padding: '0 24px',
            }}
          >
            <div style={{fontWeight: 700, fontSize: 72, color: '#d6892a', lineHeight: 1}}>{b.stat.value}</div>
            <div style={{fontWeight: 400, fontSize: 26, color: INK, lineHeight: 1.2}}>{b.stat.label}</div>
          </div>
        );
      })}
    </>
  );
};
