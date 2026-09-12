# Template: Vehicle Sheet / 载具设定图

```text
=== GPT-Image Prompt - {project_name} {episode_or_scene} {vehicle_name} 载具设定图 v{version} ===

【格式】
- 16:9 横版 + 最高分辨率
- 多视图设计板：SIDE / FRONT / TOP / 3/4 VIEW，可增加驾驶舱 / 轮组 / 引擎细节

【载具定位】
{vehicle_story_function}
{driver_or_owner}
{movement_logic}
{signature_visual_memory_point}

---

【prompt】
```

A professional vehicle design reference sheet. **Horizontal 16:9 aspect ratio. Maximum resolution output.** {studio_backdrop}. {lighting_rule}. Official film production design board.

【Layout】
{layout_detail}

【Subject — same vehicle across all views】
{vehicle_summary}

【Silhouette / Scale】
{silhouette_scale}

【Mechanical / Movement System】
{mechanical_system}

【Cockpit / Driver Interface】
{cockpit_details}

【Materials / Surface】
{material_details}

【Damage / Weathering / Customization】
{weathering}

【View Details】
{view_details}

【Critical consistency】
Same vehicle across all panels—identical silhouette, components, material, decals, damage and scale.

【Lighting】
{lighting_detail}

【Style】
Hyperrealistic film vehicle production design reference, practical build / VFX vendor sheet aesthetic. NOT illustration, NOT cartoon, NOT clean toy render.

【Quality】
Maximum mechanical detail. Every panel seam, bolt, suspension part, cockpit detail and surface scratch visible.

【Constraints】
{constraints}

```text
=== END ===

【API / LibTV 参数建议】
aspect_ratio: 16:9
node_group: 04_Vehicle_Assets
reference_images: {reference_images}

【实操注意】
1. 跑出来重点检查：
   - 载具轮廓是否稳定
   - 驾驶逻辑是否清楚
   - 尺寸比例是否正确
   - 和项目材质 DNA 是否统一
2. 跑歪兜底加强：
   - {rerun_fix_1}
   - {rerun_fix_2}
```
