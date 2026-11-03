# 丝印与 LOGO 锁定原文（可直接复制进提示词）

本文件是本技能的**权威锁定原文**。凡提示词涉及品牌字标与机身 LOGO，一律从此处复制，**不凭记忆重写**——记忆会把品牌名"按常识补全"，这正是本项目两次事故的源头。

---

## 一、变体字标 `MΛGEΛSY`（品牌 LOGO 字）

### 1. 识别要点

品牌字标常故意用**符号或变体字形替换字母**。本产品实例：

| 位次 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| 字符 | M | **Λ** | G | E | **Λ** | S | Y |

- 第 **2、6** 位是**尖角 Λ**（希腊 Lambda / 开口倒 V），**无横杠、无水平笔画**。
- **不是字母 A**。写成 `MAGEASY` 会让模型照提示词把 Λ 画成 A——**提示词本身成了破坏源**。
- 多载体出现，**各处分别锁定**：① 环带丝印（沿弧、字头朝环心）；② 壳体边缘模压字（沿边、极小）；③ 包装盒印刷（正立）。
- 若画面只露出字标尾部，保持裁切：本产品盒面只露 **`Λ · S · Y`**，其左的 `E` 被画面左缘裁切。

### 2. 锁定原文（整段复制进提示词）

```
BRAND WORDMARK LOCK — "MΛGEΛSY" is a LOGOTYPE, not plain text
- The wordmark consists of SEVEN glyphs: M · Λ · G · E · Λ · S · Y. The 2nd and 6th glyphs are the ANGULAR LAMBDA-like shape Λ — an open inverted-V / triangle with NO crossbar and NO horizontal stroke. They are NOT the letter A, and the wordmark must NEVER be spelled or rendered as "MAGEASY".
- Reproduce the exact glyph sequence, the exact glyph shapes, the arc span, the cap height and the orientation. On the curved ring band the letter tops face the ring centre; on the box the wordmark is upright.
- NEVER normalise, simplify, "correct" or auto-complete the Λ glyphs into A; never respell, re-typeset, re-space, restyle, translate or rewrite the wordmark; never rotate or straighten the curved version; never move it along the band or across the panel.
- On the packaging box only the TAIL of the wordmark is visible — the three glyphs Λ · S · Y (with part of the preceding E clipped by the left edge of the frame). Keep exactly that clipped state: do NOT complete it into the full wordmark and do NOT render the clipped E as a full letter.
- If a glyph is ambiguous at this resolution, leave it EXACTLY as it is — do not redraw it and do not substitute a different letter.
- Treat any output where Λ has become A as a failed result.
```

### 3. 配套条款

`EXPLICIT EXCEPTION`（放在 `REMOVE` 段之后，声明丝印不是瑕疵）：

```
EXPLICIT EXCEPTION — the "MΛGEΛSY" ring lettering and every wordmark, badge and text printed on the box are SURFACE GRAPHICS, not defects. They survive the cleanup untouched, at the same position, size and appearance.
```

`AVOID` 片段：

```
NORMALISING THE BRAND'S ANGULAR Λ GLYPHS INTO THE LETTER A or respelling the wordmark as MAGEASY, completing the clipped tail of the box wordmark, straightening or re-spacing the curved "MΛGEΛSY" lettering
```

---

## 二、机身 LOGO（苹果图形）与它的遮挡关系

### 1. 推定与实测

- **推定（默认成立）**：带 **环支架 / MagSafe 环**的手机，机身 LOGO 位于**环的内孔范围内**，且**常被环带部分遮挡**。**不得因单视图看不清就判为"无 LOGO"**。
- **实测（本产品，2026-09-23 用户确认）**：LOGO 位于环内孔**偏下部**（非居中）；**下缘被环带下段与其卡扣 / 铰链横切遮挡**；遮挡边界大体与环带内缘平行；可见部分为**上部（含叶片）**。
- **配色差异 ≠ 结构差异**：同一产品紫色 / 银色 / 黑色环，**LOGO 与环带的遮挡关系完全一致，按通用条款处理**；只有环的配色随图变化。

### 2. 遮挡层级（写进提示词）

由观者到机身（由外到内）：

