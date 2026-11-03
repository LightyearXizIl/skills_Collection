// ============================================================
//  全局视觉系统 —— 全片锁死,别中途改
// ============================================================

export const WIDTH = 1920;
export const HEIGHT = 1080;
export const FPS = 30;

/** 招牌强调色(Vox 红)。换成你的账号色即可,全片跟着变 */
export const ACCENT = '#E4572E';

/** 背景兜底色:场景没给 background 时用这个 */
export const BG_COLOR = '#12100E';

/** 字幕兜底背景色 */
export const CAPTION_BG = '#000000';

export const FONT_FAMILY =
  '"PingFang SC", "Microsoft YaHei", "Noto Sans SC", "Source Han Sans SC", "Helvetica Neue", Arial, sans-serif';

/** 整片配乐:放 public/music.mp3 后填 'music.mp3';留空则无配乐 */
export const BG_MUSIC: string | null = null;
export const BG_MUSIC_VOLUME = 0.18;

/** 每个 cutout 背后的偏移强调元素默认偏移量(px) */
export const DEFAULT_ACCENT_OFFSET = 14;

// ============================================================
//  类型定义
// ============================================================

export type AccentMode =
  /** 环形红描边(绕图形一圈) */
  | 'outline'
  /** 偏移红块(图形背后一个同尺寸偏移红矩形) —— 更接近 Vox 杂志拼贴感 */
  | 'block'
  /** 不要强调元素 */
  | 'none';

export type Cutout = {
  /** 相对 public/ 的路径,如 'scenes/scene1/trump.png'。透明底 PNG 最佳 */
  src: string;
  /** 相对画面中心的 X 偏移(px),右为正 */
  x?: number;
  /** 相对画面中心的 Y 偏移(px),下为正 */
  y?: number;
  /** 缩放,1 = 原始尺寸 */
  scale?: number;
  /** 延迟弹入(秒),用来做"错开半拍" */
  delay?: number;
  /** 强调元素模式,默认 'outline' */
  accent?: AccentMode;
  /** 强调元素偏移(px),默认取 DEFAULT_ACCENT_OFFSET */
  accentOffset?: number;
  /** 弹入起始缩放,默认 0.72。调大 = 弹得更轻微 */
  fromScale?: number;
  /** 弹入起始 Y 位移(px),默认 40 */
  fromY?: number;
  /** 最大渲染高度(px),默认 700。防止超大原图撑出画面 */
  maxH?: number;
};

export type ComponentConfig =
  | {
      type: 'barCompare';
      title: string;
      unit?: string;
      items: {label: string; value: number}[];
    }
  | {
      type: 'typewriter';
      text: string;
      /** 每秒出几个字,默认 7 */
      cps?: number;
    }
  | {
      type: 'lineGrow';
      points: number[];
      unit?: string;
      caption?: string;
    }
  | {
      type: 'flow';
      title?: string;
      nodes: string[];
    };

export type SceneConfig = {
  id: string;
  /** 这一段占几秒 —— 应该等于这句旁白的时长 */
  durationInSeconds: number;
  /** 背景图路径(相对 public/)。留空则用 BG_COLOR 纯色 */
  background?: string;
  /** 豆包/即梦生成的过场视频 */
  video?: {src: string; overlay?: number};
  /** 零素材代码组件,四选一 */
  component?: ComponentConfig;
  /** 中景/前景 cutout 弹入 */
  cutouts?: Cutout[];
  /** 字幕文案 */
  caption?: string;
  /** 旁白音频路径(相对 public/) */
  narration?: string;
};

// ============================================================
//  脚本时间线 —— ★ 出片时主要改这里
// ============================================================

export const scenes: SceneConfig[] = [
  {
    id: 's1',
    durationInSeconds: 4,
    caption: '这一集,我们拆开看三个数字。',
    component: {
      type: 'typewriter',
      text: '三个数字,看懂这件事',
      cps: 8,
    },
    // narration: 'scenes/s1/narration.mp3',  // 放入 mp3 后取消注释
  },
  {
    id: 's2',
    durationInSeconds: 5,
    component: {
      type: 'barCompare',
      title: '月销量对比',
      unit: '万',
      items: [
        {label: '1月', value: 3},
        {label: '2月', value: 5.5},
        {label: '3月', value: 9.2},
        {label: '4月', value: 14},
      ],
    },
    caption: '四个月,翻了近五倍。',
    // narration: 'scenes/s2/narration.mp3',  // 放入 mp3 后取消注释
  },
  {
    id: 's3',
    durationInSeconds: 5,
    component: {
      type: 'lineGrow',
      points: [12, 20, 35, 78],
      unit: 'k',
      caption: '累计交付量',
    },
    caption: '真正的拐点在第三个月。',
    // narration: 'scenes/s3/narration.mp3',  // 放入 mp3 后取消注释
  },
  {
    id: 's4',
    durationInSeconds: 4.5,
    component: {
      type: 'flow',
      title: '核心三件套',
      nodes: ['电池', '电控', '电机', '700km'],
    },
    caption: '拆到最后,是这三样东西。',
    // narration: 'scenes/s4/narration.mp3',  // 放入 mp3 后取消注释
  },
];

// ============================================================
//  工具:计算时间线
// ============================================================

export const sceneDurationInFrames = (s: SceneConfig) =>
  Math.round(s.durationInSeconds * FPS);

export const sceneStarts: number[] = scenes.reduce<number[]>((acc, s, i) => {
  acc.push(i === 0 ? 0 : acc[i - 1] + sceneDurationInFrames(scenes[i - 1]));
  return acc;
}, []);

export const totalDurationInFrames = scenes.reduce(
  (sum, s) => sum + sceneDurationInFrames(s),
  0,
);
