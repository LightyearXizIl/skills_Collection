# Prompt 编译规则

## 核心原则
Prompt 不是一句话，而是一份可生产、可质检、可迭代的资产说明书。

## 必须区分三层内容

### A. Prompt 主体
真正放入图片/视频模型的内容。

### B. API / LibTV 参数建议
放入节点设置或备注，不混入 prompt 主体。

### C. 实操注意 / 跑歪兜底加强
放入质检备注，不混入 prompt 主体。

## Prompt 文档模板

```text
=== GPT-Image Prompt - {project_name} {episode_or_scene} {asset_name} {asset_type} v{version} ===

【格式】
- {aspect_ratio}
- {layout}
- {view_count}
- {resolution_or_quality}

【资产定位】
{asset_role_and_story_function}

---

【prompt】
```

主体内部顺序：

```text
Opening format sentence
Layout
Panel / View details
Subject
Core identity
Appearance / Costume / Equipment / Structure
Color Palette
Pose / Camera / View
Critical consistency
Lighting
Style
Quality
Panel Labels if needed
Constraints
```

结束：

```text
=== END ===

【API / LibTV 参数建议】
...

【实操注意】
...

【跑歪兜底加强】
...
```

## 生成语言
- Prompt 主体优先英文，便于模型理解复杂画面。
- 标题、资产定位、实操注意可以中文。
- 专有名词可中英混排。

## 禁止事项
- 禁止只输出“生成一个 XXX”的短提示词。
- 禁止把“跑出来重点检查”放进 Prompt 主体。
- 禁止忽略版本号。
- 禁止把不同资产塞进同一个混乱节点。
- 禁止遗漏 Constraints。
