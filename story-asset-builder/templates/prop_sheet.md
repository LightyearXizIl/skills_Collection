# Template: Prop Sheet / 道具、武器、设备设定图

```text
=== GPT-Image Prompt - {project_name} {episode_or_scene} {prop_name} 道具设定图 v{version} ===

【格式】
- 默认 16:9 横版 + 最高分辨率
- 4格或 3格多视图：FRONT / SIDE / BACK / DETAIL
- 背景、材质、灯光继承当前 Project Profile

【道具定位】
{prop_story_function}
{owner_or_related_character}
{usage_scene}
{signature_feature}

---

【prompt】
```

A professional prop design reference sheet. **Horizontal 16:9 aspect ratio. Maximum resolution output.** {studio_backdrop}. {lighting_rule}. Clean production design board layout.

【Layout】
{layout_detail}

【Subject — same prop across all views】
{prop_summary}

【Form / Structure】
{form_structure}

【Materials】
{material_details}

【Functional Parts】
{functional_parts}

【Scale / Handling】
{scale_handling}

【Wear / Damage / History】
{weathering_history}

【Color Palette】
{color_palette}

【View Details】
{view_details}

【Critical consistency】
Same prop across every view: identical silhouette, structure, material, color and wear pattern.

【Lighting】
{lighting_detail}

【Style】
Hyperrealistic prop photography / film production design reference sheet. NOT illustration, NOT toy-like, NOT generic 3D render. {style_references}

【Quality】
Maximum detail. Every seam, screw, scratch, fabric edge, symbol, functional part clearly defined.

【Panel Labels】
{panel_labels}

【Constraints】
{constraints}

```text
=== END ===

【API / LibTV 参数建议】
aspect_ratio: 16:9
node_group: 03_Prop_Assets
reference_images: {reference_images}

【实操注意】
1. 跑出来重点检查：
   - 轮廓是否可识别
   - 功能结构是否清楚
   - 材质是否符合项目
   - 是否像真实可用道具，而不是装饰玩具
2. 跑歪兜底加强：
   - {rerun_fix_1}
   - {rerun_fix_2}
```
