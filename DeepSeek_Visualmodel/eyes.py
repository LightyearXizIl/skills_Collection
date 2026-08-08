"""Call a vision model to describe an image. Print result to stdout.

Providers:
  zhipu     (default) - Zhipu GLM vision models. glm-4.6v-flash / glm-4v-flash are FREE.
  dashscope           - Alibaba Cloud Bailian Qwen vision models.

Environment:
  ZHIPU_API_KEY       - required for provider=zhipu (https://open.bigmodel.cn/)
  DASHSCOPE_API_KEY   - required for provider=dashscope (https://bailian.console.aliyun.com/)
"""

import sys
import os
import json
import base64
import hashlib
import hmac
import argparse
import time
from pathlib import Path

# Fix garbled Chinese on Windows terminal
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DEFAULT_PROVIDER = "zhipu"

ZHIPU_MODELS = [
    "glm-4.6v-flash",            # 最新免费视觉模型（图片/视频/文件），默认推荐
    "glm-4v-flash",              # 经典免费视觉模型
    "glm-4.1v-thinking-flash",   # 免费，带深度思考
    "glm-5v-turbo",              # 付费旗舰
]
DASHSCOPE_MODELS = [
    "qwen3-vl-plus",             # 精度最高
    "qwen3.6-plus",              # 通用备选
    "qwen3.6-flash",             # 速度优先
]
GEMINI_MODELS = [
    "gemini-3.6-flash",          # 免费层最强视觉（需代理）
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
]

DEFAULT_MODELS = {
    "zhipu": "glm-4.6v-flash",
    "dashscope": "qwen3-vl-plus",
    "gemini": "gemini-3.6-flash",
    "siliconflow": "PaddlePaddle/PaddleOCR-VL-1.5",  # 免费视觉/OCR
}

ZHIPU_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
SILICONFLOW_URL = "https://api.siliconflow.cn/v1/chat/completions"


