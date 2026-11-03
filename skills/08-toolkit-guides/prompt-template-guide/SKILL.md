---
name: prompt-template-guide
description: >-
  查看、创建、修改、删除或排查 DeterminFlow Prompt Template 与 system prompt section 时必须加载此技能；也适用于 section 顺序、workflow_only/chat_only、cache break、自定义 template_variables、系统变量渲染以及 Agent Definition 的 prompt_template 绑定。
metadata:
  display_name: prompt-template-guide
  version: 1.0.0
  author: system
  category: general
  priority: 50
  workflow_only: false
---

# Prompt Template 指南

## 数据边界

`config/prompts_config.json` 是所有 Prompt Template 的唯一配置源。顶层
`agents.{template_name}` 包含 `description`、`sections`、`preambles`，可选
`template_variables`。`data/system_prompt.json` 是 main Prompt 缓存，
`data/prompt_history.json` 是修改历史，二者都不是编辑源。

Agent Definition 的 `prompt_template` 引用模板 key。涉及 Agent 类型或工具权限时加载
`agent-definition-guide`；涉及 Workflow 节点变量块时同时加载 `workflow-guide`。

## 修改前检查

1. 用 `list_agent_types` 或 `GET /api/prompt-templates` 列出模板。
2. 用 `get_system_prompt(agent_type=...)` 或
   `GET /api/prompt-sections?prompt_type=...&include_content=true` 读取完整 sections。
3. 检查 Agent Definition 对模板的引用；删除或改名必须先迁移引用。
4. 区分通用 section、仅聊天 section、仅 Workflow section 和类型级追加指令。
5. 明确要改变内容、顺序、启用状态还是变量声明，避免整份配置重写。

## Section 字段

| 字段 | 作用 |
|---|---|
| `name` | 模板内唯一稳定标识；重命名使用专用 API |
| `content` | Markdown 内容，可包含已注册占位符 |
| `enabled` | 是否参与组装 |
| `order` | 升序组装顺序 |
| `workflow_only` | 只在 Workflow 上下文注入 |
| `chat_only` | 只在非 Workflow 上下文注入 |
| `cache_break` | 标记缓存边界 |
| `cache_break_reason` | 解释为何此处需要缓存边界 |

不要同时把 `workflow_only` 与 `chat_only` 设为 true。缓存边界会影响成本和命中率，只有
内容确实随会话或运行频繁变化时才启用。

## 占位符规则

Section 中的 `{{name}}` 不会自动读取任意 Workflow 变量。可渲染的值来自两类：

- Core 注册的系统变量，如 `session_meta`、`workflow_overview`、`skills_section`；
- 当前模板在 `template_variables` 中声明的自定义变量块。

Workflow Agent 节点通过 `node_params.template_values` 给自定义变量块赋值；变量块的值
本身可再引用 Workflow 变量。未注册占位符会保留为字面量，不能把未替换文本当成成功。

自定义变量声明保持最小：稳定 `key`、清晰展示名、用途说明和必要默认值。删除变量前搜索
全部 section 内容与 Workflow 节点 `template_values`。

## 操作面

工具适合读取和精确更新已有 section：

- `get_system_prompt(agent_type=...)`
- `update_system_prompt(section_name=..., new_content=..., reason=..., agent_type=...)`
- `list_agent_types`

完整管理使用 Web 或 API：

| 操作 | API |
|---|---|
| 列出 sections | `GET /api/prompt-sections?prompt_type={type}` |
| 读取配置与变量 | `GET /api/prompt-sections/config?prompt_type={type}` |
| 更新单个/批量 | `PUT /api/prompt-sections/{name}`、`PUT /api/prompt-sections` |
| 新增/删除 | `POST /api/prompt-sections`、`DELETE /api/prompt-sections/{name}` |
| 重命名 | `POST /api/prompt-sections/{name}/rename` |
| 更新变量声明 | `PUT /api/prompt-sections/template-variables` |
| 重载 | `POST /api/prompt-sections/reload` |

所有 sections API 都要传正确的 `prompt_type`。使用更新工具时提供 `reason`，让 main 模板
修改进入历史。直接编辑配置仅用于项目级版本变更；编辑后必须 reload。

## 设计原则

- 一个 section 只承担一个稳定职责，名称描述目的，不描述临时内容。
- 通用行为放模板，某个 Agent 类型的短差异放 Agent Definition
  `system_prompt_template`，单次任务上下文放任务消息。
- 通过结构和工具描述传递已知信息，避免在多个 section 重复同一规则。
- `order` 留出间隔不是必要设计；排序只依赖数值。
- 修改时优先 patch 单个 section，避免覆盖其他并发配置变更。

## 验收清单

- JSON 可解析，模板 key 唯一，section name 在模板内唯一。
- Agent Definition 的每个 `prompt_template` 都存在。
- reload 成功，读取 API 返回更新后内容与顺序。
- 分别在 Chat 与 Workflow 上下文验证 `workflow_only/chat_only` 过滤。
- 自定义变量被实际渲染，未知占位符没有意外残留。
- main 模板修改后新建或刷新会话；不要只检查缓存文件。

## 常见错误

- 把模板名与 Agent 类型强制同名：它们可以不同，但引用必须存在。
- 编辑 `data/system_prompt.json`：下次重建会覆盖。
- 在 section 中直接写 `{{workflow_input}}` 却未声明自定义变量块。
- 删除 section 后仍有工具或治理指令引用其语义。
- 为静态内容设置 `cache_break`，无收益地降低缓存效率。
