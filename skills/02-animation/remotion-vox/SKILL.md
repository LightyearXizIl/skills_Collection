---
name: remotion-vox
description: 用 Remotion(React 代码生成视频)做 Vox 风格解说/特效片——锁定背景 + 黑白半调 cutout 弹入 + 偏移红描边 + 卡旁白拼场景 + 渲染 1080p mp4。内置零素材代码组件库(柱状对比/折线增长/打字机/流程框图)+ 视频过场层(接豆包/即梦 mp4)+ 本地抠图(你的车图/照片去背当 cutout)。全程自然语言指挥,不用手写代码;自带可直接跑的项目模板。触发词:"做一条 Vox 风格""remotion 出片""数据段/图表段/打字段/流程框图""做个柱状图/折线段""把这张车图抠出来""生成个过场""程序化特效视频""自动剪辑"。配音用中文 TTS 或口播原声。
agent_created: true
---

# remotion-vox — 用 Remotion 出 Vox 风格特效片

把"选题脚本 → 一条带动态特效的 mp4"这条装配线固化下来。核心是**你用自然语言描述意图,我去写/改 Remotion(React)代码**,你只在 Remotion Studio 里点几下调位置、存值。产出高辨识度的 Vox 杂志风动态图形,补口播视频"空镜不够、数据/地图/图表段干巴巴"的短板。

> 本 skill 自带一套**能直接跑、已冒烟验证过**的项目模板在 `template/`,别从零重搭。每次出片 = 复制模板 → 改 `src/config.ts` 的时间线 → 塞素材 → 预览 → 渲染。

## 六条铁律(Vox 观感 + 不返工,任何时候别破)

1. **先写台词,再配画面**。永远从"一句旁白 → 一个视觉 beat"的**脚本表**出发(见 `references/01-script-table.md`),不要先做画面再硬凑词。
2. **视觉系统全片锁死**:同一张背景 + 同一套字体 + 同一组强调色(模板默认招牌红 `#E4572E`)。每个场景**只换中景/前景的 cutout**,背景锁定才有"一镜到底"的 Vox 感。
3. **三层结构**:背景层(锁定)+ 中景层(黑白半调人物/主体弹入)+ 前景层(建筑/形状/图表)。`src/Scene.tsx` 已实现。
4. **半调是"图"不是"代码"**:cutout 的黑白半调(halftone)网点质感由**生图工具预处理进 PNG**,不在 Remotion 里做。Remotion 只负责排版、弹入动画、偏移红描边。透明底 PNG 丢进 `public/scenes/<场景>/`。
5. **带意图地做动画,但别手写函数**:底层只用 `spring`(弹出)+ `interpolate`(位移/淡入),模板已封好。你只需说"让白宫先弹进来,然后特朗普和另一个人错开半拍跟上,每个背后给一道偏移红描边"——我来调参数。
6. **Studio 里调完的数值必须 Save**。在 Remotion Studio 用 prop 面板调完 scale / XY 位置后,**不 Save 就不保留**,这是最容易白调的坑。

## 本机环境(已实测,与原始文档有出入,以此为准)

2026-09 实测结果:

