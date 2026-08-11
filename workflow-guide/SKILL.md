---
name: workflow-guide
description: >-
  创建、编辑、校验、运行或排查 DeterminFlow 工作流时必须先加载此技能；也适用于任务填参、节点审批、变量传递、网关、执行方案、子流程与工作区覆盖。涉及 Agent 定义、Prompt 模板或 Script Library 的专项设计时，继续加载对应 Core Skill。
metadata:
  display_name: workflow-guide
  version: 3.4.0
  author: system
  category: workflow
  priority: 50
  workflow_only: false
---

# Workflow 操作指南

## 先确定操作层级

DeterminFlow 有两个工作流对象：

- `definition.json` 是可复用的工作流模板。
- Task 是创建时冻结模板快照的运行实例；之后修改模板不会影响已有 Task。

版本化 Core Skill 位于 `src/core/defaults/skills/`，运行实例由启动时同步到
`data/skills/`。工作流业务数据始终位于 `data/workflows/{workflow_id}/`。

## 操作前检查

1. 先用 `list_workflows` 与 `get_workflow` 读取现状，不根据名称猜结构。
2. Agent 节点先用 `list_agent_types` 确认 `agent_type` 仍存在；详细定义规则见
   `agent-definition-guide`。
3. Script Library 节点先核对脚本身份、类型与分组；详细规则见
   `script-library-guide`。
4. 每个节点和网关都提供唯一 ID、可读 `label` 与 `position`。并行分支错开 x 坐标，
   主链按 y 坐标递增。
5. 修改前确认目标是模板、已有 Task，还是新 Task；不要把三者混为一谈。

## 首选操作面

工作流模板优先通过 Web 或 Workflow API 管理，因为 API 会在保存前校验：

| 操作 | API |
|---|---|
| 列出/读取 | `GET /api/workflows`、`GET /api/workflows/{id}` |
| 创建/更新 | `POST /api/workflows`、`PUT /api/workflows/{id}` |
| 仅校验 | `POST /api/workflows/validate` |
| 删除 | `DELETE /api/workflows/{id}` |
| 创建 Task | `POST /api/workflows/{id}/tasks` |
| 启动 Task | `POST /api/workflows/{id}/tasks/{task_id}/start` |
| 停止 Task | `POST /api/workflows/{id}/tasks/{task_id}/stop` |

主会话中已有工具覆盖读取与 Task 生命周期：`list_workflows`、`get_workflow`、
`create_and_attach_task`、`set_workflow_variable`、`start_workflow_task`、
`get_task_status`、`get_task_result`、`read_task_artifact`、`get_node_messages`、`list_tasks`、
`approve_node`、`retry_node`、`skip_node`、`stop_task`。

Main 可以同时管理多个后台 Task。`main_session_id` 是所有权事实来源；会话上的
`workflow_id/task_id` 只是最近任务的兼容默认值。除发现类工具外，所有任务修改、启动、
审批、恢复和结果查询都应显式携带完整 TaskRef：`workflow_id + task_id`。只提供其中一个
会失败，其他 Main 的任务也不可操作。

Main 所有权与逐节点审批是两个独立契约。`create_and_attach_task` 的可选参数
`main_takeover` 默认 `false`：Main 可以持续跟踪任务，但 Agent 节点完成后正常自动流转。
只有显式设为 `true` 时，每个 Agent 节点的产出才进入 Main 审批；工作流中显式定义的
Approval 节点不受该参数影响。

HTTP 创建 Task 时可用 `node_model_overrides` 为指定 Agent 节点选择 Core 已配置的
Provider 与预定义模型：

```json
{
  "node_model_overrides": {
    "writer": "provider_id:model_name"
  }
}
```

节点 ID 必须存在且 `node_type=agent`，模型引用必须出现在 Core 当前模型列表中。选择结果会
写入 Task 的定义快照和运行身份守卫，因此重试与恢复继续使用同一模型；Workflow 模板不会
被修改。该接口不接收 API Key、Base URL、Provider 类型、模型参数或回退模型。

`get_task_status` 和 `get_task_result` 支持事件驱动等待：

