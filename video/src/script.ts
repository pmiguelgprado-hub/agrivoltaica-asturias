// Guion del vídeo (2 min) → bloques con tiempos, derivado de
// docs/2026-06-28-guion-video.md. Estilo "Equilibrado": los overlays ilustran
// TU historia; el proyecto (app) se concentra al cierre.
//
// Cada bloque: from/to en segundos, etiqueta de sección (chip), titular grande
// que aparece a la izquierda y palabras-clave que van haciendo "pop".

export type Block = {
  from: number;
  to: number;
  chip: string;
  title: string;
  keywords: string[];
  kind: 'intro' | 'story' | 'mindmap' | 'closing';
};

export const blocks: Block[] = [
  {
    from: 0,
    to: 15,
    chip: 'Quién soy',
    title: 'Pablo Miguel\nGonzález Prado',
    keywords: ['Máster Ing. Industrial', 'EPI Gijón · Uniovi'],
    kind: 'intro',
  },
  {
    from: 15,
    to: 40,
    chip: 'Por qué este máster',
    title: 'Resolver problemas\nreales con criterio',
    keywords: ['Ingeniería amplia', 'Energía', 'Industria asturiana'],
    kind: 'story',
  },
  {
    from: 40,
    to: 65,
    chip: 'Qué me aporta — a mí y a mi entorno',
    title: 'Devolver lo que\naprendo al territorio',
    keywords: ['Proyectos de energía', 'Sistemas eléctricos', 'Frenar la despoblación'],
    kind: 'mindmap',
  },
  {
    from: 65,
    to: 90,
    chip: 'Más allá de las notas',
    title: 'Lo que me\nhace yo',
    keywords: ['[Idiomas]', '[Deporte]', '[Voluntariado]', 'Me lo monto hasta que funciona'],
    kind: 'story',
  },
  {
    from: 90,
    to: 110,
    chip: 'Planes de futuro',
    title: 'Ingeniería de energía\ncon impacto en Asturias',
    keywords: ['Lo técnico + el territorio', 'Esta beca = más recorrido'],
    kind: 'story',
  },
  {
    from: 110,
    to: 120,
    chip: 'De la idea a la acción',
    title: 'Ya he construido\nla herramienta',
    keywords: ['Solar sin quitar el pasto', 'Agrivoltaica ganadera'],
    kind: 'closing',
  },
];

// Mapa mental del bloque "mindmap": centro + ramas.
export const mindmap = {
  center: 'Máster',
  branches: ['Energía', 'Sistemas\neléctricos', 'Valorar\ninversiones', 'Territorio\nrural'],
};
