#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
zoom_grid.py —— 放大裁切 + 细网格，用来"读"出精确坐标

场景：`restore_regions.py` 需要环带、内孔等区域的坐标。自动检测在反光强的实拍图上
并不可靠，最稳的办法是人眼在放大网格上读数。本脚本把指定区域放大若干倍并叠加
细网格（标注的是**原图坐标**），读数即可直接填进回贴命令。

用法
----
    # 看整图（每 50px 一格）
    python zoom_grid.py --image 原图.jpg --step 50 --out 全图_网格.png

    # 只看光环区域，放大 3 倍，每 20px 一格
    python zoom_grid.py --image 原图.jpg --box 600,560,1000,940 --scale 3 --step 20 --out 光环_网格.png

参数
----
    --image   输入图
    --box     x1,y1,x2,y2 裁切框（原图坐标）；省略则整图
    --scale   放大倍数（默认 3）
    --step    网格间距，原图像素（默认 20）
    --out     输出路径
    --dots    每隔 N 个网格画一个点（默认 0 = 不画）
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover
    sys.exit("缺少依赖 Pillow。请先安装：pip install Pillow")


def main() -> int:
    ap = argparse.ArgumentParser(description="放大裁切 + 原图坐标细网格")
    ap.add_argument("--image", required=True)
    ap.add_argument("--box", help="x1,y1,x2,y2（原图坐标），省略=整图")
    ap.add_argument("--scale", type=int, default=3)
    ap.add_argument("--step", type=int, default=20)
    ap.add_argument("--out")
    ap.add_argument("--dots", type=int, default=0)
    args = ap.parse_args()

    src = Path(args.image)
    if not src.exists():
        raise SystemExit(f"找不到图片：{src}")
    img = Image.open(src).convert("RGB")
    W, H = img.size

    if args.box:
        try:
            x1, y1, x2, y2 = [int(round(float(v))) for v in args.box.split(",")]
        except ValueError:
            raise SystemExit("--box 需要 4 个整数：x1,y1,x2,y2")
    else:
        x1, y1, x2, y2 = 0, 0, W, H
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(W, x2), min(H, y2)
    if x2 - x1 < 8 or y2 - y1 < 8:
        raise SystemExit("裁切区域太小")

    crop = img.crop((x1, y1, x2, y2))
    s = max(1, args.scale)
    big = crop.resize(((x2 - x1) * s, (y2 - y1) * s), Image.LANCZOS)
    d = ImageDraw.Draw(big)
    try:
        font = ImageFont.load_default()
    except Exception:  # pragma: no cover
        font = None

    step = max(2, args.step)
    # 竖线（沿 x 方向，标注原图 x 坐标）
    gx = (x1 // step) * step
    while gx <= x2:
        px = (gx - x1) * s
        if px >= 0:
            d.line([(px, 0), (px, big.size[1])], fill=(255, 90, 90), width=1)
            if font:
                d.text((px + 2, 2), str(gx), fill=(255, 0, 0), font=font)
                d.text((px + 2, big.size[1] - 12), str(gx), fill=(255, 0, 0), font=font)
        gx += step
    # 横线（沿 y 方向，标注原图 y 坐标）
    gy = (y1 // step) * step
    while gy <= y2:
        py = (gy - y1) * s
        if py >= 0:
            d.line([(0, py), (big.size[0], py)], fill=(90, 140, 255), width=1)
            if font:
                d.text((2, py + 2), str(gy), fill=(0, 60, 220), font=font)
                d.text((big.size[0] - 40, py + 2), str(gy), fill=(0, 60, 220), font=font)
        gy += step

    if args.dots and args.dots > 0:
        gx = (x1 // args.dots) * args.dots
        while gx <= x2:
            gy = (y1 // args.dots) * args.dots
            while gy <= y2:
                px, py = (gx - x1) * s, (gy - y1) * s
                d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(0, 200, 0))
                gy += args.dots
            gx += args.dots

    out = Path(args.out) if args.out else src.with_name(src.stem + f"_zoom{s}x.png")
    big.save(out)
    print(f"已写出：{out}")
    print(f"  裁切 {x1},{y1} → {x2},{y2}（{x2 - x1}x{y2 - y1}），放大 {s}x → {big.size[0]}x{big.size[1]}")
    print(f"  网格间距 {step}px（原图坐标）：红线=竖线并标注原图 x，蓝线=横线并标注原图 y")
    print("  读数示例：环左外缘落在 x=657 与 x=677 之间 → 取 665 填入命令。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
