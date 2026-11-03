---
name: topic-auto-title
description: WorkBuddy 话题标题自动命名。按固定「emoji 对象｜目标」规范持续更新当前会话标题，让任务列表一眼可辨；支持预览标题、写回标题、暂停/恢复自动命名、固定（锁定）标题、查看配置与 Hook 激活状态。触发词：话题自动命名、会话标题、改标题、更新标题、标题规范、整理标题、自动命名、标题锁定、暂停自动命名、topic title、auto title。仅用于 WorkBuddy 会话标题；不用于文章标题、视频标题、文件名重命名。
agent_created: true
---

# WorkBuddy 话题标题自动命名

把会话标题从「首轮一次性生成」变成**跟随工作目标持续更新**。

**自包含**：只读写 WorkBuddy 自己的数据（会话转写、`workbuddy.db`、本地状态目录），不依赖任何第三方应用。运行期只需要一个 Python 解释器 —— WorkBuddy 自带运行时即可。

## 为什么需要它

WorkBuddy 自带的标题生成是**一次性**的：会话转写里只有一条 `ai-title` 事件，首轮生成后永不更新。长会话跑偏后标题仍停留在第一句话，任务列表里就再也认不出来。本技能补的就是这个缺口。

## 命名规范（不可妥协）

统一格式：**`<类别emoji> <对象>｜<目标>`**，4–48 字。

- **类别固定 8 选 1**：🎬内容制作 · 🧩工具开发 · 🔎对比调研 · 📅计划排期 · 🎨页面设计 · ⚙️运维配置 · 💬沟通协作 · 📝方法整理
  同一个任务进入修改阶段也**不换类别**。
- **对象在前**：把「登录表单」「CRT 转场」这类可辨识名词放前面；默认省略外层已有的项目名。
- **名称稳定**：准确的对象名尽量不变；只在工作目标**实质变化**时更新；「继续」「推送」「再改一下」这类词不取代主线。
- **跟随主语言**：按最近几轮用户消息的语言命名，保留产品名；偶尔一句外语不来回切换。
- 禁止：标题含路径、链接、`@`、`sk-`、反引号、多余 emoji、控制字符。

正例：`🧩 插件安装｜载荷校验`、`🎬 图像模型评测｜视频策划`

## 三种触发方式

| 方式 | 是否需要额外配置 | 说明 |
|---|---|---|
| **① 直接调用（默认可用）** | 不需要 | 用户说「整理标题」「更新标题」时立即执行；你完成较大工作量、且工作目标已实质变化时，也可主动执行 |
| **② 定时任务轮询** | 已配置好，无需操作 | 「话题标题轮询整理」定时任务**每小时**（工作日）调用 `poll`，自动挑出需要改名的会话并写回。**这是真正的后台自动路径，不需要任何审批**。注意：官方调度**不支持分钟粒度**，最小就是 1 小时（实测 `FREQ=MINUTELY` 会被拒），想更快只能靠提高频率之外的办法 |
| **③ Hook 自动提醒** | 配置已就位，已实测跑通 | 挂在 **`Stop`** 事件上，每 N 轮把命名规范喂回模型。写入 `~/.workbuddy/settings.json`（`~/.codebuddy/settings.json` 同样会被读取，**写一处即可，写两处会重复执行**）。**源码确认桌面端无「审核」门**，配置对了就会生效。⚠️ 桌面端**普通用户消息不执行 `UserPromptSubmit`**，主力通道是 `Stop`（`SessionStart`/`FinalStop` 也执行）—— 详见 `references/workbuddy-internals.md` |

方式 ① 与 ② 不依赖任何审批，随时可用。方式 ③ 的配置已写入 `~/.workbuddy/settings.json`；用 `status` 看 `hook.triggered` / `hook_config.interpreter_ok` 判断它是否真的在跑。

**安装/维修 Hook 的命令**（合并写入，勿覆盖既有字段）：
```bash
python3 -X utf8 "<技能>/scripts/title.py" install-hook      # 写入或修复（幂等，自动探测解释器绝对路径）
python3 -X utf8 "<技能>/scripts/title.py" uninstall-hook    # 移除本技能的 hook
python3 -X utf8 "<技能>/scripts/title.py" config            # 看/改 every_n_turns 等
python3 -X utf8 "<技能>/scripts/title.py" status            # 看 hook.triggered 与解释器自检
```

**排查「Hook 不注入」的正确顺序**（2026-09-16 用真实执行日志重写过，按这个顺序走）：

1. **先看解释器能不能跑**。这是最隐蔽、也最容易被当成「配置没生效」的故障。
   `status` 看 `hook_config.interpreter_ok`：
   - `false` + `hint` 提到退出码 49 → 注册命令里的 `python3` 命中了
     Microsoft Store 的**应用别名桩**（`WindowsApps\python3.exe`），
     进程直接退出、脚本从未执行。**重跑 `install-hook` 写入绝对路径即可修复。**