```
RING BAND (opaque metal, nearest) -> TRANSPARENT CASE (see-through, carrying its own surface reflections) -> PHONE BACK with the logo beneath
```

### 3. 锁定原文（v3 —— **位置条款必须在可见性条款之前**）

```
8) THE PHONE'S OWN LOGO — PRESENT, AND PARTIALLY OVERLAPPED BY THE RING BAND
   - The phone's logo sits on the phone's BACK inside the ring's inner-hole area, OFFSET TOWARD THE LOWER PART of that opening. The ring band's LOWER segment — together with the matching-metal clasp / lock tab at the bottom of the ring — cuts straight across the LOWER part of the logo and hides it; the occlusion boundary runs roughly parallel to the ring's inner edge. From the viewer the occlusion order is: RING BAND (opaque metal, nearest) -> TRANSPARENT CASE (see-through, carrying its own surface reflections) -> PHONE BACK with the logo beneath.
   - Keep the EXACT visible/hidden split: the same portion of the logo stays visible through the ring's inner opening, on the same side, at the same size and orientation, and the same portion stays hidden behind the band. Do not slide, rotate, enlarge or re-centre the logo to "uncover" it, do not change the ring's inner-hole diameter, band width or clasp position to expose more of it, and never reveal the hidden part through the metal.
   - POSITION FIRST: reproduce the logo at the SAME POSITION the source shows — inside the ring's inner opening, OFFSET TOWARD THE LOWER PART of that opening, where the ring band's lower segment overlaps it. It must NOT sit in the middle or the upper part of the opening, and it must NOT be drawn fully visible inside the opening.
   - THEN VISIBILITY: reproduce its appearance and CONTRAST exactly as the source shows it — its tone is set by whatever the back reflects around it (sometimes a dark silhouette against a bright reflection, sometimes a faint low-contrast mark). Never make it MORE visible, larger, cleaner or more contrasty than the source; never brighten it into a white print, never sharpen it into a hard graphic, never fade it out, never lift it onto the case surface, never draw it on top of the ring band.
   - POSITION / SIZE / VISIBILITY FIDELITY IS ABSOLUTE: the logo is never relocated, re-centred, re-scaled, re-lit or re-styled. If the source barely shows it at this resolution, keep EXACTLY that faint trace — do not invent a newly visible logo, and above all do not place a clear, centred logo inside the ring's opening.
   - This logo is NOT dust, NOT a smudge, NOT a scratch and NOT noise: never remove, erase, fade, bleach or crop it, and never replace it with a different mark.
   - Do not invent any ADDITIONAL logo, wordmark, text or certification mark that is not present in the source. (This forbids ADDING new marks — it is NOT a licence to delete the existing logo.)
```

`AVOID` 片段：

```
ERASING FADING OR HIDING THE PHONE'S EXISTING LOGO (inside the ring's inner hole), relocating re-centring or re-scaling that logo inside the ring's opening, making that logo more visible larger or more contrasty than the source shows, placing a clear centred logo inside the ring's opening
```

### 4. 为什么必须"三处钉桩"

只写一句"保留 LOGO"会被其他条款反制：

| 位置 | 作用 |
|---|---|
| `REMOVE` 段的 `EXPLICIT EXCEPTION` | 反向豁免：声明 LOGO 属"表面图形"，不受"清除所有使用痕迹"管辖 |
| `MATERIAL UPGRADE` 的 `8)` 段 | 正面要求：重渲染时必须在原位置、以原可见度画出来 |
| `MUST PRESERVE` + `AVOID` | 兜底（`AVOID` 里用全大写） |

---

## 三、像素级保护：出图后的回贴命令（本技能的第二步）

提示词里的 `PROTECTED REGIONS` 只是尽力而为，**最终保真是靠回贴**。经实测校准的命令：

```bash
# 1) 定位环（带交叉验证 + 叠加预览 + 置信度告警）；范围按图宽比例给
python scripts/locate_ring.py --image 精修图.jpg --verify-with 原图.jpg --out-prefix 环区 \
    --cx-range 0.52,0.68 --cy-range 0.50,0.68 --r-range 0.09,0.13

# 2) 回贴：一个整圆同时覆盖「环带上的 MΛGEΛSY」与「环内孔的机身 LOGO」
#    半径 = 环外半径 × 1.06~1.10（留余量，让边界落在环外暗部）
#    --match edited 保证成品分辨率 = 精修图分辨率
python scripts/restore_regions.py --source 原图.jpg --edited 精修图.jpg --out 成品.png \
    --match edited --circle 1133,840,228 --feather 16
```

