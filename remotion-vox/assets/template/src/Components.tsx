import React from 'react';
import {
  Easing,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import type {SceneComponent} from './config';

const panelStyle: React.CSSProperties = {
  position: 'absolute',
  left: '25%',
  right: '8%',
  top: '14%',
  bottom: '20%',
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
};

const BarChart: React.FC<{
  component: Extract<SceneComponent, {type: 'barCompare'}>;
  accent: string;
  ink: string;
}> = ({component, accent, ink}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const max = Math.max(1, ...component.items.map((item) => item.value));

  return (
    <div style={panelStyle}>
      <div style={{fontSize: 58, fontWeight: 900, color: ink, marginBottom: 38}}>
        {component.title}
      </div>
      <div style={{display: 'flex', alignItems: 'flex-end', gap: 42, height: 450}}>
        {component.items.map((item, index) => {
          const progress = spring({
            frame,
            fps,
            delay: Math.round(index * 0.12 * fps),
            config: {damping: 18, stiffness: 150},
          });
          const displayed = Math.round(item.value * progress);
          return (
            <div key={`${item.label}-${index}`} style={{flex: 1, textAlign: 'center'}}>
              <div style={{fontSize: 34, fontWeight: 800, color: ink, marginBottom: 12}}>
                {displayed}{component.unit ?? ''}
              </div>
              <div
                style={{
                  height: 360 * (item.value / max) * progress,
                  minHeight: 3,
                  backgroundColor: index === component.items.length - 1 ? accent : ink,
                  border: `5px solid ${ink}`,
                }}
              />
              <div style={{fontSize: 32, fontWeight: 800, color: ink, marginTop: 14}}>
                {item.label}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

const TypewriterText: React.FC<{
  component: Extract<SceneComponent, {type: 'typewriter'}>;
  ink: string;
  accent: string;
}> = ({component, ink, accent}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const count = Math.floor((frame / fps) * (component.charactersPerSecond ?? 7));
  const visible = component.text.slice(0, Math.max(0, count));
  const cursor = Math.floor(frame / (fps * 0.35)) % 2 === 0;

  return (
    <div style={{...panelStyle, fontSize: 108, lineHeight: 1.12, fontWeight: 950, color: ink}}>
      <span>{visible}</span>
      <span style={{color: accent, opacity: cursor ? 1 : 0}}>▌</span>
    </div>
  );
};

const LineChart: React.FC<{
  component: Extract<SceneComponent, {type: 'lineGrow'}>;
  ink: string;
  accent: string;
}> = ({component, ink, accent}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const progress = interpolate(frame, [0.2 * fps, 2.2 * fps], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.quad),
  });
  const values = component.points.length > 1 ? component.points : [0, ...component.points];
  const max = Math.max(1, ...values);
  const min = Math.min(0, ...values);
  const range = Math.max(1, max - min);
  const points = values.map((value, index) => {
    const x = (index / Math.max(1, values.length - 1)) * 1000 + 40;
    const y = 460 - ((value - min) / range) * 380;
    return `${x},${y}`;
  });

  return (
    <div style={panelStyle}>
      <svg viewBox="0 0 1100 520" style={{width: '100%', overflow: 'visible'}}>
        <line x1="40" y1="460" x2="1040" y2="460" stroke={ink} strokeWidth="6" />
        <polyline
          points={points.join(' ')}
          fill="none"
          stroke={accent}
          strokeWidth="18"
          strokeLinejoin="round"
          strokeLinecap="round"
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - progress}
        />
        {points.map((point, index) => {
          const [cx, cy] = point.split(',').map(Number);
          const pointProgress = spring({
            frame,
            fps,
            delay: Math.round((0.25 + index * 0.18) * fps),
            config: {damping: 20, stiffness: 180},
          });
          return <circle key={point} cx={cx} cy={cy} r={15 * pointProgress} fill={ink} />;
        })}
      </svg>
      <div style={{fontSize: 44, fontWeight: 900, color: ink}}>
        {component.caption ?? `最新值 ${values.at(-1)}${component.unit ?? ''}`}
      </div>
    </div>
  );
};

const FlowChart: React.FC<{
  component: Extract<SceneComponent, {type: 'flow'}>;
  ink: string;
  accent: string;
}> = ({component, ink, accent}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <div style={panelStyle}>
      {component.title ? (
        <div style={{fontSize: 58, fontWeight: 900, color: ink, marginBottom: 60}}>
          {component.title}
        </div>
      ) : null}
      <div style={{display: 'flex', alignItems: 'center', gap: 20}}>
        {component.nodes.map((node, index) => {
          const progress = spring({
            frame,
            fps,
            delay: Math.round(index * 0.18 * fps),
            config: {damping: 20, stiffness: 180},
          });
          return (
            <React.Fragment key={`${node}-${index}`}>
              <div
                style={{
                  flex: 1,
                  padding: '34px 22px',
                  border: `6px solid ${ink}`,
                  backgroundColor: index === component.nodes.length - 1 ? accent : '#FFFFFF',
                  color: ink,
                  fontSize: 38,
                  fontWeight: 900,
                  textAlign: 'center',
                  transform: `scale(${progress})`,
                }}
              >
                {node}
              </div>
              {index < component.nodes.length - 1 ? (
                <div style={{fontSize: 54, fontWeight: 900, color: accent, opacity: progress}}>→</div>
              ) : null}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};

export const ProgrammaticComponent: React.FC<{
  component: SceneComponent;
  ink: string;
  accent: string;
}> = ({component, ink, accent}) => {
  if (component.type === 'barCompare') {
    return <BarChart component={component} ink={ink} accent={accent} />;
  }
  if (component.type === 'typewriter') {
    return <TypewriterText component={component} ink={ink} accent={accent} />;
  }
  if (component.type === 'lineGrow') {
    return <LineChart component={component} ink={ink} accent={accent} />;
  }
  return <FlowChart component={component} ink={ink} accent={accent} />;
};
