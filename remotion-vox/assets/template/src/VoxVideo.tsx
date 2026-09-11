import {Audio} from '@remotion/media';
import React from 'react';
import {AbsoluteFill, Series, staticFile, useVideoConfig} from 'remotion';
import {PROJECT} from './config';
import {Scene} from './Scene';

export const VoxVideo: React.FC = () => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill>
      <Series>
        {PROJECT.scenes.map((scene) => (
          <Series.Sequence
            key={scene.id}
            durationInFrames={Math.max(1, Math.round(scene.durationInSeconds * fps))}
            premountFor={fps}
          >
            <Scene scene={scene} project={PROJECT} />
          </Series.Sequence>
        ))}
      </Series>
      {PROJECT.music ? (
        <Audio src={staticFile(PROJECT.music)} loop volume={PROJECT.musicVolume} />
      ) : null}
    </AbsoluteFill>
  );
};
