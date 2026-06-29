import React from 'react';
import {Composition} from 'remotion';
import {FPS, sec} from './theme';
import {BecaVideo} from './BecaVideo';
import {Estructura} from './Estructura';
import {StyleTest} from './StyleTest';
import {Sample} from './Sample';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="StyleTest"
        component={StyleTest}
        durationInFrames={sec(6)}
        fps={FPS}
        width={1920}
        height={1080}
      />
      <Composition
        id="Estructura"
        component={Estructura}
        durationInFrames={sec(60)}
        fps={FPS}
        width={1920}
        height={1080}
      />
      <Composition
        id="BecaVideo"
        component={BecaVideo}
        durationInFrames={sec(120)}
        fps={FPS}
        width={1920}
        height={1080}
        defaultProps={{hasFootage: false}}
      />
      <Composition
        id="Sample"
        component={Sample}
        durationInFrames={150}
        fps={FPS}
        width={1920}
        height={1080}
      />
    </>
  );
};