- `wait_for=none`：立即返回，是兼容默认值。
- `wait_for=change`：已持久化 Task 快照变化或超时后返回。
- `wait_for=terminal_or_attention`：Task 完成、失败、停止、取消，或进入
  审批/未启动等需要 Main 介入的状态时返回。
- `timeout_seconds` 是最长等待时间；`null` 表示不设截止时间，但当前调用仍可取消。

等待结果通过 `wait_outcome` 区分 `changed`、`terminal`、
`attention_required` 与 `timeout`，并返回 `terminal`、`attention_required` 和
`elapsed_seconds`。状态事件只负责唤醒，工具会重新读取持久化 Task 快照。
对结果导向的等待优先直接使用 `get_task_result`，避免终态后再调用一次结果工具。

只有 API 不可用且任务明确要求直接维护资源时，才编辑
`data/workflows/{workflow_id}/definition.json`。直接编辑后必须运行：

```bash
python data/skills/workflow-guide/scripts/validate_definition.py data/workflows/{workflow_id}/definition.json
```

可用目录或 `--all` 代替单个文件。退出码 `0` 表示通过（可含 warning），`1` 表示存在
必须修复的 error。

## 定义结构

工作流目录由模板、内联脚本和引擎生成的运行记录组成：

```text
data/workflows/{workflow_id}/
├── definition.json
├── script/
├── tasks/
└── runs/
```

定义的核心字段是 `workflow_id`、`name`、`version`、`nodes`、`edges`、`gateways`、
`variables` 和 `execution_schemes`。普通节点不能有多条出边；分支必须使用网关。

### 节点类型

| `node_type` | 用途 | 关键字段 |
|---|---|---|
| `agent` | 创建 LLM 子会话 | `agent_type`、`first_message`、`output_variable`、`auto_flow` |
| `script` | 确定性 subprocess | `node_params.script_source/script_type/script_name/script_argv` |
| `approval` | 人工审批标记 | 通用节点字段 |
| `subprocess` | 调用另一个工作流 | `sub_workflow_id`、`sub_scheme_id`、`sub_workflow_params` |

Agent 节点的常用输出控制：

- `output_variable` 把最后回复写入运行时变量池。
- `save_output_to_file` 与 `output_file_path` 把最后回复保存到共享 workspace；两者可同时用。
- `require_non_empty_output=true` 要求最后一条 LLM 回复去除首尾空白后非空。
- `json_output_field` 与 `json_output_field_min_chars` 必须同时配置；前者支持
  `body`、`data.chapters.0.body` 形式的字段路径，目标必须是字符串，字数必须严格大于阈值。
  校验发生在变量赋值和文件写入前；失败统一进入节点的 `auto_retry_count` 策略。
- `auto_flow=true` 让 LLM 输出结束即成功，通常配合
  `enable_complete_node_task=false`。
- `enable_reject_upstream` 与 `max_reject_count` 允许下游有限次打回上游。
- `auto_retry_count`、`auto_retry_interval_seconds`、`fail_auto_skip` 是失败策略；必须显式评估
  重复副作用后再启用。

Script 节点新定义使用 `script_argv` 字符串数组，不使用兼容字段 `script_args`。脚本节点
的详细目录、输出协议和身份冻结规则见 `script-library-guide`。

## 变量与共享 workspace

输入变量支持 `text`、`textarea`、`select`、`file`、`list`、`dict`。变量 key 不得以 `_`
开头；该前缀保留给系统变量。

常用引用形式：

- `{{key}}`
- `{{list_var[0]}}` 或 `{{list_var[index_var]}}`
- `{{dict_var.key}}`

`list` 与 `dict` 的值必须是合法 JSON，不能使用 Python 单引号表示。运行时变量可来自：

- Task 创建或 `set_workflow_variable` 填入的输入值；
- Agent 节点 `output_variable`；
- Script stdout 中的 `<WF_VAR>key:value</WF_VAR>`；
- 声明为 `source_type: output` 的节点产出变量。