2. **再算注入条件**：`turns - named_at_turn_count` 是否 ≥ `every_n_turns`。
   差值不够时 `hook` 会**静默返回 `{}`**，这是正常行为，不是故障。
3. **看宿主的真实执行日志**（比磁盘留痕权威）。日志在
   `~/.workbuddy/logs/<日期>/<会话名>__<hash>.log` —— **不在 `main.log`**：
   ```bash
   grep -aE "executeStopHooks|executeUserPromptSubmitHooks|\[HookExecutor\]" <该会话日志>
   ```
   能直接看到「调用了没有 / 用的什么命令 / 退出码多少」。`[HookExecutor] abnormal exit` 就是命令级失败。
4. 最后才怀疑配置位置与格式。

> ⚠️ **症状「一次触发收到两份一模一样的反馈」= 重复注册。**
> 早期把脚本副本放在别的工作区（`<工作区>/export/scripts/title.py`）时留下的注册项，
> 因路径不含技能目录名，旧去重逻辑清不掉，会与正式注册**同时执行**。
> 处理：重跑 `install-hook`（2026-09-23 起已能识别并剔除这类历史副本），
> 其输出里的 `duplicates` 非空即说明曾有重复。

> ⚠️ **不要用「我在 Bash 工具里跑得通」推断「Hook 里也跑得通」。**
> Agent 的 Bash 环境通常有沙箱注入的 PATH，HookExecutor 的 bash 环境没有。
> 两者对 `python3` 的解析结果不同 —— 这正是本技能曾经踩过的坑。
> 反向也不能推：Bash 工具里若报 `dirname` / `head` / `ls`: command not found（PATH 为空，
> 2026-09-23 实测出现过），**用解释器绝对路径调用 Python 仍然成功**；
> 需要 coreutils 时先 `export PATH="/c/Windows/System32:/c/Windows:/usr/bin:/bin"`。


## 操作

`<入口>` = 本技能 `scripts/title.py` 的绝对路径。
统一用 `python3 -X utf8 "<入口>"` —— 在 **Agent 的 Bash 环境**里 WorkBuddy 自带的受管运行时
已在 PATH 上（实测解析到 `~/.workbuddy/binaries/python/versions/<版本>/python3.exe`）。
若该环境没有 `python3`，改用受管解释器的绝对路径
（`"C:/Users/<用户>/.workbuddy/binaries/python/versions/<版本>/python.exe" -X utf8 "<入口>"`）。

> ⚠️ 这是**交互式调用**的写法。写进 **Hook 注册项**时**必须用绝对路径** ——
> Hook 的 bash 环境没有沙箱注入的 PATH，裸 `python3` 会命中应用别名桩而失败。
> `install-hook` 已自动处理，无需手工填写。

0. **`poll`** — 列出需要重新命名的会话，**不做任何写入**。
   - 默认走**双通道**筛选：① 时间窗口（上次轮询后有新活动）② **补齐**（`custom_title` 为空，即从未命名过）。
     补齐通道是必需的：时间窗口用「轮询时刻」当水位、会话用「最后活动时刻」，两个时钟不同步，
     生命周期短于轮询间隔的会话会掉进缝隙且**永久出局**（实测踩坑，详见 `references/workbuddy-internals.md`）。
     补齐通道不受轮次阈值限制，因此 1~2 轮的短会话也能被命名。
   - `--all`：忽略水位与阈值，覆盖**全部未删除会话**（含已归档）——用户说「整理标题」「全部会话」「整理所有标题」时用这个。
   - `--compact`：输出可读摘要而不是 JSON（含候选来源 `来源: window/backfill`），先看这个再决定改哪些，省上下文。
   - `--no-backfill`：退回纯时间窗口行为，仅用于排查。
   - 其他：`--max N` 限制候选数；`--dry-run` 不推进水位（`--all` 本来就只读）；`--include-self` 不排除当前工作目录的会话。
1. **`status`** — 看配置、数据目录、已记录会话数，**Hook 是否真的被触发过**（`hook.triggered` / `hook.last`），
   以及注册项里的解释器能否执行（`hook_config.interpreter_ok` / `hint`）。
2. **`context`** — 取出命名输入：`current_title`、`original_goal`、`recent_turns`、`turn_count`。
   默认取当前工作目录下最近的会话；用 `--session <id>` / `--cwd <路径>` 指定。
3. **判断是否需要更新** — 按上面的稳定规则比对 `current_title`。**不需要就明确说不需要**，不要为了动作而改名。
4. **`apply --title "🧩 对象｜目标" --reason "变化原因"`** — 自动校验格式、检查重名、写入并**读回核验**。
   返回 `renamed` / `unchanged` / `ambiguous_title` / `locked` / `disabled`。
