# 素材目录

每个场景一个文件夹,放该场景的素材。

```
public/scenes/
├─ s1/
│  ├─ narration.mp3      # 该场景的旁白(放进去后在 config.ts 取消注释)
│  └─ (cutout PNGs)
├─ s2/
└─ ...
```

## 路径写法

`config.ts` 里所有路径**相对 `public/`**,且用**正斜杠**:

```ts
background: 'scenes/s1/bg.png',       // ✅ 正确
background: 'scenes\\s1\\bg.png',     // ❌ 反斜杠,会挂
background: 'D:/xxx/bg.png',          // ❌ 绝对路径,会挂
```

## 素材要求

| 类型 | 要求 |
|---|---|
| 背景 `bg.png` | 1920×1080,横屏。全片共用一张最有 Vox 感 |
| cutout | **透明底 PNG**,黑白半调预处理过。高度建议 ≤1400px |
| 过场 `clips/*.mp4` | 放 `public/clips/`,3 秒左右 |
| 旁白 `narration.mp3` | 时长应 ≈ 该场景 `durationInSeconds` |
| 配乐 `music.mp3` | 放 `public/` 根下 |

## 占位符用法

还没图时用占位块调排版,不会报错:

```ts
cutouts: [{src: 'PLACEHOLDER:车', x: 300, y: 0, scale: 1}]
```

`PLACEHOLDER:` 开头的 src 会渲染成带标签的虚线框。
