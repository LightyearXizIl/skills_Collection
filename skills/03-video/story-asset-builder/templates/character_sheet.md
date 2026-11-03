# Template: Character Sheet / 人物设定图

```text
=== GPT-Image Prompt - {project_name} {episode_or_scene} {character_name} 默认形态四视图人设图 v{version} ===

【格式】
- 9:16 竖版 + 最高分辨率
- 4宫格不等大：上小下大
- 左上正脸特写 + 右上侧脸特写 + 左下脖子以下全身无脸 + 右下背面全身含后脑勺
- 背景、光线、色调继承当前 Project Profile

【角色定位】
{character_role}
{story_function}
{hierarchy_or_power_level}
{relationship_to_other_assets}

---

【prompt】
```

A character design reference sheet. **Vertical 9:16 aspect ratio. Maximum resolution output.** {studio_backdrop}. {lighting_rule}. Same visual DNA as the project profile: {visual_dna}.

【Layout】
**2x2 grid with unequal panel heights**:
- Top row: two smaller panels, each approximately 1/3 of total canvas height — head/face close-ups
- Bottom row: two larger panels, each approximately 2/3 of total canvas height — full body shots
- Thin neutral dividing lines between all four panels
- All four panels share the same backdrop, same lighting setup, same color palette

【4 Panels】
**Top-left panel — FRONT FACE CLOSE-UP**:
Tight close-up of {character_name}'s face, framed from collarbone-line up to top of head. Subject facing camera directly. Face fully visible. Preserve: {face_key_features}.

**Top-right panel — SIDE FACE CLOSE-UP (PROFILE)**:
Tight side profile close-up, framed from collarbone-line up to top of head. Subject facing camera-right. Profile silhouette clearly visible. Preserve: {side_profile_key_features}.

**Bottom-left panel — FULL BODY FROM NECK DOWN, FRONT VIEW (NO FACE)**:
Full body shot from collarbone-line down to feet, facing camera directly. The face/head is intentionally cropped out at the top of this panel. Focus on body proportions, costume, equipment, weapons and material details. Zero face involvement.

**Bottom-right panel — FULL BODY BACK VIEW (INCLUDING BACK OF HEAD)**:
Full body shot from head to feet, facing directly away from camera. Includes back of head, hairstyle/back headwear, back-mounted equipment and rear costume details.

【Subject — same character across all 4 panels】
{character_summary}

【Character Core】
{age_range}, {body_type}, {temperament}, {role_logic}. NOT {body_negative_list}.

【Face / Ethnicity / Age / Texture】
{face_and_identity_details}

【Hair / Makeup / Skin】
{hair_makeup_skin_details}

【Costume】
{costume_details}

【Equipment / Weapons / Props】
{equipment_details}

【Color Palette】
{color_palette}

【Pose - same across all 4 panels】
{pose_rule}

【Critical consistency】
SAME individual character in all 4 panels: identical face structure, hairstyle, costume, equipment, colors, body proportions, material aging, and lighting direction.

【Lighting - critical】
{lighting_detail}

【Style】
Hyperrealistic photographic character design rendering—shot like a high-end practical costume photographed in a film production studio for a cinematic lookbook reference board. NOT illustration, NOT obvious 3D CGI render. {style_references}

【Quality】
Maximum resolution output. Clean detail definition. Real physical costume cinematic photography aesthetic. {quality_details}

【Panel Labels】
Small clean monospace sans-serif black text below each panel:
- Top-left: "FRONT FACE"
- Top-right: "SIDE FACE"
- Bottom-left: "BODY FRONT (NO FACE)"
- Bottom-right: "BACK"
Title at top center of canvas: "{english_title} — DEFAULT FORM CHARACTER SHEET"

【Constraints】
{constraints}

```text
=== END ===

【API / LibTV 参数建议】
aspect_ratio: 9:16
node_group: 01_Character_Assets
model: image reference sheet model available in LibTV
reference_images: {reference_images}

【实操注意】
1. 跑出来重点检查：
   - 角色是否同一个人
   - 左下 panel 是否严格无脸
   - 服装 / 装备 / 体型 / 年龄是否正确
   - 风格是否符合 Project Profile
   - Title + 4 labels 是否准确
2. 跑歪兜底加强：
   - {rerun_fix_1}
   - {rerun_fix_2}
   - {rerun_fix_3}
```
