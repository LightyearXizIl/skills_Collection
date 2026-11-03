---
name: skill-rule-authoring-guide
description: >-
  创建、更新、修补、删除、分组或排查 DeterminFlow Skill 与 Rule 时必须加载此技能；也适用于判断知识应进入 Skill、强制约束应进入 Rule、运行时 data/skills 与版本化 Core Skills 的边界、Plugin 只读资源以及幽灵配置清理。
metadata:
  display_name: skill-rule-authoring-guide
  version: 1.0.0
  author: system
  category: general
  priority: 50
  workflow_only: false
---

# Skill 与 Rule 编写指南

## 先做存储判断

| 内容 | 目标 |
|---|---|
| 可复用的操作步骤、领域方法、检查清单 | Skill |
| 每次都必须遵守的简短行为约束 | Rule |
| Agent 的身份、工具和模型边界 | Agent Definition |
| 通用 system prompt 结构 | Prompt Template |
| 一次性事实或项目临时说明 | 不创建 Skill/Rule |

不要把同一要求同时复制到 Skill、Rule 和 Prompt。Rule 说明“必须/禁止什么”，Skill 说明
“在某类任务中怎样做”。

## 三层资源边界

1. `src/core/defaults/skills/` 是随 Core 源码和发行版发布的通用版本化 Skills。
2. `data/skills/` 与 `data/rules/` 是当前实例的可写运行时资源。
3. Plugin bundle 提供的 Skills/Rules 是带 owner 的只读资源；修改它们要回到 Plugin 源码。

Core 启动会把未被用户定制的版本化 Skill 同步到 `data/skills/`。一旦运行时副本被修改，
同步器会保留定制内容，不再覆盖。`skill_manage` 只管理运行时 `data/skills/`，不会把修改
自动回写到 `src/core/defaults/skills/`。

因此：

- 普通用户或实例级资源使用管理工具。
- 随 Core 发版的 Skill 必须修改版本化源、增加测试，再执行 provisioning（供应同步）。
- Rule 当前只有运行时与 Plugin 层，不要虚构 `src/core/defaults/rules/`。

## Skill 格式

每个 Skill 是目录中的 `SKILL.md`：

```text
skill-name/
├── SKILL.md
├── scripts/
├── references/
└── assets/
```

目录名和 frontmatter `name` 使用相同 kebab-case（短横线命名），只能包含小写字母、数字和
单个连字符。最小 frontmatter：

```yaml
---
name: example-guide
description: 在什么任务、操作和故障场景下必须加载，以及它解决什么问题。
---
```

Description 是发现入口，必须包含触发条件；不要把“何时使用”只写在 body。Body 使用
祈使句，给出必要顺序、决策点、验证和常见失败。SKILL.md 保持聚焦，详细资料放
`references/`，确定性重复操作放 `scripts/`。

## Rule 格式

Rule 位于 `data/rules/{rule-id}/RULE.md`，最小 frontmatter 包含 `name` 与
`description`，body 只写可判断、可执行的约束。规则应满足：

- 能明确判断是否违反；
- 适用范围与例外清楚；
- 不重复上层系统约束；
- 不把长流程或教学说明塞入 Rule。

## 使用管理工具

读取使用 `get_skills`、`get_rules`。修改使用专用工具，不直接编辑运行时目录：

| 资源 | CRUD | 分组 |
|---|---|---|
| Skill | `skill_manage` | `skill_group_manage` |
| Rule | `rule_manage` | `rule_group_manage` |

Skill actions：`create`、`edit`、`patch`、`delete`、`write_file`、`remove_file`。
Rule actions：`create`、`edit`、`patch`、`delete`。优先用 `patch` 做唯一的精确替换；找不到
或匹配多处时先重新读取，不要盲目改用整文件覆盖。

创建和删除是结构变化，先确认目标与影响。Plugin 资源标记为只读时停止，定位它的 owner
和源仓库。

## 配置一致性

`config/skills_config.json` 与 `config/rules_config.json` 只应引用真实存在的资源 ID。
Skills 配置同时有 `skill_configs`（启用、优先级、自动注入、Workflow 范围）和 `skills`
（分组等兼容配置）；修改自动注入时两处要一致。

删除资源后清理两处配置和 Prompt 中的显式引用。目录不存在但配置仍存在是幽灵配置，
不会恢复内容，还会误导 UI 与 Prompt。

自动注入有固定 token 成本。只有每次会话都需要的短 Core 协议才默认开启；其余依赖
description 发现并按需用 `get_skills` 加载。

## 安全与质量检查

1. frontmatter 可解析，name 与目录一致，description 不超过系统限制。
2. 不包含 Secret、私钥、凭据、用户数据或危险的隐式执行指令。
3. 引用的工具名、API、路径与当前代码一致。
4. 示例命令限定目标，不使用宽泛破坏性操作。
5. Skill 支撑文件只放在 `scripts/`、`references/`、`assets/`。
6. 运行 Skill validator，并让运行时 loader 实际加载。
7. 对版本化 Core Skills，验证 provisioning 后 API 列表与白名单完全一致。

## 验收清单

- `get_skills` 或 `get_rules` 能读取新内容。
- 启用状态、自动注入、Workflow 范围和分组符合预期。
- Plugin 资源没有被运行时副本遮蔽或产生同 ID 冲突。
- 配置中没有不存在的 ID，Prompt 中没有旧 Skill 引用。
- 版本化 Core Skill 已同步到全新临时 `data/skills` 并通过 loader。
- 删除操作后 API、配置、目录和调用方引用均已清理。
