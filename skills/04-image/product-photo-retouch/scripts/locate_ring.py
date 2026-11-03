#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
locate_ring.py —— 在实拍图上定量定位「圆环支架」（圆心 + 内外半径）

用途：restore_regions.py 需要知道环的圆心/半径，才能把环带上的弧形字标与
环内孔的 LOGO 从原图贴回。手量容易偏，本脚本给出可复核的数值与叠加预览。

原理
----
环在任何方向上都有两条强边缘：外缘（金属→背景/平台）与内缘（金属→内孔）。
对每个候选 (cx, cy, r_out)：
    得分 = 外缘圆周上的梯度均值 + 内缘圆周上的梯度均值
内缘半径独立搜索（不能按固定比例，环带厚度因机位而异），取内缘边缘最强的半径。
梯度取 3x3 邻域最大值，容忍 1px 的圆不完美与轻微透视。

为什么可靠（与上一版的差别）
--------------------------
上一版同时搜索「外缘 + 内孔 + 环外」三项并按对比度加权，在光面机身背面
（大面积室内反光、亮环叠在亮反光上）会锁到错误的小亮斑。
本版只要求「外缘一圈亮、内缘一圈亮」，并且**强制输出叠加预览与双缘强度**，
强度过低会直接告警——不合格的结果不会被当成答案交出去。

用法
----
    python locate_ring.py --image 图.jpg --out-prefix 环区
    # 生成 环区_fit.png（叠加预览，务必人眼复核）并打印可直接复制的回贴命令

    # 建议同时给两张图做交叉验证（原图 + 精修输出）：
    python locate_ring.py --image 精修图.jpg --verify-with 原图.jpg --out-prefix 环区

输出
----
    环区_fit.png      拟合结果叠加图（红=内缘 绿=外缘 蓝=环带中线）
    控制台            环心 / 内外半径 / 双缘强度 / 置信度告警 / 回贴命令

依赖：Pillow、numpy
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import numpy as np
    from PIL import Image, ImageDraw
except ImportError:  # pragma: no cover
    sys.exit("缺少依赖。请先安装：pip install Pillow numpy")


def edge_map(gray: np.ndarray) -> np.ndarray:
    gy, gx = np.gradient(gray.astype(np.float32))
    return np.hypot(gx, gy)


def radial_profile(mag: np.ndarray, cx: float, cy: float, radii: np.ndarray, n_ang: int) -> np.ndarray:
    """一次算出「同一圆心、各半径」圆周上的梯度强度（3x3 邻域取最大，容忍 1px 误差）。

    关键优化：对每个候选圆心只做一次半径扫描，外缘与内缘都从这条曲线上取值，
    避免在 (圆心 × 外径 × 内径) 三重循环里重复采样（旧写法在本项目图上要跑 3 分钟以上）。
    """
    h, w = mag.shape
    ang = np.linspace(0.0, 2.0 * np.pi, n_ang, endpoint=False)
    cos, sin = np.cos(ang), np.sin(ang)
    xs = cx + radii[:, None] * cos[None, :]
    ys = cy + radii[:, None] * sin[None, :]
    xi = np.clip(np.round(xs).astype(np.int32), 0, w - 1)
    yi = np.clip(np.round(ys).astype(np.int32), 0, h - 1)
    vals = mag[yi, xi]
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            vals = np.maximum(vals, mag[np.clip(yi + dy, 0, h - 1), np.clip(xi + dx, 0, w - 1)])
    return vals.mean(axis=1)


