---
name: story-asset-builder
description: 将剧本、短片创意、分镜或世界观拆解为人物、场景、道具、怪兽、载具、色卡、分镜和视频段落资产，并编译成可用于 LibTV 画布的标准化提示词文档。用于剧本资产拆解、LibTV 资产画布规划和提示词编译；实际创建画布前必须确认 LibTV 能力与授权可用。
---

# story-asset-builder

## 中文名
剧本资产生成器 / Story Asset Builder

## 定位
本 Skill 用于把任意剧本、短片创意、分镜描述、世界观设定，自动拆解成 LibTV 画布里的资产节点，并按“工业化提示词文档”格式生成可复用 Prompt。

它不是替代 LibTV skill / LibTV CLI，而是作为上层“资产导演 + Prompt 编译器”使用：

```text
用户输入剧本需求
→ 解析项目与风格 Profile
→ 拆解人物 / 场景 / 道具 / 怪兽 / 载具 / 色卡 / 分镜 / 视频段落
→ 套用对应资产模板
→ 生成标准化 Prompt 文档
→ 调用已安装的 LibTV skill / LibTV CLI 在画布创建节点
→ 把 Prompt、参数建议、实操注意、跑歪兜底加强写入对应节点
→ 用户在 LibTV 里确认生成
```

## 何时触发
当用户出现以下需求时，优先使用本 Skill：

- “根据剧本创建 LibTV 资产画布”
- “帮我拆人物、道具、场景、怪兽节点”
- “按某个提示词文档格式生成资产 Prompt”
- “我只想在 LibTV 确认生成，前面节点和提示词自动帮我建好”
- “创建某个短剧 / 漫剧 / AI电影 / 产品片的资产准备工作流”
- “把剧本变成角色设定图、道具图、场景图、分镜图、视频节点”

## 依赖
必须提前安装并授权 LibTV skill / LibTV CLI。若没有检测到 LibTV 相关能力，先提醒用户安装或授权，不要假装已经创建画布。

安装位置建议：

```text
~/.openclaw/skills/story-asset-builder/
```

LibTV 访问要求：

```text
LIBTV_ACCESS_KEY 已配置，或用户已在 OpenClaw / 飞书 ClawBot 中完成 LibTV 授权。
```

## 工作原则

### 1. 不写死项目
不要把“万物生”写成唯一项目。本 Skill 是通用剧本资产生成器。
“万物生”只是一个 profile 样板。遇到新剧本时，应先判断：

```text
是否指定项目 Profile？
- 是：读取该 profile，继承风格规则。
- 否：根据剧本自动创建临时 Project Profile。
```

### 2. 先拆资产，再建节点
不要直接把用户剧本塞进一个大 Prompt。必须先输出并执行资产拆解：

```text
角色资产
场景资产
道具资产
怪兽 / 生物资产
载具资产
色卡 / 视觉 DNA 资产
关键帧 / 分镜资产
视频段落资产
```

### 3. Prompt 必须工程化
生成 Prompt 时，必须采用“标题 + 格式 + 资产设定 + prompt 主体 + constraints + 实操注意”的文档结构。
不要只输出一句普通提示词。

### 4. 实操注意不是生图 Prompt
`【实操注意】`、`【跑歪兜底加强】`必须写入节点备注、质检说明或同级文档，不要混入生图 Prompt 主体。

### 5. LibTV 画布必须有结构
创建 LibTV 画布时，必须按资产类型分组：

```text
00_Project_Profile
01_Character_Assets
02_Creature_Assets
03_Prop_Assets
04_Vehicle_Assets
05_Environment_Assets
06_Color_And_Material_DNA
07_Storyboard_And_Keyframes
08_Video_Segments
09_QA_Notes_And_Rerun_Fixes
```

### 6. 默认先创建资产图节点，不直接生成最终视频
除非用户明确要求“直接出视频”，否则只准备资产节点和 Prompt，不启动最终视频合成。

## 标准执行流程

### Step 1：读取用户需求
从用户输入中提取：

```text
project_name
story_type
episode_or_scene
script_text
visual_reference
style_reference
output_goal
platform_or_model_preference
```

### Step 2：选择或创建 Project Profile
优先级：

1. 用户明确指定 profile
2. 从剧本类型匹配已有 profile
3. 自动创建临时 profile
4. 使用 profiles/default_cinematic.yaml

### Step 3：资产拆解
输出资产清单，每个资产必须包含：

```yaml
asset_id:
asset_name:
asset_type:
asset_role:
priority:
template:
libtv_node_group:
required_views:
aspect_ratio:
prompt_status:
qa_risk:
```

### Step 4：Prompt 编译
根据资产类型套用模板：

```text
人物 → templates/character_sheet.md
怪兽 / 生物 → templates/creature_sheet.md
道具 / 武器 → templates/prop_sheet.md
载具 → templates/vehicle_sheet.md
场景 → templates/environment_sheet.md
色卡 → templates/color_palette.md
分镜 → templates/storyboard_grid.md
视频 → templates/video_prompt.md
```

