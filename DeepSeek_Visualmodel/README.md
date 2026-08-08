# DeepSeek_Visualmodel

给**无原生视觉的大模型**（如 DeepSeek 等纯文本模型）"看图"的能力。把图片发送到外部视觉模型，返回详细的中文文字描述，让主模型基于描述理解图片内容。

## 这个技能是干嘛的

- **场景**：你的 AI 助手看不到你发的图片（显示"不支持的图片"），用它把图片变成文字描述
- **原理**：`eyes.py` 把图片 base64 编码 → 调用视觉大模型 → 输出中文描述（截图内容、UI 元素、文字、颜色、异常等）
- **适用**：截图分析、报错排查、OCR 文字提取、图片内容问答

## 支持的视觉服务（4 选 1）

| Provider | 默认模型 | 费用 | 特点 |
|----------|----------|------|------|
| `zhipu`（默认） | `glm-4.6v-flash` | 免费 | 128K 上下文，OCR/细节强，国内直连 |
| `gemini` | `gemini-3.6-flash` | 免费层 | 视觉能力最强（国内需代理） |
| `siliconflow` | `PaddlePaddle/PaddleOCR-VL-1.5` | 免费 | OCR 文字提取专用 |
| `dashscope` | `qwen3-vl-plus` | 按量付费 | 阿里云百炼（需充值） |

## API Key 配置（重要，不内置密钥）

本技能**不包含任何 API key**，请自行申请并设置环境变量（Windows 用户级或 shell 环境）：

| 环境变量 | 申请地址 |
|----------|----------|
| `ZHIPU_API_KEY` | https://open.bigmodel.cn/ |
| `GEMINI_API_KEY` | https://aistudio.google.com/apikey |
| `SILICONFLOW_API_KEY` | https://siliconflow.cn/ |
| `DASHSCOPE_API_KEY` | https://bailian.console.aliyun.com/ |

至少配置一个（推荐 `ZHIPU_API_KEY`，全免费）。

## 使用方法

```bash
# 基本用法（默认 zhipu / glm-4.6v-flash）
python eyes.py "图片.png" --prompt "这张图里写了什么？"

# 指定视觉服务
python eyes.py "图片.png" --prompt "详细描述这张截图" --provider gemini
python eyes.py "图片.png" --prompt "提取图中所有文字" --provider siliconflow

# 完整参数
python eyes.py <图片路径> --prompt <问题> [--provider zhipu|gemini|siliconflow|dashscope] [--model <模型名>]
```

## 注意事项

- 智谱旧格式 key（`id.secret`）会自动做 JWT 认证，`sk-` 开头的新 key 直接使用
- SiliconFlow 的 OCR 模型需要**真实尺寸图片**（过小会报错）
- 免费模型偶尔遇到 429 限流或网络抖动，稍等重试即可
- 结果输出到标准输出（stdout），错误信息输出到 stderr
