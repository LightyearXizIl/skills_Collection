# 标准交接结构

两个 Skill 使用同一 `yichen-content-handoff/v1` 结构。交接是运行摘要，不是新的授权。

```json
{
  "handoff_version": "yichen-content-handoff/v1",
  "producer_skill": "yichen-content-archive",
  "operation": "content_archive",
  "scope": {
    "platforms": ["xiaohongshu"],
    "input_kind": "known_urls",
    "discovery_performed": false
  },
  "authorization": {
    "private_read_authorized_this_turn": null,
    "download_authorized_this_turn": true,
    "authorization_not_transferable": true
  },
  "artifacts": [
    {
      "kind": "archive_manifest",
      "path": "/absolute/path/archive-manifest.jsonl",
      "count": 3
    }
  ],
  "counts": {
    "input": 3,
    "success": 2,
    "failed": 1,
    "skipped": 0,
    "unsupported": 0
  },
  "failures": [
    {
      "item_ref": "input.txt:3",
      "stage": "download",
      "reason": "access_denied"
    }
  ],
  "next_step": {
    "action": "none",
    "requires_explicit_user_request": true
  }
}
```

## 约束

- `producer_skill` 只能是 `yichen-content-archive` 或 `yichen-bookmarks-export`。
- `operation` 只能是 `content_archive` 或 `bookmark_export`。
- `discovery_performed` 必须为 `false`。
- 收藏导出交接的 `download_authorized_this_turn` 必须为 `false`。
- `authorization_not_transferable` 必须为 `true`；任何后续私人读取、登录态使用或下载按目标 Skill 重新判断。
- `artifacts[].path` 使用绝对路径。私人 URL、敏感查询参数和凭证放在受控本地文件中，不内嵌到交接 JSON。
- `counts` 五项必须存在；没有失败时 `failures` 使用空数组。
- `next_step` 只描述可选动作，不触发另一个 Skill。