### Step 5：LibTV 画布创建
调用已安装 LibTV skill / CLI，执行：

```text
create_session / 开启新项目
创建节点组
创建每个资产节点
写入 Prompt 主体
写入尺寸 / 比例 / 模型建议
写入实操注意与跑歪兜底加强
把所有工作流放到画布上
返回 LibTV project 链接
```

若画布没有节点，或节点为空，必须重试并提示：

```text
重试创建整个工作流放在画布
你的节点是空的，重新创建工作流，要把结果也放到节点里
```

### Step 6：返回给用户
最终回复必须包含：

```text
1. 已创建的项目名
2. 资产节点数量
3. 节点分组概览
4. LibTV project 链接，若工具返回
5. 需要用户确认生成的节点
6. 若失败，明确说明失败点和下一步
```

## Prompt 文档标准结构
每个资产 Prompt 文档必须尽量使用以下结构：

```text
=== GPT-Image Prompt - {project_name} {asset_name} {asset_type} v{version} ===

【格式】
- aspect ratio
- layout
- view count
- model / quality suggestion

【资产定位】
- story function
- visual memory point
- relation to other assets
- hierarchy / power level if applicable

---

【prompt】
```

Prompt 主体：
- opening format sentence
- Layout
- Panel / View details
- Subject
- Core identity
- Costume / Equipment / Structure
- Color Palette
- Pose / View / Camera
- Critical consistency
- Lighting
- Style
- Quality
- Panel Labels if needed
- Constraints

```text
=== END ===

【API / LibTV 参数建议】
size / aspect ratio / quality / model / reference images / node group

【实操注意】
1. 跑出来重点检查
2. 跑歪兜底加强
3. 版本迭代建议
```

## LibTV 节点命名规范

```text
{序号}_{资产类型}_{资产名}_v{版本}
```

示例：

```text
01_Character_沙猎喽啰A钩索手_v1
02_Creature_机械赛加羚羊_v1
03_Environment_部落崖壁市集_v1
04_Prop_旧收音机_v1
05_Storyboard_第一场九宫格_v1
```

## 默认模型建议
仅作为节点备注，不强制。具体以 LibTV 当前可用模型为准。

```yaml
image_reference_sheet: GPT-Image / Neo Image / Seedream / LibTV 当前可用图片模型
video_generation: Seedance 2.0 默认；用户明确要求时可用 Kling O3/3.0
aspect_ratio:
  character_sheet: 9:16
  creature_sheet: 16:9
  prop_sheet: 16:9 or 1:1
  environment_sheet: 16:9
  storyboard_grid: 16:9 or 3:4
  video: 根据用户平台，默认 16:9；短视频默认 9:16
```

## 失败处理

如果无法调用 LibTV：

```text
我已经完成资产拆解和 Prompt 编译，但当前环境没有可用的 LibTV 调用能力 / 授权，无法直接创建画布。请确认已安装 LibTV skill / CLI 并配置 access_key。你也可以把我生成的节点创建指令复制到 OpenClaw 中执行。
```

如果节点没有放在画布：

```text
请确认是否把整个生成工作流创建在了画布上。若没有，请重试创建整个工作流放在画布。
```

如果生成结果不合格：

```text
不要直接重写全部 Prompt。先定位失败项，再从对应资产的【跑歪兜底加强】中追加修复句，创建 v2 节点。
```

---

## Canvas Blueprint 硬规则 v2

任何时候，只要用户要求创建 LibTV 画布，必须先读取并遵守：

```text
rules/libtv_canvas_rules.md
```

创建画布前必须生成 Canvas Blueprint，不能直接创建散乱节点。

默认画布必须使用 6 个分区：

```text
01_PROJECT_INDEX：项目总览区
02_STYLE_DNA：视觉风格 / 色卡 / 材质 / 灯光区
03_CHARACTERS：人物资产区
04_WORLD_ASSETS：场景 / 道具 / 怪兽 / 载具区
05_STORYBOARD_VIDEO：分镜 / 关键帧 / 视频区
99_ARCHIVE：废弃节点 / 失败节点 / 重跑节点区
```

所有节点必须使用统一命名：

```text
序号_资产类型_资产名称_用途_v版本号
```

每个资产小组默认包含：

```text
PROMPT / GENERATE / QA / REF可选 / V2_RETRY可选
```

禁止把所有 Prompt、生成节点、QA 节点分别堆在一起。每个资产的小组必须靠近摆放，并在最终回复里返回节点索引表。

如果用户说：

```text
使用 story-asset-builder 创建画布
按标准画布蓝图创建
按标准 Canvas Blueprint 创建
重新整理当前 LibTV 画布
```

应自动执行以上规则，不要要求用户重复输入画布排版规则。
