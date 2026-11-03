import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  OffthreadVideo,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import type {Cutout, SceneConfig} from './config';
import {
  ACCENT,
  BG_COLOR,
  CAPTION_BG,
  DEFAULT_ACCENT_OFFSET,
  FONT_FAMILY,
} from './config';
import {Placeholder, VoxComponent} from './Components';

/**
 * 单个 cutout:spring 弹入 + 偏移强调元素。
 * 强调元素两种:
 *   outline —— 环形红描边(8 方向 drop-shadow)
 *   block   —— 背后一个同尺寸偏移红矩形(Vox 杂志拼贴感)
 */
const CutoutItem: React.FC<{cutout: Cutout}> = ({cutout}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const enter = spring({
    frame: frame - (cutout.delay ?? 0) * fps,
    fps,
    config: {damping: 12, mass: 0.6, stiffness: 95},
  });

  const s = interpolate(enter, [0, 1], [cutout.fromScale ?? 0.72, 1]) * (cutout.scale ?? 1);
  const dy = interpolate(enter, [0, 1], [cutout.fromY ?? 40, 0]);
  const opacity = interpolate(enter, [0, 0.35], [0, 1]);

  const accent = cutout.accent ?? 'outline';
  const off = cutout.accentOffset ?? DEFAULT_ACCENT_OFFSET;

  const outlineFilter =
    accent === 'outline'
      ? Array.from({length: 8}, (_, i) => {
          const a = (i / 8) * Math.PI * 2;
          const dx = Math.cos(a) * off * 0.5;
          const dy2 = Math.sin(a) * off * 0.5;
          return `drop-shadow(${dx}px ${dy2}px 0 ${ACCENT})`;
        }).join(' ')
      : undefined;

  const isPlaceholder = cutout.src.startsWith('PLACEHOLDER:');

  return (
    <div
      style={{
        position: 'absolute',
        left: '50%',
        top: '50%',
        transform: `translate(calc(-50% + ${cutout.x ?? 0}px), calc(-50% + ${cutout.y ?? 0}px)) scale(${s}) translateY(${dy}px)`,
        opacity,
      }}
    >
      <div style={{position: 'relative'}}>
        {accent === 'block' ? (
          <div
            style={{
              position: 'absolute',
              inset: 0,
              background: ACCENT,
              transform: `translate(${off}px, ${off}px)`,
            }}
          />
        ) : null}
        {isPlaceholder ? (
          <div style={{width: 320, height: 320}}>
            <Placeholder label={cutout.src.replace('PLACEHOLDER:', '')} />
          </div>
        ) : (
          <Img
            src={staticFile(cutout.src)}
            style={{
              position: 'relative',
              maxHeight: cutout.maxH ?? 700,
              width: 'auto',
              filter: outlineFilter,
            }}
          />
        )}
      </div>
    </div>
  );
};

/** 字幕:底部居中,淡入 + 轻微上浮 */
const Caption: React.FC<{text: string}> = ({text}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame, fps, config: {damping: 200, mass: 0.5, stiffness: 90}});

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'flex-end',
        alignItems: 'center',
        paddingBottom: 80,
      }}
    >
      <div
        style={{
          transform: `translateY(${interpolate(p, [0, 1], [26, 0])}px)`,
          opacity: p,
          background: CAPTION_BG,
          padding: '18px 40px',
          borderLeft: `8px solid ${ACCENT}`,
          fontFamily: FONT_FAMILY,
          fontSize: 46,
          fontWeight: 700,
          color: '#FFFFFF',
          letterSpacing: 1,
          maxWidth: '80%',
          textAlign: 'center',
          lineHeight: 1.35,
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};

/**
 * 三层场景:
 *   背景层(锁定) → 视频层 → 组件层 → cutout 层 → 字幕层
 */
export const Scene: React.FC<{scene: SceneConfig}> = ({scene}) => {
  return (
    <AbsoluteFill style={{backgroundColor: BG_COLOR, overflow: 'hidden'}}>
      {/* 1. 背景层 */}
      {scene.background ? (
        <Img
          src={staticFile(scene.background)}
          style={{width: '100%', height: '100%', objectFit: 'cover'}}
        />
      ) : null}

      {/* 2. 视频过场层(豆包/即梦 mp4) */}
      {scene.video ? (
        <>
          <OffthreadVideo
            src={staticFile(scene.video.src)}
            style={{width: '100%', height: '100%', objectFit: 'cover'}}
          />
          <AbsoluteFill
            style={{backgroundColor: `rgba(0,0,0,${scene.video.overlay ?? 0.4})`}}
          />
        </>
      ) : null}

      {/* 3. 代码组件层(零素材) */}
      {scene.component ? (
        <AbsoluteFill
          style={{justifyContent: 'center', alignItems: 'center', zIndex: 2}}
        >
          <VoxComponent config={scene.component} />
        </AbsoluteFill>
      ) : null}

      {/* 4. cutout 弹入层 */}
      <AbsoluteFill style={{zIndex: 3}}>
        {(scene.cutouts ?? []).map((c, i) => (
          <CutoutItem key={`${c.src}-${i}`} cutout={c} />
        ))}
      </AbsoluteFill>

      {/* 5. 字幕层 */}
      {scene.caption ? (
        <AbsoluteFill style={{zIndex: 4}}>
          <Caption text={scene.caption} />
        </AbsoluteFill>
      ) : null}

      {/* 旁白:每个场景播自己那段 */}
      {scene.narration ? <Audio src={staticFile(scene.narration)} /> : null}
    </AbsoluteFill>
  );
};
