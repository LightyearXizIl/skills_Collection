# 提示词骨架

## 使用规则

1. 只填 `{{}}` 槽位，不要改动固定句型——固定部分承载的是风格约束，改动会让模型回到默认审美。
2. 提示词全英文。**中文一律不入提示词**，标题后期叠加。
3. 每个模板都默认 `no text, no letters, no watermark`。字标若非后期贴，另起一段单独写（见文末「字标变体」）。
4. 画幅参数按模型写：`--ar 3:4`（MJ 系）/ `aspect_ratio: 3:4`（API 系）/ 直接写 `vertical 3:4 portrait`.
5. 一次只改一个变量。同一图位重跑时，先固定 seed，再改一个词。

---

## 全局风格前缀（三方向通用，放最前）

```
editorial product photography for a premium tech-accessory brand,
clean commercial finish, controlled studio lighting, no lens flare, no HDR halo,
neutral color science, true-to-material color, fine detail retention, no beauty retouching
```

## 全局负向词

```
text, letters, chinese characters, watermark, logo overlay, collage, split screen,
oversaturated, neon, plastic sheen, CGI look, fake bokeh, warped geometry,
extra fingers, deformed hand, floating product shadow, cluttered background, cheap stock photo
```

---

# 方向 A｜材质叙事派（PITAKA）

## A1 材质微距（封面或第三图位）

```
macro close-up of {{product}} at a 45-degree angle, extreme shallow depth of field,
near-black seamless background fading to #171718,
single raking light from the upper left at a shallow 20-degree grazing angle
that reveals the woven fiber texture of the material,
opposite side falls into complete shadow, smooth gradient across the frame,
matte anodized camera ring catching one thin specular highlight,
{{material}} texture in razor-sharp focus in the mid-plane,
foreground and background fully blurred,
monochrome grade, near-zero saturation, only the product's own coating keeps color,
premium engineering mood, 85mm macro lens, f/2.8, vertical 3:4 portrait
```

## A2 系列矩阵（系列/配色图位）

```
{{count}} units of {{product}} arranged in a diagonal stagger, tilted about -18 degrees,
overlapping and bleeding off the frame edges, forming a dense material wall,
warm off-white seamless background #E8E3DF, very soft top light,
faint contact shadows only, no hard cast shadow,
each unit a different {{color_list}} woven finish, textures clearly readable,
matte metal camera rings, no reflections of the studio,
precise repetition, catalog rhythm, 50mm lens, f/8, wide 4:3
```

## A3 单件英雄位（内页）

```
single {{product}} standing upright on warm off-white seamless #F4F1ED,
three-quarter front view, slight tilt,
soft large-area key light from the left, gentle falloff to the right,
one thin reflective line tracing the chamfered edge,
background clean with a barely visible gradient, product occupies 60% of frame height,
museum-object presentation, 100mm lens, f/11, vertical 3:4
```

---

# 方向 B｜活力场景派（TORRAS）

## B1 人物封面

```
half-body portrait of {{model}} holding {{product}} in the right third of the frame,
the hand grips the product naturally, fingers correctly wrapped around the edge,
{{product}} facing camera so the {{key_feature}} is legible,
mid-grey seamless studio backdrop #7D7C82, one stop darker than the subject,
large soft frontal key light, subtle rim light from behind left,
a single flat {{accent_color}} geometric shape (quarter circle) sits behind the model
with a hard clean edge, no gradient, no outline,
cool color grade, slightly desaturated highlights,
white brand lockup reserved at top-left as empty space, no text rendered,
35mm lens, f/4, vertical 3:4 portrait
```

## B2 场景静物（功能演绎）

```
{{product}} presented inside an invented physical stage that materializes its benefit:
{{stage_props}},
45-degree top-down view, product spilling out of its packaging,
loose inserts, cards and stickers scattered at slightly crooked angles,
cold environment palette {{cool_palette}} with a single warm orange packaging block
occupying under 15% of the frame,
real contact shadows, ambient occlusion, mild reflections on the acrylic surface,
crisp commercial still life, 50mm lens, f/9, vertical 3:4
```

## B3 上手细节（比例与手感）

```
two hands holding {{product}} against a plain {{bg}} background,
crop from mid-forearm, arms entering from the bottom edge,
natural skin texture, visible knuckles and veins, no smoothing,
the product's thickness relative to the fingers must read clearly,
soft daylight from a large window at camera left, gentle shadow under the hands,
documentary honesty, 85mm lens, f/4, vertical 3:4
```

---

# 方向 C｜极简排印派（MOFT）

## C1 排印封面（留白给中文标题）

