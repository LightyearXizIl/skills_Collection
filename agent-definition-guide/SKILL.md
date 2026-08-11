---
name: agent-definition-guide
description: >-
  创建、修改、删除或排查 DeterminFlow Agent Definition 时必须加载此技能；也适用于选择 agent_type、最小工具权限、Prompt 模板绑定、模型覆盖、Skill/Rule 可见分组、子会话可用性与 Workflow Agent 节点配置。
metadata:
  display_name: agent-definition-guide
  version: 1.0.1
  author: system
  category: general
  priority: 50
  workflow_only: false
---

# Agent Definition 指南

## 先区分三个概念

- Agent Definition 定义一种可复用 Agent 类型，事实源是 `config/agents_config.json`。
- Prompt Template 定义该类型使用的系统提示词 sections，事实源是
  `config/prompts_config.json`。
- Workflow Agent 节点只是引用 `agent_type`，不会复制 Agent Definition。

修改 Prompt 时加载 `prompt-template-guide`；修改 Workflow 节点时加载
`workflow-guide`。

## 修改前检查

1. 用 `list_agent_types` 或 `GET /api/agent-definitions/config` 读取当前定义。
2. 用 `GET /api/tools` 获取真实工具名，不根据文档或旧配置猜测。
3. 用 `GET /api/prompt-templates` 确认 `prompt_template` 存在。
4. 搜索 Workflow、Cron 与调用方对目标 `agent_type` 的引用，评估删除或改名影响。
5. 先决定最小职责，再分配最小工具白名单；不要从 `['*']` 开始缩减。

## 核心字段

| 字段 | 说明 |
|---|---|
| `description` | 明确何时选择此类型，供主 Agent 和 UI 判断 |
| `prompt_template` | `prompts_config.json` 中的模板 key |
| `tools` | `null` 表示仅通信工具，`['*']` 表示全部可用工具，数组表示白名单 |
| `disallowed_tools` | 在白名单基础上继续剔除 |
| `model` | 可选模型覆盖；空值继承父 Agent |
| `model_params` | thinking、reasoning、temperature、top_p、stream timeout 等覆盖 |
| `max_turns` | 最大工具轮次，不是质量目标 |
| `system_prompt_template` | 追加到基础 Prompt 的类型级指令 |
| `include_skills` / `include_rules` | 是否注入运行时 Skills / Rules |
| `visible_skill_group_ids` / `visible_rule_group_ids` | 限制可见资源组 |
| `copy_main_workspace` | `null` 继承全局设置，布尔值显式覆盖 |
| `available_for_sub_session` | 是否允许用户或主 Agent 创建该类型的子会话 |
| `extension_options` | Plugin 提供的扩展配置；必须符合对应 Plugin 契约 |

所有 Sub Agent 都会先应用全局禁用列表。目前 `create_sub_session`、
`check_sub_progress` 与 `delete_session` 不会因 `tools=['*']` 而重新获得。

## 操作面

| 操作 | API |
|---|---|
| 读取配置 | `GET /api/agent-definitions/config` |
| 新建 | `POST /api/agent-definitions` |
| 更新 | `PUT /api/agent-definitions/{agent_type}` |
| 删除 | `DELETE /api/agent-definitions/{agent_type}` |
| 重载 | `POST /api/agent-definitions/reload` |

优先使用 Web 或 API。只有 API 未暴露目标字段且任务明确要求修改项目配置时，才编辑
`config/agents_config.json`，随后调用 reload。不要在运行时绕过配置管理器写内存对象。

新增 API 支持 `agent_type`、`description`、`tools`、`disallowed_tools`、`model`、
`max_turns`、`system_prompt_template`、`copy_main_workspace`、`extension_options` 与
`model_params`。更新 API 还支持可见 Skill/Rule 分组和 `prompt_template`。未暴露字段需要
项目配置变更和对应测试，不能假装 API 已支持。

## 权限设计

按照一个职责一个类型设计：

1. 列出完成职责所必需的读工具。
2. 仅在任务确实需要修改状态时加入写工具。
3. 对命令执行、外部网络、资源管理等高影响工具单独论证。
4. 用 `disallowed_tools` 表达临时或环境级额外禁用，不用它掩盖过宽白名单。
5. Workflow 节点若需要 `complete_node_task` 或 `reject_upstream`，由节点开关控制，
   不把它们错误地当作普通 Agent Definition 白名单。

## Prompt 与模型绑定

- `prompt_template` 必须存在；删除模板前先迁移全部 Agent Definition 引用。
- `system_prompt_template` 只放该 Agent 类型特有的短指令；通用结构放 Prompt Template。
- `model` 和 `model_params` 是覆盖层。没有明确原因时继承默认值，避免配置漂移。
- `model` 始终使用 `provider_id:model_name`；不要在 Agent Definition 中写
  `provider_type`。Provider Adapter 会按该实例的类型领取 `model_params` 中支持的字段。
- `max_turns` 太低会截断任务，太高会放大循环成本；根据工具步骤设置并通过真实任务验证。

## 验收清单

- reload 成功，`list_agent_types` 能看到预期定义。
- `prompt_template` 与工具名全部存在。
- 最小工具集能完成代表性任务，越权工具不可见。
- `available_for_sub_session=false` 的内部类型不会出现在可创建类型中。
- 新建子会话验证 Prompt、workspace、Skill/Rule 可见性和模型配置；已有会话不作为验证对象。
- 删除或改名后不存在 Workflow、Cron、Prompt 或测试中的悬空引用。

## 常见错误

- `tools=[]` 与 `tools=null` 语义不同：空数组没有普通工具，`null` 保留通信工具语义。
- `tools=['*']` 仍受全局禁用列表约束。
- 只创建 Agent Definition、不创建同名 Prompt Template：使用显式已有模板即可；二者不要求同名。
- 修改配置后只看文件：必须 reload 并创建新会话验证。
- 删除内置或被引用类型：先迁移引用，再删除，最后做启动交叉校验。
