import React from 'react';
import {
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import type {ComponentConfig} from './config';
import {ACCENT, FONT_FAMILY, WIDTH} from './config';

/**
 * 占位块:还没素材时用来调排版。
 * 用法:cutouts: [{src: 'PLACEHOLDER:车', ...}]
 */
export const Placeholder: React.FC<{label: string}> = ({label}) => (
  <div
    style={{
      width: '100%',
      height: '100%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      border: `4px dashed ${ACCENT}`,
      color: ACCENT,
      fontFamily: FONT_FAMILY,
      fontSize: 42,
      fontWeight: 700,
      opacity: 0.85,
      boxSizing: 'border-box',
    }}
  >
    {label}
  </div>
);

/**
 * 零素材代码组件库。
 * 全部用 spring(弹出) + interpolate(位移/淡入/数值) 驱动,不依赖任何外部图片。
 */

const Title: React.FC<{children: React.ReactNode}> = ({children}) => (
  <div
    style={{
      fontFamily: FONT_FAMILY,
      fontSize: 56,
      fontWeight: 800,
      color: '#FFFFFF',
      letterSpacing: 2,
      marginBottom: 48,
      textShadow: `6px 6px 0 ${ACCENT}`,
    }}
  >
    {children}
  </div>
);

// ------------------------------------------------------------
// 1. barCompare —— 柱状对比:柱子长起 + 数字滚动
// ------------------------------------------------------------

const BarCompare: React.FC<{
  title: string;
  unit?: string;
  items: {label: string; value: number}[];
}> = ({title, unit = '', items}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const max = Math.max(...items.map((i) => i.value), 1);

  return (
    <div
      style={{
        width: WIDTH * 0.62,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
      }}
    >
      <Title>{title}</Title>
      <div style={{display: 'flex', alignItems: 'flex-end', gap: 40, height: 420}}>
        {items.map((item, i) => {
          const p = spring({
            frame: frame - i * 6,
            fps,
            config: {damping: 14, mass: 0.7, stiffness: 90},
          });
          const h = interpolate(p, [0, 1], [0, (item.value / max) * 360]);
          const num = interpolate(p, [0, 1], [0, item.value]);

          return (
            <div
              key={item.label}
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'flex-end',
                height: '100%',
                width: 120,
              }}
            >
              <div
                style={{
                  fontFamily: FONT_FAMILY,
                  fontSize: 40,
                  fontWeight: 800,
                  color: ACCENT,
                  marginBottom: 10,
                }}
              >
                {num.toFixed(item.value % 1 === 0 ? 0 : 1)}
                <span style={{fontSize: 24, marginLeft: 4}}>{unit}</span>
              </div>
              <div
                style={{
                  width: 110,
                  height: h,
                  background: i === items.length - 1 ? ACCENT : '#E8E3DC',
                  boxShadow:
                    i === items.length - 1 ? `10px 10px 0 rgba(228,87,46,0.35)` : 'none',
                }}
              />
              <div
                style={{
                  fontFamily: FONT_FAMILY,
                  fontSize: 28,
                  fontWeight: 600,
                  color: '#CFC7BD',
                  marginTop: 14,
                }}
              >
                {item.label}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

// ------------------------------------------------------------
// 2. typewriter —— 文字逐字蹦出 + 光标
// ------------------------------------------------------------

const Typewriter: React.FC<{text: string; cps?: number}> = ({
  text,
  cps = 7,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const shown = Math.min(text.length, Math.floor((frame / fps) * cps));
  const visible = text.slice(0, shown);
  const caretOn = Math.floor(frame / 12) % 2 === 0;

  return (
    <div
      style={{
        fontFamily: FONT_FAMILY,
        fontSize: 92,
        fontWeight: 800,
        color: '#FFFFFF',
        textShadow: `8px 8px 0 ${ACCENT}`,
        letterSpacing: 4,
        display: 'flex',
        alignItems: 'center',
      }}
    >
      <span>{visible}</span>
      <span style={{opacity: caretOn ? 1 : 0, color: ACCENT, marginLeft: 6}}>|</span>
    </div>
  );
};

// ------------------------------------------------------------
// 3. lineGrow —— 折线画出 + 面积填充 + 端点强调
// ------------------------------------------------------------

const LineGrow: React.FC<{
  points: number[];
  unit?: string;
  caption?: string;
}> = ({points, unit = '', caption}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({
    frame,
    fps,
    config: {damping: 200, mass: 0.6, stiffness: 60},
  });

  const w = WIDTH * 0.62;
  const h = 420;
  const max = Math.max(...points, 1);
  const min = Math.min(...points, 0);
  const range = max - min || 1;

  const xy = points.map((v, i) => ({
    x: (i / (points.length - 1)) * w,
    y: h - ((v - min) / range) * (h - 90) - 45,
  }));

  const d = xy.map((pt, i) => `${i === 0 ? 'M' : 'L'}${pt.x},${pt.y}`).join(' ');
  const area = `${d} L${w},${h} L0,${h} Z`;

  return (
    <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
      {caption ? <Title>{caption}</Title> : null}
      <svg width={w} height={h} style={{overflow: 'visible'}}>
        <defs>
          <linearGradient id="lg-fill" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={ACCENT} stopOpacity={0.45} />
            <stop offset="100%" stopColor={ACCENT} stopOpacity={0.02} />
          </linearGradient>
        </defs>

        <path d={area} fill="url(#lg-fill)" opacity={interpolate(p, [0, 0.6, 1], [0, 0, 1])} />

        <path
          d={d}
          fill="none"
          stroke={ACCENT}
          strokeWidth={7}
          strokeLinecap="round"
          strokeLinejoin="round"
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - p}
        />

        {xy.map((pt, i) => {
          const dotP = spring({
            frame: frame - 8 - i * 8,
            fps,
            config: {damping: 12, mass: 0.5, stiffness: 120},
          });
          return (
            <g key={i}>
              <circle cx={pt.x} cy={pt.y} r={11 * dotP} fill="#FFFFFF" />
              <circle cx={pt.x} cy={pt.y} r={20 * dotP} fill={ACCENT} opacity={0.25} />
              <text
                x={pt.x}
                y={pt.y - 34}
                textAnchor="middle"
                fill="#FFFFFF"
                style={{
                  fontFamily: FONT_FAMILY,
                  fontSize: 32,
                  fontWeight: 800,
                  opacity: dotP,
                }}
              >
                {points[i]}
                {unit}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
};

// ------------------------------------------------------------
// 4. flow —— 流程/框图:方块依次点亮
// ------------------------------------------------------------

const Flow: React.FC<{title?: string; nodes: string[]}> = ({title, nodes}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  return (
    <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
      {title ? <Title>{title}</Title> : null}
      <div style={{display: 'flex', alignItems: 'center', gap: 24}}>
        {nodes.map((n, i) => {
          const p = spring({
            frame: frame - i * 7,
            fps,
            config: {damping: 12, mass: 0.6, stiffness: 100},
          });
          const isLast = i === nodes.length - 1;

          return (
            <React.Fragment key={n}>
              <div
                style={{
                  padding: '30px 44px',
                  background: isLast ? ACCENT : '#1E1B18',
                  border: `4px solid ${isLast ? ACCENT : '#4A443E'}`,
                  color: '#FFFFFF',
                  fontFamily: FONT_FAMILY,
                  fontSize: 44,
                  fontWeight: 700,
                  transform: `scale(${interpolate(p, [0, 1], [0.6, 1])})`,
                  opacity: p,
                  boxShadow: isLast ? `10px 10px 0 rgba(255,255,255,0.18)` : 'none',
                  whiteSpace: 'nowrap',
                }}
              >
                {n}
              </div>
              {i < nodes.length - 1 ? (
                <div
                  style={{
                    width: 46,
                    height: 6,
                    background: ACCENT,
                    opacity: interpolate(p, [0, 1], [0, 1]),
                  }}
                />
              ) : null}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};

// ------------------------------------------------------------
// 分发器
// ------------------------------------------------------------

export const VoxComponent: React.FC<{config: ComponentConfig}> = ({config}) => {
  switch (config.type) {
    case 'barCompare':
      return (
        <BarCompare title={config.title} unit={config.unit} items={config.items} />
      );
    case 'typewriter':
      return <Typewriter text={config.text} cps={config.cps} />;
    case 'lineGrow':
      return (
        <LineGrow points={config.points} unit={config.unit} caption={config.caption} />
      );
    case 'flow':
      return <Flow title={config.title} nodes={config.nodes} />;
    default:
      return null;
  }
};
