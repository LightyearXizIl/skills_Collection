# WorkBuddy 内部结构速查（实现与排障依据）

> 均为 2026-09-16 在本机的实测结论。改动本技能实现前先读这里。

## 会话标题

- **唯一真源**：`~/.workbuddy/workbuddy.db`（SQLite）的 `sessions` 表。
  - `title` — 自动生成的标题
  - `custom_title` — 用户改名专用标题（非空时优先显示）
  - 其它相关字段：`id`、`cwd`、`status`、`created_at`、`updated_at`、`last_activity_at`
- 标题**没有第二处存储**：`~/.workbuddy/storage/**`、`local_storage/**`、`workspace/sessions/**` 都不含标题
  （`workspace/sessions/<id>/` 下只有 `modify_backup` / `.modify_backup_meta` / `snapfile`，是文件变更回滚快照，与标题无关）。
- 自带标题生成是**一次性**的：会话转写里只有一条 `type: "ai-title"` 事件，首轮生成后不再更新。

### 两个必须知道的写入陷阱（实测踩过）

1. **运行中的引擎会用内存里的会话行回写数据库**，把外部改的 `title` 覆盖回旧值。
   实测：批量改名后，5 个非活跃会话保住了新标题，而**当前活跃会话的 `title` 被改回了首轮标题**。
2. **`custom_title` 是受保护字段**：它是用户改名（`/rename`）的落点，引擎回写不会覆盖它，且读取/展示优先取它。

→ 因此 `write_title()` **同时写 `title` 和 `custom_title`**，并以 `custom_title` 的读回结果作为核验依据。
只写 `title` 的做法对活跃会话必然失败。

### 界面显示：列表从数据库读，但只在被拉取时

- 列表真源确认：daemon 的 **`[listSessions][RPC] returning N records`**（daemon.log）返回的就是数据库里的
  `name`（= `custom_title` 优先）。**它每次都是现读数据库，不是内存缓存。**
  实测样本（2026-09-16 14:14:06）：返回的 `name` 已是技能刚写入的新标题。
- 因此「改完看不到」的原因不是 daemon 缓存，而是**渲染进程没有重新拉取**：今天全天 `listSessions` 只被调用 6 次
  （10:56、13:59、14:14，每次成对出现），**不是定时轮询**，属按需触发（打开任务列表 / 切换工作区 / 应用启动）。
- 渲染进程侧有 `CT.store.session notify` 与 `ipc.push.wb-event.*` 推送通道（`TaskChatList` 组件消费），
  但这些 IPC 只能由主进程发出，外部脚本无法触发。
- 官方能主动推送的通道是 `POST /api/v1/sessions/:id/rename`，但本机该服务 `authEnabled: true`；
  在 `settings.json` / `local_storage`（解压后）等处都**没有**找到可用凭据 → 走不通。

**结论**：数据层可即时写入（`custom_title`），界面层**无法做到无感实时推送**；让用户**重新拉取一次列表**
（打开任务列表 / 切工作区 / 重启）即可看到，通常不必重启。对外说明时不要承诺"实时"，也不要断言"必须重启"。

## 删除会话的语义

- 宿主删除会话是**软删除**：只把 `sessions.deleted_at` 置为当前毫秒时间戳，行仍保留（本机 7 个已删会话都在库里）。
- 因此自动清理也应当只写 `deleted_at`，与宿主语义一致、可恢复，且不碰标题与其它字段。
- 排查/统计时必须以 `where deleted_at is null` 过滤，否则会把历史自动化会话也算进来。
  （实测：不过滤会看到早已"删除"的每日新闻推送会话，容易误判。）

## 会话转写

- 路径：`~/.workbuddy/projects/<slug>/<sessionId>.jsonl`
  - `<slug>` = 工作目录路径把非字母数字字符替换成 `-`
    （例：`c:\Users\EDY\WorkBuddy\2026-09-16-13-04-06` → `c-Users-EDY-WorkBuddy-2026-09-16-13-04-06`）
- 逐行 JSON，`type` 取值：
  - `message` — `role: "user"` 的内容项是 `input_text`；`role: "assistant"` 是 `output_text`
  - `reasoning` / `function_call` / `function_call_result` / `file-history-snapshot` / `ai-title` — 命名时跳过
