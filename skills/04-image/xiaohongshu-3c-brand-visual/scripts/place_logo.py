#!/usr/bin/env python3
"""把 MAGEASY 字标按规范压到图片左上角。

用法:
    python place_logo.py --image out.png
    python place_logo.py --image out.png --color white --width 28 --out final.png

规则来自 references/06-brand-logo.md：
  · 位置固定左上角，距左 8.9% 画宽，距上 6.7% 画高
  · 宽默认 26% 画宽（24–30% 区间），高按 7.08:1 自动
  · 只有纯黑 #000000 与纯白 #FFFFFF 两种，不透明、无描边、无投影
  · --color auto 时按覆盖区平均明度自动选色（>0.6 用黑，否则用白）

字标必须用本脚本压，不要交给生成模型——模型会把 MΛGEΛSY 写成 MAGEASY。
"""
import argparse
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.join(HERE, "..", "assets", "brand")
LOGOS = {"black": os.path.join(BRAND, "mageasy-black.png"),
         "white": os.path.join(BRAND, "mageasy-white.png")}

MARGIN_X = 0.089
MARGIN_Y = 0.067
DEFAULT_WIDTH = 0.26


def mean_luma(img, box):
    region = img.crop(box).convert("L").resize((24, 8))
    px = list(region.getdata())
    return sum(px) / len(px) / 255.0


def main():
    ap = argparse.ArgumentParser(description="压 MAGEASY 字标到左上角")
    ap.add_argument("--image", required=True)
    ap.add_argument("--out", default="")
    ap.add_argument("--color", default="auto", choices=["auto", "black", "white"])
    ap.add_argument("--width", type=float, default=DEFAULT_WIDTH * 100,
                    help="字标宽度占画宽的百分比，默认 26")
    ap.add_argument("--logo", default="", help="自定义字标路径，覆盖内置素材")
    a = ap.parse_args()

    base = Image.open(a.image).convert("RGBA")
    W, H = base.size

    lw = max(1, int(round(W * a.width / 100.0)))
    src = a.logo or LOGOS["black"]
    logo = Image.open(src).convert("RGBA")
    lh = max(1, int(round(logo.height * lw / logo.width)))
    logo = logo.resize((lw, lh), Image.LANCZOS)

    x = int(round(W * MARGIN_X))
    y = int(round(H * MARGIN_Y))

    if a.color == "auto":
        luma = mean_luma(base, (x, y, min(W, x + lw), min(H, y + lh)))
        color = "black" if luma > 0.6 else "white"
        if not a.logo:
            logo = Image.open(LOGOS[color]).convert("RGBA").resize((lw, lh), Image.LANCZOS)
        print(f"auto color: {color} (luma {luma:.2f})")
    else:
        color = a.color
        if not a.logo:
            logo = Image.open(LOGOS[color]).convert("RGBA").resize((lw, lh), Image.LANCZOS)

    if x + lw > W or y + lh > H:
        print("warning: logo exceeds canvas, shrink --width", file=sys.stderr)

    base.alpha_composite(logo, (x, y))
    out = a.out or os.path.splitext(a.image)[0] + "_logo" + os.path.splitext(a.image)[1]
    base.convert("RGB").save(out, quality=95)
    print(f"logo {lw}x{lh} at ({x},{y}) color={color} -> {out}")


if __name__ == "__main__":
    main()
