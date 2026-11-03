# 安装与使用

WorkBuddy 话题标题自动命名技能。把会话标题从「首轮一次性生成」变成**跟随工作目标持续更新**。

---

## 一、安装

把整个 `topic-auto-title/` 目录放到 user-level 技能目录：

```
~/.workbuddy/skills/topic-auto-title/
```

Windows 上即 `C:\Users\<你的用户名>\.workbuddy\skills\topic-auto-title\`。

放好后**重启 WorkBuddy**（或等热重载生效）。技能会被自动发现，无需其它注册步骤。

### 目录结构

```
topic-auto-title/
├── SKILL.md                        # 技能主文档（触发词、命名规范、命令）
├── README.md                       # 本文件
├── references/
│   └── workbuddy-internals.md      # 内部机制与排障（实现依据）
├── scripts/
│   └── title.py                    # 全部功能实现（单文件，无第三方依赖）
└── hooks/
    └── entry.sh                    # Hook 兼容层（可选，见下）
```

**唯一运行期依赖是一个 Python 3 解释器。** WorkBuddy 自带的受管运行时即可，
不需要 `pip install` 任何东西。

---

## 二、快速开始

不用配 Hook 也能直接用。对助手说「**整理标题**」或「**更新标题**」即可。

想开自动提醒（每 N 轮自动判断是否需要改名），执行一次：

```bash
python3 -X utf8 "<技能目录>/scripts/title.py" install-hook
```

> Windows 上如果 `python3` 报错，改用解释器绝对路径，例如：
> `"C:/Users/<你>/.workbuddy/binaries/python/versions/<版本>/python.exe" -X utf8 "<技能目录>/scripts/title.py" install-hook`

该命令会：
1. 自动探测一个**真能执行**的 Python 解释器（会实际运行一次来验证，不只看 `which`）
2. 把 Hook 写入 `~/.workbuddy/settings.json`（合并写入，**不会**覆盖你已有的其它配置）
3. 注册 `Stop` 与 `UserPromptSubmit` 两个事件

验证：

```bash
python3 -X utf8 "<技能目录>/scripts/title.py" status
```

看这几个字段：
- `hook_config.effective` 为 `true` → Hook 已生效
- `hook_config.interpreter_ok` 为 `true` → 注册的解释器可用
- `hook.triggered` 为 `true` → Hook 已经被真实调用过

---

## 三、命名规范

统一格式 **`<类别emoji> <对象>｜<目标>`**，4–48 字。

| 类别 | 用途 |
|---|---|
| 🎬 | 内容制作 |
| 🧩 | 工具开发 |
| 🔎 | 对比调研 |
| 📅 | 计划排期 |
| 🎨 | 页面设计 |
| ⚙️ | 运维配置 |
| 💬 | 沟通协作 |
| 📝 | 方法整理 |

例：`🧩 插件安装｜载荷校验`、`🎬 图像模型评测｜视频策划`

对象放在前面（可辨识的名词），省略外层项目名；只在工作目标**实质变化**时更新，
「继续」「再改一下」这类词不取代主线。

---

## 四、常用命令

`<入口>` = `<技能目录>/scripts/title.py` 的绝对路径。

| 命令 | 作用 |
|---|---|
| `poll --compact` | 列出需要改名的会话（只读，不写入） |
| `poll --all --compact` | 覆盖全部未删除会话 |
| `context` | 取某个会话的命名输入 |
| `apply --title "<新标题>"` | 写回标题 |
| `status` | 看配置、Hook 状态、解释器自检 |
| `install-hook` / `uninstall-hook` | 注册 / 移除 Hook（幂等） |
| `config --every-n-turns N` | 改提醒频率（默认 3 轮） |
| `lock` / `pause` / `resume` | 锁定标题 / 暂停 / 恢复自动命名 |

---

## 五、排障

### Hook 配了但没反应

**按顺序查，不要一上来就怀疑配置：**

1. **先看解释器能不能跑** —— `status` 里 `hook_config.interpreter_ok`。
   如果是 `false`，多半是 `python3` 命中了 Windows 的
   **Microsoft Store 应用别名桩**（`WindowsApps\python3.exe`），
   非交互执行必然退出码 49，脚本一个字都不跑。
   → 重跑 `install-hook`，它会写入绝对路径。

2. **再算轮次阈值** —— `turns - 上次命名的轮次` 是否 ≥ `every_n_turns`。
   不够时脚本会**静默返回 `{}`**，这是正常行为，不是故障。

3. **一次收到两份相同反馈 = 重复注册**。多见于早期把脚本副本放在某个工作区
   （`<工作区>/export/scripts/title.py`），那份注册项与正式注册**同时执行**。
   → 重跑 `install-hook` 即可清理；它的输出里 `duplicates` 非空表示查到过重复。

4. **看宿主的真实执行日志**（比什么都准）：
   ```
   ~/.workbuddy/logs/<日期>/<会话名>__<hash>.log
   ```
   注意**不在** `main.log` 里。搜：
   ```bash
   grep -aE "\[HookExecutor\]|executeStopHooks" <该会话日志>
   ```
   看到 `[HookExecutor] abnormal exit` 就是命令级失败。

### 为什么「我在终端里跑得通」不代表 Hook 跑得通

Agent 的终端环境有沙箱注入的 PATH，Hook 的执行环境**没有**。
两者对 `python3` 的解析结果可能完全不同 —— 这是本技能开发中踩过的最深的坑。
凡是写进配置交给宿主执行的命令，一律用**绝对路径**。

反向也不成立：终端里若报 `dirname` / `head` / `ls`: command not found（PATH 为空），
**用解释器绝对路径调用 Python 依然成功**，那只是 shell 工具链缺 PATH，
不代表脚本本身有问题。

更多机制细节见 `references/workbuddy-internals.md`。

---

## 六、卸载

```bash
python3 -X utf8 "<入口>" uninstall-hook   # 移除 Hook（保留其它工具的配置）
```

然后删除 `~/.workbuddy/skills/topic-auto-title/` 目录即可。
数据目录 `~/.workbuddy/topic-title/` 可一并删除（只存本技能的状态与日志）。

---

## 七、说明

- 本技能**只读写 WorkBuddy 自己的数据**：会话转写、`workbuddy.db`、本地状态目录。
  不依赖、不联网、不上报任何内容。
- 标题写入的是 `sessions.custom_title` 字段（引擎保护字段，不会被运行中的引擎回写覆盖）。
- 自动提醒走 **`Stop` 事件** —— 桌面端实测普通用户消息不执行 `UserPromptSubmit`，
  但 `Stop` 在每次回答结束时必定触发。