- 同目录另有 `<sessionId>.meta.json`、`<sessionId>.file-rollback.ndjson`，与本技能无关

## Hook 系统

### 配置位置（已从源码确认，两处都读）

**纠正**：先前判断「桌面端只读 `~/.workbuddy/settings.json`、不读 `~/.codebuddy`」——**这个结论是错的**。
从 `cli/dist/codebuddy-headless.js` 提取到的配置搜索路径原文：

```js
"~/.codebuddy/settings.json", "~/.codebuddy/settings.local.json",
"~/.workbuddy/settings.json", "~/.workbuddy/settings.local.json",
".codebuddy/settings.json", ".codebuddy/settings.local.json"
```

**两处都会读取。** 所以 Hook 不触发的原因**不是路径问题**。
（`~/.workbuddy/settings.json` 是桌面端主配置，字段更全；两处写一处即可，写两处会重复执行。）

### Hook 的实际加载与执行链路（源码依据）

```js
// 1. 取配置：settingsManager.get("hooks") → hooks["UserPromptSubmit"]
async getHooks(eA){
  let eu = await this.settingsManager.get("hooks");
  if(eu){ let el = eu[eA]; el && ec.push(...el) }
  ...载入插件 hook + scoped hook
}

// 2. 执行入口：没有 hook 就直接返回
async executeUserPromptSubmitHooks(eA, el){
  if(!await this.hookManager.hasHooks(HookEvent.USER_PROMPT_SUBMIT)) return;
  ...
  let el = await this.hookManager.executeHooks(HookEvent.USER_PROMPT_SUBMIT, ep);
  if(el.hookSpecificOutput?.additionalContext)
    eA.hookContexts.userPromptSubmitContext = el.hookSpecificOutput.additionalContext;
}
```

**关键发现：源码中不存在 hook 的「审核/信任/快照」机制。**
搜索 `hookSnapshot` / `trustedHooks` / `approveHook` / `pendingHooks` 均无结果。
唯一的信任门 `allowUntrustedFrontmatterHooks` 只作用于 **frontmatter hooks**（写在 Agent/Skill 的
frontmatter 里的 hook），与 `settings.json` 里的 command hook **无关**。

→ 官方文档说的「Requires review in the `/hooks` panel」是 **CLI（CodeBuddy Code）的行为**，
桌面端这条链路里没有这道门。**不要把「未审核」当作 Hook 不触发的默认解释。**

### 怎么观测 Hook 到底有没有执行（2026-09-16 实测修正）

**先纠正一个曾经的错误结论。** 之前写过「执行链路日志是 `debug` 级别、默认关闭，
所以只能靠脚本自己留痕」。这只说对了一半 —— 真正的执行日志是
**`Info` 级别、默认可见**的，关键在于**要找对文件**：

```
~/.workbuddy/logs/2026-09-16/<会话名>__<hash>.log     ← Hook 执行日志在这里
~/.workbuddy/logs/main.log                            ← 这里搜不到，别浪费时间
```

Hook 的执行日志是**按会话分文件**的（`logs/<日期>/<标题>__<hash>.log`），
不在全局 `main.log` / `daemon.log` 里。全局文件里只有 `[conversation-runtime] hook timing`
这类**同名的、完全无关的**插件 hook 计时记录（那是 `resolveCommand`/`beforePrompt`，
不是事件 hook），很容易混淆。

正确做法：先在 `logs/<日期>/` 下找到**当前会话**的日志文件，再搜这些关键字：

```bash
grep -aE "executeStopHooks|executeSessionStartHooks|executeFinalStopHooks|executeUserPromptSubmitHooks" <日志文件>
```

命中的行会直接告诉你**事件被调用了几次、用的什么命令、退出码是多少**：

```
[SessionHookManager] executeStopHooks sessionId=... stopHookActive=false stopReason=completed
[HookExecutor] spawn pid=26748 shell=.../bash.exe timeout=15000ms cmd=python3 -X utf8 ".../title.py" hook
[HookExecutor] abnormal exit pid=26748 code=49 elapsed=223ms timedOut=false
```

这三行就能定位「注册没生效 / 命令找不到 / 脚本内部出错」的全部区别 —— **比磁盘留痕更权威**。

