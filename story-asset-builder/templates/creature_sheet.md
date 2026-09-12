# Template: Creature Sheet / 怪兽、生物、机械兽设定图

```text
=== GPT-Image Prompt - {project_name} {episode_or_scene} {creature_name} 多视图设定图 v{version} ===

【格式】
- 16:9 横版 + 最高分辨率
- 4格均等 2x2：SIDE + FRONT + TOP + 3/4 VIEW
- 背景、光线、材质继承当前 Project Profile

【兽 / 怪兽设定】
{creature_role}
{species_or_construction}
{tactical_function}
{signature_visual_memory_point}
{scale_rule}
{world_dna}

---

【prompt】
```

A creature design reference sheet. **Horizontal 16:9 aspect ratio. Maximum resolution output.** {studio_backdrop}. {lighting_rule}. Same studio environment and visual DNA as {project_name}.

【Layout】
**2x2 equal grid**:
- Top-left: SIDE VIEW
- Top-right: FRONT VIEW
- Bottom-left: TOP-DOWN VIEW
- Bottom-right: 3/4 PERSPECTIVE VIEW
Thin neutral dividing lines between all four panels. Creature centered in each panel with even space margin.

【Subject — same creature across all 4 panels】
{creature_summary}

【Species / Anatomy / Construction — CRITICAL】
{species_anatomy_or_mechanical_structure}

【Scale】
{scale_details}

【Surface / Material】
{surface_material_details}

【Signature Visual Memory Point — MOST CRITICAL】
{signature_details}

【Eyes / Mouth / Limbs / Body Parts】
{body_part_details}

【Functional Story Elements】
{functional_elements}

【Decorations / Damage / Weathering】
{decoration_weathering}

【4 Panels detail】
**Top-left panel — SIDE VIEW**: {side_view_detail}
**Top-right panel — FRONT VIEW**: {front_view_detail}
**Bottom-left panel — TOP-DOWN VIEW**: {top_view_detail}
**Bottom-right panel — 3/4 PERSPECTIVE VIEW**: {three_quarter_detail}

【Critical consistency】
SAME individual creature in all 4 panels—identical proportions, signature feature, materials, markings, damage pattern, and lighting setup.

【Lighting - critical】
{lighting_detail}

【Style】
Hyperrealistic photographic creature design rendering—shot like a high-end practical animatronic creature or VFX production reference board. NOT illustration, NOT obvious 3D CGI render. {style_references}

【Quality】
Maximum resolution output. Sharp clean details. Every structural seam, texture, surface mark and functional part clearly defined.

【Panel Labels】
Small clean monospace sans-serif black text below each panel:
- Top-left: "SIDE"
- Top-right: "FRONT"
- Bottom-left: "TOP"
- Bottom-right: "3/4 VIEW"
Title at top center: "{english_title} — DESIGN SHEET"

【Constraints】
{constraints}

```text
=== END ===

【API / LibTV 参数建议】
aspect_ratio: 16:9
node_group: 02_Creature_Assets
model: image reference sheet model available in LibTV
reference_images: {reference_images}

【实操注意】
1. 跑出来重点检查：
   - 核心物种 / 怪兽识别点是否明显
   - 体型比例是否正确
   - 是否四视图一致
   - 是否符合项目材质 DNA
   - 文字标签是否准确
2. 跑歪兜底加强：
   - {rerun_fix_1}
   - {rerun_fix_2}
   - {rerun_fix_3}
```
