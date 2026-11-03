# 12 段提示词骨架（英文，可直接复制填空）

> 用法：按 `⟨⟩` 提示替换为本图实测内容；段落顺序不可调整。丝印与 LOGO 段直接从 `03-wordmark-and-logo-locks.md` 复制。
> 模式标注：`[C]` = 产品区域重渲染模式（本骨架默认）；纯清洁模式（A）删去 `MATERIAL UPGRADE` 与 `ENHANCE` 两段，并把 `TASK` 改为 `clean-up EDIT ONLY`。

---

```
TASK
Edit the supplied product photo. This is an in-context EDIT: clean up the whole frame, then RE-RENDER THE
PRODUCT REGION ONLY at photoreal CGI / 3D-render quality (Cinema 4D + Octane/Redshift, Blender Cycles or
KeyShot grade, physically-based rendering, studio HDRI lighting). Keep the source image's exact framing,
camera angle, perspective, crop, resolution and aspect ratio. The BACKGROUND stays the original photograph;
only the product itself is re-rendered.

HARD SCENE LOCK — the scene comes from the SOURCE photo and must stay
- ⟨台面 / 承托面⟩: keep the ⟨材质、纹理走向、色调、反光特性、高光带⟩ exactly as it is. Do not re-grain, re-color or flatten it.
- Keep the lighting direction and the object's cast shadow unchanged ⟨（画面哪一侧更亮）⟩.
- ⟨背景道具 / 包装 / 陈列物⟩: keep them exactly as they are — same geometry, same colour scheme, same panels, same graphics, same position, angle and crop.
- Do NOT rewrite, re-letter, re-space, translate, correct or complete any text, wordmark or graphic printed on ⟨道具名⟩. Small text is illegible at this resolution — keep it exactly as it looks; never sharpen illegible text into different words and never invent text, logos or certification marks that are not there.
- ⟨若画面中有倒置 / 侧置的印刷内容⟩: keep it IN ITS ORIGINAL ORIENTATION — do not rotate it upright and do not re-space it.

PRODUCT LOCK — the re-render must reproduce every one of these exactly
- ⟨总体形态与套装关系，如：ONE-PIECE CLEAR case over a black phone；壳的凸起边框属壳体、与机身平台为两件、共 2 阶⟩
- ⟨唯一零件必写数量与位置：只出现在某侧 / 某处，对侧为 0⟩
- ⟨部件清单：逐件写数量 + 形状 + 相对位置 + 排布，并写 "add nothing, remove nothing"⟩
- ⟨连接件 / 支架 / 铰链：写起点 → 方向 → 弯曲 / 断口位置 → 终点，并禁止闭合 / 断口消失⟩
- ⟨透明件必写：开窗是真贯通开口，内部结构透过它可见，不得画成实心面板⟩
- ⟨机身 LOGO 与遮挡关系：从 03-wordmark-and-logo-locks.md 的 8) 段整段复制⟩
- ⟨字标 / 丝印：从 03-wordmark-and-logo-locks.md 复制对应句⟩

MATERIAL UPGRADE — the core of this task (product only)
Re-render every product surface with correct PBR material response, as if the product were lit by a studio
HDRI and rendered with ray tracing. The materials must read as DENSE, SPECULAR and PHYSICALLY CORRECT — not as
a photographic copy with lifted contrast.

1) ⟨透明件⟩ — CLEAR POLYCARBONATE with a CLEARCOAT layer
   - Refractive transparent solid: visible real wall thickness, correct Fresnel edge brightening, and REFRACTION of ⟨其后结构⟩ through the material.
   - A crisp, thin, CONTINUOUS clearcoat specular line along every bevel.
   - NO milky haze, NO grey film, NO double contour outlines.

2) ⟨光面件，如机身背面 / 屏幕玻璃⟩ — glossy, low roughness
   - Deep, clean tone with a CONTINUOUS, coherent reflection: a smooth soft gradient, not a blotchy or dirty smear.
   - Keep a real reflection PRESENT, but clean and physically plausible. Do NOT invent objects, people or shapes inside the reflection, and do NOT mirror the background props into it.
   - If the surface is SWITCHED OFF (screen), it stays off: pure deep black, no wallpaper, no icons, no status bar, no clock, no notifications, no UI of any kind.

3) ⟨哑光件⟩ — satin matte with micro-bevels
   - Broad, smooth gradient highlight with a long soft falloff; mathematically clean tonal gradient: no photographic noise, no blotches, no iso-noise.
   - Every sharp machined edge catches a THIN, BRIGHT, RAZOR-SHARP micro-bevel highlight line — the hallmark of a CGI render.

4) ⟨镜片组⟩
   - Barrel walls and stepped end rings: pure matte black, near-zero specular, uniform roughness, crisp concentric circular edges.
   - Lens glass: REAL optical depth — the glass stays DARK, with only a FAINT multi-coat AR reflection (subtle blue-violet / teal tint at low intensity) and a small, bright, sharply-defined reflection of the light source. Never light, bright, milky or saturated green lens glass.

5) ⟨扩散件 / 指示灯⟩
   - Frosted / diffused surface with even, softly luminous tone and no hard specular. ⟨小暗点保持极小、暗、哑光，不得放大、不得变成额外镜头⟩

6) ⟨金属件⟩ — anisotropic brushed metal + machined bevels
   - ANISOTROPIC brushed ⟨银 / 紫 / 黑 —— 按本图配色⟩: the specular highlight must STRETCH into a directional streak along the brushing direction, with tight roughness.
   - Continuous HDRI environment gradient: bright near-white highlight arc, smooth mid-tone, then deep dark occlusion on the inner side.
   - CNC-machined precision: crisp, perfectly circular bevel edges, clean inner hole, no wobble.

7) GLOBAL CGI QUALITY ON THE PRODUCT
   - Clean ambient occlusion in every crevice, seam and contact line; correct contact shadow depth where the product meets the surface.
   - Physically-correct reflections only: never invented shapes, never a mirrored copy of the background props.
   - Perfectly smooth gradients, crisp edge definition, zero grain, zero sensor noise, zero compression artifacts, zero chromatic fringing, zero depth-of-field blur on the product.
   - Keep the product's BASE HUE unchanged ⟨列出固有色⟩ — only material response, tone and contrast change; the hue does NOT.

REMOVE (clean the ENTIRE frame)
1. ALL usage traces on the product: fingerprints, greasy smudges, scuff haze, handling marks and faint scratches — remove completely for a brand-new look.
2. Every dust speck, grit and loose particle on ⟨镜片 / 平台 / 金属件⟩.
3. Every dust speck, micro-grit and smear on ⟨金属件与斜面⟩.
4. Fine white lint fibres, fluff, fuzz and stray fibres on the transparent parts, especially near edges, corners and raised rims.
5. ALL dust, lint, fluff, stray fibres and loose hairs on ⟨背景台面与道具⟩ too. Remove ONLY the foreign particles; keep ⟨台面纹理 / 印刷图形 / 材质结构⟩ fully intact.

DO NOT interpret "smooth / clean / no noise" as permission to erase the product's REAL surface micro-grain:
keep the brushed grain of the metal, keep the micro-texture of the matte surfaces, keep ⟨织物织纹 / 木纹 / 印刷网点⟩. Remove noise and dust; keep genuine material structure.

EXPLICIT EXCEPTION — ⟨丝印 / LOGO / 印刷内容⟩ are SURFACE GRAPHICS, not defects. They survive the cleanup untouched, at the same position, size and appearance.

PROTECTED REGIONS — DO NOT REPAINT, DO NOT RE-LETTER, LEAVE UNTOUCHED
- ⟨列出禁止重绘的区域，逐个点名，例如：the curved "MΛGEΛSY" wordmark on the ring band；the phone's own logo on the back inside the ring's inner opening⟩. These regions are PROTECTED and must be EXCLUDED from the edit entirely.
- Inside these regions: do not repaint, redraw, re-letter, reshape, smooth, sharpen or "clean" anything. Treat them as if they had been masked out BEFORE the edit — inside them the output must be IDENTICAL to the source: same glyph shapes, same stroke widths, same sizes, same positions, same curvature, same contrast, same local reflections.
- Geometry, occlusion and lighting in the REST of the product may change with the re-render, but ⟨字标 / LOGO⟩ themselves are NEVER regenerated or approximated.
- If you cannot guarantee that a protected region comes out unchanged, leave it untouched rather than approximating it. Regenerating or altering either region is a failed result.
- These regions are NOT dust, NOT smudges, NOT scratches and NOT noise — they must never be cleaned away.

⟨此处插入 03-wordmark-and-logo-locks.md 的 BRAND WORDMARK LOCK 整段⟩

> **出图后必须做回贴**（`scripts/restore_regions.py`）：先用 `--grid` 出坐标网格量取区域，再用 `--circle / --annulus` 把原图的字标与 LOGO 区域贴回精修图。**字标与 LOGO 的最终保真靠这一步，不靠模型。**

ENHANCE (expand dynamic range: blacker blacks, whiter whites)   ← 仅在用户要求"全新感 / 黑更黑白更白"时保留
- Apply an S-curve to the product: deepen its blacks, its cast shadow and the inner-shadow; push the brightest speculars on the edges to bright, crisp, near-white highlights. Deep clean blacks with NO grey haze lift.
- Grade the overall frame with a moderate contrast lift for punch, BUT keep ⟨背景的光影图案 / 印刷色 / 材质纹理⟩ exactly as they are — do not flatten, clip, recolor or erase them.
- On the glossy surfaces, keep the reflection clean and coherent while deepening the blacks beneath it.

MUST PRESERVE — do not alter, move, straighten, re-typeset or regenerate any of these
- ⟨把 PRODUCT LOCK 的每一条改写为"保持"句式，逐条列出，不得只写一句"保持产品不变"⟩
- ⟨结构层级 / 阶数 / 贯通关系⟩
- ⟨唯一零件的数量与位置⟩
- ⟨断口 / 铰链 / 支耳的形态与位置⟩
- ⟨丝印与 LOGO 的可见/隐藏分割⟩
- ⟨背景道具与台面的全部印刷与纹理⟩
- The product's outer silhouette, proportions, corner radii and part layout stay identical to the source — the geometry does NOT change, only the material rendering.

OUTPUT
The same photograph, same resolution and aspect ratio, same framing and same scene. The product looks like a photoreal CGI product render (studio HDRI, ray-traced speculars, PBR materials) — while ⟨背景与道具⟩ remain exactly the original photograph, and ⟨丝印 / LOGO⟩ are still exactly where they were. Clean, dust-free, premium, physically plausible.

AVOID
⟨场景与道具的替换或改动⟩, rewriting or completing illegible printed text, INVENTING TEXT, LOGOS OR MARKS NOT PRESENT IN THE SOURCE, ERASING FADING OR HIDING ANY EXISTING LOGO OR WORDMARK, ⟨字标退化的具体写法，如 NORMALISING THE Λ GLYPHS INTO A⟩, ⟨构件被合并 / 闭合 / 抹平的具体项⟩, shutting off / turning on anything that should stay off, invented or mirrored reflections, newly invented pinholes or enlarged existing ones, changed product silhouette or proportions, new text/logo/watermark, plastic-toy / clay-render / low-poly game-asset look, cartoon or toon shading, flat washed-out shading, over-glossy chrome-like or wet-plastic look, milky or foggy transparent parts, double contour outlines, clipped detail-less dead blacks, blown-out white speculars with no shape, over-sharpening halos, color shift, vignette, HDR blow-out, grain / sensor noise / JPEG artifacts on the product, blur or denoise that flattens ⟨材质纹理⟩.
```

---

## 填写要点

1. **`PRODUCT LOCK` 是骨架的核心**：这一段没写全，后面材质写得再好也是"越修越不象"。
2. **同一产品的多张图各写一套**：`PRODUCT LOCK` 可复用，`HARD SCENE LOCK` 必须逐图重写（台面、道具、光影、文字朝向都可能不同）。
3. **`MUST PRESERVE` 不是 `PRODUCT LOCK` 的复读**：前者写"保持什么"，后者写"是什么"；把 `PRODUCT LOCK` 的每条**改写为保持句式**逐条列出。
4. **`AVOID` 只留真会犯的错**：已在正文说清、模型不易误解的，不在 `AVOID` 里机械重复；`AVOID` 的价值在于"用最强语气钉住最易退化的那 3–5 项"。
5. **需要绝对约束时加失败判据**：`Treat any output where … as a failed result.`