**本机实测的各事件执行次数**（2026-09-16）：

| 事件 | 执行次数 |
|---|---|
| `FinalStop` | 33 |
| `Stop` | 11 |
| `SessionStart` | 6 |
| `UserPromptSubmit` | **0**（初始统计） |

→ 早期统计得出「桌面端只执行 `Stop`/`SessionStart`/`FinalStop`，`UserPromptSubmit` 从不执行」。
**后续验证修正了这个绝对结论**：当输入源是「系统注入的消息」（例如 Stop hook 自己触发的续跑）
而非普通用户消息时，`UserPromptSubmit` **会**被执行。实测同一时刻出现两条记录：

```
{"action":"injected","via":"stop"}
{"action":"injected","via":"user_prompt_submit"}
```

→ 准确表述：**普通用户消息提交时 `UserPromptSubmit` 不执行；系统注入类输入会执行。**
两者都不可靠地覆盖全部场景，因此**两个事件都注册才是正确策略**，互为保险。
`Stop` 是主力通道（普通交互必定触发），`UserPromptSubmit` 是补充。

脚本自己的 `logs/hook-runs.jsonl` 仍有价值 —— 它能区分「宿主调用了但脚本静默返回」
与「脚本内部抛错」，是分层排查的第二道依据。`via` 字段还能告诉你这次走的是哪个通道。


### 注入是有条件的，不满足就静默返回 {}

`hook` 子命令在下列任一情况直接返回 `{}`（这是正常行为，不是故障）：

| 条件 | 含义 |
|---|---|
| `enabled = false` | 被 `pause` |
| `emit_context = false` | 关闭了注入 |
| `state.locked = true` | 该会话被 `lock` |
| `turns < every_n_turns` | 会话轮次太少 |
| `turns - named_at_turn_count < every_n_turns` | **距上次命名不足 N 轮（最常见）** |

所以「Hook 配置好了但看不到注入」时，**先算这个差值**，再怀疑配置。

### 事件与注入格式

- 事件家族 27+，含 `Stop`、`UserPromptSubmit`、`SessionStart`、`PreToolUse`、`PostToolUse`、`PreCompact`
- **桌面端可用的注入通道是 `Stop`，不是 `UserPromptSubmit`。** 两者格式完全不同：

  `UserPromptSubmit`（桌面端不执行，仅为兼容其它宿主而挂）：
  ```json
  {"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"..."}}
  ```

  `Stop`（桌面端实际执行）：**不返回即可静默结束；返回 `decision:block` 会让本轮继续**，
  内容以 `Stop hook feedback: <reason>` 的形式喂回模型 —— 效果与注入等价：
  ```json
  {"decision":"block","reason":"..."}
  ```

  源码依据（`cli/dist/codebuddy-headless.js`）：
  ```js
  !el.allowed && el.message && el.blocking
    ? (eA.hookContexts.continueRequest = {message:{type:"message",role:"user",
        content:`Stop hook feedback: ${el.message}`, providerData:{isMeta:!0}}})
  ```

- **防无限循环**：Stop hook 触发续跑后，下一轮结束时会带上 `stop_hook_active: true`。
  脚本必须判这个字段并直接返回 `{}`，否则会自我递归。本技能已处理（`reason="stop_hook_active"`）。
- Hook 输入含 `session_id`、`transcript_path`、`cwd`、`permission_mode`、`hook_event_name`、`prompt`
- 配置结构：`{"hooks":{"<EventName>":[{"matcher":"<可选>","hooks":[{"type":"command","command":"...","timeout":15}]}]}}`
- **性能实测**：本技能的 hook 脚本单次执行 **0.21 秒**，远低于 15 秒超时，不存在超时风险。

## Windows 上的几个坑

