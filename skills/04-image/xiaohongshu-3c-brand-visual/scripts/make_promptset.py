#!/usr/bin/env python3
"""生成小红书 3C 配件图提示词套组骨架。

用法:
    python make_promptset.py --direction A --product "MagEZ Case 6" \
        --colors "黑灰/暗红" --selling "0.99mm 超薄芳纶" --out set.md

只生成占位齐全的骨架，槽位需人工按 references/02-prompt-templates.md 打磨。
"""
import argparse
import datetime
import sys

PREAMBLE = (
    "editorial product photography for a premium tech-accessory brand, "
    "clean commercial finish, controlled studio lighting, no lens flare, no HDR halo, "
    "neutral color science, true-to-material color, fine detail retention, no beauty retouching"
)

NEGATIVE = (
    "text, letters, chinese characters, watermark, logo overlay, collage, split screen, "
    "oversaturated, neon, plastic sheen, CGI look, fake bokeh, warped geometry, "
    "extra fingers, deformed hand, floating product shadow, cluttered background, cheap stock photo"
)

SHOTS = {
    "A": [
        ("01 封面 · 同色场域双件",
         "two units of {product} on a tonal field derived from the product's own color, background is "
         "the same hue two stops darker with soft radial falloff and heavy corner vignette, one unit "
         "standing upright and one lying flat in front, both grounded on the lower third with a long soft "
         "shadow to the lower right, single hard side light at 30 degrees, one crisp specular line along "
         "the right edge, {colors} family palette, no complementary colors, no props, "
         "100mm lens, f/8, vertical 3:4 portrait"),
        ("02 材质微距",
         "macro close-up of {product} at a 45-degree angle, extreme shallow depth of field, resting on the "
         "same woven material as its own surface so it camouflages into the texture, grazing light across "
         "the weave, heavy vignette, near-zero saturation, 85mm macro lens, f/2.8, vertical 3:4 portrait"),
        ("02 系列矩阵",
         "several units of {product} arranged in a diagonal stagger, tilted about -18 degrees, "
         "overlapping and bleeding off the frame edges, warm off-white seamless background #E8E3DF, "
         "very soft top light, faint contact shadows only, each unit a different {colors} finish, "
         "textures clearly readable, 50mm lens, f/8, wide 4:3"),
        ("03 功能演示",
         "{product} shown mid-action performing its core function, three-quarter view, "
         "single soft key light, no props other than what the action requires, cool grey backdrop, "
         "50mm lens, f/6.3, vertical 3:4"),
        ("04 上手比例",
         "one hand holding {product} against a plain warm off-white background, crop from mid-forearm, "
         "natural skin texture, the product's thickness relative to the fingers must read clearly, "
         "soft window light at camera left, 85mm lens, f/4, vertical 3:4"),
        ("05 场景代入",
         "{product} on a desk surface in a quiet workspace, morning side light, shallow depth of field, "
         "restrained props, 35mm lens, f/2.8, vertical 3:4"),
        ("06 配色矩阵",
         "a clean 3x3 grid of {product} in nine colorways from {colors}, each cell a pale grey panel "
         "#F4F4F4 with gutters about 2.6% of the image width, product centered, "
         "ultra-soft shadow, perfectly aligned, vertical 3:4"),
        ("07 细节标注",
         "extreme close-up of the button and chamfer of {product}, raking light, "
         "empty space reserved on the left for two annotation lines, 100mm macro, f/5.6, vertical 3:4"),
        ("08 参数页底图",
         "{product} straight-on on pure white, small and centered in the lower half, "
         "upper 55% completely empty white space for a spec table, flat even lighting, vertical 3:4"),
        ("09 品牌收尾",
         "{product} at rest on a warm off-white field with a long soft shadow, minimal, "
         "generous negative space, 50mm lens, f/11, vertical 3:4"),
    ],
    "B": [
        ("01 封面 · 人物",
         "half-body portrait of a model holding {product} in the right third of the frame, "
         "the hand grips the product naturally, product facing camera, mid-grey seamless backdrop "
         "#7D7C82, large soft frontal key light, subtle rim light, a single flat light-blue geometric "
         "quarter circle behind the model with a hard clean edge, cool color grade, "
         "white brand lockup reserved at top-left as empty space, 35mm lens, f/4, vertical 3:4 portrait"),
        ("02 功能场景",
         "{product} presented inside an invented physical stage that materializes its benefit, "
         "45-degree top-down view, product spilling out of its packaging, loose inserts and cards at "
         "slightly crooked angles, cold environment palette, a single warm orange packaging block under "
         "15% of frame, real contact shadows, acrylic reflections, 50mm lens, f/9, vertical 3:4"),
        ("03 动作分解",
         "three-panel friendly sequence showing the product going from flat to standing, "
         "consistent lighting, white background, 50mm lens, f/8, horizontal strips"),
        ("04 手持细节",
         "two hands holding {product}, crop from mid-forearm, arms entering from the bottom edge, "
         "natural skin texture, no smoothing, soft daylight from camera left, 85mm lens, f/4, vertical 3:4"),
        ("05 生活场景",
         "{product} in a real daily context, natural window light, depth of field separating product "
         "from background, muted set dressing, 35mm lens, f/2.8, vertical 3:4"),
        ("06 配色矩阵",
         "a clean 3x3 grid of {product} in nine colorways from {colors}, pale grey panels, "
         "centered product, ultra-soft shadow, vertical 3:4"),
        ("07 细节",
         "close-up of the pivot and hinge area of {product}, soft directional light, "
         "visible machining marks, 100mm macro, f/5.6, vertical 3:4"),
        ("08 参数页底图",
         "{product} on white in the lower half, upper 55% empty for a compatibility table, vertical 3:4"),
        ("09 收尾",
         "{product} with one orange accent element, cool grey field, brand statement space in the "
         "upper third, 50mm lens, f/11, vertical 3:4"),
    ],
    "C": [
        ("01 封面 · 排印",
         "{product} placed in the lower 55% of the frame on a pure white background, upper 30% of the "
         "image left completely empty as clean white space, flat even lighting, minimal shadow, "
         "10-degree turn, high-key, precise edges, no text or logo rendered, 50mm lens, f/11, vertical 3:4"),
        ("02 材质",
         "macro of the surface of {product} on white, soft grazing light, texture readable, "
         "100mm macro, f/8, vertical 3:4"),
        ("03 教程三联",
         "{product} in its deployed state occupying the upper 65% of the frame on white, below it a row "
         "of three rounded-corner thumbnails showing the sequence, pale grey fill, vertical 3:4"),
        ("04 上手",
         "one hand holding {product} on white, cropped at the wrist, natural skin, soft shadow, vertical 3:4"),
        ("05 场景",
         "{product} on a clean desk with two restrained objects, soft daylight, vertical 3:4"),
        ("06 九色矩阵",
         "a clean 3x3 grid of {product} in nine colorways from {colors}, pale grey panels #F4F4F4, "
         "gutters about 2.6% of the image width, ultra-soft shadow, vertical 3:4"),
        ("07 插画位",
         "flat vector illustration centered on white, a semi-transparent glossy bubble enclosing the "
         "scene, flat geometric shapes, palette lemon yellow #EEE682 and cream #FDF7D5 with a green-to-blue "
         "gradient, no outlines, no text, vertical 3:4"),
        ("08 参数页底图",
         "{product} small and centered on white with the upper 60% empty for a spec list, vertical 3:4"),
        ("09 收尾",
         "{product} alone on white with one small blue accent bar, generous margins, vertical 3:4"),
    ],
}