| 依赖 | 状态 | 说明 |
|---|---|---|
| **Node.js** | ✅ v22.22.2 | 托管路径 `C:\Users\EDY\.workbuddy\binaries\node\versions\22.22.2-2\` |
| **npm** | ✅ 同目录 `npm.cmd` | 用托管 npm,别用系统 npm |
| **Python** | ✅ 3.13.14 | `C:\Users\EDY\.workbuddy\binaries\python\versions\3.13.12\python.exe` |
| **ffmpeg** | ⚠️ **系统未装** | **不影响**:Remotion 4 内置 ffmpeg,渲染 mp4 无需系统级 ffmpeg。只有想手动转码/合流才需要装 |
| **rembg** | ❌ **未装** | 抠图功能需先装,见下。或用替代方案 |

**必记**:本文档原始版本声称"ffmpeg 已装、rembg 已装",实测**均不成立**。别被误导。

### Node / npm 调用方式(Windows)

```bash
NODE="C:/Users/EDY/.workbuddy/binaries/node/versions/22.22.2-2/node.exe"
NPM="C:/Users/EDY/.workbuddy/binaries/node/versions/22.22.2-2/npm.cmd"
```

### rembg 安装(需要抠图时才装)

```bash
PY="C:/Users/EDY/.workbuddy/binaries/python/versions/3.13.12/python.exe"
"$PY" -m pip install rembg[cpu] onnxruntime
```

首次运行会下载 u2net 模型(约 170MB),之后离线可用。

**替代方案(免装)**:本机已有 `buddy-image-processing` 技能,支持通用抠图/matting。给一张图说"抠图"即可,适合不想装 rembg 的场景。

### 中文配音(三选一)

原文档用的 ElevenLabs 英式音色**对中文不适配**,改用:

1. **自己的口播原声**(最推荐,一致性强)—— 导出 mp3 放进对应场景文件夹。
2. **edge-tts**(免费、离线可用、中文自然度高):
   ```bash
   "$PY" -m pip install edge-tts
   "$PY" -m edge_tts --voice zh-CN-YunxiNeural --text "旁白内容" --write-media narration.mp3
   ```
   常用中文音色:`zh-CN-YunxiNeural`(男/解说)、`zh-CN-XiaoxiaoNeural`(女/温柔)、`zh-CN-YunjianNeural`(男/浑厚)。
3. **pyttsx3**(完全离线,机械感较强,仅应急)。

## 项目结构(每次出片复制 `template/` 得到)

```
my-video/
├─ package.json          # 依赖 + 命令(studio / render / still)
├─ remotion.config.ts
├─ tsconfig.json
├─ src/
│  ├─ config.ts          # ★你主要改这里:全局视觉 + scenes 脚本时间线
│  ├─ Scene.tsx          # 三层场景(背景锁定 + cutout 弹入 + 红描边 + 字幕 + 旁白)
│  ├─ Components.tsx     # 零素材代码组件库(4 种)
│  ├─ VoxVideo.tsx       # 主序列:按每段旁白时长把场景背靠背拼起来
│  ├─ SmokeTest.tsx      # 无素材自检合成
│  └─ Root.tsx           # 注册合成
├─ public/
│  ├─ scenes/
│  │  ├─ scene1/  bg.png  trump.png  narration.mp3
│  │  └─ scene2/  ...     （每个场景一个文件夹;共享背景可复用同一张）
│  └─ music.mp3          # 可选整片配乐
└─ out/                  # 渲染产物
```

## 端到端流程(照这个顺序,把每步的意图讲给我)

1. **复制模板**:把本 skill 的 `template/` 复制成新项目目录(如 `~/Documents/视频工程/<选题>/`),进去 `npm install`。
2. **先生成脚本表**:给我一个选题,我产出"台词 × 前景 × 中景 × 素材来源"的表格。**原则:一句旁白配一个 beat**。
3. **锁视觉系统**:在 `src/config.ts` 顶部确认背景/字体/强调色;竖屏还是横屏(`WIDTH/HEIGHT`)。
4. **填 scenes**:把脚本表落进 `src/config.ts` 的 `scenes` 数组——每条写 `durationInSeconds`(=这句旁白时长)、`cutouts`(位置/缩放/交错 delay)、`caption`。**先不放真图也能跑**(用占位块调排版动画)。
5. **备素材**:每个场景一个 `public/scenes/<id>/` 文件夹,放共享背景 + 透明底半调 cutout;把 `config.ts` 里对应 `background`/`src`/`narration` 路径填上。
6. **开预览**:`npm run studio`。
7. **调位置**:Studio 里选 `VoxVideo`,用 prop 面板/直接改 `config.ts` 调每个 cutout 的 `x/y/scale/delay`。**调完 Save**。要属性面板就说"给我 prop controls"。报错就丢回一句 "Fix this error please"。
8. **加动画意图**:用大白话让我调弹入节奏——"错开半拍""弹得再软一点""红描边偏移再大些"。我改的是 `Scene.tsx` 里的 spring config / drop-shadow 偏移。
9. **配音对齐**:把每段中文旁白 mp3 放进对应场景文件夹、填 `narration`。模板会让每个场景**播自己那段旁白、并按其时长占时**,自动背靠背。
10. **配乐/音效**(可选):`public/music.mp3` + 打开 `config.ts` 里 `BG_MUSIC` 开关。注:Studio 里拖动预览音频会发卡,**渲染出来是干净的**,别被吓到。
11. **渲染出片**:`npm run render`(默认 `out/video.mp4`)。想把混音放 Premiere 里做,就只渲纯画面。

## 素材从哪来(四档:能用代码画的,就别去找素材)

Remotion 是"用代码生成画面",一大半你以为要找的东西**不用找、直接画**。按优先级:

1. **代码组件(零素材,首选)** —— 数字/图表/打字/流程/箭头全走这,见下"组件库"。
2. **矢量图标 / 你的图** —— 具体物件用 SVG 图标(透明、不用抠);你的车/出镜图抠成透明底(rembg 或 `buddy-image-processing`)。
3. **豆包/即梦视频过场** —— 只有"必须真实感的动态过场"才用,见 `references/03-doubao-prompts.md`。
4. **拆脚本表时,我给每个 beat 标来源**(🟢代码 / 🟡豆包 / 🟣你的图),让你一眼知道哪些不用管。大部分 beat 是"代码,不用找"。

## 组件库(代码直接画,在场景里加 `component`,零外部素材)

在 `config.ts` 某个场景里写 `component: {...}`,四选一:

| 组件 | 干嘛 | 配置示例 |
|---|---|---|
| `barCompare` | 柱状对比,柱子长起 + 数字滚动 | `{type:'barCompare', title:'月销量', unit:'万', items:[{label:'1月',value:3},...]}` |
| `typewriter` | 文字逐字蹦出 + 光标 | `{type:'typewriter', text:'为什么它能卖爆?', cps:7}` |
| `lineGrow` | 折线画出 + 面积填充 + 端点强调 | `{type:'lineGrow', points:[12,20,35,78], unit:'k', caption:'累计交付'}` |
| `flow` | 流程/芯片框图,方块依次点亮 | `{type:'flow', title:'三电', nodes:['电池','电控','电机','700km']}` |

一个场景可同时有 `background` / `video` / `component` / `cutouts`,自动按 **背景 → 视频 → 组件 → cutout → 字幕** 叠在一条时间线。实现见 `src/Components.tsx`,要新组件跟我说。

## 视频过场(豆包/即梦)

见 `references/03-doubao-prompts.md`。要点:只给"必须真实感的过场"用;我写提示词 + 接进片子,你在即梦网页两下生成+下载。生成的 mp4 丢 `public/clips/`,场景加 `video: {src:'clips/xxx.mp4', overlay:0.4}`。

## 抠图(你的照片 → 透明底 cutout)

**方案 A — rembg**(本地离线,需先装):
```bash
PY="C:/Users/EDY/.workbuddy/binaries/python/versions/3.13.12/python.exe"
"$PY" -c "from rembg import remove; open('out.png','wb').write(remove(open('输入.jpg','rb').read()))"
```

**方案 B — 本机技能**(免装):直接用 `buddy-image-processing` 技能的通用 matting 能力。

矢量图(SVG)本来就透明,不用抠。

## 车 / AI 内容怎么用(本地化)

- **最实用的用法不是整片**,而是给**口播插一段 10~20 秒的 Vox 动态**:讲参数对比做"数据段"(数字弹入 + 折线图),讲车型/路线做"地图段",讲发布会时间线做"图表段"。把这段 mp4 拿进剪辑管线当 B-roll。
- cutout 换成车、logo、参数框;背景换成品牌底色;红描边可换成账号强调色(改 `config.ts` 的 `ACCENT`)。
- 配音直接用你口播原声那一句,画面卡着这句的时长走。

## 排错

- **渲染很慢/卡在下载**:首次渲染 Remotion 在拉无头 Chromium,等一次即可,之后有缓存。
- **`staticFile` 找不到图**:资源必须放在 `public/` 下,路径相对 `public/`(如 `scenes/scene1/bg.png`),别写绝对路径。
- **音频在 Studio 里发卡**:正常现象,以渲染产物为准。
- **改了 `config.ts` 时长但总长不对**:总帧数由各场景 `durationInSeconds` 求和自动算(见 `VoxVideo.tsx` 的 `totalDurationInFrames`),改完刷新 Studio 即可。
- **只想要画面、混音去 Premiere**:渲纯 `VoxVideo` 时把 `config.ts` 里 `narration` 和 `BG_MUSIC` 留空,导出无声画面。
- **`npm` 不是内部命令**:用托管 npm 绝对路径 `C:/Users/EDY/.workbuddy/binaries/node/versions/22.22.2-2/npm.cmd`。
- **Windows 路径反斜杠**:`config.ts` 里所有素材路径用**正斜杠** `scenes/scene1/bg.png`,不要用 `scenes\scene1\bg.png`。
- **`remotion still --frame=N` 抽帧结果都是同一帧**(实测,Remotion 4.0.523):可能与 Sequence 拼合场景的全局帧号不兼容。**改用 ffmpeg 直接抽视频帧**:
  ```bash
  ./node_modules/@remotion/compositor-win32-x64-msvc/ffmpeg.exe \
    -y -ss 7 -i out/video.mp4 -frames:v 1 out/check_t7.png
  ```
  模板自带的 compositor 内置 ffmpeg,无需系统 ffmpeg。
- **首次渲染 20+ 分钟**:Remotion 首次跑要做 webpack bundling + 启动 compositor,慢是正常的;之后每次渲染 5~20 秒。
- **沙箱环境写 `/tmp` 路径可能失败**:抽帧或写中间文件用项目目录 `out/`,别用 `/tmp`。

## 参考文档

- `references/01-script-table.md` — 脚本表模板 + 完整示例
- `references/02-prompts.md` — 常用 prompt 原话,照抄改词
- `references/03-doubao-prompts.md` — 视频过场提示词
- `references/04-env-setup.md` — 本机环境明细与依赖安装