def fit(mag, cx0, cx1, cy0, cy1, r0, r1, coarse=5, inner_lo=0.55, inner_hi=0.95):
    """粗搜 → 细搜。返回 (best, top6)；best = (总分, 外缘, 内缘, cx, cy, r_out, r_in)。"""
    h, w = mag.shape
    cx0, cx1 = max(0, int(cx0)), min(w - 1, int(cx1))
    cy0, cy1 = max(0, int(cy0)), min(h - 1, int(cy1))
    r0, r1 = max(3, int(r0)), int(r1)
    radii_full = np.arange(r0, r1 + 1, dtype=float)

    def sweep(cxs, cys, r_step, n_ang):
        rr = radii_full[::r_step]
        cands = []
        for cx in cxs:
            for cy in cys:
                prof = radial_profile(mag, cx, cy, rr, n_ang)
                for j in range(len(rr)):
                    r_out = rr[j]
                    k0 = int(np.searchsorted(rr, inner_lo * r_out))
                    k1 = int(np.searchsorted(rr, inner_hi * r_out)) - 1
                    if k1 <= k0:
                        continue
                    k = k0 + int(np.argmax(prof[k0:k1 + 1]))          # 最强内缘（可能是环带内部倒角线）
                    k1h = int(np.searchsorted(rr, 0.82 * r_out)) - 1   # 内孔边界候选（比例 ≤0.82）
                    kh = k0 + int(np.argmax(prof[k0:k1h + 1])) if k1h > k0 else k
                    cands.append((prof[j] + prof[k], prof[j], prof[k], cx, cy,
                                  int(r_out), int(rr[k]), int(rr[kh])))
        cands.sort(key=lambda t: -t[0])
        return cands

    c1 = sweep(range(cx0, cx1 + 1, coarse), range(cy0, cy1 + 1, coarse), 2, 240)
    if not c1:
        raise SystemExit("搜索范围内没有可用候选，请放宽 --cx-range / --cy-range / --r-range")
    _, _, _, bx, by, br, _, _ = c1[0]
    c2 = sweep(range(max(0, bx - coarse), bx + coarse + 1),
               range(max(0, by - coarse), by + coarse + 1), 1, 720)
    c2.sort(key=lambda t: -t[0])
    return c2[0], c2[:6]


def draw_overlay(img: Image.Image, cx, cy, r_in, r_out, out_path: Path, pad=310):
    w, h = img.size
    box = (max(0, int(cx - pad)), max(0, int(cy - pad)),
           min(w, int(cx + pad)), min(h, int(cy + pad)))
    crop = img.convert("RGB").crop(box).copy()
    d = ImageDraw.Draw(crop)
    for r, color in ((r_in, (255, 0, 0)), (r_out, (0, 255, 0)), (0.5 * (r_in + r_out), (0, 160, 255))):
        d.ellipse([cx - r - box[0], cy - r - box[1], cx + r - box[0], cy + r - box[1]],
                  outline=color, width=2)
    crop.save(out_path)
    return out_path