同一个 Task 内的 Agent 和 Script 节点共享 workspace。通过 Chat Main 创建时，默认
`workspace_mode=task_isolated`，路径位于
`data/workspaces/_main/{session_id}/tasks/{task_id}/`；需要多个 Task 共享资料时，显式使用
`named_shared` 与安全的 `workspace_ref`。`legacy_shared` 保留
`data/workspaces/{workflow_id}/` 兼容行为。相对文件路径均基于实际 workspace，系统通过
以下变量暴露运行上下文：

| 系统变量 | 含义 |
|---|---|
| `_system.workspace_path` | 实际共享 workspace |
| `_system.workflow_id` | 工作流 ID |
| `_system.task_id` | Task ID |
| `_system.task_name` | Task 名称 |
| `_system.current_time` | 每节点重新计算的 ISO 时间 |
| `_system.operator` | 当前执行人标识 |

## 网关与执行方案

| `gateway_type` | 约束 |
|---|---|
| `parallel` | 至少两条出边，必须有对应 `converge` |
| `converge` | 至少两条入边，恰好一条出边 |
| `condition` | 至少两条出边，非默认边有表达式，至少一条默认边 |
| `loop` | 恰好两条出边：循环体与默认退出边；不支持嵌套循环 |

条件表达式支持 `==`、`!=`、`>=`、`<=`、`>`、`<` 与 `contains`。Loop 常用表达式是
`for item in items`、`for key, value in config`、`for i in range(5)`。

执行方案只保存 `selected_node_ids`。创建 Task 时，`selected_node_ids` 优先于 `scheme_id`，
`disabled_node_ids` 仅用于兼容旧调用。子流程通过 `sub_scheme_id` 选择目标工作流方案。

## Task 安全顺序

```text
create_and_attach_task（按需显式 main_takeover=true，默认只跟踪）
  -> 保存返回的 workflow_id + task_id
  -> set_workflow_variable（显式 TaskRef，必要时重复）
  -> start_workflow_task（显式 TaskRef，后台执行）
  -> get_task_status（必要时 wait_for=change）
  -> approve_node / retry_node / skip_node（显式 TaskRef + 最新 attempt_count）
  -> get_task_result（可 wait_for=terminal_or_attention）
  -> 必要时 read_task_artifact 或 stop_task
```

启动前检查所有 `required` 输入和 file 路径。运行中不要修改 definition 并期待当前 Task
变化；需要新定义时创建新 Task。一个 Main 可继续创建其他 Task，旧 Task 不会被解绑或
停止。Agent 节点可能产生审批请求，审批消息会提供完整 TaskRef 与 `attempt_count`；调用
控制工具时原样携带，过期操作会返回 `node_control_stale`。拒绝时提供可执行反馈。

## 验收清单

- 模板 API 校验通过，或直接编辑后校验脚本返回 0。
- START 到 END 完整可达，无孤立节点、悬空边或重复 ID。
- 节点位置可读，变量均已定义或明确由上游产出。
- Agent 类型、Prompt 模板和 Script Library 身份真实存在。
- 新建 Task 使用了最新模板快照，启动后状态与节点摘要可查询。
- 同一 Main 的多个 Task 可独立寻址，默认工作空间互不污染，其他 Main 不能越权控制。
- 终态 Task 可通过 `get_task_result` 返回节点摘要、公开输出和受控产物描述符。
- 失败策略不会把有外部副作用的节点静默重复执行。

## 常见故障定位

- 节点重叠：检查 `position`。
- `{{key}}` 保留原样：检查 Task 参数、上游输出和 key 拼写。
- definition 更新未生效：当前 Task 使用旧快照，重新创建 Task。
- Main 所属任务在每个 Agent 后等待：检查 Task 的 `main_takeover` 是否被显式启用；默认值应为
  `false`，显式 Approval 节点除外。
- file 变量为空或失败：检查实际 workspace、路径和 `required`。
- Loop 失败：检查 JSON 值、两条出边、默认退出边与循环表达式。
- 并行保存失败：检查 parallel/converge 配对和嵌套限制。
- Prompt section 变量未渲染：加载 `prompt-template-guide` 检查系统变量或
  `template_variables` 声明。
