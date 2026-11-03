#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
restore_regions.py —— 把指定区域从「原图」贴回「精修图」

为什么需要它：图像编辑模型无法保证品牌字标（如 MΛGEΛSY）、机身 LOGO、包装印刷等
精细图形的保真——只要"重绘"就会改形或乱码。可靠做法是两步：
    第一步（尽力）：提示词里把这些区域声明为 PROTECTED REGIONS，排除在编辑之外；
    第二步（保证）：出图后把该区域的原始像素按掩膜贴回来。

本脚本执行第二步：以「原图」为像素来源、「精修图」为底图，按矩形 / 圆 / 圆环 /
自定义掩膜把指定区域的原像素混合回去，边缘做羽化过渡。

基本用法
--------
    python restore_regions.py --source 原图.jpg --edited 精修图.jpg --out 最终.jpg \
        --circle 512,640,120 --annulus 512,640,150,205 --feather 2

坐标辅助（强烈建议先跑一次）
----------------------------
    python restore_regions.py --source 原图.jpg --grid 100 --out 原图_网格.jpg
    # 生成的网格图上量出区域参数，再填进 --rect / --circle / --annulus

参数
----
    --rect  x1,y1,x2,y2          矩形（可重复）
    --circle cx,cy,r             圆（可重复）
    --ellipse cx,cy,ax,ay[,angle]  椭圆（可重复；适合透视下略呈椭圆的圆环）
                                   angle = 旋转角（度，逆时针为正），省略即轴对齐
    --annulus cx,cy,rin,rout[,angle]
                                 圆环（可重复；适合环带上的弧形丝印）；同样支持旋转角
    --mask  mask.png             自定义掩膜：白色=取原图，黑色=保留精修图（可重复）
    --invert-mask                反转自定义掩膜
    --feather F                  羽化半径（像素），默认 2.0；0 = 硬边
    --match source|edited        尺寸不一致时以谁为准（见下）
    --check                      只打印尺寸/区域/覆盖率，不写文件
    --grid N                     坐标辅助：在原图上每 N 像素画网格

尺寸（--match）
--------------
生图工具常按 1920px 输出，而原图可能是 1448px，两者尺寸往往不一致。
    --match source（默认）：输出与原图同尺寸，贴回的原图像素无损，但成品分辨率被降低。
    --match edited        ：输出与精修图同尺寸（成品交付常用），原图会被等比放大后贴回。
坐标一律填在「输出画布」的坐标系里：
    --match source 时填原图坐标；--match edited 时填精修图坐标。

依赖：Pillow
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps
except ImportError:  # pragma: no cover
    sys.exit("缺少依赖 Pillow。请先安装：pip install Pillow")

try:
    import numpy as np
except ImportError:  # --level-match 才需要
    np = None


def parse_floats(raw: str, n: int, label: str) -> tuple:
    parts = [p.strip() for p in str(raw).split(",")]
    if len(parts) != n:
        raise SystemExit(f"{label} 需要 {n} 个数值，收到的是：{raw}")
    try:
        return tuple(float(p) for p in parts)
    except ValueError:
        raise SystemExit(f"{label} 含有非数值内容：{raw}")


def parse_floats_any(raw: str, allowed: tuple, label: str) -> tuple:
    """接受多种个数（用于 --ellipse cx,cy,ax,ay 与 cx,cy,ax,ay,angle 都合法）。"""
    parts = [p.strip() for p in str(raw).split(",")]
    if len(parts) not in allowed:
        raise SystemExit(
            f"{label} 需要 {' 或 '.join(str(a) for a in allowed)} 个数值，收到的是：{raw}")
    try:
        return tuple(float(p) for p in parts)
    except ValueError:
        raise SystemExit(f"{label} 含有非数值内容：{raw}")


