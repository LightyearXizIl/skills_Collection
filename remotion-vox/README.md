# VoxMotion 自动剪辑

`remotion-vox` 是一个用 Remotion 把中文或英文旁白脚本制作成 Vox 风格动态图形解说视频的 Skill。它支持逐句拆镜、代码图表、打字机、流程图、cutout 排版、旁白对齐、Studio 预览和 MP4 渲染。

## 使用

安装 Skill 后，可直接提供旁白脚本和成片要求：

```text
用 VoxMotion 自动剪辑把这段旁白制作成 16:9 的 Vox 风格解说视频
```

Skill 内置了可复制的 Remotion 工程模板，也可以在现有 Remotion 项目中做最小改动。新建独立工程时可运行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/new_project.ps1 -Destination "<绝对目标目录>"
```

## 依赖

- Node.js 和 npm
- 模板中固定的 Remotion 4.0.523、React 19.3.0 与 TypeScript 5.9.3
- FFmpeg 由 Remotion 渲染流程按实际环境使用
- `rembg`、AI 图像/视频、TTS 和外部上传服务均为可选能力，不内置 API key

## 设计边界

- 适合旁白驱动的动态图形解说视频，不用于普通素材拼接剪辑。
- 数字、日期和事实性内容需要保留来源；未核实内容必须明确标注。
- 不会在未授权时调用收费生成、TTS 或上传服务。

## 来源与许可

本 Skill 由 [LightyearXizIl](https://github.com/LightyearXizIl) 原创，采用 [MIT License](./LICENSE)。
