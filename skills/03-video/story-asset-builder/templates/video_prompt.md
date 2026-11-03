# Template: Video Prompt / 视频生成提示词

```text
=== Video Prompt - {project_name} {episode_or_scene} {segment_name} v{version} ===

【视频定位】
{segment_function}
{duration}
{platform}
{reference_assets}

---

[STYLE LOCK]
{style_lock}

[SCENE]
{scene_description}

[CHARACTER LOCK]
{character_lock}

[CAMERA]
{camera_language}

[ACTION TIMELINE]
0s-{time_1}: {action_1}
{time_1}-{time_2}: {action_2}
{time_2}-{time_3}: {action_3}
{time_3}-{duration}: {action_4}

[EMOTION / PERFORMANCE]
{emotion_performance}

[LIGHTING]
{lighting}

[SOUND / MUSIC]
{sound_music}

[CONTINUITY]
{continuity_rules}

[NEGATIVE / AVOID]
{negative_rules}

【LibTV 参数建议】
model: Seedance 2.0 default unless user requests Kling O3/3.0
aspect_ratio: {aspect_ratio}
duration: {duration}
reference_images: {reference_images}
reference_video: {reference_video}
node_group: 08_Video_Segments

【实操注意】
1. 嘴型 / 动作 / 镜头 / 角色一致性重点检查
2. 如果角色漂移，先锁参考图，再重跑
3. 如果视频没放到画布，要求：重试创建整个工作流放在画布
```
