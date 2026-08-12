---
name: yichen-unified-search
description: 逸尘自用的统一网页与社交平台搜索编排器。用于关键词驱动的实时公共网页检索、并行批量搜索、金融/学术/法律/安全等垂直搜索，以及 GitHub、微信公众号、小红书、抖音、今日头条、Twitter/X、B站、YouTube、小宇宙等平台的公开内容发现；可对本次搜索所得候选做原文核验和轻量富化，并把不同后端结果统一交接为候选记录。AnySearch 负责公共网页、批量与垂直搜索，平台原生/OpenCLI 只作对应平台适配器。不用于读取或下载用户直接给出的已知 URL、URL 文件或已确认候选；此类任务使用 yichen-content-archive。
---

# 逸尘统一搜索

把搜索拆成“定范围 → 选后端 → 取候选 → 标准化 → 核验”。只编排现有工具，不复制搜索、抓取或登录实现。

## 固定边界

1. 只搜索和读取用户当轮目标所需的公开内容；不发帖、不评论、不点赞、不关注、不私信、不改变账号状态。
2. 绝对不得操控微信桌面端或移动端 UI。微信公众号只走匿名公共搜索；需要公众号后台或非公开数据时停止并说明此 Skill 不处理。
3. 不读取、同步或搜索私人收藏、书签、个人 Feed、群组、通知、私信、草稿或后台数据。
4. 不下载媒体、不归档、不建立长期数据库、不运行定时监控。用户要读取、下载、转写或归档已审核 URL 清单时，交给 `$yichen-content-archive` 并重新确认动作与范围。
5. 不绕过验证码、登录墙、限流或风控。缺失字段写 `null`，零结果只表示本次后端未返回候选。
6. 用户直接给出已知 URL、URL 文件，或要求读取/下载/归档已确认候选时，停止搜索并交给 `$yichen-content-archive`。只有用户明确要求“搜索引用、讨论或关联这个 URL 的其他公开内容”时，才把 URL 标记为 `--input-kind url-seed`；该模式只把 URL 当发现线索，不读取或归档 URL 本身。
7. 公共网页搜索词、候选核验 URL 和垂直参数会发给 AnySearch；X 公共搜索词首先发给官方 Grok CLI 原生 `x_search`，只有明确额度耗尽时才会发给匿名 FxTwitter。不得提交密码、Cookie、个人数据、商业秘密或其他敏感查询。

## 路由

先运行离线路由器检查计划；它不联网，也不执行后端：

```bash
python3 ~/.agents/skills/yichen-unified-search/scripts/route_search.py \
  --query "检索词" --platform auto --mode search --limit 10
```

把 URL 当作公开搜索种子而不是已知内容读取时，必须显式标记：

```bash
python3 ~/.agents/skills/yichen-unified-search/scripts/route_search.py \
  --query "搜索引用 https://example.com/research 的公开报道" \
  --platform web --input-kind url-seed --limit 10
```

按以下优先级执行：

1. 明确要求公共网页、新闻、多个独立关键词、`site:` 查询或垂直领域发现时，使用 AnySearch。
2. 垂直领域先执行 AnySearch `get_sub_domains`，再带齐所有必填参数搜索；不确定是否垂直时，用 `batch_search` 并行一条通用查询和若干垂直查询。
3. 明确要求某平台的站内/原生覆盖时，才使用该平台适配器。不要把平台适配器当成通用网页兜底。
4. 明确要求批量跨关键词时，优先使用 AnySearch；平台限定批量改成公共 `site:` 查询，并标明它不是站内全量结果。
5. 只有需要核验或轻量富化本次搜索刚返回的候选时，才对该候选使用 AnySearch `extract`。不得用它读取用户直接给出的已知 URL。
6. AnySearch 不可用时说明错误；只有用户同意后才改用其他公共网页搜索。不要静默切换到读取账号登录态的后端。

完整后端、命令形状和登录门槛见 [references/routes.md](references/routes.md)。

## 登录与安全门

- 小红书、抖音站内搜索：执行前说明平台、原始关键词和预计条数，取得用户当轮明确授权读取 Chrome 登录态；一次授权不扩展到其他关键词、平台或后续任务。
- Twitter/X：所有关键词搜索第一层固定为官方 Grok CLI 账号 OAuth + 原生 `x_search`。只有输出明确证明账号额度或使用上限耗尽时，才进入匿名 FxTwitter；未登录、401/403、权限、输入、超时、网络和服务错误都必须停止，不能冒充额度错误。FxTwitter 仍失败或零结果时，才按既有只读链进入 OpenCLI → xreach；只有明确进入浏览器登录态适配器时，才按对应工具提示取得当轮授权。
- B站、YouTube、微信、今日头条和小宇宙公共发现：先匿名。出现登录限定时停止；本 Skill 不升级为登录读取。
- AnySearch API Key：匿名额度可直接使用。收到新 Key 时先询问，用户明确同意后才能保存；不要让用户在聊天中粘贴 Key。

## 标准流程

1. 复述范围：关键词、平台、时间范围、条数、是否需要原生站内覆盖。
2. 运行 `route_search.py`；检查 `status`、`authorization`、`steps` 和 `limitations`。
3. X 搜索先运行 `python3 ~/.agents/skills/yichen-web-research/scripts/doctor_yichen.py`，确认 `$yichen-grok-consult`、Grok CLI OAuth 与原生 `x_search` 可用，再调用该工具。工具内部固定执行 Grok CLI → 仅明确额度耗尽时 FxTwitter → OpenCLI → xreach；不得因零结果、超时、网络或服务错误提前跳到 FxTwitter。其他多后端或登录态任务也运行该 doctor；OpenCLI 路线再运行 `opencli doctor`。不要回调总路由 Skill，也不要把命令存在当成可用。
4. 仅调用计划中的既有后端。AnySearch 从 `~/.agents/skills/anysearch/runtime.conf` 读取当前 `Command`，不要复制 CLI，也不要硬编码代理或 Key。
5. 把每个后端输出映射到 [references/candidate-schema.md](references/candidate-schema.md)；保持原始 URL、来源平台、后端和限制。
6. 先 URL 去重，再按标题/作者/发布时间做近重复合并；不要把互动量当成事实正确性。
7. 对最终将引用的本轮搜索候选，可用 AnySearch `extract` 打开原文核验或补少量正文线索。搜索卡片和摘要只能作发现线索；不要把核验扩展成下载或归档。
8. 交付候选与覆盖说明；标明每个平台的登录态使用、失败、截断、时间筛选和索引局限。

## 最小交付

返回一个候选交接包：

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

若用户只要答案，可用 Markdown 展示精选候选，但内部仍保留同一字段语义。不要把候选列表冒充完整、穷尽或已核验事实。
