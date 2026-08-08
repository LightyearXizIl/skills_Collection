---
name: DeepSeek_Visualmodel
description: "Use when the user shares an image that the current model can't natively see, or when the user asks to analyze/describe/understand an image. Route every image through this skill — send the image path to eyes.py, which calls a vision model (default glm-4.6v-flash, FREE) via Zhipu and returns a Chinese text description. Then answer the user's question based on that description."
---

# Image Vision (智谱 GLM Vision Models)

## Overview

This skill bundles a Python script (`eyes.py`) that sends an image to 智谱 (Zhipu)'s GLM vision models and returns a detailed Chinese text description. Use this whenever the user wants help with an image.

**Background:** The current model (DeepSeek V4 Flash) cannot natively see images. This skill bridges that gap by routing images through GLM vision models — the vision model does the seeing, and the text description is fed back into the conversation so the main model can reason about the image content.

## When to use

- User sends an image that the current model can't display (shows as [Unsupported Image])
- User asks "what's in this image?", "describe this picture", "analyze this screenshot"
- User provides an image path and wants help understanding it

## How to use

### Step 1: Run the script

**Always use `glm-4.6v-flash` (free, best quality).** I can't see the image before running the model, so there's no way to "pick the right model" — just use the best one every time.

**Always pass the user's exact question as `--prompt`:**

```bash
python "E:\Vibe coding\skills\DeepSeek_Visualmodel\eyes.py" "<image_path>" \
  --prompt "<用户的具体问题>"
```

Only switch to `glm-4v-flash` if the user explicitly asks for speed over accuracy.

### Step 2: Read the output and answer

The script prints the description to stdout. Read it directly from the command output and answer the user's question about the image based on that description.

### Prerequisites

- `pip install dashscope requests` (already installed globally; requests is used for the Zhipu API)
- `ZHIPU_API_KEY` environment variable must be set (get a free key at https://open.bigmodel.cn/)
- `glm-4.6v-flash` / `glm-4v-flash` are **FREE** — no payment needed

## Available Models

### zhipu（默认，免费）

| Model | Use case | Price |
|-------|----------|-------|
| `glm-4.6v-flash` (default) | **Always use.** Latest free vision model, 128K context, strong OCR/table/detail. | 免费 |
| `glm-4v-flash` | Classic free vision model. Quick look, simple photos. | 免费 |
| `glm-4.1v-thinking-flash` | Free, with deep reasoning (slower). | 免费 |
| `glm-5v-turbo` | Paid flagship, highest accuracy. | 付费 |

### gemini（免费层，需代理）

| Model | Use case | Price |
|-------|----------|-------|
| `gemini-3.6-flash` (default) | Free Tier strongest vision. | 免费 |
| `gemini-3.5-flash` / `gemini-3.5-flash-lite` | Alternatives. | 免费 |

### siliconflow（国内直连）

| Model | Use case | Price |
|-------|----------|-------|
| `PaddlePaddle/PaddleOCR-VL-1.5` (default) | Free OCR / visual text extraction. | 免费 |

### dashscope（备选，百炼 key 额度已耗尽）

`qwen3-vl-plus` / `qwen3.6-plus` / `qwen3.6-flash`

## Options

| Flag | Description |
|------|-------------|
| `--provider` | `zhipu` (default), `gemini`, `siliconflow` or `dashscope` |
| `--model` | Switch model, e.g. `glm-4v-flash` for a quick look |
| `--prompt` | **Always pass the user's exact question.** Targeted questions dramatically outperform the generic default. |
| `--high-res` | dashscope only; other providers handle high-res automatically — not needed |

## Environment Variables

| Variable | Provider | Where to get |
|----------|----------|--------------|
| `ZHIPU_API_KEY` | zhipu | https://open.bigmodel.cn/ |
| `GEMINI_API_KEY` | gemini | https://aistudio.google.com/apikey |
| `SILICONFLOW_API_KEY` | siliconflow | https://siliconflow.cn/ |
| `DASHSCOPE_API_KEY` | dashscope | https://bailian.console.aliyun.com/ |

## Notes

- **Always `glm-4.6v-flash`.** I can't preview the image, so use the best free model every time.
- Description prints to stdout, read it directly from the command output.
- If the API returns 401/403, the ZHIPU_API_KEY is invalid or missing — remind the user to check it at https://open.bigmodel.cn/usercenter/proj-mgmt/apikeys.