def draw_rotated_ellipse(mask: Image.Image, cx, cy, ax, ay, angle_deg, fill: int = 255) -> None:
    """在 mask 上叠加一个可旋转的实心椭圆（fill=0 即为挖空）。

    旋转过的圆环（斜视 / 手持角度下的支架）用轴对齐椭圆套不住，
    会把环带一角留在外面 —— 那一角就会被模型重绘，字标照样毁。
    """
    if abs(angle_deg) < 1e-6:
        ImageDraw.Draw(mask).ellipse([cx - ax, cy - ay, cx + ax, cy + ay], fill=fill)
        return
    R = int(math.ceil(math.hypot(ax, ay))) + 2
    layer = Image.new("L", (2 * R, 2 * R), 0)
    ImageDraw.Draw(layer).ellipse([R - ax, R - ay, R + ax, R + ay], fill=255)
    layer = layer.rotate(-angle_deg, resample=Image.BICUBIC, center=(R, R))
    if fill == 255:
        mask.paste(255, (int(round(cx)) - R, int(round(cy)) - R), layer)
    else:
        inv = ImageChops.invert(layer)
        mask.paste(0, (int(round(cx)) - R, int(round(cy)) - R), inv)


def build_mask(size: tuple, args) -> Image.Image:
    """构建 L 模式掩膜：255 = 取原图，0 = 保留精修图。"""
    w, h = size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)

    for raw in args.rect:
        x1, y1, x2, y2 = parse_floats(raw, 4, "rect")
        draw.rectangle([min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)], fill=255)

    for raw in args.circle:
        cx, cy, r = parse_floats(raw, 3, "circle")
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)

    for raw in args.ellipse:
        vals = parse_floats_any(raw, (4, 5), "ellipse")
        cx, cy, ax, ay = vals[:4]
        angle = vals[4] if len(vals) == 5 else 0.0
        draw_rotated_ellipse(mask, cx, cy, ax, ay, angle)

    for raw in args.annulus:
        vals = parse_floats_any(raw, (4, 5), "annulus")
        cx, cy, rin, rout = vals[:4]
        angle = vals[4] if len(vals) == 5 else 0.0
        layer = Image.new("L", (w, h), 0)
        draw_rotated_ellipse(layer, cx, cy, rout, rout, angle, fill=255)
        draw_rotated_ellipse(layer, cx, cy, rin, rin, angle, fill=0)
        mask = ImageChops.lighter(mask, layer)

    for raw in args.mask:
        p = Path(raw)
        if not p.exists():
            raise SystemExit(f"找不到掩膜文件：{p}")
        m = Image.open(p).convert("L")
        if m.size != (w, h):
            print(f"  提示：掩膜 {p.name} 尺寸 {m.size} 与画布 {(w, h)} 不一致，已缩放对齐")
            m = m.resize((w, h), Image.LANCZOS)
        if args.invert_mask:
            m = ImageOps.invert(m)
        mask = ImageChops.lighter(mask, m)

    return mask


def write_grid(source: Image.Image, args) -> int:
    step = max(10, int(args.grid))
    base = source.convert("RGB")
    draw = ImageDraw.Draw(base)
    try:
        font = ImageFont.load_default()
    except Exception:  # pragma: no cover
        font = None
    w, h = base.size
    for x in range(0, w, step):
        major = (x % (step * 5) == 0)
        draw.line([(x, 0), (x, h)], fill=(255, 0, 0) if major else (255, 170, 170), width=1)
        if major and font:
            draw.text((x + 2, 2), str(x), fill=(255, 0, 0), font=font)
    for y in range(0, h, step):
        major = (y % (step * 5) == 0)
        draw.line([(0, y), (w, y)], fill=(255, 0, 0) if major else (255, 170, 170), width=1)
        if major and font:
            draw.text((2, y + 2), str(y), fill=(255, 0, 0), font=font)
    out_path = Path(args.out) if args.out else source.with_name(source.stem + "_grid.png")
    base.save(out_path)
    print(f"网格图已写出：{out_path}")
    print(f"  网格间距 {step}px；红色主线每 {step * 5}px 标注一次坐标（左上角为 0,0）")
    return 0


