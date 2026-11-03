import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {ACCENT, FONT_FAMILY} from './config';

/**
 * 无素材自检合成:确认渲染管线通(Chromium / 编码 / 字体)。
 * 跑 `npm run smoke` 出 out/smoke.mp4,能出片就说明环境 OK。
 */
export const SmokeTest: React.FC = () => {
  const frame = useCurrentFrame();
  const x = interpolate(frame, [0, 90], [80, 1500]);

  return (
    <AbsoluteFill style={{backgroundColor: '#12100E', fontFamily: FONT_FAMILY}}>
      <AbsoluteFill
        style={{justifyContent: 'center', alignItems: 'center', gap: 30}}
      >
        <div style={{fontSize: 72, fontWeight: 800, color: '#FFFFFF'}}>
          Remotion 管线自检
        </div>
        <div style={{fontSize: 34, color: ACCENT, fontWeight: 700}}>
          能看见这行字 + 红块在动 = 环境正常
        </div>
      </AbsoluteFill>
      <div
        style={{
          position: 'absolute',
          top: 780,
          left: x,
          width: 220,
          height: 60,
          backgroundColor: ACCENT,
        }}
      />
    </AbsoluteFill>
  );
};
