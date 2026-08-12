# 后端路由与命令契约

只在需要执行具体平台搜索时读取本文件。命令均为只读搜索；不要附带下载、收藏、评论、发布或归档步骤。

平台适配器的总安全规则以 `~/.agents/skills/yichen-web-research/SKILL.md` 为事实源；具体搜索边界以本 Skill 为准。多后端或登录态任务先运行：

```bash
python3 ~/.agents/skills/yichen-web-research/scripts/doctor_yichen.py
opencli doctor  # 仅 OpenCLI 路线需要
```

按照体检的真实 active backend 执行；命令存在不等于后端可用。

## AnySearch：默认公共后端

先读 `~/.agents/skills/anysearch/runtime.conf` 的 `Command`，以 `<anysearch_cmd>` 表示完整命令前缀。不要复制 AnySearch CLI，不要覆盖其配置。

```bash
# 公共网页
<anysearch_cmd> search "query" --max_results 10

# 仅核验/轻量富化本次搜索所得候选；extract 没有 format/markdown 参数
<anysearch_cmd> extract "<candidate-url-from-current-search>"

# 批量；单批最多 5 个查询，每个查询最多 10 条
<anysearch_cmd> batch_search --queries \
  '[{"query":"q1","max_results":10},{"query":"q2","max_results":10}]'

# 垂直领域：先发现子域和必填参数
<anysearch_cmd> get_sub_domains --domain legal
<anysearch_cmd> search "query" --domain legal --sub_domain "<returned-sub-domain>" \
  --sub_domain_params '{"required_key":""}'
```

支持的垂直大类以 AnySearch 实时 `get_sub_domains` 输出为准。所有标记为 required 的参数都必须出现；没有适用值时传空字符串。AnySearch 失败后先报告，不静默换后端。

## 平台适配器

| 平台意图 | 既有适配器 | 登录门槛 | 重要限制 |
|---|---|---|---|
| GitHub 仓库/代码/Issue/PR | `gh search ...` | 公共数据先匿名；需要更高额度时再由用户登录 | 只搜索，不 clone、不改仓库 |
| 微信公众号跨号关键词 | `opencli weixin search` | 匿名公共搜狗微信路线 | 绝不操控微信 UI；不进后台 |
| 小红书站内关键词 | `opencli xiaohongshu search` | 必须取得当轮 Chrome 登录态授权 | 只返回候选；不下载、不展开评论 |
| 抖音站内关键词 | `opencli douyin search` | 必须取得当轮 Chrome 登录态授权 | 低频串行；不下载、不展开评论 |
| 今日头条综合非视频 | `opencli toutiao search` | 专用匿名 profile，不读取用户 Chrome | 单关键词、低频、无自动重试 |
| Twitter/X 公共搜索 | `$yichen-grok-consult` → 仅额度耗尽时 `fxtwitter_search.py` → OpenCLI → xreach | Grok CLI 使用账号 OAuth；FxTwitter 匿名；后续浏览器会话回退按工具授权 | 所有关键词搜索先走 Grok 原生 `x_search`；只有明确额度或使用上限耗尽才能进入 FxTwitter |
| B站公开视频 | `bili search` | 匿名优先 | 只生成候选 URL，不下载 |
| YouTube 公开视频 | `yt-dlp` 的 flat `ytsearch` | 匿名优先 | 只列元数据和 URL，不下载 |
| 小宇宙全站关键词 | AnySearch `site:xiaoyuzhoufm.com` | 匿名公共网页 | OpenCLI 不提供全站关键词搜索 |

### 命令形状

```bash
# GitHub：按对象选择 repos/code/issues/prs
gh search repos "query" --sort stars --limit 10
gh search code "query" --limit 10
gh search issues "query" --limit 10
gh search prs "query" --limit 10

# 微信公众号公共关键词
opencli weixin search "query" --page 1 --limit 10

# 小红书/抖音：执行前取得本次关键词和条数的明确授权
opencli xiaohongshu search "query" --days 1 --content all --limit 20 --enrich -f yaml
opencli douyin search "query" --days 1 --content all --limit 30 --enrich -f yaml

# 今日头条：只保留文章和非视频图文帖
opencli toutiao search "query" --days 1 --limit 20 -f yaml

# X 第一层：先检查现有 OAuth，再调用已安装的 yichen-grok-consult 搜索工具
grok models
# 该工具负责核验 completed XSearch。

# 仅当 Grok 输出明确证明账号额度或使用上限耗尽时，工具内部才运行：
python3 ~/.agents/skills/yichen-unified-search/scripts/fxtwitter_search.py \
  --query "query" --limit 20 --days 1

# FxTwitter 仍失败或零结果时，才继续 OpenCLI → xreach。
# B站 / YouTube：仅发现候选
bili search "query" --type video --page 1 -n 20 --json
yt-dlp --flat-playlist --dump-single-json "ytsearch20:query"
```

## 选择细则

- 用户说“全网、新闻、官网、多个关键词、批量、垂直领域”时，使用 AnySearch。
- 用户说“某平台站内、该平台最新帖子、平台账号/作品”时，使用对应平台适配器。
- 用户只说“社交媒体讨论”但未指定平台时，先用 AnySearch 的 `social_media` 垂直域发现公开候选；需要站内覆盖再让用户指定平台。
- 平台限定的批量查询默认改成 AnySearch `site:` 公共网页查询；在覆盖说明中写明“不等于站内全量”。
- AnySearch `extract` 只用于核验或轻量富化本次搜索所得候选，并保留候选 ID 与原始查询的 provenance。用户直接给出的已知 URL、URL 文件，以及读取/下载/归档已确认候选的任务，交给 `$yichen-content-archive`。
- 用户明确要求“搜索引用、讨论或关联某 URL 的其他公开内容”时，可用 `--input-kind url-seed` 把 URL 作为发现查询的一部分；该模式不得读取、下载或归档种子 URL 本身。默认 `auto` 遇到任意 URL 仍安全交接到归档层。
- 平台原生适配器只在必须补平台结构化字段时使用。
- 小红书、抖音授权前可输出计划，不可实际运行命令。
- X 关键词搜索一律先执行 `$yichen-grok-consult` 的 `search_x_with_grok`。该工具固定使用 Grok CLI 原生 `x_search`；只有明确账号额度或使用上限耗尽时才进入 `fxtwitter_search.py`，FxTwitter 失败或零结果后才继续 OpenCLI → xreach。
- 未登录、401/403、权限、输入、超时、网络、服务异常、零结果或搜索证据不可核验都不是额度耗尽；这些情况必须停止并报告，禁止静默调用 FxTwitter。
- FxTwitter 请求只发公开关键词，不携带 Cookie、Token 或 X 登录态；只请求一页，不自动翻页、不自动重试。它是第三方公共索引，零结果不能证明 X 上没有相关内容。
- FxTwitter 返回普通推文、引用推文和 Article 候选时，保留引用对象与 Article 标题、预览和封面元数据；搜索阶段不得展开 Article 全文。全文读取仍交给 `$yichen-content-archive`。
- `$yichen-grok-consult` 当前不可调用时，只报告主链不可用；不要自动安装插件，也不要绕过固定四层链另找账号后端。
- 任何验证码、登录墙、权限错误或账号安全提示都应停止，不尝试绕过或自动重试。
