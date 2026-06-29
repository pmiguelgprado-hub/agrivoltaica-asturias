// Paleta cálida rural — coherente con el tema de la app agrivoltaica.
export const theme = {
  bg: '#1c1510',
  bgAlt: '#2a1f17',
  cream: '#f6efe3',
  amber: '#e8a13a', // sol
  amberSoft: '#f0c47a',
  green: '#7aa05a', // pasto
  greenDark: '#41502d',
  sky: '#8fb9cc',
  text: '#f6efe3',
  textDim: 'rgba(246,239,227,0.66)',
  card: 'rgba(28,21,16,0.55)',
  stroke: 'rgba(246,239,227,0.14)',
  font: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
};

export const FPS = 30;
export const sec = (s: number) => Math.round(s * FPS);
