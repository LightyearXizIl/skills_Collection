# 候选结果交接结构

把所有后端结果映射到同一个 envelope。未知值使用 JSON `null`，不要用空字符串或 `0` 伪造。

## Envelope

```json
{
  "schema_version": "1.0",
  "request": {
    "queries": ["example"],
    "platforms": ["web"],
    "time_range": null,
    "requested_limit": 10
  },
  "routes": [
    {
      "platform": "web",
      "backend": "anysearch",
      "mode": "search",
      "login_state_used": false,
      "status": "completed",
      "limitations": []
    }
  ],
  "candidates": [],
  "coverage": [],
  "errors": []
}
```

## Candidate

```json
{
  "candidate_id": "web:stable-source-id-or-url-hash",
  "query": "example",
  "platform": "web",
  "backend": "anysearch",
  "rank": 1,
  "title": "Result title",
  "url": "https://example.com/item",
  "canonical_url": "https://example.com/item",
  "snippet": "Search-result snippet, not verified body text.",
  "author": null,
  "published_at": null,
  "content_type": "web_page",
  "language": null,
  "metrics": {
    "likes": null,
    "comments": null,
    "collects": null,
    "shares": null,
    "views": null
  },
  "access": {
    "visibility": "public",
    "login_state_used": false
  },
  "verification": {
    "status": "candidate",
    "opened_original": false,
    "checked_at": null
  },
  "provenance": {
    "source_id": null,
    "retrieved_at": "2026-01-01T00:00:00+08:00",
    "route_reason": "public_web_default"
  },
  "limitations": []
}
```

## 字段规则

- `candidate_id`：使用平台稳定 ID；没有稳定 ID 时使用 canonical URL 的哈希。不要把排名当 ID。
- `platform`：使用 `web/github/wechat/xiaohongshu/douyin/toutiao/x/bilibili/youtube/xiaoyuzhou` 等稳定枚举。
- `backend`：记录真实执行后端，不写笼统的“搜索引擎”。
- `rank`：保留单次后端返回顺序；合并后不要据此宣称全网热度。
- `canonical_url`：只移除明确的临时追踪参数；无法判断时与原始 `url` 相同。
- `published_at`、`retrieved_at`、`checked_at`：使用带时区 ISO 8601；相对时间无法可靠换算时保留在 `limitations`，时间字段为 `null`。
- `metrics`：后端未返回即为 `null`；明确返回零才写 `0`。
- `verification.status`：只允许 `candidate/verified/excluded`。只有真实打开原文并核对关键主张后才写 `verified`。
- AnySearch `extract` 只能核验或轻量富化本次搜索 envelope 中已有的 candidate；在 provenance 中保留原始查询和 candidate ID。不得把用户直接给出的 URL 临时塞入候选后调用。
- `visibility`：只允许 `public/authenticated_public`；本 Skill 不产生 private 候选。
- `coverage`：逐后端记录查询数、返回数、截断、时间筛选、登录态和已知索引限制。
- `errors`：保存可公开的错误类别和影响；不得记录 Cookie、Token、Key、完整认证响应或敏感查询。

## 去重与核验

1. 先按 canonical URL 去重。
2. 再按平台稳定 ID 合并。
3. 仅在标题、作者和发布时间均高度一致时合并近重复内容，并保留所有 provenance。
4. 把搜索摘要视为线索，不作为正文引文。
5. 对最终引用候选打开原文；无法访问则保留为 candidate 或排除，不根据摘要补写事实。
