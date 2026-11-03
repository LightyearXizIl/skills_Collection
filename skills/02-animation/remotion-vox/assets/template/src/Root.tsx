import React from 'react';
import {Composition} from 'remotion';
import {FPS, PROJECT, TOTAL_DURATION_IN_FRAMES} from './config';
import {SmokeTest} from './SmokeTest';
import {VoxVideo} from './VoxVideo';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="VoxVideo"
        component={VoxVideo}
        durationInFrames={TOTAL_DURATION_IN_FRAMES}
        fps={FPS}
        width={PROJECT.width}
        height={PROJECT.height}
      />
      <Composition
        id="SmokeTest"
        component={SmokeTest}
        durationInFrames={3 * FPS}
        fps={FPS}
        width={PROJECT.width}
        height={PROJECT.height}
      />
    </>
  );
};