1. **Hook 强制走 Git Bash（`bash.exe`），且 PATH 不可信 —— 必须用解释器绝对路径。**
   这一条曾经写错过，2026-09-16 用真实日志纠正：

   桌面端的 `HookExecutor` 是这么起进程的：
   ```
   [HookExecutor] spawn pid=26748 shell=.../PortableGit/versions/1.2.0/bin/bash.exe timeout=15000ms
                  cmd=python3 -X utf8 ".../title.py" hook
   [HookExecutor] abnormal exit pid=26748 code=49 elapsed=223ms timedOut=false
   Hook exited with non-blocking error code 49:
   Python was not found; run without arguments to install from the Microsoft Store,
   or disable this shortcut from Settings > Apps > Advanced app settings > App execution aliases.
   ```

   **结论：Hook 注册成功了、宿主也真的调用了，但 `python3` 在那个 shell 里命中了
   `%LOCALAPPDATA%\Microsoft\WindowsApps\python3.exe` —— 那是
   `AppInstallerPythonRedirector.exe` 的应用别名桩，非交互执行必然退出码 49，
   脚本一个字都没跑。** 这种失败在日志里表现为「Hook 没反应」，极容易被误判成配置问题。

   注意区分两个环境：
   - **Agent 的 Bash 工具环境**：通常有沙箱注入的受管 PATH，但**不保证**
     （2026-09-23 实测某会话 PATH 为空：shim 报 `line 3: dirname: command not found`，
     `head` / `ls` 等 coreutils 全部不可用）。此时**只要用解释器绝对路径调用 Python 依然成功**，
     坏掉的只是 shell 工具链。若确实需要 coreutils，先显式补 PATH：
     ```bash
     export PATH="/c/Windows/System32:/c/Windows:/usr/bin:/bin"
     ```
   - **HookExecutor 的 bash 环境**：没有这层注入，`python3` 会命中别名桩。
   ⇒ **不要用「我在 Bash 工具里跑得通」推断「Hook 里也跑得通」**，反向同理：
   「Bash 工具里 `head`/`ls` 报 command not found」**不代表** Python 调用会失败。

   → 正确做法：注册命令写**解释器绝对路径**，例如
   `"C:/Users/<user>/.workbuddy/binaries/python/versions/3.13.12/python.exe" -X utf8 "<脚本>" hook`。
   `install-hook` 会自动探测并写入（优先级：`TOPIC_TITLE_PYTHON` →
   当前解释器 `sys.executable` → 受管运行时 → PATH 候选，**每个候选都真跑一次验证**，
   不能只看 `which`）。`status` 会回报 `interpreter` / `interpreter_ok` / `hint` 做交叉验证。

2. **Python 需要 Windows 风格路径**。把 Git Bash 的 `/c/Users/...` 传给 Windows Python 会被解析成 `C:\c\Users\...`。
   → 用 `cygpath -m <posix-path>` 转成 `C:/Users/...` 再传参。
3. **中文 Windows 的 Python 默认按 GBK 输出**，`ensure_ascii=False` 的 JSON 会乱码。
   → 必须 `-X utf8` 或设 `PYTHONUTF8=1` / `PYTHONIOENCODING=utf-8`。
   实测：不设时整段乱码，但 **`json.loads` 仍能通过、不报错**，属于静默损坏，必须肉眼核对中文。
4. **重复注册会静默累积 —— `Stop` 每轮跑两遍，用户看到两份反馈。**
   2026-09-23 实测 `~/.workbuddy/settings.json` 里 `Stop` 与 `UserPromptSubmit` 各挂了
   **两条**命令：一条指向本技能 `scripts/title.py`，另一条指向某个早期工作区里的副本
   （`<工作区>/export/scripts/title.py`）。

   **根因**：旧的去重逻辑只认命令串里含 `topic-auto-title` 这个技能目录名，
   而那份副本的路径里根本没有该字符串 → 永远清不掉，`install-hook` 再跑多少次都留着。
   症状很有辨识度：一次触发收到**内容完全相同的两份** hook 反馈。

   **修复**：去重判定改为 `_is_our_hook()` —— 命令含 `topic-auto-title` **或**
   引用了名为 `title.py` 的脚本，两者皆判为「本技能的注册」。同时 `install-hook`
   的校验从「存在任意一条」收紧为「**规范命令**必须在位」，并在输出里回传
   `duplicates`（>1 条时列出），避免"只是历史副本还在"被误判成安装成功。
   清理方式：直接重跑 `install-hook`（幂等，会把历史副本一并剔除，其它工具配置不受影响）。

## 为什么写标题只能走数据库

