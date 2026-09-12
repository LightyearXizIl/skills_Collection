# Changelog

## v0.2.0 — Canvas Blueprint Update

新增：

- `rules/libtv_canvas_rules.md` 重写为 Canvas Blueprint v2
- `SKILL.md` 新增 Canvas Blueprint 硬规则
- `quick_prompts/04_create_clean_canvas.txt`
- `quick_prompts/05_reorganize_existing_canvas.txt`

核心变化：

- 创建 LibTV 画布前必须先生成 Canvas Blueprint
- 默认 6 区排版：项目总览、风格 DNA、人物资产、世界资产、分镜视频、归档区
- 统一节点命名：序号_资产类型_资产名称_用途_v版本号
- 每个资产按 PROMPT / GENERATE / QA 小组靠近摆放
- 禁止散乱节点、空节点、无命名节点、重复节点