实测要点（本项目，2026-09-23）：

| 项 | 取值 / 结论 |
|---|---|
| 环的实测几何（精修图 1920px 坐标） | 环心 (1133,840)、外半径 214、内半径 144（环带厚 70） |
| 贴回半径 | 228（＝外半径 ×1.065），覆盖环带 + 环内孔 + 少量外缘暗部 |
| 羽化 | `--feather 16`；实测边界梯度能量 / 邻带 = **0.14**，无可见接缝 |
| 成品尺寸 | **`--match edited`**（＝精修图尺寸）。压回原图尺寸会被用户打回 |
| `--level-match` | **默认不用**。本图邻域"暗部一致、亮部差 20 级"，对齐会把金属环压暗 |

**优先用整圆，而不是 `--annulus` + `--circle` 两次贴回**：整圆一步到位，不会在两块交集处留下不一致的边界；只要半径留足余量，环带与内孔都被覆盖。

---

### 4. 变体：外部来源不统一时的「双向禁止」写法（2026-09-23 新增）

**风险场景**：同一品牌字标在不同**载体**上可能用不同字形——本批三张照片里，**盒面大字放大到 6× 后第 2／6 位看起来是带横杠的 A**，而环带上那串字淡到无法判定；用户此前确认的是 `MΛGEΛSY`。

**此时不能只写单向禁止**：只写"不得把 Λ 规范化成 A"，模型在**盒面本来是 A** 的地方就会**把 A 改成 Λ**——提示词又一次成了破坏源（与 §一 的事故同源，只是方向相反）。

**安全写法（照原样 + 双向禁止 + 失败判据）**：

```
BRAND WORDMARK LOCK — reproduce the wordmark EXACTLY as the source prints it
- The brand wordmark is a SEVEN-glyph mark. Reproduce the exact glyph sequence, the exact glyph shapes, the cap height, the orientation and (on the curved ring band) the exact arc span and letter orientation.
- NEVER normalise, simplify, "correct" or auto-complete any glyph, and NEVER substitute one letterform for another IN EITHER DIRECTION: never turn the brand's angular glyph into a plain A, and never turn a plain A into the angular glyph.
- Never respell, re-typeset, re-space, restyle, translate or rewrite the wordmark; never straighten the curved version.
- If a glyph is ambiguous at this resolution, leave it EXACTLY as it is — do not redraw it.
- Treat any output in which a glyph has been substituted by a different letterform as a failed result.
```

**多载体分别锁定的原则**：环带丝印 / 壳体模压字 / 盒面印刷**各自独立**——不要求三处一致，只要求**各处与该处原图一致**；并要求"不得把某一处的字形推广到另一处"。

**判定顺序**：① 先向用户确认各载体的字形（给 a/b/c 三选项，见下）；② 用户确认前，用上面的**双向禁止**版本交付（安全性最高）；③ 确认后，把该载体的字形写死（约束力更强）。
- a：环上 `MΛGEΛSY`、盒面普通 `MAGEASY`（按载体分别写死）
- b：两处都是 `MΛGEΛSY`（统一按 Λ 写死）
- c：两处都是普通 `MAGEASY`（统一按 A 写死，并更正本文件 §一 的位次表）

---

## 五、迁移到其他品牌 / 产品

1. **字标**：先逐字符抄下实物字标（含符号与变体字形），再按位次列出并描述字形，最后照抄上面的 `BRAND WORDMARK LOCK` 结构。**拼写一律以用户确认为准**。
2. **LOGO**：先判"产品上是否应有图形标识"（有环 / 有磁吸结构的产品，LOGO 常在环内孔内），再判"它与哪些前景部件在视线上重叠"，据此写可见 / 隐藏分割。
3. **顺序铁律**：**位置 → 尺寸 → 可见性**，三者分开写；顺序颠倒会让模型先挑"最好看的位置"再执行"保持微弱"。
4. **失败判据**：对最容易退化的那一项，加一句 `Treat any output where … as a failed result.`