```
{{product}} placed in the lower 55% of the frame on a pure white background,
upper 30% of the image left completely empty as clean white space,
all props removed, only {{product}} and its soft contact shadow,
flat even lighting, minimal shadow, product angle near-straight-on with a 10-degree turn,
high-key, precise edges, catalogue clarity,
empty space reserved for typography, absolutely no text or logo rendered,
50mm lens, f/11, vertical 3:4
```

## C2 插画封面（品牌人格位）

```
flat vector illustration centered on a white canvas,
a semi-transparent glossy bubble enclosing the scene, thin highlight arc along the bubble edge,
inside: {{illustration_subject}} rendered in flat geometric shapes with no outlines,
palette of lemon yellow #EEE682, cream #FDF7D5, grass green, and a green-to-blue gradient,
tiny black brush-stroke details for hair or fabric folds,
playful editorial tone, generous white margin around the bubble,
no text, vertical 3:4
```

## C3 九宫格矩阵

```
a clean 3x3 grid of {{product}} in nine different colorways,
each cell a pale grey panel #F4F4F4 with gutters about 2.6% of the image width,
product centered in every cell, straight-on top view, ultra-soft shadow,
colorways jump across hue and value between adjacent cells: {{color_list}},
perfectly aligned, no text, no labels, catalogue flat-lay,
vertical 3:4 with equal outer margins
```

## C4 三联教程

```
{{product}} in {{state_a}} occupying the upper 65% of the frame on white,
below it a row of three rounded-corner thumbnails showing the sequence
{{step_1}}, {{step_2}}, {{step_3}},
thumbnails at 20% frame height, corner radius about 1.3% of the image width, pale grey fill,
consistent soft light across all four images, no text,
instructional clarity, vertical 3:4
```

---

## A4 同色场域双件（A 方向封面主力，实测最高频）

```
two units of {{product}} on a tonal field derived from the product's own color,
background is the same hue two stops darker, seamless with soft radial falloff and heavy corner vignette,
one unit standing upright, one lying flat in front, both grounded on the lower third
with a long soft shadow falling to the lower right,
single hard side light at 30 degrees, one crisp specular line along the right edge,
monochromatic family palette {{color}}, no complementary colors, no props,
100mm lens, f/8, vertical 3:4 portrait
```

## B4 技术图解（B 方向说明图位）

```
exploded layered structure of {{product}} floating in dark {{hue}} space,
{{n}} semi-transparent layers stacked vertically with equal spacing,
each layer edge catching a thin rim light,
a thin leader line runs from the third layer to a framed blank label area at the lower left,
deep gradient background from #101018 at center to near-black at the edges,
cinematic engineering presentation, no text rendered inside the label,
50mm lens, f/11, vertical 3:4
```

## C1 上下双格（C 方向封面主力）

```
one white canvas split into two stacked panels separated by a white gap of about 2.8% of the image height,
upper panel: {{product}} in {{state_a}}, lower panel: the same product in {{state_b}},
identical camera angle and identical lighting in both panels so the two states read as a comparison,
flat even light, ultra-soft contact shadows, no text, generous white margins,
50mm lens, f/11, vertical 3:4
```

## C7 促销海报（C 方向活动图位）

```
bold promo poster layout on a bright {{field_color}} field,
{{product}} cluster in the center arranged in a fan with slight overlap,
one large clean geometric shape behind the cluster,
a circular badge shape reserved at the upper right, left empty with no text inside,
high-key, punchy, commercial, 50mm lens, f/9, vertical 3:4
```

## 字标变体（仅当模型字标能力可用时）

优先后期贴。若必须直出，单独一段，且只写形状不写内容：

```
small white wordmark occupying the top-left corner, width equal to 12% of the image width,
geometric sans-serif letterforms, flat, no effects
```

字标保真是硬边界：变体字标、含特殊字符的字标（如 `MΛGEΛSY`）、机身 LOGO 遮挡关系，**一律走后期回贴**，参 `product-photo-retouch` 的 `PROTECTED REGIONS` 流程。

## 图生图模式（已有实拍图）

结构锁定条款放在提示词最前，且要在可见性描述之前：

```
keep the product's geometry, proportions, port placement and material weave exactly as in the source image,
do not redesign the object.
only replace the background with {{bg}}, adjust lighting to {{light}},
and recompose to vertical 3:4 with the product occupying {{ratio}} of the frame.
```

反例（会翻车）：先写"把产品放在画面右侧、让镜头圈朝向光"再写"保持结构"——模型会先重新摆产品再"保持"，遮挡关系必然丢失。
