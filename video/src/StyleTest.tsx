import React from 'react';
import {AbsoluteFill} from 'remotion';
import {RoughMindMap} from './components/RoughMindMap';

// Prueba de estilo: una sola slide (el mapa mental hand-drawn) sobre canvas
// oscuro tipo Excalidraw/Nate Herk. Para validar el look antes del rebuild.
export const StyleTest: React.FC = () => {
  return (
    <AbsoluteFill style={{backgroundColor: '#0d0d0d'}}>
      <RoughMindMap />
    </AbsoluteFill>
  );
};
