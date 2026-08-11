---
name: script-library-guide
description: >-
  创建、更新、删除、引用或排查 DeterminFlow Script Library 脚本时必须加载此技能；也适用于 Workflow Script 节点、inline 与 library 选择、SCRIPT.md、script_argv、共享 workspace、WF_VAR/script_out 输出协议、Plugin 脚本 owner 冲突与 Task 身份冻结。
metadata:
  display_name: script-library-guide
  version: 1.0.0
  author: system
  category: workflow
  priority: 50
  workflow_only: false
---

# Script Library 指南

## 何时用 inline，何时用 library

- 只服务一个 Workflow、与模板一起演进的脚本使用 `inline`，位于
  `data/workflows/{workflow_id}/script/{name}.{sh|py}`。
- 被多个 Workflow 复用、需要独立说明的脚本使用 `library`，实例可写目录是
  `data/script-library/{group}/{name}/`。
- Plugin 可提供只读 Script Library roots；修改它们必须回到 Plugin 源码。

涉及完整 Workflow 拓扑、变量和 Task 生命周期时同时加载 `workflow-guide`。

## 目录与身份

```text
data/script-library/{group}/{name}/
├── {name}.sh        # 或 {name}.py，二选一
└── SCRIPT.md        # 推荐：说明用途、输入、输出、副作用和版本
```

`group` 与 `name` 只使用字母、数字、下划线或连字符。入口文件名必须与脚本目录名一致。
同一个 `{group}/{name}` 只能有一个 active owner；用户资源与 Plugin 资源重名会 fail closed，
不会按优先级静默覆盖。

Task 创建时会冻结 library 脚本的 owner、revision 与文件摘要。执行前再次核验；脚本或
Plugin revision 漂移时拒绝执行。因此更新脚本后要创建新 Task，不能期待旧 Task 自动采用
新内容。

## Script 节点配置

新节点使用数组形式 `script_argv`：

```json
{
  "node_type": "script",
  "node_params": {
    "script_source": "library",
    "script_type": "python",
    "script_group": "utils",
    "script_name": "normalize",
    "script_argv": ["--input", "{{source_file}}", "--mode", "strict"],
    "timeout": "300"
  }
}
```

- `script_source` 是 `inline` 或 `library`。
- `script_type` 是 `shell` 或 `python`，必须与真实入口一致。
- `script_group` 仅在 library 模式必需。
- `script_argv` 每项是一个完整 argv，变量中的空格、引号和 JSON 不会被 Shell 再拆分。
- `script_args` 只兼容历史定义，新建和修改不要使用。
- `timeout` 是正整数秒；根据真实最坏耗时设置，不用无限超时掩盖卡死。

引擎直接以 argv 启动，不经过 Shell。执行工作目录是 Workflow 共享 workspace。环境变量
包括 `WORKFLOW_ID`、`TASK_ID`、`SCRIPT_DIR`、`WORKSPACE_DIR`；Plugin owner 还可提供其
声明的运行环境。

## 输出协议

脚本通过 stdout 与 Workflow 交换结构化结果：

```text
<WF_VAR>result_key:value</WF_VAR>
<script_out>给节点历史与下游摘要使用的短说明</script_out>
```

- 标签大小写必须完全一致。
- 每个 `WF_VAR` 的 key 使用稳定变量名；list/dict 值输出合法 JSON 双引号格式。
- 业务日志不要伪造协议标签。
- stdout/stderr 会截断，长产物写入共享 workspace，只输出路径与摘要。
- 退出码非 0、超时、入口缺失、身份漂移或协议解析错误都应视为节点失败。

## 管理 API

| 操作 | API |
|---|---|
| 列分组 | `GET /api/workflows/script-library/groups` |
| 列脚本 | `GET /api/workflows/script-library/scripts?group={group}` |
| 读/写脚本 | `GET/PUT /api/workflows/script-library/{group}/{name}/script?type={type}` |
| 读/写说明 | `GET/PUT /api/workflows/script-library/{group}/{name}/meta` |
| 删除脚本 | `DELETE /api/workflows/script-library/{group}/{name}` |
| 删除空分组 | `DELETE /api/workflows/script-library/{group}` |

写 API 只写用户 root。读取 API 可解析 active user/Plugin roots。不要用 API 修改只读 Plugin
脚本；同名冲突时先解决 owner 边界。

## SCRIPT.md 内容

说明至少包含：

- 脚本用途和不适用场景；
- `script_type`、argv 参数和必需环境变量；
- 读取与写入的 workspace 路径；
- `WF_VAR` 与 `script_out` 输出；
- 外部副作用、幂等性和重试风险；
- version 与 owner。

不要在说明或脚本中写 Secret；通过受控环境注入。

## 验证顺序

1. 列出 catalog，确认 owner、group、name 与 type 唯一且正确。
2. 在隔离 workspace 直接运行脚本，覆盖正常输入、空输入与错误输入。
3. 检查退出码、stdout 协议、stderr 和产物路径。
4. 创建新 Workflow Task，确认创建时身份冻结成功。
5. 运行 Script 节点，核对变量池、节点 summary 和下游消费。
6. 有副作用的脚本验证幂等性；不幂等时禁用自动重试或增加显式保护。

## 常见错误

- 目录叫 `hello-world`，入口却叫 `hello_world.sh`：入口必须与目录名相同。
- library 节点没填 `script_group`：解析失败。
- 更新脚本后运行旧 Task：身份守卫因漂移拒绝执行。
- 把 JSON 放进 `script_args`：Shell 拆分破坏参数，改用 `script_argv`。
- 从脚本目录写相对产物：当前工作目录是共享 workspace，不是 `SCRIPT_DIR`。
- 用户与 Plugin 定义同 ID：catalog 冲突，必须改名或停用 owner。
