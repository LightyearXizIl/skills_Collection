# Vox 风格 Remotion 工程模板

零素材即可跑通。四种代码组件已实现,不用找图。

## 快速开始

```bash
# 1. 安装依赖
npm install

# 2. 环境自检(能出 out/smoke.mp4 就说明管线通)
npm run smoke

# 3. 开 Studio 可视化调
npm run studio

# 4. 渲染出片
npm run render      # → out/video.mp4
```

Windows 上若 `npm` 不在 PATH,用托管路径:
```bash
C:/Users/EDY/.workbuddy/binaries/node/versions/22.22.2-2/npm.cmd install
```

## 你主要改 src/config.ts

| 区块 | 改什么 |
|---|---|
| 顶部常量 | 分辨率 `WIDTH/HEIGHT`、`ACCENT` 强调色、`BG_COLOR` 背景色、配乐开关 |
| `scenes` 数组 | 脚本时间线:每段时长、组件、cutout、字幕、旁白 |

## 场景对象字段

```ts
{
  id: 's1',                        // 唯一 ID
  durationInSeconds: 4,            // 该段占几秒(应 = 旁白时长)
  background: 'scenes/s1/bg.png',  // 可选,背景图
  video: {src:'clips/x.mp4', overlay:0.4},  // 可选,过场视频
  component: {...},                // 可选,四种代码组件之一
  cutouts: [{...}],                // 可选,透明底图弹入
  caption: '字幕文案',              // 可选
  narration: 'scenes/s1/n.mp3',    // 可选,旁白
}
```

## Cutout 字段

```ts
{
  src: 'scenes/s1/car.png',  // 或 'PLACEHOLDER:车' 用占位块
  x: 300,                    // 相对中心 X 偏移(px),右为正
  y: -40,                    // 相对中心 Y 偏移(px),下为正
  scale: 1,                  // 缩放
  delay: 0.4,                // 延迟弹入(秒)—— 做"错开半拍"
  accent: 'outline',         // 'outline' 环形描边 | 'block' 偏移红块 | 'none'
  accentOffset: 14,          // 强调元素偏移(px)
  fromScale: 0.72,           // 弹入起始缩放
  fromY: 40,                 // 弹入起始 Y 位移
  maxH: 700,                 // 最大渲染高度
}
```

## 四种组件

```ts
// 柱状对比
component: {type:'barCompare', title:'月销量', unit:'万',
            items:[{label:'1月',value:3},{label:'2月',value:5.5}]}

// 打字机
component: {type:'typewriter', text:'为什么它能卖爆?', cps:7}

// 折线增长
component: {type:'lineGrow', points:[12,20,35,78], unit:'k', caption:'累计交付'}

// 流程框图
component: {type:'flow', title:'三电', nodes:['电池','电控','电机','700km']}
```

## 目录

- `src/config.ts` —— ★ 主要改这里
- `src/Scene.tsx` —— 三层场景(背景/视频/组件/cutout/字幕)
- `src/Components.tsx` —— 四种代码组件
- `src/VoxVideo.tsx` —— 主序列拼接
- `src/SmokeTest.tsx` —— 无素材自检
- `public/scenes/` —— 素材(见该目录 README)

## 注意

- 素材路径相对 `public/`,用**正斜杠**。
- Studio 里调完参数**必须 Save**,否则不保留。
- 首次渲染会下载无头 Chromium,慢是正常的。
