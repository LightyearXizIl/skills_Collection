---
name: remotion-vox
description: 用 Remotion 把中文或英文旁白脚本制作成 Vox 风格解说视频、动态图表段或口播 B-roll；适用于脚本拆镜、代码绘图、cutout 排版、旁白对齐、预览与 MP4 渲染，不用于普通素材拼接剪辑。
license: MIT
---

# VoxMotion 自动剪辑

把“一句旁白对应一个视觉 beat”落实为可预览、可修改、可渲染的 Remotion 工程。默认优先用代码绘制信息图，只有具体人物、物体或真实动态镜头才使用外部素材。

## 开始前

1. 明确交付是完整视频还是插入口播的动态图形段，并确认画幅、旁白脚本、目标时长和已有素材。缺少但不影响开工的信息可先采用明确标注的临时值。
2. 不假设 Node.js、Remotion、FFmpeg、rembg、任何 MCP、API key 或登录态已经存在；先检查实际环境。不要把依赖安装到全局。
3. 数字、日期和事实性内容保留来源列；没有可靠来源时标成“待核实”，不要为了画面完整而编造。
4. 不经用户授权，不调用收费的生图、视频生成、TTS 或外部上传服务。

## 创建工程

优先运行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/new_project.ps1 -Destination "<绝对目标目录>"
```

脚本只会复制 [assets/template](assets/template)，目标目录非空时会停止，不覆盖现有工程。若用户已有 Remotion 工程，则在原工程内做最小改动，不复制模板覆盖。

## 工作流

1. 先读 [references/script-table.md](references/script-table.md)，把旁白拆成逐句视觉 beat，并标注素材来源与事实核验状态。
2. 再读 [references/visual-system.md](references/visual-system.md)，确定全片背景、字体、强调色、cutout 处理和动画节奏。默认全片锁定这套视觉系统。
3. 把场景写入 `src/config.ts`。优先使用 `barCompare`、`lineGrow`、`typewriter`、`flow` 四类代码组件；具体人物或物体再使用透明 PNG cutout。
4. 本地素材必须放在 `public/` 下，并在代码中通过 `staticFile()` 使用。视频和音频分别使用 `@remotion/media` 的 `Video` 与 `Audio`。
5. 动画只由 `useCurrentFrame()`、`spring()` 和 `interpolate()` 驱动；禁止 CSS transition、CSS keyframes 和随机时间源。每个 `Sequence` 都应预挂载。
6. 旁白放在所属场景内，使每个场景随自己的旁白开始并在场景结束时截断。场景时长应依据实际音频或已确认的时间码，而不是猜测。
7. 先运行 `npm run typecheck`，再运行 `npm run studio` 检查构图；最后用 `npm run render` 输出 `out/video.mp4`。
8. 渲染后至少检查开头、中段、结尾帧，以及字幕溢出、素材缺失、黑帧、图表数值、旁白切断和音乐盖住人声的问题。说明哪些是本地验证，哪些仍需真人或真实设备确认。

## 素材决策

- 代码即可表达：数字、柱状对比、折线、打字、流程框图、箭头和标签。
- 用户提供的图片：先确认使用范围；需要透明 cutout 时可在本地检测 `rembg` 后处理，保留原图。
- AI 生成的图片或视频：仅在代码与现有素材不能表达时使用。需要生成时读 [references/generated-media.md](references/generated-media.md)。
- 可复用提示：需要给用户或另一个模型下达制作指令时，读 [references/prompts.md](references/prompts.md)。

## 不可破坏的约束

- 先台词、后画面；每句旁白至少对应一个明确视觉动作或信息变化。
- 同一成片保持固定背景、字体和强调色；场景只替换中景与前景。
- 半调质感应预处理进图片，不在每帧做高成本像素处理。
- cutout 保持透明底、黑白主体和一致的强调色偏移描边。
- 不覆盖用户现有素材、配置或输出；需要替换时先使用新文件名或取得明确确认。
- 不把 Studio 预览当成最终成片证据；以实际渲染文件和抽帧检查为准。