COPY = {
    "A": ["只有 {t}，却比钢硬 5 倍", "{t}｜把材料做到极致", "轻一点，才能久一点"],
    "B": ["一个壳，搞定 {t}", "1 分钟上手 {t}", "{t}｜看到你的每一面"],
    "C": ["今天起，我们常在 {t}", "{t}，重新定义支点", "{t}｜新色到齐"],
}

DIRECTION_NAME = {
    "A": "A 材质叙事派（PITAKA）",
    "B": "B 活力场景派（TORRAS）",
    "C": "C 极简排印派（MOFT）",
}


def build(direction, product, colors, selling, tag):
    shots = SHOTS[direction]
    lines = [
        f"# 小红书套组｜{product}",
        "",
        f"- 方向：{DIRECTION_NAME[direction]}",
        f"- 产品：{product}",
        f"- 配色：{colors}",
        f"- 主卖点：{selling}",
        f"- 生成时间：{datetime.date.today().isoformat()}",
        "",
        "## 标题候选（选 1 条，8–14 字）",
        "",
    ]
    for i, c in enumerate(COPY[direction], 1):
        lines.append(f"{i}. " + c.format(t=tag))
    lines += [
        "",
        "## 全局风格前缀（放在每条提示词最前）",
        "",
        "```",
        PREAMBLE,
        "```",
        "",
        "## 全局负向词",
        "",
        "```",
        NEGATIVE,
        "```",
        "",
        "## 九图提示词",
        "",
    ]
    for name, tpl in shots:
        body = tpl.format(product=product, colors=colors, selling=selling)
        lines += [
            f"### {name}",
            "",
            "```",
            PREAMBLE + ", " + body,
            "```",
            "",
        ]
    lines += [
        "## 排版参数（3:4，按占比，像素随画布）",
        "",
        "| 项 | 值（占画面宽 %W / 高 %H） |",
        "|---|---|",
        "| 画幅 | 3:4 竖版，sRGB，像素由出图工具决定 |",
        "| 外边距 | 8.9% W，底边距 11.1% H |",
        "| 主标 | 8.9–12.2% W / 字重 800–900 / 行高 1.05 |",
        "| 副标 | 3.7–4.4% W / 400 / #6B6B6B |",
        "| 字标 | 高 4.1–5.2% W，位置固定左上 |",
        "",
        "## 交付前自检",
        "",
        "1. 缩到约 18% 画面宽能否 1 秒认出产品与主标",
        "2. 九图并排背景明度差是否 ≤15%",
        "3. 顶部 8.3% H / 底部 11.1% H / 右下 11%W×8.3%H 是否无关键信息",
        "",
    ]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="生成小红书 3C 配件图提示词套组")
    p.add_argument("--direction", required=True, choices=["A", "B", "C", "a", "b", "c"])
    p.add_argument("--product", required=True, help="产品型号，如 MagEZ Case 6")
    p.add_argument("--colors", default="black / grey", help="配色，用 / 分隔")
    p.add_argument("--selling", default="", help="主卖点，用于文案槽位")
    p.add_argument("--tag", default="", help="文案里的短称，默认取 product 首个词")
    p.add_argument("--out", default="", help="输出路径，默认 stdout")
    a = p.parse_args()

    d = a.direction.upper()
    tag = a.tag or a.product.split()[0]
    md = build(d, a.product, a.colors, a.selling, tag)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"written: {a.out} ({len(md)} chars)")
    else:
        sys.stdout.write(md)


if __name__ == "__main__":
    main()
