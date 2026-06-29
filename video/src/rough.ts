import rough from 'roughjs';

// Genera trazos "a mano alzada" (motor de Excalidraw) de forma DETERMINISTA.
// Clave Remotion: con `seed` fijo, los paths son idénticos en cada frame → no
// "hierven". Calcula siempre dentro de useMemo SIN dependencia del frame.

const gen = rough.generator();

export type RPath = {d: string; stroke: string; strokeWidth: number; fill: string};

const toPaths = (drawable: ReturnType<typeof gen.rectangle>): RPath[] =>
  gen.toPaths(drawable).map((p) => ({
    d: p.d,
    stroke: p.stroke ?? 'none',
    strokeWidth: p.strokeWidth ?? 1,
    fill: p.fill ?? 'none',
  }));

// Rectángulo redondeado dibujado a mano (rough no redondea, usamos un path).
export const roughRoundedRect = (
  x: number,
  y: number,
  w: number,
  h: number,
  r: number,
  opts: {seed: number; fill?: string; stroke?: string; strokeWidth?: number},
): RPath[] => {
  const d =
    `M${x + r},${y} h${w - 2 * r} a${r},${r} 0 0 1 ${r},${r} v${h - 2 * r} ` +
    `a${r},${r} 0 0 1 ${-r},${r} h${-(w - 2 * r)} a${r},${r} 0 0 1 ${-r},${-r} ` +
    `v${-(h - 2 * r)} a${r},${r} 0 0 1 ${r},${-r} z`;
  return toPaths(
    gen.path(d, {
      roughness: 1.5,
      bowing: 1.2,
      fillStyle: 'solid',
      fill: opts.fill ?? 'transparent',
      stroke: opts.stroke ?? '#1b1b1b',
      strokeWidth: opts.strokeWidth ?? 2.4,
      seed: opts.seed,
    }),
  );
};

// Flecha a mano con punta (línea ligeramente curvada + dos trazos de cabeza).
export const roughArrow = (
  x1: number,
  y1: number,
  x2: number,
  y2: number,
  opts: {seed: number; stroke?: string; strokeWidth?: number},
): RPath[] => {
  const stroke = opts.stroke ?? '#1b1b1b';
  const strokeWidth = opts.strokeWidth ?? 2.4;
  const base = {roughness: 1.4, bowing: 2, stroke, strokeWidth, seed: opts.seed};
  // ligera curva: punto de control desplazado perpendicular
  const mx = (x1 + x2) / 2;
  const my = (y1 + y2) / 2;
  const dx = x2 - x1;
  const dy = y2 - y1;
  const len = Math.hypot(dx, dy) || 1;
  const nx = -dy / len;
  const ny = dx / len;
  const cx = mx + nx * 16;
  const cy = my + ny * 16;
  const line = toPaths(gen.curve([[x1, y1], [cx, cy], [x2, y2]], base));
  // cabeza de flecha
  const ang = Math.atan2(y2 - cy, x2 - cx);
  const head = 16;
  const a1 = ang + Math.PI - 0.45;
  const a2 = ang + Math.PI + 0.45;
  const h1 = toPaths(
    gen.line(x2, y2, x2 + Math.cos(a1) * head, y2 + Math.sin(a1) * head, {...base, seed: opts.seed + 1}),
  );
  const h2 = toPaths(
    gen.line(x2, y2, x2 + Math.cos(a2) * head, y2 + Math.sin(a2) * head, {...base, seed: opts.seed + 2}),
  );
  return [...line, ...h1, ...h2];
};

// Subrayado a mano (para resaltar una palabra del titular).
export const roughUnderline = (
  x: number,
  y: number,
  w: number,
  opts: {seed: number; stroke?: string; strokeWidth?: number},
): RPath[] =>
  toPaths(
    gen.line(x, y, x + w, y, {
      roughness: 1.8,
      bowing: 3,
      stroke: opts.stroke ?? '#e8a13a',
      strokeWidth: opts.strokeWidth ?? 5,
      seed: opts.seed,
    }),
  );
