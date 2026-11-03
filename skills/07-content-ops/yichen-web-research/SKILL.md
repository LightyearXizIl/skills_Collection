---
name: yichen-web-research
description: 逸尘自用的互联网研究总入口。用于跨平台且跨阶段，或用户尚未确定工具的研究任务，把“搜索发现、候选核验、内容归档、按需转写分析”路由到 yichen-unified-search、yichen-content-archive、yichen-bookmarks-export 与 yichen-asr。若用户只要求搜索、只处理已知链接、只导出私人收藏或只转写已有音视频，应直接使用对应子 Skill。Use when an internet-research request spans multiple stages, the correct child route is unclear, or the user explicitly invokes $yichen-web-research.
---

# 逸尘互联网研究

这是用户自有的研究路由层，不是 OpenCLI、AnySearch 或任何单一 CLI 的包装。底层后端可以替换，用户意图和安全边界保持稳定。

## 何时使用总入口

仅在以下情况使用本 Skill：

- 请求跨越两个以上阶段，例如“先搜索，再选出并归档来源”。
- 请求跨越多个平台且不止搜索，还需要候选确认、归档、转写或后续分析。
- 用户只描述研究目标，尚未指定搜索、归档或收藏导出。
- 需要先体检多个后端，再决定安全可用路线。

单一明确动作直接路由：

单阶段搜索无论涉及一个还是多个平台，都直接进入 `$yichen-unified-search`；“跨平台”本身不是触发总路由的充分条件。

| 用户意图 | 目标 Skill |
|---|---|
| 关键词搜索、批量发现、平台站内搜索、候选核验 | `$yichen-unified-search` |
| 已知 URL、URL 文件、已确认候选或明确容器的读取、下载、归档（含 X Post、Quote、Article） | `$yichen-content-archive` |
| 导出小红书、抖音或 X/Twitter 的私人收藏与书签链接 | `$yichen-bookmarks-export` |
| 已有音视频的字幕、ASR、口播粗剪或内容分析 | `$yichen-asr` |

## 固定流程

```text
研究目标
  -> yichen-unified-search
  -> 标准候选清单
  -> 用户确认或原请求已明确选择范围
  -> yichen-content-archive
  -> 按需交给 yichen-asr、视觉分析或知识库 Skill
```

搜索结束后不得自动下载。收藏导出结束后也不得自动读取正文或下载媒体；下载需要独立、明确的当轮请求。

## 后端定位

- AnySearch：公共网页、批量搜索、垂直搜索和搜索候选的轻量原文核验。
- Twitter/X：关键词搜索交给 `$yichen-unified-search`，固定 Grok CLI 原生 `x_search` 优先；已知 X URL 交给 `$yichen-content-archive`，固定匿名 FxTwitter → Jina 优先。
- 平台原生 CLI/API：GitHub、YouTube、B站等结构化公共搜索。
- OpenCLI：仅作为部分平台的只读适配器，不是本体系的强制依赖或总入口。
- 本地平台 Skill：已知链接解析、媒体下载、公众号正文和批量归档。
- 浏览器或账号登录态：只在匿名路线不足且目标平台规则允许时，按具体目标取得当轮授权。

不得因为某个后端已安装或浏览器已登录，就绕过子 Skill 的授权门。

## 安全边界

1. 所有社交平台保持只读：不发帖、不评论、不点赞、不收藏、不关注、不私信，不改变账号状态。
2. 绝对不得操控微信桌面端或移动端 UI；不得发消息、发布、编辑、创建草稿、删除、群发或关注。
3. 小红书、抖音的 Chrome 登录态搜索必须在执行前说明平台、原始关键词和预计条数，并取得用户当轮明确授权。
4. 私人收藏、书签、Feed 和账号后台数据必须取得当轮对具体平台与范围的明确授权；授权不可转移到下载。
5. 匿名公开路线优先。不得绕过验证码、登录墙、付费墙、限流、地区限制或访问控制。
6. 不打印或保存 Cookie、Token、API Key、登录凭证及敏感 URL 参数。
7. 不覆盖既有产物，不自动删除临时文件。任何清理都必须先获得用户明确允许，并且只能移入废纸篓。
8. 付费 API 或可能产生显著额度消耗的批量转写，在执行前说明范围和预计数量。
9. ASR 自动路由在任务提交后不得跨服务商重提；余额未知时不得表述为充足或不足。

## 多后端体检

跨平台或登录态任务开始前运行：

```bash
python3 ~/.agents/skills/yichen-web-research/scripts/doctor_yichen.py
```

OpenCLI 相关任务再运行：

```bash
opencli doctor
```

体检只证明后端和安全契约可识别，不等于已经获得登录态或私人数据读取授权。

## 交接约定

搜索层至少交接：

```json
{
  "schema_version": "1.0",
  "request": {},
  "routes": [],
  "candidates": [],
  "coverage": [],
  "errors": []
}
```

归档层只接收用户已知链接、已确认候选或明确的有限容器；收藏层只输出链接文件和不可转移授权状态。各子 Skill 的当前 `SKILL.md` 与 references 是执行事实源。

## 唯一入口与子 Skill 调用

- 本 Skill 是唯一的互联网研究总入口，不保留旧名称兼容入口。
- 用户显式调用 `$yichen-web-research` 时，先按上表判断任务阶段；需要子 Skill 时，必须完整读取对应当前文件后再执行：
  - `~/.agents/skills/yichen-unified-search/SKILL.md`
  - `~/.agents/skills/yichen-content-archive/SKILL.md`
  - `~/.agents/skills/yichen-bookmarks-export/SKILL.md`
  - `~/.agents/skills/yichen-asr/SKILL.md`
- 子 Skill 是独立的执行规则，不是可递归调用的函数。路由后直接按目标 Skill 执行，目标 Skill 不得再回到本总入口。
- 若子 Skill、必要后端、登录态或额度不可用，如实报告具体缺口；不得把“已经正确路由”表述成“外部平台必然成功”。
