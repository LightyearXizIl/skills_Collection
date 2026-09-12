# Template: Storyboard Grid / 九宫格分镜

```text
=== GPT-Image Prompt - {project_name} {episode_or_scene} 九宫格分镜 v{version} ===

【格式】
- 3x3 nine-panel grid image
- 九个独立电影画面，细黑边分隔
- 所有画面属于同一场戏 / 同一段落 / 同一视觉风格

【分镜定位】
{storyboard_function}
{sequence_summary}
{continuity_rule}

---

【prompt】
```

Generate a single 3x3 nine-panel grid image, nine separate cinematic frames arranged in a 3-row, 3-column grid, each panel divided by thin black borders, like a film contact sheet / storyboard sheet.

All nine panels depict {sequence_continuity}. Keep the same visual DNA: {visual_dna}. Same color palette, same lighting logic, same atmosphere, same character and environment continuity across all panels.

【Panel List】
Panel 1 (top-left): {panel_1}
Panel 2 (top-center): {panel_2}
Panel 3 (top-right): {panel_3}
Panel 4 (middle-left): {panel_4}
Panel 5 (middle-center): {panel_5}
Panel 6 (middle-right): {panel_6}
Panel 7 (bottom-left): {panel_7}
Panel 8 (bottom-center): {panel_8}
Panel 9 (bottom-right): {panel_9}

【Preserve】
{preserve_rules}

【Constraints】
{constraints}

【Photographic Tone】
Each panel is a cinematic film still that may appear slightly soft and imperfect, like a real photograph. Natural lens depth of field, realistic light falloff, subtle organic film grain, restrained color grading, not HDR, not over-sharpened.

Avoid: oversharpening, artificial sharpness, heavy digital grain, HDR effect, AI-generated aesthetic, overpolished look, oversaturation, glossy highlight blowout, cartoon or obvious CGI look, inconsistent characters, inconsistent environment.

```text
=== END ===

【API / LibTV 参数建议】
aspect_ratio: 16:9 or 3:4 according to platform
node_group: 07_Storyboard_And_Keyframes
reference_images: {reference_images}

【实操注意】
1. 跑出来重点检查：
   - 九格是否完整
   - 是否同一场戏连续
   - 角色 / 场景 / 光线是否一致
   - 每格是否有明确镜头差异
2. 跑歪兜底加强：
   - {rerun_fix_1}
   - {rerun_fix_2}
```
