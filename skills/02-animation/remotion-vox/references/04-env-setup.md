# 本机环境明细与依赖安装

实测日期:2026-09-10。以下结论**以实测为准**,原始 skill 文档的假设有两处不成立。

## 实测结果

| 依赖 | 状态 | 路径/版本 | 备注 |
|---|---|---|---|
| Node.js | ✅ 已装 | `C:\Users\EDY\.workbuddy\binaries\node\versions\22.22.2-2\node.exe` | v22.22.2,满足 ≥18 |
| npm | ✅ 已装 | 同目录 `npm.cmd` | v12 附带。**别用系统 npm** |
| Python | ✅ 已装 | `C:\Users\EDY\.workbuddy\binaries\python\versions\3.13.12\python.exe` | 3.13.14 |
| ffmpeg | ⚠️ **系统未装** | — | **不影响出片**:Remotion 4 内置 ffmpeg |
| rembg | ❌ **未装** | — | 抠图功能需先装,见下 |

### 与原始文档的两处出入

原文档写「ffmpeg:已装」「rembg:已装(免费、离线)」,**实测均不成立**。如果你看到旧版描述,忽略它。

## 命令速查(Windows / Git Bash)

```bash
# Node 与 npm(托管路径,必须写全)
NODE="C:/Users/EDY/.workbuddy/binaries/node/versions/22.22.2-2/node.exe"
NPM="C:/Users/EDY/.workbuddy/binaries/node/versions/22.22.2-2/npm.cmd"

# Python(托管路径)
PY="C:/Users/EDY/.workbuddy/binaries/python/versions/3.13.12/python.exe"
```

## 关于 ffmpeg

Remotion 4 的 `@remotion/renderer` 自带 ffmpeg 二进制,渲染 mp4 / 抽帧 / 编码全部走它,
**不需要系统级 ffmpeg**。

只有在你想手动做这些时才需要单独装:
- 命令行手动转码、剪切、合流
- 把渲染产物再压一遍

要装的话(任选一):
```bash
winget install ffmpeg        # WinGet
choco install ffmpeg         # Chocolatey
```

## rembg 安装(抠图功能)

不抠图可以完全不装 —— 用 `buddy-image-processing` 技能的通用 matting 替代。

```bash
PY="C:/Users/EDY/.workbuddy/binaries/python/versions/3.13.12/python.exe"

# 安装(CPU 版,无需 CUDA)
"$PY" -m pip install "rembg[cpu]" onnxruntime
```

首次运行会下载 u2net 模型(约 170MB),之后离线可用。

用法:
```bash
"$PY" -c "from rembg import remove; open('out.png','wb').write(remove(open('输入.jpg','rb').read()))"
```

**注意**:下载模型需要联网;若网络不通,改用 `buddy-image-processing` 技能。

## 中文 TTS 安装(可选)

```bash
PY="C:/Users/EDY/.workbuddy/binaries/python/versions/3.13.12/python.exe"
"$PY" -m pip install edge-tts
```

生成旁白:
```bash
"$PY" -m edge_tts --voice zh-CN-YunxiNeural \
  --text "这一集,我们拆开看三个数字。" \
  --write-media narration.mp3
```

常用中文音色:

| voice_id | 特点 |
|---|---|
| `zh-CN-YunxiNeural` | 男声,解说感强,**默认推荐** |
| `zh-CN-YunjianNeural` | 男声,浑厚,适合纪录片 |
| `zh-CN-XiaoxiaoNeural` | 女声,温柔 |
| `zh-CN-YunyangNeural` | 男声,新闻播报 |

先听再定:
```bash
"$PY" -m edge_tts --list-voices | grep zh-CN
```

## 首次渲染会慢

Remotion 首次渲染会下载无头 Chromium(约 150MB),**只此一次**,之后有缓存。
看到卡在 "Downloading browser" 属正常,别中断。

## 验证环境

复制模板 → `npm install` → `npm run smoke`,能出 `out/smoke.mp4` 就说明整条管线通。

```bash
cd <你的项目目录>
"$NPM" install
"$NPM" run smoke
```