| 通道 | 状态 |
|---|---|
| `POST /api/v1/sessions/:id/rename` | 存在，但本机服务 `authEnabled: true` 且未认证，后台进程不可用 |
| CLI | 无 rename 子命令 |
| `/rename` 斜杠命令 | 仅交互式会话内可用，Hook 无法调用 |
| 直写 `sessions.title` | ✅ 实测可写、可读回 |

写法：写前 `PRAGMA busy_timeout`，用 `update ... where id=?` 限定单行，写完立刻读回核验。
这属于绕过官方通道，WorkBuddy 未向 Hook 提供等价能力；不应顺手改其它字段。

## 探测本机服务的注意事项

- `curl` 在本机默认走系统代理，探测 `127.0.0.1` 必须加 `--noproxy '*'`，否则会得到误导性的连接失败。
- 活跃会话端点登记在 `~/.workbuddy/sessions/<pid>.json` 的 `url` / `endpoint` 字段。

## 定时任务（automation）的硬约束

- **调度最小粒度是 1 小时**。写入 `FREQ=MINUTELY;INTERVAL=3` 会被拒：
  `Unsupported RRULE frequency: MINUTELY. Supported frequencies are DAILY, HOURLY, WEEKLY, MONTHLY and YEARLY.`
  想"每 3 分钟"只能另找外部调度（Windows 计划任务 / 守护进程），不能靠错峰创建多个任务堆出来。
- **每运行一次就新建一个会话**（`automation_runs.thread_id` 形如 `automation-<id>:<ts>`），所以自动化必须自带清理。
- 排期字段落在 `automations` 表的 `rrule` / `next_run_at` / `last_run_at`；`deleted_at` 非空即软删除（`list` 不会显示）。
- `cwds` 决定自动化会话的工作目录，也决定了用 `cleanup --cwd` 能精准区分"自己的会话"和"用户的会话"。

## 为什么不用外部调度器代替

WorkBuddy 自带 CLI 可以独立运行（`node "<app>/resources/app.asar.unpacked/cli/bin/codebuddy" --version` → 正常输出 `2.137.1`），
但 `-p` **无头调用极重**：实测 **8 分 26 秒仍未产出任何输出**（启动即加载 MCP 服务，RSS 约 318MB）。
因此用外部进程"每 3 分钟检测 + 调 CLI 命名"不具可行性，不要朝这个方向设计。
（`schtasks` 本身可用，`/query` 输出为 GBK 编码，读取时要用 `errors="replace"`。）

## 踩坑：纯时间窗口的候选筛选必然漏会话

**症状**：某一个会话的标题栏长期不更新，且该会话的 `custom_title` 始终为 `NULL`。

**根因**：`sessions.updated_at` 是**最后一次活动时刻**，而水位 `last_poll_at` 记的是**上一轮轮询的执行时刻**。
候选条件 `updated_at > last_poll_at` 混用了两个不同步的时钟，于是：

```
上轮轮询 14:00 → 水位 = 14:00
会话创建 14:14 → 活动结束 14:16 → status = completed
下轮轮询 15:00 → 水位推到 15:00，该会话 updated_at(14:16) < 水位 → 永久出局
```

**只要会话的生命周期短于轮询间隔、且正好落在两次轮询之间，就必然漏掉，且不会自愈。**
日志侧的表现是：`state/` 下**没有**该会话的状态文件（它从未进入候选集，而不是被跳过）。

**修法**：候选筛选改为**双通道**，用与会话生命周期无关的判据兜底：

| 通道 | 条件 | 作用 |
|---|---|---|
| 时间窗口 | `updated_at > last_poll_at` | 捕捉有新活动的会话 |
| 补齐 | `custom_title is null or trim(...) = ''` | 捕捉从未命名过的会话 |

判据选 `custom_title` 而非 `title`，因为 `title` 会被引擎回写覆盖、可能残留旧值；
`custom_title` 只有本技能会写，为空就等价于"没命名过"。

补齐通道还必须**绕过 `every_n_turns` 轮次增量过滤**——它本就没有基线，
再要求"攒够 N 轮"会让只有 1~2 轮的短会话永远等不到命名时机。

对应开关：`poll --no-backfill` 可退回旧的纯窗口行为（排查用）；`poll --all` 仍用于全量重扫。

