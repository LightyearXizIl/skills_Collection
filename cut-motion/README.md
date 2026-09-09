# cut-motion

把本地口播素材转换为精剪成片的 Agent 工作流 Skill，覆盖转写、粗剪审核、字幕或动态文案、HyperFrames/GSAP 动效、校验、渲染和同任务修订。

## 使用

```text
使用 $cut-motion 剪辑这个口播视频：D:\Videos\source.mp4
使用 $cut-motion 继续上一版任务，只调整动画排版，不改粗剪。
```

Skill 会把内置运行时复制到独立任务目录，不会把用户媒体、日志或渲染结果写回 Skill 目录。真正处理视频前需完整阅读运行时的 `AGENTS.md`，并遵守其中的审核状态机和授权边界。

## 环境与许可

- 基础环境：Python 3、Node.js/npm、FFmpeg/FFprobe；Windows 使用 WSL2 或等效 Unix shell。
- 完整流程还会按任务使用 ChatCut、HyperFrames 和 GSAP。安装依赖、启用插件、登录服务或下载字体前必须取得用户明确同意。
- Skill 本身不包含 API key、用户媒体或所需的 Smiley Sans 字体。
- 来源：[Endless1936/cut-motion](https://github.com/Endless1936/cut-motion)，固定快照 `b4afa7f2823db07322caf624ffc9096ea48145c9`。
- 上游代码、文档和可复用模板采用 Apache-2.0；人物参考图及第三方工具、字体和媒体的权利边界以同目录 `NOTICE` 为准。
