import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile} from 'remotion';
import {Scene} from './Scene';
import {
  BG_MUSIC,
  BG_MUSIC_VOLUME,
  sceneDurationInFrames,
  sceneStarts,
  scenes,
} from './config';

/**
 * 主序列:按每段旁白时长把场景背靠背拼起来。
 * 每个场景从自己的旁白开始、到自己的旁白结束。
 */
export const VoxVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{backgroundColor: '#000000'}}>
      {scenes.map((scene, i) => (
        <Sequence
          key={scene.id}
          name={scene.id}
          from={sceneStarts[i]}
          durationInFrames={sceneDurationInFrames(scene)}
        >
          <Scene scene={scene} />
        </Sequence>
      ))}

      {BG_MUSIC ? (
        <Audio src={staticFile(BG_MUSIC)} volume={BG_MUSIC_VOLUME} />
      ) : null}
    </AbsoluteFill>
  );
};
