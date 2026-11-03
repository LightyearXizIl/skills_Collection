import {Audio, Video} from '@remotion/media';
import React from 'react';
import {
  AbsoluteFill,
  Img,
  staticFile,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import type {ProjectConfig, SceneConfig} from './config';
import {ProgrammaticComponent} from './Components';

const CutoutLayer: React.FC<{
  cutout: NonNullable<SceneConfig['cutouts']>[number];
  accent: string;
  ink: string;
}> = ({cutout, accent, ink}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const progress = spring({
    frame,
    fps,
    delay: Math.round((cutout.delayInSeconds ?? 0) * fps),
    config: {damping: 16, stiffness: 170, mass: 0.9},
  });
  const offset = cutout.outlineOffset ?? 16;
  const style: React.CSSProperties = {
    position: 'absolute',
    left: `${cutout.x}%`,
    top: `${cutout.y}%`,
    width: cutout.width ?? 420,
    transform: `translate(-50%, -50%) scale(${(cutout.scale ?? 1) * progress})`,
    transformOrigin: 'center bottom',
    filter: `grayscale(1) drop-shadow(${offset}px ${offset}px 0 ${accent})`,
  };

  if (cutout.src) {
    return <Img src={staticFile(cutout.src)} style={style} />;
  }

  return (
    <div
      style={{
        ...style,
        height: 360,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        border: `8px solid ${ink}`,
        backgroundColor: '#FFFFFF',
        color: ink,
        fontSize: 48,
        fontWeight: 900,
        filter: `drop-shadow(${offset}px ${offset}px 0 ${accent})`,
      }}
    >
      {cutout.label ?? 'CUTOUT'}
    </div>
  );
};

export const Scene: React.FC<{
  scene: SceneConfig;
  project: ProjectConfig;
}> = ({scene, project}) => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: project.backgroundColor,
        color: project.ink,
        fontFamily: project.fontFamily,
        overflow: 'hidden',
      }}
    >
      {project.background ? (
        <Img
          src={staticFile(project.background)}
          style={{width: '100%', height: '100%', objectFit: 'cover'}}
        />
      ) : (
        <AbsoluteFill
          style={{
            backgroundImage:
              'radial-gradient(circle at center, rgba(22,22,22,0.08) 1.5px, transparent 1.5px)',
            backgroundSize: '14px 14px',
          }}
        />
      )}

      {scene.video ? (
        <AbsoluteFill>
          <Video
            src={staticFile(scene.video.src)}
            muted
            style={{width: '100%', height: '100%', objectFit: 'cover'}}
          />
          <AbsoluteFill
            style={{backgroundColor: project.ink, opacity: scene.video.overlay ?? 0.35}}
          />
        </AbsoluteFill>
      ) : null}

      {scene.component ? (
        <ProgrammaticComponent
          component={scene.component}
          ink={project.ink}
          accent={project.accent}
        />
      ) : null}

      {(scene.cutouts ?? []).map((cutout, index) => (
        <CutoutLayer
          key={`${scene.id}-cutout-${index}`}
          cutout={cutout}
          accent={project.accent}
          ink={project.ink}
        />
      ))}

      {scene.caption ? (
        <div
          style={{
            position: 'absolute',
            left: '8%',
            right: '8%',
            bottom: '5%',
            padding: '18px 28px',
            backgroundColor: project.ink,
            color: '#FFFFFF',
            fontSize: 40,
            lineHeight: 1.25,
            fontWeight: 800,
            textAlign: 'center',
          }}
        >
          {scene.caption}
        </div>
      ) : null}

      {scene.narration ? <Audio src={staticFile(scene.narration)} /> : null}
    </AbsoluteFill>
  );
};
