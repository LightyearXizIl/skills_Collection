---
name: codex-local-plugin-install
description: 把第三方 GitHub 仓库作为本地插件安装进本机 Codex（桌面端/CLI），包括本地 marketplace 配置、插件注册、Hook 信任引导与生效验证。触发词：安装 Codex 插件、codex plugin add、本地插件市场、marketplace.json、信任 Hook、Stop hook 不生效、codex 插件装了没用。适用于「帮我查找 GitHub 仓库 X，下载并安装完整插件」这类请求。
agent_created: true
---

# 安装第三方 Codex 插件（本地 marketplace 方式）

把 GitHub 上的 Codex 插件装进本机 Codex。核心是：**Codex 只能从 marketplace 安装插件**，而多数插件仓库本身不是 marketplace，必须自己包一层。

## 第 0 步：先判断这是不是 Codex 插件

仓库里出现 `.codex-plugin/plugin.json`、`hooks/hooks.json`、`skills/` → Codex 本地插件，走本流程。

**若任务要求在 WorkBuddy 中运行该插件，直接说明不可行**：这类插件的 hook 事件、App Server JSON-RPC、话题改名接口都由 Codex 宿主提供。可改成「在 Codex 中安装 + 在 WorkBuddy 侧装一个管理技能」的两段式方案。

## 第 1 步：核验与审计

1. 确认仓库存在、看 license 与最近提交时间。
2. 克隆到工作区 `_tmp/`，克隆时排除 `.git`。
3. 审计：`hooks/*.json` 的 command、`scripts/*.py` 里的网络调用与 `subprocess` 目标、是否有 `rmtree`/写入用户目录的行为。确认子进程只调用宿主二进制、日志不含对话原文，再继续。

## 第 2 步：建本地 marketplace（关键）

marketplace 清单路径：`~/.agents/plugins/marketplace.json`。

**ROOT 语义容易踩坑**：清单在 `<ROOT>/.agents/plugins/marketplace.json`，`source.path` 相对 **`<ROOT>`** 解析。对用户级清单，`<ROOT>` 就是家目录。用 `codex plugin marketplace list` 打印的 ROOT 列核对。

```json
{
  "name": "personal",
  "interface": { "displayName": "Personal" },
  "plugins": [
    {
      "name": "<插件名>",
      "source": { "source": "local", "path": "./.agents/plugins/<插件名>" },
      "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
      "category": "Productivity"
    }
  ]
}
```

- 插件文件放到 `~/.agents/plugins/<插件名>/`，必须含 `.codex-plugin/plugin.json` 与 `hooks/hooks.json`。
- 已有同名清单时**追加** `plugins` 条目，不要整体覆盖。
- **清单必须是无 BOM 的 UTF-8**，否则报 `invalid marketplace file ... expected value at line 1 column 1`，且会导致 `marketplace list` 整体失败。
- 注意：本机 Write 工具在**覆盖**已有文件时会保留原文件的 BOM。写 JSON 前先查 `od -An -tx1 -N3 <file>`，若为 `ef bb bf` 则用 `tail -c +4 <file> > tmp && mv tmp <file>` 剥离。

## 第 3 步：安装

```bash
codex plugin marketplace list
codex plugin list
codex plugin add <插件名>@personal --json
```

`codex plugin add` 会把插件复制到 `~/.codex/plugins/cache/<marketplace>/<插件名>/<版本>/`，并在 `~/.codex/config.toml` 写入 `[plugins."<插件名>@personal"] enabled = true`。改 config 前先备份。

## 第 4 步：自检与依赖修复

在**插件安装缓存目录**（不是源目录）执行插件的 doctor：

```bash
cd ~/.codex/plugins/cache/personal/<插件名>/<版本>
py -3 -X utf8 scripts/<入口>.py doctor      # Windows
```

- 报「未找到 Codex CLI」：`codex.exe` 通常不在 PATH。用路径稳定的那份（如 `~/.codex/plugins/.plugin-appserver/codex.exe`），避免用 `AppData\Local\OpenAI\Codex\bin\<hash>\codex.exe` 这类带哈希、会随版本失效的路径。然后 `configure --codex-bin "<路径>"`。
- 模型名先用 `~/.codex/models_cache.json` 里的 `slug` 核对再配置，不要猜。
- 确认 `codex features list` 中相关 feature（如 `hooks`）为 true。

## 第 5 步：Hook 信任（只能用户在界面操作）

**这一步无法自动化**，不要修改信任数据库，也不要加 `--dangerously-bypass-hook-trust`。信任按 hook 定义的哈希记录，改一个字符就要重新信任。

告诉用户：

1. **先完全退出并重启 Codex 桌面端**（会话已开着时新增的 hook 不会被加载）。
2. 打开 **设置 → Hooks**（CLI 里是 `/hooks`）。
3. 找到本插件来源的那条（如 `stop`），确认命令是插件自己的脚本 → 点 **Trust / 信任**。
4. 若列表里看不到，先确认已重启、且插件状态为 `installed, enabled`。

## 第 6 步：验证生效（区分证据强度）

| 证据 | 能证明什么 | 不能证明什么 |
|---|---|---|
| 插件自带测试通过 | 处理链路逻辑正确 | 宿主是否触发 |
| `doctor` 中 `hook.status = ready` | 已加载 + 已启用 + 已信任 | 真的触发过 |
| 直接跑入口命令 | 脚本能读话题、能调模型 | 宿主已触发 |
| **新对话正常聊完一轮后看标题** | 真正生效 | — |

自动触发必须在**已安装、已启用、已信任**的新对话里验收。预览类命令可用真实话题 ID 验证读取与命名链路，不加 `--apply` 时不会写入。

## 兜底

- 结果状态是「预览 / 待信任 / 已启用但未触发」时，如实说明，不要当成已生效。
- 桌面端置顶列表可能仍显示旧标题，需要宿主侧同步；不要宣称 hook 能刷新所有缓存。