5. **`ambiguous_title`** — 与已记录的其他会话标题重复，本次保留原名。用对话里真实的项目/模块/主题区分；无法区分就保留原名，**不要编造编号**。
6. **`lock --session <id>` / `unlock --session <id>`** — 固定或恢复某会话的自动命名。
7. **`pause` / `resume`** — 全局暂停/恢复。
8. **`cleanup --cwd <目录> [--keep-minutes 10] [--dry-run]`** — 软删除某目录下自动化产生的历史会话，防止任务列表被轮询会话堆满。只写 `deleted_at`，可恢复；默认保留最近 10 分钟内有活动的会话，因此不会删掉正在运行的那一轮。**用户自己的会话绝不能被清理**，务必用 `--cwd` 限定到自动化目录并先 `--dry-run` 核对。

## 「整理全部会话」的标准流程

用户说「整理标题」「全部会话」「整理所有标题」时：

1. `poll --all --compact` — 拿到全部会话的现标题、首轮目标、近期用户消息。**先看摘要**，不要逐个 `context`。
2. 逐个判断（这是本技能的核心，不要跳）：
   - 标题已是 `<emoji> <对象>｜<目标>` 且反映当前工作 → **保持不动**，并明确说出「保持」。
   - 标题是**原始首轮句、文件路径、微信/网盘路径、被截断的长句** → 一定要改。
   - 工作目标已实质变化 → 改；只多聊了几句 → 不改。
3. 信息不足时，对该会话单独跑 `context --session <id>` 补充判断依据，**不要猜**。
4. 逐个 `apply --session <id> --title "..." --reason "..."`。一次一个，便于定位失败。
5. 全部做完后复检一遍：读回 6 个未删除会话的标题，确认都符合格式，再向用户汇报改动清单。

## 硬性约束

- **只改标题字段**（`sessions.title` 与 `sessions.custom_title`），不触碰其它会话状态、不删改对话内容。
- **必须同时写 `custom_title`**：运行中的引擎会用内存里的会话行回写 `title`，会把外部改动覆盖回旧值（实测过）；`custom_title` 受引擎保护，是唯一稳定的落点。只写 `title` 对活跃会话必然失败。
- 用户在 WorkBuddy 里用 `/rename` 手工设过的标题同样落在 `custom_title`；本技能会覆盖它，这是预期行为（`apply` 的 `--reason` 会留痕，`lock` 可长期保护某会话）。
- **界面显示与数据库是两回事，要分开说**：daemon 的 `listSessions` 每次都现读数据库（所以库里是对的就能被正确返回），
  但渲染进程只在**被拉取时**才更新列表——打开任务列表 / 切换工作区 / 应用启动，实测不是定时轮询。
  所以改完要如实说「库已写入并读回核验一致；**重新打开一次任务列表即可看到**」，
  **不要承诺"实时生效"，也不要断言"必须重启"**。若用户说仍显示旧标题，先复检数据库实际值，再解释拉取时机。
- `locked` 为真时拒绝写入；`pause` 状态下 Hook 不注入、`apply` 拒绝执行。
- Hook 注入有频率限制，默认每 3 个用户轮次一次。改 `~/.workbuddy/topic-title/config.json` 的 `every_n_turns`；`emit_context: false` 可完全关闭注入。
- 归档/置顶整理**未实现**：WorkBuddy 没有等价的宿主能力，不要自行发挥去改数据库其它字段。

## 定时任务（后台自动路径）

- 名称「话题标题轮询整理」，**每 1 小时、仅工作日**运行（官方最小粒度），工作目录 `C:\Users\EDY\WorkBuddy\topic-title-automation`。
- 自包含三步：① 跑 `poll` → ② `idle` 就跳过、`pending` 才判断并 `apply` → ③ **无论结果如何都跑 `cleanup`** 清掉上一次轮询留下的会话。
- **注意**：WorkBuddy 的定时任务**每运行一次就新建一个会话**，所以第 ③ 步是必需的：
  ```
  python3 -X utf8 "<入口>" cleanup --cwd "C:\Users\EDY\WorkBuddy\topic-title-automation" --keep-minutes 10
  ```
  - `cleanup` 只写 `deleted_at`（软删除，与宿主删除会话语义一致，可恢复），不碰标题与其它字段。
  - 保留最近 10 分钟窗口是为了**不删掉正在运行的本轮**，所以每轮最多留 1 条，上一轮在下一轮被清掉。这是设计，不要"优化"掉。
  - 先 `--dry-run` 看命中清单再实删。
  - 它自己的工作目录会被 `poll` 自动排除，不会自我循环。
- 频率说明：**不要**因为「水位机制会自动补齐」就放心降低频率——纯时间窗口**不会补齐**，
  间隔越大会漏得越多（这是已经踩过的坑）。现在靠 `custom_title` 为空的补齐通道兜底，
  但补齐只覆盖「从未命名过」的会话；**已被命名过、之后又变了目标的会话**仍依赖时间窗口命中。
  因此频率保持现状，不要主动调低。

## 参考

排障或需要改动实现时先读 `references/workbuddy-internals.md`：会话标题与转写的存储结构、Hook 配置位置与注入格式、Windows 下 Git Bash / `cygpath` / GBK 编码三个坑、以及为什么写标题只能走数据库。
