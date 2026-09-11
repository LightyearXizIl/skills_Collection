export const FPS = 30;

export type Cutout = {
  src?: string;
  label?: string;
  x: number;
  y: number;
  scale?: number;
  delayInSeconds?: number;
  width?: number;
  outlineOffset?: number;
};

export type BarCompare = {
  type: 'barCompare';
  title: string;
  unit?: string;
  items: Array<{label: string; value: number}>;
};

export type Typewriter = {
  type: 'typewriter';
  text: string;
  charactersPerSecond?: number;
};

export type LineGrow = {
  type: 'lineGrow';
  points: number[];
  unit?: string;
  caption?: string;
};

export type Flow = {
  type: 'flow';
  title?: string;
  nodes: string[];
};

export type SceneComponent = BarCompare | Typewriter | LineGrow | Flow;

export type SceneConfig = {
  id: string;
  durationInSeconds: number;
  caption?: string;
  narration?: string;
  video?: {
    src: string;
    overlay?: number;
  };
  component?: SceneComponent;
  cutouts?: Cutout[];
};

export type ProjectConfig = {
  width: number;
  height: number;
  backgroundColor: string;
  background?: string;
  ink: string;
  accent: string;
  fontFamily: string;
  music?: string;
  musicVolume: number;
  scenes: SceneConfig[];
};

export const PROJECT: ProjectConfig = {
  width: 1920,
  height: 1080,
  backgroundColor: '#F3EBDD',
  ink: '#161616',
  accent: '#E4572E',
  fontFamily: 'Arial, "Microsoft YaHei", sans-serif',
  musicVolume: 0.12,
  scenes: [
    {
      id: 'hook',
      durationInSeconds: 4,
      caption: '一句旁白，一个视觉 beat',
      component: {
        type: 'typewriter',
        text: '为什么这条曲线突然起飞？',
        charactersPerSecond: 8,
      },
      cutouts: [
        {label: '主体 A', x: 17, y: 64, scale: 1, delayInSeconds: 0.15},
      ],
    },
    {
      id: 'data',
      durationInSeconds: 5,
      caption: '示例数据，请替换为有来源的真实数据',
      component: {
        type: 'barCompare',
        title: '示例对比',
        unit: '单位',
        items: [
          {label: 'A', value: 32},
          {label: 'B', value: 58},
          {label: 'C', value: 81},
        ],
      },
    },
  ],
};

export const TOTAL_DURATION_IN_FRAMES = Math.max(
  1,
  Math.round(
    PROJECT.scenes.reduce((sum, scene) => sum + scene.durationInSeconds, 0) * FPS,
  ),
);
