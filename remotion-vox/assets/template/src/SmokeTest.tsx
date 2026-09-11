import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {PROJECT} from './config';

export const SmokeTest: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const pop = spring({frame, fps, config: {damping: 16, stiffness: 170}});
  const line = interpolate(frame, [0.3 * fps, 1.8 * fps], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: PROJECT.backgroundColor,
        color: PROJECT.ink,
        fontFamily: PROJECT.fontFamily,
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <div
        style={{
          transform: `scale(${pop})`,
          fontSize: 116,
          lineHeight: 1,
          fontWeight: 950,
          filter: `drop-shadow(18px 18px 0 ${PROJECT.accent})`,
        }}
      >
        REMOTION VOX
      </div>
      <div
        style={{
          width: `${line * 960}px`,
          height: 18,
          marginTop: 62,
          backgroundColor: PROJECT.accent,
        }}
      />
      <div style={{fontSize: 38, fontWeight: 800, marginTop: 32}}>
        template smoke test
      </div>
    </AbsoluteFill>
  );
};