def encode_image(image_path: str) -> str:
    """Encode a local image as a base64 data URL."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")

    suffix = path.suffix.lower()
    mime_map = {
        ".jpg": "jpeg", ".jpeg": "jpeg", ".png": "png",
        ".webp": "webp", ".bmp": "bmp",
    }
    mime = mime_map.get(suffix, "jpeg")
    return f"data:image/{mime};base64,{data}"


def zhipu_bearer_token(api_key: str) -> str:
    """Zhipu accepts either a direct API key (sk-...) or a JWT signed with the id.secret format."""
    if api_key.startswith("sk-") or "." not in api_key:
        return api_key

    def b64url(data) -> str:
        if isinstance(data, str):
            data = data.encode()
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

    key_id, secret = api_key.split(".", 1)
    header = {"alg": "HS256", "sign_type": "SIGN"}
    now = int(time.time())
    payload = {"api_key": key_id, "exp": now + 3600, "timestamp": now * 1000}
    signing_input = (
        f"{b64url(json.dumps(header, separators=(',', ':')))}."
        f"{b64url(json.dumps(payload, separators=(',', ':')))}"
    )
    signature = hmac.new(secret.encode(), signing_input.encode(), hashlib.sha256).digest()
    return f"{signing_input}.{b64url(signature)}"


def call_openai_compatible(url: str, api_key: str, model: str, image_ref: str, prompt: str) -> str:
    """Generic OpenAI-compatible chat/completions call (zhipu / gemini / siliconflow)."""
    import requests

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_ref}},
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    }

    resp = requests.post(
        url,
        headers={"Authorization": f"Bearer {api_key}"},
        json=payload,
        timeout=180,
    )

    if resp.status_code != 200:
        try:
            err = resp.json()
            msg = err.get("error", {}).get("message") or err.get("msg") or str(err)
        except Exception:
            msg = resp.text[:200]
        sys.stderr.write(f"API error ({resp.status_code}): {msg}\n")
        sys.exit(1)

    data = resp.json()
    return data["choices"][0]["message"]["content"]


def call_zhipu(model: str, image_ref: str, prompt: str) -> str:
    api_key = os.environ.get("ZHIPU_API_KEY", "")
    if not api_key:
        sys.stderr.write(
            "ZHIPU_API_KEY not set.\n"
            "Get a free key at https://open.bigmodel.cn/\n"
            "GLM-4V-Flash / GLM-4.6V-Flash are free models.\n"
        )
        sys.exit(1)
    return call_openai_compatible(ZHIPU_URL, zhipu_bearer_token(api_key), model, image_ref, prompt)


def call_gemini(model: str, image_ref: str, prompt: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        sys.stderr.write(
            "GEMINI_API_KEY not set.\n"
            "Get a free key at https://aistudio.google.com/apikey\n"
            "Gemini Flash models are free in the Free Tier.\n"
        )
        sys.exit(1)
    return call_openai_compatible(GEMINI_URL, api_key, model, image_ref, prompt)


def call_siliconflow(model: str, image_ref: str, prompt: str) -> str:
    api_key = os.environ.get("SILICONFLOW_API_KEY", "")
    if not api_key:
        sys.stderr.write(
            "SILICONFLOW_API_KEY not set.\n"
            "Get a free key at https://siliconflow.cn/\n"
            "Free models are tagged 'Free' in the model list.\n"
        )
        sys.exit(1)
    return call_openai_compatible(SILICONFLOW_URL, api_key, model, image_ref, prompt)


def call_dashscope(model: str, image_ref: str, prompt: str, high_res: bool) -> str:
    try:
        import dashscope
    except ImportError:
        sys.stderr.write("dashscope not installed. Run: pip install dashscope\n")
        sys.exit(1)

    api_key = os.environ.get("DASHSCOPE_API_KEY", dashscope.api_key or "")
    if not api_key:
        sys.stderr.write(
            "DASHSCOPE_API_KEY not set.\n"
            "Get a free key at https://bailian.console.aliyun.com/\n"
        )
        sys.exit(1)

    messages = [
        {
            "role": "user",
            "content": [
                {"image": image_ref},
                {"text": prompt},
            ],
        }
    ]

    kwargs = dict(model=model, messages=messages)
    if high_res:
        kwargs["vl_high_resolution_images"] = True

    resp = dashscope.MultiModalConversation.call(**kwargs)

    if resp.status_code != 200:
        sys.stderr.write(f"API error ({resp.status_code}): {resp.message}\n")
        sys.exit(1)

    return resp.output.choices[0].message.content[0]["text"]


def main():
    parser = argparse.ArgumentParser(description="Describe an image with a vision model")
    parser.add_argument("image", help="Path to the image file")
    parser.add_argument("--prompt",
                        default=(
                            "请精确描述这张图片的内容，不要遗漏细节。按以下结构输出：\n"
                            "1. 整体场景/布局（这是什么类型的图片？界面截图、照片、文档？）\n"
                            "2. 所有文字内容（逐字抄录，不要概括或改写）\n"
                            "3. UI 元素（按钮、菜单、输入框、弹窗、标签页等，含位置关系）\n"
                            "4. 视觉特征（颜色、图标、高亮、错误/警告标记）\n"
                            "5. 任何异常或值得注意的细节（报错信息、缺失内容、布局错乱等）"
                        ),
                        help="Custom prompt for the vision model")
    parser.add_argument("--provider", default=DEFAULT_PROVIDER,
                        choices=["zhipu", "dashscope", "gemini", "siliconflow"],
                        help=f"Vision API provider (default: {DEFAULT_PROVIDER})")
    parser.add_argument("--model", default=None,
                        help=f"Model name (default: {DEFAULT_MODELS[DEFAULT_PROVIDER]})")
    parser.add_argument("--file-url", action="store_true",
                        help="Use file:// URL instead of base64 (dashscope only)")
    parser.add_argument("--high-res", action="store_true",
                        help="Enable high resolution mode (dashscope only; zhipu handles it automatically)")
    args = parser.parse_args()

    provider = args.provider
    model = args.model or DEFAULT_MODELS[provider]

    if provider == "zhipu" and model not in ZHIPU_MODELS:
        sys.stderr.write(f"Warning: unknown model '{model}' for zhipu. Known: {', '.join(ZHIPU_MODELS)}\n")
    if provider == "dashscope" and model not in DASHSCOPE_MODELS:
        sys.stderr.write(f"Warning: unknown model '{model}' for dashscope. Known: {', '.join(DASHSCOPE_MODELS)}\n")
    if provider == "gemini" and model not in GEMINI_MODELS:
        sys.stderr.write(f"Warning: unknown model '{model}' for gemini. Known: {', '.join(GEMINI_MODELS)}\n")

    try:
        image_ref = encode_image(args.image)
    except FileNotFoundError as e:
        sys.stderr.write(f"{e}\n")
        sys.exit(1)

    if args.file_url:
        image_ref = f"file://{os.path.abspath(args.image)}"

    sys.stderr.write(f"Calling {provider}:{model}...\n")

    if provider == "zhipu":
        text = call_zhipu(model, image_ref, args.prompt)
    elif provider == "gemini":
        text = call_gemini(model, image_ref, args.prompt)
    elif provider == "siliconflow":
        text = call_siliconflow(model, image_ref, args.prompt)
    else:
        text = call_dashscope(model, image_ref, args.prompt, args.high_res)

    print(text)


if __name__ == "__main__":
    main()
