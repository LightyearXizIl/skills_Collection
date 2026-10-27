# 本机环境

这是用户提供并在整合时检查的本机配置；执行每次任务仍需验证路径与依赖，不依赖 PATH 上的其他版本。

| 用途 | 路径 |
|---|---|
| 项目根目录 | E:\A-自媒体\林依依\抖音-林依依 |
| 视频项目根 | E:\A-自媒体\林依依\抖音-林依依\01_视频项目 |
| FFmpeg | C:\Users\16054\Documents\ComfyUI\tools\ffmpeg\ffmpeg.exe |
| FFprobe | C:\Users\16054\Documents\ComfyUI\tools\ffmpeg\ffprobe.exe |
| Python | C:\Users\16054\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe |
| large-v3 | E:\Comfy-Desktop\ComfyUI-Shared\models\speech_recognition\faster-whisper-large-v3 |
| 字体 | C:\Windows\Fonts\NotoSerifSC-VF.ttf |

Python 需要 numpy、Pillow、faster-whisper。语音识别脚本只接受已存在的本地模型目录，使用 local_files_only；缺失就报错，不联网下载。字体和工具缺失也直接报告，不切换宋体或其他字体。

原始执行包保留在：
`E:\A-自媒体\林依依\抖音-林依依\00_长期资产库\2026-10-19_v1_唱歌视频字幕流水线\一键复制给Codex.txt`

整合裁决：采用该包的歌词逐字保真、干声实测、ASR 仅核句序、标题居中及 ASCII 临时目录；保留既有默认复制归档，移动改为具体任务授权后可选。修复原脚本的相关运算效率、音名映射和测量 JSON 缺失标记；弱相关不按零偏移处理。原包关于 ASR 固定偏移、路径错误与字体日志的经验不能视为所有输入均成立的技术结论。
