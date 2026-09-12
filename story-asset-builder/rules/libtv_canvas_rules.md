# LibTV 画布创建规则 v2 — Canvas Blueprint

## 目标
让 LibTV 画布不是一堆散节点，而是清晰、可读、可检查、可复用的资产生产看板。

核心原则：

```text
剧本 → 资产清单 → Canvas Blueprint → LibTV 节点创建 → 节点索引表
```

任何创建 LibTV 画布的任务，都必须先生成 Canvas Blueprint，再创建节点。

---

## Canvas Blueprint Rule

只要用户要求创建 LibTV 画布，必须先生成 Canvas Blueprint。除非用户明确说“不要规划，直接创建”，否则不得跳过。

Canvas Blueprint 必须包含：

1. 项目总览区
2. 风格 DNA 区
3. 人物资产区
4. 场景 / 道具 / 怪兽 / 载具资产区
5. 分镜 / 关键帧 / 视频区
6. 废弃 / 重跑 / 归档区

---

## 默认画布分区

```text
01_PROJECT_INDEX：项目总览区
02_STYLE_DNA：视觉风格 / 色卡 / 材质 / 灯光区
03_CHARACTERS：人物资产区
04_WORLD_ASSETS：场景 / 道具 / 怪兽 / 载具区
05_STORYBOARD_VIDEO：分镜 / 关键帧 / 视频区
99_ARCHIVE：废弃节点 / 失败节点 / 重跑节点区
```

### 推荐空间排布

```text
左侧：01_PROJECT_INDEX + 02_STYLE_DNA
中上：03_CHARACTERS
中下：04_WORLD_ASSETS
右侧：05_STORYBOARD_VIDEO
底部 / 最右下：99_ARCHIVE
```

如果 CLI 支持坐标，应按从左到右的流程摆放：

```text
Project / Style → Asset Prompt → Generate → QA / Retry → Storyboard / Video
```

如果 CLI 不支持坐标，也必须通过节点名称、分组、备注和索引表维持上述结构。

---

## 节点命名规则

统一格式：

```text
序号_资产类型_资产名称_用途_v版本号
```

示例：

```text
01_INDEX_项目总览_v1
02_STYLE_视觉DNA_v1
03_CHARACTER_主角_四视图_v1
04_ENV_地下储藏室_场景设定_v1
05_PROP_旧收音机_道具设定_v1
06_CREATURE_门外未知存在_概念设定_v1
07_STORYBOARD_第一场_九宫格_v1
08_VIDEO_第一场_图生视频_v1
99_ARCHIVE_废弃节点区_v1
```

资产类型建议：

```text
INDEX / STYLE / CHARACTER / ENV / PROP / CREATURE / VEHICLE / STORYBOARD / KEYFRAME / VIDEO / QA / RETRY / ARCHIVE
```

---

## 每个资产小组结构

每个资产默认最多包含以下节点：

```text
PROMPT：完整提示词
GENERATE：生成节点
QA：实操注意 / 跑歪兜底加强
REF：参考图节点，可选
V2_RETRY：重跑节点，可选
```

每个资产的小组必须靠近摆放，不允许把所有 PROMPT 堆在一起，也不允许把所有 GENERATE 堆在一起。

推荐命名：

```text
03_CHARACTER_主角_PROMPT_v1
03_CHARACTER_主角_GENERATE_v1
03_CHARACTER_主角_QA_v1
03_CHARACTER_主角_V2_RETRY_v2
```

---

## README / INDEX 节点

每个 LibTV 画布必须创建一个 `01_INDEX_项目总览_v1` 节点，放在画布左上或第一个节点位置。

INDEX 节点必须包含：

```text
项目名：
一句话剧情：
项目 Profile：
资产数量：
画布分区：
节点命名规则：序号_资产类型_资产名称_用途_v版本号
使用顺序：先看 STYLE_DNA，再看 CHARACTERS，再看 WORLD_ASSETS，最后看 STORYBOARD_VIDEO
待用户确认生成的节点：
```

---

## Canvas Blueprint 输出格式

创建画布前，必须先输出如下规划表：

```yaml
canvas_blueprint:
  project_name:
  profile:
  layout_version: canvas_blueprint_v2
  sections:
    - id: 01_PROJECT_INDEX
      purpose: 项目总览区
      nodes:
        - node_name:
          node_type:
          asset_ref:
          action: create_note / create_prompt / create_generate / create_qa
          generate_now: false
    - id: 02_STYLE_DNA
      purpose: 视觉风格 / 色卡 / 材质 / 灯光区
      nodes: []
    - id: 03_CHARACTERS
      purpose: 人物资产区
      nodes: []
    - id: 04_WORLD_ASSETS
      purpose: 场景 / 道具 / 怪兽 / 载具区
      nodes: []
    - id: 05_STORYBOARD_VIDEO
      purpose: 分镜 / 关键帧 / 视频区
      nodes: []
    - id: 99_ARCHIVE
      purpose: 废弃 / 失败 / 重跑节点区
      nodes: []
```

用户没有明确要求“立即创建”时，应先等待用户确认 Blueprint。

用户明确说“直接创建画布 / 自动创建画布 / 不用确认”时，可以在生成 Blueprint 后直接执行创建，但仍必须在最终回复里返回 Blueprint 摘要与节点索引表。

---

## 禁止事项

禁止：

- 禁止直接把所有节点散乱创建到画布
- 禁止无命名节点
- 禁止重复空节点
- 禁止把所有 prompt 堆在一起
- 禁止未经规划直接创建大量节点
- 禁止把【实操注意】混入生图 Prompt 主体
- 禁止创建只有标题没有内容的空节点
- 禁止把失败节点和正式资产节点混在同一区域

---

## 默认执行流程

```text
1. 先拆解资产清单
2. 再生成 Canvas Blueprint
3. 再按 Blueprint 创建 LibTV 画布节点
4. 创建完成后输出节点索引表
5. 如果节点乱了，执行“按标准 Canvas Blueprint 重新整理当前画布”
```

---

## 画布失败处理

如果工作流没有放到画布：

```text
请确认是否把整个生成工作流创建在了画布上？如果没有，请重试创建整个工作流放在画布。
```

如果节点为空：

```text
你的节点是空的，重新创建工作流，要把结果也放到节点里。
```

如果节点散乱：

```text
按 story-asset-builder/rules/libtv_canvas_rules.md 的 Canvas Blueprint Rule 重新整理当前画布；不要重新生成图片，只重排、重命名、归档和补充 INDEX 节点。
```

如果无法调用 LibTV：

```text
只输出资产清单 + Prompt 文档 + Canvas Blueprint + LibTV 节点创建指令，提醒用户安装 / 授权 LibTV skill 或 CLI。
```
