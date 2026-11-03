import React from 'react';
import {Composition} from 'remotion';
import {SmokeTest} from './SmokeTest';
import {VoxVideo} from './VoxVideo';
import {FPS, HEIGHT, WIDTH, totalDurationInFrames} from './config';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="VoxVideo"
        component={VoxVideo}
        durationInFrames={Math.max(1, totalDurationInFrames)}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
      <Composition
        id="SmokeTest"
        component={SmokeTest}
        durationInFrames={FPS * 4}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
    </>
  );
};
