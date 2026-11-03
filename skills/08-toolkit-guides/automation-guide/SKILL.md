---
name: automation-guide
description: >-
  创建、查看、更新、暂停、恢复、立即运行、删除或排查 DeterminFlow Cron 自动化任务时必须加载此技能；也适用于 once/interval/cron 调度、时区、Agent 类型与权限、重复次数、静默输出、失败重试和历史输出核验。
metadata:
  display_name: automation-guide
  version: 1.0.0
  author: system
  category: workflow
  priority: 50
  workflow_only: false
---

# Cron 自动化指南

## 核心边界

Cron Job 是按计划启动一次独立 Agent 运行的自动化，不是 Workflow 节点调度器。Job 的
`prompt` 必须自包含，不能依赖创建它的聊天上下文。如果自动化要操作 Workflow，所选
`agent_type` 必须拥有对应工具，并在 prompt 中写明工作流 ID、输入、成功条件与停止条件。

涉及 Agent 权限时加载 `agent-definition-guide`；涉及工作流运行时加载
`workflow-guide`。

## 创建前检查

1. 先调用 `cronjob(action='status')` 与 `cronjob(action='list')`，避免重复任务。
2. 用 `list_agent_types` 确认 `agent_type` 存在并拥有完成任务所需的最小工具。
3. 明确调度时区、首次执行时间、是否允许重复、停止条件与空结果语义。
4. 评估外部写入、消息发送、付费模型和非幂等操作的重复执行风险。
5. Prompt 写入稳定 ID 和路径，不依赖“上次”“这个项目”等对话指代。

## `cronjob` 工具

| action | 必需字段 | 用途 |
|---|---|---|
| `status` | 无 | 调度器状态 |
| `list` | 无 | 列出 Job |
| `get` | `job_id` | 读取完整 Job 与 prompt |
| `create` | `schedule`、`prompt` | 创建并启用 Job |
| `update` | `job_id` | 更新白名单字段或 schedule |
| `pause` / `resume` | `job_id` | 暂停或恢复 |
| `run` | `job_id` | 立即触发一次 |
| `output` | `job_id` | 列输出；加 `filename` 读取内容 |
| `remove` | `job_id` | 删除 Job |

创建和更新可使用 `name`、`agent_type`、`silent_on_empty`、`model_override`、`max_turns`、
`repeat`。更新还可设置 `enabled`。`repeat=null` 表示不限次数；周期任务没有明确持续价值时
不要使用无限重复。

## 调度格式

```text
once:2026-08-04T09:00:00+08:00
interval:60
cron:0 9 * * *
```

- `once` 使用带时区的 ISO 8601 时间，避免本地时间歧义。
- `interval` 的值是整数分钟。
- `cron` 使用标准五段表达式；系统会用 croniter 校验。
- 修改 schedule 后重新读取 Job，确认 `next_run_at` 符合预期。

## Prompt 设计

一个可运行的自动化 Prompt 应包含：

1. 精确目标和在范围内的资源。
2. 读取顺序与允许使用的现有能力。
3. 成功、无变化、失败分别如何处理。
4. 不得执行的外部副作用或删除操作。
5. 输出格式和保存位置。
6. 对重复执行的幂等策略。

`silent_on_empty=true` 时，无新内容的 Agent 应按运行契约返回 `[SILENT]`，系统不保存空
结果。不要用静默模式隐藏错误；真正失败要产生可诊断输出。

## 安全操作顺序

```text
status/list
  -> create
  -> get（核对 schedule、prompt、agent_type、repeat）
  -> run（低风险代表性任务可手动冒烟）
  -> output（核验真实产物）
  -> 保持启用，或 pause 后修正
```

修改已有 Job 时先 `get` 保存当前契约，只更新必要字段，再次 `get`。`run` 是实际执行，
会产生模型成本和业务副作用；只有用户授权的任务才能触发。删除前先 pause，并确认不再
需要历史引用。

## 验收清单

- schedule 可解析，时区和 `next_run_at` 正确。
- `agent_type` 存在，工具权限足够且不过宽。
- Prompt 不依赖聊天上下文，目标、边界和输出完整。
- `repeat`、`silent_on_empty`、`max_turns` 和模型成本符合预期。
- 代表性运行产生新鲜 output；健康状态或配置存在不等于执行成功。
- 重复运行不会重复创建不可恢复资源，或已有幂等键/去重机制。

## 常见错误

- 使用不带时区的 `once`：执行时间解释不明确。
- 默认 `researcher` 没有所需写工具：先选择或设计正确 Agent Definition。
- 只看 Job `enabled=true` 就宣称自动化成功：必须检查运行状态与新 output。
- `interval` 任务没有 repeat 或停止条件：会无限消耗资源。
- Prompt 写“继续上次任务”：独立运行拿不到原聊天上下文。
- 非幂等任务失败后盲目 `run`：先确认上次是否已产生部分副作用。
