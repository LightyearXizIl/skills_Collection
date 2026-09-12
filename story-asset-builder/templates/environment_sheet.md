# Template: Environment Sheet / 场景环境设定图

```text
=== GPT-Image Prompt - {project_name} {episode_or_scene} {environment_name} 场景设定图 v{version} ===

【格式】
- 默认 16:9 横版 + 最高分辨率
- 可选：单张主视觉 / 3视图空间设定 / 九宫格环境情绪板

【场景定位】
{environment_story_function}
{time_of_day}
{mood}
{key_story_action}
{visual_memory_point}

---

【prompt】
```

A professional cinematic environment concept reference image. **Horizontal 16:9 aspect ratio. Maximum resolution output.** {environment_type}. {lighting_rule}. Same visual DNA as {project_name}: {visual_dna}.

【Scene】
{scene_summary}

【Spatial Layout】
{spatial_layout}

【Architecture / Set Design】
{architecture_set_design}

【Key Props / Story Elements】
{key_props_story_elements}

【Atmosphere】
{atmosphere}

【Color Palette】
{color_palette}

【Camera / Composition】
{camera_composition}

【Lighting - critical】
{lighting_detail}

【Style】
Photorealistic cinematic film still / production design environment reference. Natural lens behavior, realistic scale, believable set dressing. {style_references}

【Quality】
Maximum resolution. Architectural details, environmental textures, props and atmosphere are clear but natural. Not over-sharpened.

【Constraints】
{constraints}

```text
=== END ===

【API / LibTV 参数建议】
aspect_ratio: 16:9
node_group: 05_Environment_Assets
reference_images: {reference_images}

【实操注意】
1. 跑出来重点检查：
   - 空间结构是否清楚
   - 关键剧情区域是否可用
   - 风格和色彩是否继承 Profile
   - 是否可作为后续镜头背景资产
2. 跑歪兜底加强：
   - {rerun_fix_1}
   - {rerun_fix_2}
```