def main() -> int:
    ap = argparse.ArgumentParser(description="定位圆环支架（圆心 + 内外半径），输出可复核的叠加预览",
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--image", required=True, help="要定位的图（通常是精修输出）")
    ap.add_argument("--verify-with", help="交叉验证图（通常是原图）；两张图应只是等比缩放关系")
    ap.add_argument("--out-prefix", default="ring", help="输出文件前缀，默认 ring")
    ap.add_argument("--cx-range", default="0.50,0.72", help="环心 x 搜索范围，占宽比例，默认 0.50,0.72")
    ap.add_argument("--cy-range", default="0.45,0.75", help="环心 y 搜索范围，占高比例，默认 0.45,0.75")
    ap.add_argument("--r-range", default="0.08,0.14", help="环外半径搜索范围，占宽比例，默认 0.08,0.14")
    args = ap.parse_args()

    path = Path(args.image)
    if not path.exists():
        raise SystemExit(f"找不到图像：{path}")
    img = Image.open(path)
    gray = np.asarray(img.convert("L"))
    w, h = img.size
    mag = edge_map(gray)

    def frac(s):
        return tuple(float(v) for v in s.split(","))

    fx0, fx1 = frac(args.cx_range)
    fy0, fy1 = frac(args.cy_range)
    fr0, fr1 = frac(args.r_range)

    print(f"图像：{path.name}  {w}x{h}")
    print("搜索中（约 10~40 秒）…")
    best, top = fit(mag,
                    int(fx0 * w), int(fx1 * w), int(fy0 * h), int(fy1 * h),
                    int(fr0 * w), int(fr1 * w))
    score, e_out, e_in, cx, cy, r_out, r_in, r_hole = best

    print("\nTop 6（总得分 / 外缘 / 内缘 / 环心 / 外径 / 最强内缘 / 内孔候选）：")
    for s, eo, ei, c_x, c_y, ro, ri, rh in top:
        print(f"   {s:7.1f}  {eo:6.1f} {ei:6.1f}   ({c_x},{c_y})  r_out={ro}  r_in={ri}  r_hole={rh}")

    print(f"\n结果：环心=({cx},{cy})  外半径={r_out}")
    print(f"      最强内缘={r_in}（比例 {r_in / max(1, r_out):.2f}）／较内的一圈边缘={r_hole}（比例 {r_hole / max(1, r_out):.2f}）")
    print("      注意：内缘常锁在环带内部的倒角线上，不等于内孔边界。本工具只需「外半径」——")
    print("            回贴用整圆（半径 = 外半径 ×1.06~1.10），内缘数值仅供参考。")
    warn = []
    if e_out < 15:
        warn.append(f"外缘强度偏低（{e_out:.1f}，经验阈值 ≥15）")
    if warn:
        print("⚠ 置信度告警：" + "；".join(warn))
        print("  请务必打开叠加预览人工复核；不可靠时改用放大网格手量（zoom_grid.py）。")
    else:
        print(f"✓ 置信度：外缘强度足够（{e_out:.1f}）")

    out_overlay = draw_overlay(img, cx, cy, r_hole, r_out, Path(f"{args.out_prefix}_fit.png"))
    print(f"\n叠加预览（务必人眼复核）：{out_overlay}")

    margin = max(6, int(0.065 * r_out))
    print("\n可直接复制的回贴命令（坐标已在当前图坐标系）：")
    print(
        "python restore_regions.py --source 原图.jpg --edited 精修图.jpg --out 成品.png \\\n"
        f"    --match edited --circle {cx},{cy},{r_out + margin} --feather 16"
    )

    if args.verify_with:
        p2 = Path(args.verify_with)
        if not p2.exists():
            raise SystemExit(f"找不到交叉验证图：{p2}")
        img2 = Image.open(p2)
        gray2 = np.asarray(img2.convert("L"))
        w2, h2 = img2.size
        mag2 = edge_map(gray2)
        sx, sy = w / w2, h / h2
        print(f"\n交叉验证：{p2.name} {w2}x{h2}（缩放到 {path.name} 为 sx={sx:.4f} sy={sy:.4f}）")
        best2, _ = fit(mag2, int(fx0 * w2), int(fx1 * w2), int(fy0 * h2), int(fy1 * h2),
                       int(fr0 * w2), int(fr1 * w2))
        _, eo2, ei2, cx2, cy2, ro2, ri2, rh2 = best2
        mx, my = cx2 * sx, cy2 * sy
        mr = ro2 * sx
        dx, dy, dr = mx - cx, my - cy, mr - r_out
        print(f"   该图拟合：环心=({cx2},{cy2})  外半径={ro2}  内孔候选={rh2}（外缘强度 {eo2:.1f}）")
        print(f"   映射后差异：Δ环心=({dx:+.1f},{dy:+.1f})  Δ外径={dr:+.1f}")
        tol = max(4.0, 0.03 * r_out)
        if abs(dx) <= tol and abs(dy) <= tol and abs(dr) <= tol * 2:
            print(f"✓ 两图拟合互相吻合（容差 {tol:.0f}px / {tol * 2:.0f}px）——说明两图是纯等比缩放，坐标可直接复用。")
        else:
            print("⚠ 两图拟合不吻合：说明两图不只是缩放关系（可能有裁切或位移），坐标不可直接复用。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