def level_match(src_arr, edt_arr, mask: Image.Image):
    """把原图（贴回来源）的影调对齐到精修图，消除贴回边界的可见接缝。

    做法：取「贴回区外圈」的邻近环带（原图与精修图在同一位置都有内容），
    逐通道取 10% / 90% 分位点作为两级锚点，构造一条保持 0→0、255→255 的
    分段线性影调曲线，施加到整张原图。只动影调，不动字形、位置、结构。

    （不用单纯的 gain/offset：环带以暗区为主，纯线性匹配会把明亮金属环整体
    压暗；分位锚点能保住亮部，同时把暗部接缝抹平。）
    """
    if np is None:
        raise SystemExit("--level-match 需要 numpy：pip install numpy")
    blur = mask.filter(ImageFilter.GaussianBlur(radius=14.0))
    m = np.asarray(mask, dtype=np.float32) / 255.0
    b = np.asarray(blur, dtype=np.float32) / 255.0
    band = (b > 0.06) & (m < 0.03)
    if band.sum() < 500:
        print("  提示：邻近环带过小，跳过色调匹配")
        return src_arr
    out = src_arr.astype(np.float32).copy()
    desc = []
    for c in range(3):
        s = src_arr[..., c].astype(np.float32)[band]
        e = edt_arr[..., c].astype(np.float32)[band]
        lo_s, hi_s = (float(np.percentile(s, q)) for q in (10.0, 90.0))
        lo_e, hi_e = (float(np.percentile(e, q)) for q in (10.0, 90.0))
        x = out[..., c]
        if hi_s - lo_s < 6.0:  # 平坦区：退化为纯平移
            desc.append(f"ch{c}: 平移 {lo_e - lo_s:+.1f}")
            out[..., c] = x + (lo_e - lo_s)
            continue
        scale = (hi_e - lo_e) / (hi_s - lo_s)
        desc.append(f"ch{c}: 暗{lo_s:.0f}→{lo_e:.0f} 亮{hi_s:.0f}→{hi_e:.0f} 斜率{scale:.2f}")
        y = np.empty_like(x)
        seg1 = x <= lo_s
        seg2 = (x > lo_s) & (x < hi_s)
        seg3 = ~(seg1 | seg2)
        y[seg1] = x[seg1] * (lo_e / lo_s if lo_s > 1.0 else 1.0)
        y[seg2] = lo_e + (x[seg2] - lo_s) * scale
        y[seg3] = hi_e + (x[seg3] - hi_s) * ((255.0 - hi_e) / max(1e-6, 255.0 - hi_s))
        out[..., c] = y
    print("  色调匹配 : " + " | ".join(desc))
    return np.clip(out, 0, 255).astype(np.uint8)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="把指定区域从原图贴回精修图（保护字标 / LOGO / 印刷不被重绘破坏）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--source", required=True, help="原图路径（像素来源）")
    ap.add_argument("--edited", help="精修图路径（底图）")
    ap.add_argument("--out", help="输出路径；--grid 模式下为网格图输出路径")
    ap.add_argument("--rect", action="append", default=[], help="矩形 x1,y1,x2,y2，可重复")
    ap.add_argument("--circle", action="append", default=[], help="圆 cx,cy,r，可重复")
    ap.add_argument("--ellipse", action="append", default=[],
                    help="椭圆 cx,cy,ax,ay[,angle]，可重复；第 5 个数为旋转角（度，逆时针为正）")
    ap.add_argument("--annulus", action="append", default=[],
                    help="圆环 cx,cy,rin,rout[,angle]，可重复；第 5 个数为旋转角（度，逆时针为正）")
    ap.add_argument("--mask", action="append", default=[], help="自定义掩膜 PNG，可重复")
    ap.add_argument("--invert-mask", action="store_true", help="反转自定义掩膜")
    ap.add_argument("--feather", type=float, default=2.0, help="羽化半径（像素），默认 2.0；0 = 硬边")
    ap.add_argument("--match", choices=["source", "edited"], default="source",
                    help="尺寸不一致时以谁为准：source=输出与原图同尺寸且贴回像素无损（默认）；edited=输出与精修图同尺寸")
    ap.add_argument("--level-match", action="store_true",
                    help="把贴回区的影调线性对齐到精修图（消除可见接缝；需要 numpy）")
    ap.add_argument("--sharpen-amount", type=float, default=0.0,
                    help="贴回区锐度补偿（USM 强度 %%，默认 0=关闭）。大幅放大贴回时用，建议 60~90")
    ap.add_argument("--sharpen-radius", type=float, default=2.0, help="USM 半径，默认 2.0")
    ap.add_argument("--sharpen-threshold", type=int, default=4, help="USM 阈值，默认 4")
    ap.add_argument("--grid", type=int, help="坐标辅助模式：每 N 像素画网格")
    ap.add_argument("--check", action="store_true", help="只打印检查信息，不写文件")
    args = ap.parse_args()

    src_path = Path(args.source)
    if not src_path.exists():
        raise SystemExit(f"找不到原图：{src_path}")
    source = Image.open(src_path)

    if args.grid:
        return write_grid(source, args)

    if not args.edited or not args.out:
        raise SystemExit("需要同时提供 --edited 与 --out（或使用 --grid 模式）")

    edited_path = Path(args.edited)
    if not edited_path.exists():
        raise SystemExit(f"找不到精修图：{edited_path}")
    edited = Image.open(edited_path)

    # 尺寸不一致是常态（生图工具常按 1920px 输出，而原图可能是 1448px），
    # 这里自动对齐，并把“被缩放的那一侧”如实告知。
    if source.size != edited.size:
        if args.match == "source":
            print(f"尺寸不一致：原图 {source.size}，精修图 {edited.size}")
            print(f"  按 --match source 处理：精修图已缩放到 {source.size}，贴回的原图区域保持像素无损。")
            edited = edited.resize(source.size, Image.LANCZOS)
        else:
            print(f"尺寸不一致：原图 {source.size}，精修图 {edited.size}")
            print(f"  按 --match edited 处理：原图已缩放到 {edited.size}，贴回区域会被重采样（略失真）。")
            source = source.resize(edited.size, Image.LANCZOS)

    mask = build_mask(source.size, args)
    total = float(source.size[0] * source.size[1])
    covered = sum(mask.histogram()[128:]) / total

    print(f"画布尺寸 : {source.size[0]} x {source.size[1]}")
    print(f"区域数量 : rect={len(args.rect)}  circle={len(args.circle)}  ellipse={len(args.ellipse)}  annulus={len(args.annulus)}  mask={len(args.mask)}")
    print(f"覆盖比例 : {covered * 100:.2f}%")

    if covered == 0:
        raise SystemExit("掩膜为空——至少要给一个 --rect / --circle / --annulus / --mask 区域。")
    if covered > 0.60:
        print("  警告：覆盖比例超过 60%，贴回面积过大，精修效果会被大面积覆盖。")

    if args.check:
        return 0

    if args.level_match:
        matched = level_match(
            np.asarray(source.convert("RGB")),
            np.asarray(edited.convert("RGB")),
            mask,
        )
        source = Image.fromarray(matched)

    if args.sharpen_amount and args.sharpen_amount > 0:
        # 贴回区会被按比例放大（例如原图 1086px → 4K），放大后偏软；
        # 用轻量 USM 把"边缘锐度"提到与周围相当。只改变锐度，不改字形与位置。
        source = source.convert("RGB").filter(
            ImageFilter.UnsharpMask(
                radius=float(args.sharpen_radius),
                percent=int(round(float(args.sharpen_amount))),
                threshold=int(args.sharpen_threshold),
            )
        )
        print(f"  锐度补偿 : USM 强度 {args.sharpen_amount:.0f}% 半径 {args.sharpen_radius} 阈值 {args.sharpen_threshold}")

    if args.feather and args.feather > 0:
        mask = mask.filter(ImageFilter.GaussianBlur(radius=float(args.feather)))

    src_rgba = source.convert("RGBA")
    edt_rgba = edited.convert("RGBA")
    src_rgba.putalpha(mask)
    out = Image.alpha_composite(edt_rgba, src_rgba)

    out_path = Path(args.out)
    suffix = out_path.suffix.lower()
    # 两图都没有真透明通道时，PNG 也存成 RGB —— 4K 交付下 RGBA 白胖近三成
    had_alpha = any(("A" in (im.mode or "")) for im in (source, edited))
    if suffix in (".jpg", ".jpeg"):
        out.convert("RGB").save(out_path, quality=96, subsampling=1, optimize=True)
    elif not had_alpha:
        out.convert("RGB").save(out_path)
    else:
        out.save(out_path)
    print(f"已写出   : {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
